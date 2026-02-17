import asyncio
import httpx
import time

# 1. 配置频道列表 (ID 对应 CCTV 官网接口参数)
CCTV_CHANNELS = {
    "CCTV-1 综合": "cctv1",
    "CCTV-2 财经": "cctv2",
    "CCTV-3 综艺": "cctv3",
    "CCTV-4 中文国际": "cctv4",
    "CCTV-5 体育": "cctv5",
    "CCTV-5+ 体育赛事": "cctv5plus",
    "CCTV-6 电影": "cctv6",
    "CCTV-7 国防军事": "cctv7",
    "CCTV-8 电视剧": "cctv8",
    "CCTV-9 纪录": "cctv9",
    "CCTV-10 科教": "cctv10",
    "CCTV-11 戏曲": "cctv11",
    "CCTV-12 社会与法": "cctv12",
    "CCTV-13 新闻": "cctv13",
    "CCTV-14 少儿": "cctv14",
    "CCTV-15 音乐": "cctv15",
    "CCTV-16 奥林匹克": "cctv16",
    "CCTV-17 农业农村": "cctv17",
}

async def fetch_m3u8(name, pid):
    """从央视接口动态获取直播流地址"""
    api_url = f"https://vdn.apps.cntv.cn/api/getHttpVideoInfo.do?pid={pid}"
    headers = {
        "User-Agent": "Mozilla/5.0 (iPhone; CPU iPhone OS 17_0 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.0 Mobile/15E148 Safari/604.1"
    }
    
    try:
        async with httpx.AsyncClient(timeout=10) as client:
            response = await client.get(api_url, headers=headers)
            if response.status_code == 200:
                data = response.json()
                # 提取 HLS 链接
                m3u8_url = data.get("hls_url")
                if m3u8_url:
                    return f"#EXTINF:-1 group-title=\"央视频道\",{name}\n{m3u8_url}"
    except Exception as e:
        print(f"抓取 {name} 失败: {e}")
    return None

async def main():
    print("🚀 开始获取央视全套直播源...")
    tasks = [fetch_m3u8(name, pid) for name, pid in CCTV_CHANNELS.items()]
    results = await asyncio.gather(*tasks)
    
    # 过滤掉抓取失败的结果
    valid_results = [r for r in results if r]
    
    # 生成 M3U 文件
    with open("cctv.m3u", "w", encoding="utf-8") as f:
        f.write("#EXTM3U\n")
        f.write("\n".join(valid_results))
    
    print(f"✅ 完成！成功保存 {len(valid_results)} 个频道至 cctv.m3u")

if __name__ == "__main__":
    asyncio.run(main())
