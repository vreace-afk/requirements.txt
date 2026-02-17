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

# 1. 央视官方 ID 列表 (尝试动态抓取)
CCTV_MAP = {
    "CCTV-1 综合": "cctv1", "CCTV-2 财经": "cctv2", "CCTV-3 综艺": "cctv3",
    "CCTV-4 中文国际": "cctv4", "CCTV-5 体育": "cctv5", "CCTV-5+ 体育赛事": "cctv5plus",
    "CCTV-6 电影": "cctv6", "CCTV-7 国防军事": "cctv7", "CCTV-8 电视剧": "cctv8",
    "CCTV-9 纪录": "cctv9", "CCTV-10 科教": "cctv10", "CCTV-11 戏曲": "cctv11",
    "CCTV-12 社会与法": "cctv12", "CCTV-13 新闻": "cctv13", "CCTV-14 少儿": "cctv14",
    "CCTV-15 音乐": "cctv15", "CCTV-16 奥林匹克": "cctv16", "CCTV-17 农业农村": "cctv17",
}

# 2. 备用聚合源 (增加了一个非常全的源)
EXTERNAL_M3U_URLS = [
    "https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u",
    "https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u",
    "https://raw.githubusercontent.com/Guover/IPTV/master/CH.m3u",
    "https://raw.githubusercontent.com/ssili126/tv/main/itvlist.m3u" # 新增备用源
]

async def fetch_cctv_url(name, pid):
    api_url = f"https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={pid}"
    headers = {"User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"}
    try:
        async with httpx.AsyncClient(timeout=8, follow_redirects=True) as client:
            resp = await client.get(api_url, headers=headers)
            m3u8_url = resp.json().get("hls_url")
            if m3u8_url:
                group = "体育频道" if "体育" in name or "奥林匹克" in name else "央视频道"
                if "电影" in name: group = "电影频道"
                return f'#EXTINF:-1 group-title="{group}" tvg-name="{name}",{name}\n{m3u8_url}'
    except: pass
    return None

async def fetch_external_sources():
    extra_channels = []
    # 更加强力的正则规则：支持 CCTV-1, CCTV1, 央视, 4K, 8K 等
    rules = [
        (r".*?(CCTV|央视|cctv|4K|8K).*", "央视频道"),
        (r".*?卫视", "地方卫视"),
        (r".*?(电影|CHC|HBO|影院|剧场|影视|动作|喜剧|功夫).*", "电影频道"),
        (r".*?(体育|五星|劲爆|高尔夫|足球|NBA|赛车|运动).*", "体育专区")
    ]
    
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        for url in EXTERNAL_M3U_URLS:
            try:
                resp = await client.get(url)
                content = resp.text
                for pattern_str, group_name in rules:
                    # 匹配不区分大小写
                    regex = re.compile(rf'(#EXTINF:.*?,({pattern_str}).*?\n(http.*?))', re.IGNORECASE)
                    matches = regex.findall(content)
                    for _, name, link in matches:
                        clean_name = name.strip()
                        # 智能分流
                        final_group = group_name
                        if any(x in clean_name for x in ["体育", "足球", "NBA"]): final_group = "体育专区"
                        if any(x in clean_name for x in ["电影", "影院", "CHC"]): final_group = "电影频道"
                        
                        extra_channels.append(f'#EXTINF:-1 group-title="{final_group}" tvg-name="{clean_name}",{clean_name}\n{link.strip()}')
            except: continue
            
    # 按频道名去重
    unique_data = {line.split(',')[1]: line for line in extra_channels}.values()
    return list(unique_data)

def update_readme(count):
    cdn_url = f"https://jsd.onmicrosoft.cn/gh/{USER_CONFIG['github_user']}/{USER_CONFIG['repo_name']}/cctv.m3u"
    content = f"""# 📺 我的私人直播源
## 🔗 订阅地址
`{cdn_url}`
## 📊 状态汇总
- **频道总数**: {count}
- **最后更新**: {os.popen('date').read().strip()}
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

async def main():
    print("🚀 正在强力捕获频道...")
    tasks = [fetch_cctv_url(name, pid) for name, pid in CCTV_MAP.items()]
    cctv_res = [r for r in await asyncio.gather(*tasks) if r]
    ext_res = await fetch_external_sources()
    
    # 将央视频道排在最前面
    all_links = cctv_res + ext_res
    with open("cctv.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n" + "\n".join(all_links))
    
    update_readme(len(all_links))
    print(f"✨ 补全完成！当前频道数：{len(all_links)}")

if __name__ == "__main__":
    asyncio.run(main())
