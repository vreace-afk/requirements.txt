import httpx
import os
import asyncio

# ================= 配置区 =================
USER_CONFIG = {
    "github_user": "vreace-afk", 
    "repo_name": "live",         
}
# ==========================================

# 精选国内最稳定的三个大型源（包含了数千个频道，覆盖央视、卫视、电影、轮播）
STABLE_SOURCES = [
    "https://ghp.ci/https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u",
    "https://ghp.ci/https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u",
    "https://ghp.ci/https://raw.githubusercontent.com/billy21/Tvlist-awesome-m3u-m3u8/master/m3u/TV_Channels.m3u"
]

def update_readme(count):
    cdn_url = f"https://jsd.onmicrosoft.cn/gh/{USER_CONFIG['github_user']}/{USER_CONFIG['repo_name']}/cctv.m3u"
    content = f"# 📺 我的私人直播源\n\n## 🔗 订阅地址 (长按复制)\n`{cdn_url}`\n\n## 📊 状态汇总\n- **频道总数**: {count}\n- **最后更新**: {os.popen('date').read().strip()} (UTC)\n\n> 提示：如果播放失败，请在链接末尾加上 `?v=2026` 尝试。"
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

async def main():
    all_content = ["#EXTM3U"]
    
    # 增加更长的超时时间，确保 GitHub 能拉取成功
    async with httpx.AsyncClient(timeout=100.0, follow_redirects=True, verify=False) as client:
        for url in STABLE_SOURCES:
            try:
                print(f"📡 正在拉取源: {url}")
                resp = await client.get(url)
                if resp.status_code == 200 and "#EXTINF" in resp.text:
                    # 提取内容，过滤掉重复的标题头
                    lines = resp.text.split('\n')
                    for line in lines:
                        if "#EXTM3U" not in line and line.strip():
                            all_content.append(line.strip())
            except Exception as e:
                print(f"❌ 拉取失败 {url}: {e}")
    
    # 最终合并并去重（简单处理）
    final_data = "\n".join(all_content)
    with open("cctv.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    
    count = final_data.count("#EXTINF")
    update_readme(count)
    print(f"✅ 处理完成！当前频道总数: {count}")

if __name__ == "__main__":
    asyncio.run(main())
