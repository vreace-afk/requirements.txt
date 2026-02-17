import os

# ================= 配置区 =================
USER_CONFIG = {
    "github_user": "vreace-afk", 
    "repo_name": "live",         
}

# 使用官方 HLS 代理源，这些源在电信网络下兼容性最强
DIRECT_CHANNELS = """#EXTINF:-1 group-title="央视频道" tvg-name="CCTV1",CCTV-1 综合
http://ivi.bupt.edu.cn/hls/cctv1hd.m3u8
#EXTINF:-1 group-title="央视频道" tvg-name="CCTV3",CCTV-3 综艺
http://ivi.bupt.edu.cn/hls/cctv3hd.m3u8
#EXTINF:-1 group-title="央视频道" tvg-name="CCTV6",CCTV-6 电影
http://ivi.bupt.edu.cn/hls/cctv6hd.m3u8
#EXTINF:-1 group-title="央视频道" tvg-name="CCTV13",CCTV-13 新闻
http://ivi.bupt.edu.cn/hls/cctv13.m3u8
#EXTINF:-1 group-title="地方卫视" tvg-name="湖南卫视",湖南卫视
http://ivi.bupt.edu.cn/hls/hunanhd.m3u8
#EXTINF:-1 group-title="地方卫视" tvg-name="浙江卫视",浙江卫视
http://ivi.bupt.edu.cn/hls/zjhd.m3u8
#EXTINF:-1 group-title="地方卫视" tvg-name="广东卫视",广东卫视
http://ivi.bupt.edu.cn/hls/gdhd.m3u8
"""
# ==========================================

def update_readme(count):
    cdn_url = f"https://jsd.onmicrosoft.cn/gh/{USER_CONFIG['github_user']}/{USER_CONFIG['repo_name']}/cctv.m3u"
    content = f"# 📺 私人直播源（全兼容版）\n\n## 🔗 订阅地址\n`{cdn_url}`\n\n## 📊 状态汇总\n- **频道总数**: {count}\n- **更新时间**: {os.popen('date').read().strip()}\n"
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

def main():
    final_data = "#EXTM3U\n" + DIRECT_CHANNELS.strip()
    with open("cctv.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    count = final_data.count("#EXTINF")
    update_readme(count)
    print(f"✅ 全兼容源已就绪！共 {count} 个频道")

if __name__ == "__main__":
    main()
