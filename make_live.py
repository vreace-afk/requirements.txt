import asyncio
import httpx
import re
import os

# ================= 配置区 =================
USER_CONFIG = {
    "github_user": "vreace-afk", 
    "repo_name": "live",         
}
# ==========================================

# 保底源：如果所有外部抓取都失败，直接使用这些稳定的静态链接
BASE_CHANNELS = """
#EXTINF:-1 group-title="央视频道" tvg-name="CCTV-1",CCTV-1 综合
https://live.itv.org.cn/cctv1.m3u8
#EXTINF:-1 group-title="央视频道" tvg-name="CCTV-13",CCTV-13 新闻
https://live.itv.org.cn/cctv13.m3u8
#EXTINF:-1 group-title="地方卫视" tvg-name="湖南卫视",湖南卫视
https://live.itv.org.cn/hunantv.m3u8
#EXTINF:-1 group-title="地方卫视" tvg-name="浙江卫视",浙江卫视
https://live.itv.org.cn/zhejiangtv.m3u8
"""

EXTERNAL_M3U_URLS = [
    "https://ghp.ci/https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u",
    "https://ghp.ci/https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u",
    "https://raw.githubusercontent.com/Guover/IPTV/master/CH.m3u"
]

async def fetch_external_sources():
    extra_channels = []
    rules = [
        (r".*?(CCTV|央视|cctv|4K|8K).*", "央视频道"),
        (r".*?卫视", "地方卫视"),
        (r".*?(电影|CHC|HBO|影院|剧场|影视|动作|喜剧).*", "电影频道"),
        (r".*?(体育|五星|劲爆|高尔夫|足球|NBA|赛车).*", "体育专区")
    ]
    
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True, verify=False) as client:
        for url in EXTERNAL_M3U_URLS:
            try:
                resp = await client.get(url)
                if resp.status_code == 200:
                    content = resp.text
                    for pattern_str, group_name in rules:
                        regex = re.compile(rf'(#EXTINF:.*?,({pattern_str}).*?\n(http.*?))', re.IGNORECASE)
                        matches = regex.findall(content)
                        for _, name, link in matches:
                            extra_channels.append(f'#EXTINF:-1 group-title="{group_name}" tvg-name="{name.strip()}",{name.strip()}\n{link.strip()}')
            except: continue
    return list({line.split(',')[1]: line for line in extra_channels}.values())

def update_readme(count):
    cdn_url = f"https://jsd.onmicrosoft.cn/gh/{USER_CONFIG['github_user']}/{USER_CONFIG['repo_name']}/cctv.m3u"
    content = f"# 📺 我的私人直播源\n\n## 🔗 订阅地址\n`{cdn_url}`\n\n## 📊 状态汇总\n- **频道总数**: {count}\n- **最后更新**: {os.popen('date').read().strip()}\n"
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

async def main():
    # 1. 抓取外部源
    ext_res = await fetch_external_sources()
    
    # 2. 无论如何都加上保底源，确保总数不为 0
    final_list = BASE_CHANNELS.strip().split('\n') + ext_res
    
    # 3. 写入文件
    with open("cctv.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n" + "\n".join(final_list))
    
    update_readme(len([l for l in final_list if "#EXTINF" in l]))
    print(f"✨ 运行完成，总计 {len([l for l in final_list if '#EXTINF' in l])} 个频道")

if __name__ == "__main__":
    asyncio.run(main())
