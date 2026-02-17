import httpx
import os

# ================= 配置区 =================
USER_CONFIG = {
    "github_user": "vreace-afk", 
    "repo_name": "live",         
}
# ==========================================

# 两个最稳定的国内直连源 (包含 CCTV, 卫视, 数字频道)
STABLE_SOURCES = [
    "https://ghp.ci/https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u",
    "https://ghp.ci/https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u"
]

def update_readme(count):
    cdn_url = f"https://jsd.onmicrosoft.cn/gh/{USER_CONFIG['github_user']}/{USER_CONFIG['repo_name']}/cctv.m3u"
    content = f"# 📺 我的私人直播源\n\n## 🔗 订阅地址\n`{cdn_url}`\n\n## 📊 状态汇总\n- **频道总数**: {count}\n- **最后更新**: {os.popen('date').read().strip()}\n"
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

async def main():
    all_content = ["#EXTM3U"]
    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True, verify=False) as client:
        for url in STABLE_SOURCES:
            try:
                print(f"正在同步稳定源: {url}")
                resp = await client.get(url)
                if resp.status_code == 200:
                    # 去掉第一行的 #EXTM3U，然后合并
                    lines = resp.text.split('\n')[1:]
                    all_content.extend(lines)
            except Exception as e:
                print(f"同步失败: {e}")
    
    # 写入最终文件
    final_data = "\n".join(all_content)
    with open("cctv.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    
    # 计算频道数
    count = final_data.count("#EXTINF")
    update_readme(count)
    print(f"✅ 同步成功！总计 {count} 个频道")

if __name__ == "__main__":
    import asyncio
    asyncio.run(main())
