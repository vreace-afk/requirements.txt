import os

# ================= 配置区 =================
USER_CONFIG = {
    "github_user": "vreace-afk", 
    "repo_name": "live",         
}

# 针对电信宽带优化的“秒开”源（使用电信官方 CDN 或腾讯/阿里转发流）
DIRECT_CHANNELS = """#EXTINF:-1 tvg-name="CCTV1" group-title="央视频道",CCTV-1 综合
http://ivi.bupt.edu.cn/hls/cctv1hd.m3u8
#EXTINF:-1 tvg-name="CCTV6" group-title="央视频道",CCTV-6 电影
http://ivi.bupt.edu.cn/hls/cctv6hd.m3u8
#EXTINF:-1 tvg-name="CCTV13" group-title="央视频道",CCTV-13 新闻
http://ivi.bupt.edu.cn/hls/cctv13.m3u8
#EXTINF:-1 tvg-name="湖南卫视" group-title="地方卫视",湖南卫视
https://pili-live-hls.huya.com/src/1394541539-1394541539-7063116819448004608-2789269784-10057-A-0-1-imgplus.m3u8
#EXTINF:-1 tvg-name="浙江卫视" group-title="地方卫视",浙江卫视
https://pili-live-hls.huya.com/src/1394541541-1394541541-7063116828037939200-2789270114-10057-A-0-1-imgplus.m3u8
#EXTINF:-1 tvg-name="广东卫视" group-title="地方卫视",广东卫视
http://ivi.bupt.edu.cn/hls/gdhd.m3u8
"""

def update_readme(count):
    # 使用 gitmirror 镜像，这个镜像在电信网络下最快
    proxy_url = f"https://raw.gitmirror.com/{USER_CONFIG['github_user']}/{USER_CONFIG['repo_name']}/main/cctv.m3u"
    
    content = f"# 📺 私人直播源 (电信秒开版)\n\n## 🔗 影视仓/TVBox 地址\n`{proxy_url}`\n\n## 📊 状态汇总\n- **频道总数**: {count}\n- **更新时间**: {os.popen('date').read().strip()}\n"
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

def main():
    final_data = "#EXTM3U\n" + DIRECT_CHANNELS.strip()
    with open("cctv.m3u", "w", encoding="utf-8", newline='\n') as f:
        f.write(final_data)
    count = final_data.count("#EXTINF")
    update_readme(count)
    print(f"✅ 电信加速源已更新！")

if __name__ == "__main__":
    main()
