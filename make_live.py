import os

# ================= 配置区 =================
USER_CONFIG = {
    "github_user": "vreace-afk", 
    "repo_name": "live",         
}

# 这里的链接来自大厂 CDN，兼容性测试：移动、电信均可秒开
DIRECT_CHANNELS = """#EXTINF:-1 tvg-name="CCTV1" group-title="央视频道",CCTV-1 综合
http://39.134.115.163:8080/PLTV/88888888/224/3221225618/index.m3u8
#EXTINF:-1 tvg-name="CCTV6" group-title="央视频道",CCTV-6 电影
http://39.134.115.163:8080/PLTV/88888888/224/3221225633/index.m3u8
#EXTINF:-1 tvg-name="CCTV13" group-title="央视频道",CCTV-13 新闻
http://39.134.115.163:8080/PLTV/88888888/224/3221225579/index.m3u8
#EXTINF:-1 tvg-name="湖南卫视" group-title="地方卫视",湖南卫视
http://ws-rtmp-hls.miguvideo.com/migu/621510489/1.m3u8
#EXTINF:-1 tvg-name="浙江卫视" group-title="地方卫视",浙江卫视
http://ws-rtmp-hls.miguvideo.com/migu/609095655/1.m3u8
#EXTINF:-1 tvg-name="东方卫视" group-title="地方卫视",东方卫视
http://ws-rtmp-hls.miguvideo.com/migu/609099304/1.m3u8
#EXTINF:-1 tvg-name="江苏卫视" group-title="地方卫视",江苏卫视
http://ws-rtmp-hls.miguvideo.com/migu/609099239/1.m3u8
"""

def update_readme(count):
    # 使用 gitmirror 镜像，这个镜像在电信网络下加载 M3U 速度最快
    proxy_url = f"https://raw.gitmirror.com/{USER_CONFIG['github_user']}/{USER_CONFIG['repo_name']}/main/cctv.m3u"
    
    content = f"# 📺 私人直播源 (全网通修复版)\n\n## 🔗 影视仓/TVBox 地址\n`{proxy_url}`\n\n## 📊 状态汇总\n- **频道总数**: {count}\n- **更新时间**: {os.popen('date').read().strip()}\n\n> 提示：如果依然显示 0kb，请尝试在影视仓内切换到“硬解”模式。"
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

def main():
    final_data = "#EXTM3U\n" + DIRECT_CHANNELS.strip()
    with open("cctv.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    count = final_data.count("#EXTINF")
    update_readme(count)
    print(f"✅ 全网通源已更新！")

if __name__ == "__main__":
    main()
