import httpx
import os
import asyncio

# ================= 配置区 =================
USER_CONFIG = {
    "github_user": "vreace-afk", 
    "repo_name": "live",         
}
# ==========================================

# 使用国内镜像加速地址 (ghp.ci)，确保 GitHub Actions 能抓到数据
STABLE_SOURCES = [
    "https://ghp.ci/https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u",
    "https://ghp.ci/https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u"
]

# 绝对保底频道 (即使上面两个镜像都挂了，也会有这几个台)
EMERGENCY_CHANNELS = """#EXTINF:-1 group-title="保底央视" tvg-name="CCTV1",CCTV-1 综合
http://39.134.115.163:8080/PLTV/88888888/224/3221225618/index.m3u8
#EXTINF:-1 group-title="保底央视" tvg-name="CCTV6",CCTV-6 电影
http://39.134.115.163:8080/PLTV/88888888/224/3221225633/index.m3u8
#EXTINF:-1 group-title="保底央视" tvg-name="CCTV13",CCTV-13 新闻
http://39.134.115.163:8080/PLTV/88888888/224/3221225579/index.m3u8
"""

def update_readme(count):
    cdn_url = f"https://jsd.onmicrosoft.cn/gh/{USER_CONFIG['github_user']}/{USER_CONFIG['repo_name']}/cctv.m3u"
    content = f"# 📺 我的私人直播源\n\n## 🔗 订阅地址\n`{cdn_url}`\n\n## 📊 状态汇总\n- **频道总数**: {count}\n- **最后更新**: {os.popen('date').read().strip()}\n"
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

async def main():
    all_content = ["#EXTM3U"]
    success_count = 0
    
    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True, verify=False) as client:
        for url in STABLE_SOURCES:
            try:
                print(f"正在通过镜像同步: {url}")
                resp = await client.get(url)
                if resp.status_code == 200 and "#EXTINF" in resp.text:
                    # 合并内容
                    lines = resp.text.split('\n')[1:]
                    all_content.extend(lines)
                    success_count += 1
            except Exception as e:
                print(f"同步失败: {e}")
    
    # 如果外部同步全失败了，就用保底频道
    if success_count == 0:
        print("⚠️ 外部源全部失效，启用保底逻辑")
        all_content.append(EMERGENCY_CHANNELS)
    
    final_data = "\n".join([l for l in all_content if l.strip()])
    with open("cctv.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    
    count = final_data.count("#EXTINF")
    update_readme(count)
    print(f"✅ 处理完成！当前频道总数: {count}")

if __name__ == "__main__":
    asyncio.run(main())
