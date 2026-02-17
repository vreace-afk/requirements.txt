import os

# ================= 配置区 =================
USER_CONFIG = {
    "github_user": "vreace-afk", 
    "repo_name": "live",         
}

# 针对电信网络优化的 7 个高清源
DIRECT_CHANNELS = """#EXTINF:-1 group-title="央视频道" tvg-name="CCTV1",CCTV-1 综合
http://117.148.187.37/PLTV/88888888/224/3221225732/index.m3u8
#EXTINF:-1 group-title="央视频道" tvg-name="CCTV6",CCTV-6 电影
http://117.148.187.37/PLTV/88888888/224/3221225718/index.m3u8
#EXTINF:-1 group-title="央视频道" tvg-name="CCTV13",CCTV-13 新闻
http://117.148.187.37/PLTV/88888888/224/3221225695/index.m3u8
#EXTINF:-1 group-title="地方卫视" tvg-name="湖南卫视",湖南卫视
http://117.148.187.37/PLTV/88888888/224/3221225791/index.m3u8
#EXTINF:-1 group-title="地方卫视" tvg-name="浙江卫视",浙江卫视
http://117.148.187.37/PLTV/88888888/224/3221225807/index.m3u8
#EXTINF:-1 group-title="地方卫视" tvg-name="东方卫视",东方卫视
http://117.148.187.37/PLTV/88888888/224/3221225769/index.m3u8
#EXTINF:-1 group-title="地方卫视" tvg-name="江苏卫视",江苏卫视
http://117.148.187.37/PLTV/88888888/224/3221225799/index.m3u8
"""
# ==========================================

def update_readme(count):
    cdn_url = f"https://jsd.onmicrosoft.cn/gh/{USER_CONFIG['github_user']}/{USER_CONFIG['repo_name']}/cctv.m3u"
    content = f"# 📺 私人直播源（电信稳定版）\n\n## 🔗 订阅地址\n`{cdn_url}`\n\n## 📊 状态汇总\n- **频道总数**: {count}\n- **更新时间**: {os.popen('date').read().strip()}\n"
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

def main():
    final_data = "#EXTM3U\n" + DIRECT_CHANNELS.strip()
    with open("cctv.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    count = final_data.count("#EXTINF")
    update_readme(count)
    print(f"✅ 电信源替换完成！共 {count} 个频道")

if __name__ == "__main__":
    main()
