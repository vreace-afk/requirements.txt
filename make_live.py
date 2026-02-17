import asyncio
import httpx
import re
import os

# ================= 配置区 =================
USER_CONFIG = {
    "github_user": "vreace-afk", 
    # ！！！请修改为你的用户名！！！
    "repo_name": "live",         # ！！！请修改为你的仓库名！！！
}
# ==========================================

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
    "https://raw.githubusercontent.com/Guover/IPTV/master/CH.m3u"
]

async def fetch_cctv_url(name, pid):
    api_url = f"https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={pid}"
    headers = {"User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X)"}
    try:
        async with httpx.AsyncClient(timeout=10, follow_redirects=True) as client:
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
    rules = [(r".*?卫视", "地方卫视"), (r".*?(电影|CHC|HBO|影院|剧场)", "电影频道"), (r".*?(体育|五星|劲爆|高尔夫|足球|NBA)", "体育专区")]
    async with httpx.AsyncClient(timeout=15, follow_redirects=True) as client:
        for url in EXTERNAL_M3U_URLS:
            try:
                resp = await client.get(url)
                content = resp.text
                for pattern_str, group_name in rules:
                    regex = re.compile(rf'(#EXTINF:.*?,({pattern_str}).*?\n(http.*?))')
                    matches = regex.findall(content)
                    for full_block, name, link in matches:
                        extra_channels.append(f'#EXTINF:-1 group-title="{group_name}" tvg-name="{name.strip()}",{name.strip()}\n{link.strip()}')
            except: continue
    unique_data = {line.split(',')[1]: line for line in extra_channels}.values()
    return list(unique_data)

def update_readme(cctv_count, ext_count):
    cdn_url = f"https://jsd.onmicrosoft.cn/gh/{USER_CONFIG['github_user']}/{USER_CONFIG['repo_name']}/cctv.m3u"
    readme_content = f"""# 📺 我的自动直播源系统

## 🔗 直播源链接 (国内秒开)
`{cdn_url}`

## 📊 当前状态
- **更新时间**: {os.popen('date').read().strip()}
- **央视频道**: {cctv_count} 个
- **卫视/电影/体育**: {ext_count} 个
- **总计**: {cctv_count + ext_count} 个

## 🛠️ 使用方法
1. 复制上方链接。
2. 在 PotPlayer, TVBox 或 IPTV Pro 中添加网络链接即可。
"""
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(readme_content)

async def main():
    print("🎬 正在同步数据...")
    cctv_tasks = [fetch_cctv_url(name, pid) for name, pid in CCTV_MAP.items()]
    cctv_results = [r for r in await asyncio.gather(*cctv_tasks) if r]
    external_results = await fetch_external_sources()
    
    with open("cctv.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n" + "\n".join(cctv_results) + "\n" + "\n".join(external_results))
    
    print("📝 正在更新 README...")
    update_readme(len(cctv_results), len(external_results))
    print("✨ 全部完成！")

if __name__ == "__main__":
    asyncio.run(main())

