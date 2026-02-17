import os

# ================= 配置区 =================
USER_CONFIG = {
    "github_user": "vreace-afk", 
    "repo_name": "live",         
}

# 聚合源中验证过的稳定链接
DIRECT_CHANNELS = """#EXTINF:-1 tvg-name="CCTV1" group-title="央视频道",CCTV-1 综合
http://39.134.115.163:8080/PLTV/88888888/224/3221225618/index.m3u8
#EXTINF:-1 tvg-name="CCTV6" group-title="央视频道",CCTV-6 电影
http://39.134.115.163:8080/PLTV/88888888/224/3221225633/index.m3u8
#EXTINF:-1 tvg-name="CCTV13" group-title="央视频道",CCTV-13 新闻
http://39.134.115.163:8080/PLTV/88888888/224/3221225579/index.m3u8
#EXTINF:-1 tvg-name="湖南卫视" group-title="地方卫视",湖南卫视
http://223.110.243.136/PLTV/3/224/3221227226/index.m3u8
#EXTINF:-1 tvg-name="浙江卫视" group-title="地方卫视",浙江卫视
http://223.110.243.136/PLTV/3/224/3221227204/index.m3u8
#EXTINF:-1 tvg-name="东方卫视" group-title="地方卫视",东方卫视
http://223.110.243.136/PLTV/3/224/3221227166/index.m3u8
"""

def update_readme(count):
    # 提供两个备选地址
    proxy_1 = f"https://ghp.ci/https://raw.githubusercontent.com/{USER_CONFIG['github_user']}/{USER_CONFIG['repo_name']}/main/cctv.m3u"
    proxy_2 = f"https://raw.gitmirror.com/{USER_CONFIG['github_user']}/{USER_CONFIG['repo_name']}/main/cctv.m3u"
    
    content = f"# 📺 私人直播源\n\n## 🔗 影视仓/TVBox 配置地址\n- **地址一 (推荐)**: `{proxy_1}`\n- **地址二 (备选)**: `{proxy_2}`\n\n## 📊 状态汇总\n- **频道总数**: {count}\n- **更新时间**: {os.popen('date').read().strip()}\n"
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

def main():
    # 构造标准 M3U，注意 group-title 的位置
    final_data = "#EXTM3U x-tvg-url=\"https://live.fanmingming.com/e.xml\"\n" + DIRECT_CHANNELS.strip()
    
    # 强制以 utf-8 编码写入
    with open("cctv.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    
    count = final_data.count("#EXTINF")
    update_readme(count)
    print(f"✅ 影视仓优化版已就绪！共 {count} 个频道")

if __name__ == "__main__":
    main()
