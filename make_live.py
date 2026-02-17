import asyncio
import httpx
import re
import os

USER_CONFIG = {
    "github_user": "vreace-afk", 
    "repo_name": "live",         
}

CCTV_MAP = {
    "CCTV-1 综合": "cctv1", "CCTV-2 财经": "cctv2", "CCTV-3 综艺": "cctv3",
    "CCTV-4 中文国际": "cctv4", "CCTV-5 体育": "cctv5", "CCTV-5+ 体育赛事": "cctv5plus",
    "CCTV-6 电影": "cctv6", "CCTV-7 国防军事": "cctv7", "CCTV-8 电视剧": "cctv8",
    "CCTV-9 纪录": "cctv9", "CCTV-10 科教": "cctv10", "CCTV-11 戏曲": "cctv11",
    "CCTV-12 社会与法": "cctv12", "CCTV-13 新闻": "cctv13", "CCTV-14 少儿": "cctv14",
    "CCTV-15 音乐": "cctv15", "CCTV-16 奥林匹克": "cctv16", "CCTV-17 农业农村": "cctv17",
}

EXTERNAL_M3U_URLS = [
    "https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u",
    "https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u",
    "https://raw.githubusercontent.com/Guover/IPTV/master/CH.m3u",
    "https://ghp.ci/https://raw.githubusercontent.com/ssili126/tv/main/itvlist.m3u" # 使用代理加速
]

async def fetch_external_sources():
    extra_channels = []
    rules = [
        (r".*?(CCTV|央视|cctv|4K|8K).*", "央视频道"),
        (r".*?卫视", "地方卫视"),
        (r".*?(电影|CHC|HBO|影院|剧场|影视|动作|喜剧|功夫|点播).*", "电影频道"),
        (r".*?(体育|五星|劲爆|高尔夫|足球|NBA|赛车|运动).*", "体育专区")
    ]
    
    # 增加超时到 30 秒，并增加重试
    async with httpx.AsyncClient(timeout=30.0, follow_redirects=True, verify=False) as client:
        for url in EXTERNAL_M3U_URLS:
            try:
                print(f"正在抓取: {url}")
                resp = await client.get(url)
                if resp.status_code == 200:
                    content = resp.text
                    for pattern_str, group_name in rules:
                        regex = re.compile(rf'(#EXTINF:.*?,({pattern_str}).*?\n(http.*?))', re.IGNORECASE)
                        matches = regex.findall(content)
                        for _, name, link in matches:
                            extra_channels.append(f'#EXTINF:-1 group-title="{group_name}" tvg-name="{name.strip()}",{name.strip()}\n{link.strip()}')
            except Exception as e:
                print(f"抓取失败 {url}: {e}")
                continue
    return list({line.split(',')[1]: line for line in extra_channels}.values())

def update_readme(count):
    cdn_url = f"https://jsd.onmicrosoft.cn/gh/{USER_CONFIG['github_user']}/{USER_CONFIG['repo_name']}/cctv.m3u"
    content = f"# 📺 我的私人直播源\n\n## 🔗 订阅地址\n`{cdn_url}`\n\n## 📊 状态汇总\n- **频道总数**: {count}\n- **最后更新**: {os.popen('date').read().strip()}\n"
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

async def main():
    ext_res = await fetch_external_sources()
    # 如果抓取到了内容才写入，防止把旧的好文件覆盖成空的
    if len(ext_res) > 0:
        with open("cctv.m3u", "w", encoding="utf-8") as f:
            f.write("#EXTM3U\n" + "\n".join(ext_res))
        update_readme(len(ext_res))
        print(f"🎉 成功补齐！共 {len(ext_res)} 个频道")
    else:
        print("❌ 本次抓取失败，未更新文件，防止清空列表")

if __name__ == "__main__":
    asyncio.run(main())
