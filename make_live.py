import os

# ================= 配置区 =================
USER_CONFIG = {
    "github_user": "vreace-afk", 
    "repo_name": "live",         
}

# 针对电信 IPv6 环境优化的 4K/高清专线
DIRECT_CHANNELS = """#EXTINF:-1 tvg-name="CCTV1" group-title="央视IPv6",CCTV-1 综合 (高清)
http://[240e:97c:2f:2::e1]/ottrrs.miguvideo.com/PLTV/88888888/224/3221225618/index.m3u8
#EXTINF:-1 tvg-name="CCTV6" group-title="央视IPv6",CCTV-6 电影 (高清)
http://[240e:97c:2f:2::e1]/ottrrs.miguvideo.com/PLTV/88888888/224/3221225633/index.m3u8
#EXTINF:-1 tvg-name="CCTV13" group-title="央视IPv6",CCTV-13 新闻 (高清)
http://[240e:97c:2f:2::e1]/ottrrs.miguvideo.com/PLTV/88888888/224/3221225579/index.m3u8
#EXTINF:-1 tvg-name="湖南卫视" group-title="卫视IPv6",湖南卫视 (高清)
http://[240e:94:d4a1:1:c::1]/migu/621510489/1.m3u8
#EXTINF:-1 tvg-name="浙江卫视" group-title="卫视IPv6",浙江卫视 (高清)
http://[240e:94:d4a1:1:c::1]/migu/609095655/1.m3u8
#EXTINF:-1 tvg-name="东方卫视" group-title="卫视IPv6",东方卫视 (高清)
http://[240e:94:d4a1:1:c::1]/migu/609099304/1.m3u8
#EXTINF:-1 tvg-name="江苏卫视" group-title="卫视IPv6",江苏卫视 (高清)
http://[240e:94:d4a1:1:c::1]/migu/609099239/1.m3u8
"""

def update_readme(count):
    # 使用 gitmirror 镜像，这个地址加载 m3u 文件最快
    proxy_url = f"https://raw.gitmirror.com/{USER_CONFIG['github_user']}/{USER_CONFIG['repo_name']}/main/cctv.m3u"
    
    content = f"# 📺 私人直播源 (IPv6 专线版)\n\n## 🔗 影视仓/TVBox 配置地址\n`{proxy_url}`\n\n## 📊 状态汇总\n- **频道总数**: {count}\n- **更新时间**: {os.popen('date').read().strip()}\n\n> **注意**: 请保持 VPN 关闭以确保 IPv6 通道可用。"
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

def main():
    final_data = "#EXTM3U\n" + DIRECT_CHANNELS.strip()
    with open("cctv.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    count = final_data.count("#EXTINF")
    update_readme(count)
    print(f"✅ IPv6 专线源已就绪！")

if __name__ == "__main__":
    main()
