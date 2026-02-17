import httpx
import os
import asyncio

# ================= 配置区 =================
USER_CONFIG = {
    "github_user": "vreace-afk", 
    "repo_name": "live",         
}
# ==========================================

# 1. 即使断网也绝对存在的“永久频道列表” (包含 CCTV 和 卫视)
EMERGENCY_LIST = """#EXTINF:-1 group-title="央视频道" tvg-name="CCTV1",CCTV-1 综合
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
"""

# 2. 尝试同步的外部大仓库
STABLE_SOURCES = [
    "https://ghp.ci/https://raw.githubusercontent.com/fanmingming/live/main/tv/m3u/ipv6.m3u",
    "https://ghp.ci/https://raw.githubusercontent.com/YanG-1989/m3u/main/Gather.m3u"
]

def update_readme(count):
    cdn_url = f"https://jsd.onmicrosoft.cn/gh/{USER_CONFIG['github_user']}/{USER_CONFIG['repo_name']}/cctv.m3u"
    content = f"# 📺 我的私人直播源\n\n## 🔗 订阅地址\n`{cdn_url}`\n\n## 📊 状态汇总\n- **频道总数**: {count}\n- **最后更新**: {os.popen('date').read().strip()} (UTC)\n\n> **说明**: 如果总数只有个位数，说明云端同步繁忙，系统已启用保底模式。"
    with open("README.md", "w", encoding="utf-8") as f:
        f.write(content)

async def main():
    # 初始内容设为保底列表
    all_content = ["#EXTM3U", EMERGENCY_LIST.strip()]
    
    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True, verify=False) as client:
        for url in STABLE_SOURCES:
            try:
                print(f"📡 尝试同步外部源: {url}")
                resp = await client.get(url)
                if resp.status_code == 200 and "#EXTINF" in resp.text:
                    # 抓取成功，把内容加进去
                    lines = resp.text.split('\n')[1:]
                    all_content.extend(lines)
                    print(f"✅ 同步 {url} 成功")
            except Exception as e:
                print(f"❌ 同步失败: {e}")
    
    # 合并数据
    final_data = "\n".join([l for l in all_content if l.strip()])
    with open("cctv.m3u", "w", encoding="utf-8") as f:
        f.write(final_data)
    
    # 统计频道数 (排除 EXTM3U 头部)
    count = final_data.count("#EXTINF")
    update_readme(count)
    print(f"🏁 任务结束，当前频道总数: {count}")

if __name__ == "__main__":
    asyncio.run(main())
