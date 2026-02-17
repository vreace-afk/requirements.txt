import os

# ================= 配置区 =================
USER_CONFIG = {
    "github_user": "vreace-afk", 
    "repo_name": "live",         
}

# 采用聚合播放器常用的稳定源，这些源你刚才验证过能用
DIRECT_CHANNELS = """#EXTINF:-1 group-title="央视频道" tvg-name="CCTV1",CCTV-1 综合
http://39.134.115.163:8080/PLTV/88888888/224/3221225618/index.m3u8
#EXTINF:-1 group-title="央视频道" tvg-name="CCTV6",CCTV-6 电影
http://39.134.115.163:8080/PLTV/88888888/224/3221225633/index.m3u8
#EXTINF:-1 group-title="央视频道" tvg-name="CCTV13",CCTV-13 新闻
http://39.134.115.163:8080/PLTV/88888888/224/3221225579/index.m3u8
#EXTINF:-1 group-title="地方卫视" tvg-name="湖南卫视",湖南卫视
http://223.110.243.136/PLTV/3/224/3221227226/index.m3u8
#EXTINF:-1 group-title="地方卫视" tvg-name="浙江卫视",浙江卫视
http://223.110.243.136/PLTV/3/224/3221227204/index.m3u8
#EXTINF:-1 group-title="地方卫视" tvg-name="江苏卫视",江苏卫视
http://223.110.243.136/PLTV/3/224/3221227196/index.m3u8
"""

def update_readme(count):
    # 更换地址生成逻辑：改用 Raw 代理地址，不走 jsDelivr
    raw_url = f"https://ghp.ci/https://raw.githubusercontent.com/{USER_CONFIG['github_user']}/{USER_CONFIG['repo_name']}/main/cctv.m3u"
    content = f"# 📺 私人直播源\n\n## 🔗 TVBox 专用地址 (推荐)\n`{raw_url}`\n\n## 📊 状态汇总\n- **频道总数**: {count}\n- **更新时间**: {os.popen('date').read().strip()}\n"
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

def main():
    final_data = "#EXTM3U\n" + DIRECT_CHANNELS.strip()
    with open("cctv.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    count = final_data.count("#EXTINF")
    update_readme(count)
    print(f"✅ 源已更新！共 {count} 个频道")

if __name__ == "__main__":
    main()
