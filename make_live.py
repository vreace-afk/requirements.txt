import os

# ================= 配置区 =================
USER_CONFIG = {
    "github_user": "vreace-afk", 
    "repo_name": "live",         
}

# 这里的链接是经过筛选的“高清直连”源，兼容性最高
DIRECT_CHANNELS = """#EXTINF:-1 group-title="央视频道" tvg-name="CCTV1",CCTV-1 综合
http://39.134.115.163:8080/PLTV/88888888/224/3221225618/index.m3u8
#EXTINF:-1 group-title="央视频道" tvg-name="CCTV6",CCTV-6 电影
http://39.134.115.163:8080/PLTV/88888888/224/3221225633/index.m3u8
#EXTINF:-1 group-title="央视频道" tvg-name="CCTV13",CCTV-13 新闻
http://39.134.115.163:8080/PLTV/88888888/224/3221225579/index.m3u8
#EXTINF:-1 group-title="地方卫视" tvg-name="湖南卫视",湖南卫视
http://39.134.65.162/migu/621510489/1.m3u8
#EXTINF:-1 group-title="地方卫视" tvg-name="浙江卫视",浙江卫视
http://223.110.243.136/PLTV/3/224/3221227204/index.m3u8
#EXTINF:-1 group-title="地方卫视" tvg-name="东方卫视",东方卫视
http://223.110.243.136/PLTV/3/224/3221227166/index.m3u8
#EXTINF:-1 group-title="地方卫视" tvg-name="江苏卫视",江苏卫视
http://223.110.243.136/PLTV/3/224/3221227196/index.m3u8
"""
# ==========================================

def update_readme(count):
    cdn_url = f"https://jsd.onmicrosoft.cn/gh/{USER_CONFIG['github_user']}/{USER_CONFIG['repo_name']}/cctv.m3u"
    content = f"# 📺 私人直播源（稳定修复版）\n\n## 🔗 订阅地址\n`{cdn_url}`\n\n## 📊 状态汇总\n- **频道总数**: {count}\n- **更新时间**: {os.popen('date').read().strip()}\n\n> 注意：如果电视无法播放，请尝试在链接后加 `?v=2026`。"
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

def main():
    # 直接写入硬编码的内容，跳过不稳定的网络抓取
    final_data = "#EXTM3U\n" + DIRECT_CHANNELS.strip()
    
    with open("cctv.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    
    count = final_data.count("#EXTINF")
    update_readme(count)
    print(f"✅ 修复完成！当前硬编码频道数: {count}")

if __name__ == "__main__":
    main()
