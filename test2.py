import requests
import pandas as pd
import time

# ===================== 最新配置 (2026.4) =====================
BASE_URL = "https://clawhub.ai/api/v1/skills"  # 正确列表接口
PAGE_SIZE = 50
OUTPUT_FILE = "clawhub_all_skills.csv"
DELAY = 1.5
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/122.0.0.0 Safari/537.36",
    "Accept": "application/json"
}
# ==============================================================

def fetch_all_clawhub_skills():
    all_skills = []
    cursor = ""
    page_num = 1
    print("🚀 开始抓取 ClawHub.ai 所有技能 (游标分页)...")

    while True:
        try:
            # 游标分页参数
            params = {
                "limit": PAGE_SIZE,
                "cursor": cursor
            }
            
            response = requests.get(BASE_URL, params=params, headers=HEADERS, timeout=15)
            response.raise_for_status()
            data = response.json()

            skills_list = data.get("skills", [])
            next_cursor = data.get("nextCursor", None)

            if not skills_list:
                print(f"\n📌 第 {page_num} 页无数据，抓取完成！")
                break

            # 清洗字段（适配最新返回结构）
            for skill in skills_list:
                skill_info = {
                    "技能ID": skill.get("id", ""),
                    "Slug": skill.get("slug", ""),
                    "名称": skill.get("name", ""),
                    "描述": skill.get("description", "").replace("\n", " ").replace("\r", ""),
                    "作者": skill.get("authorHandle", ""),
                    "分类": ", ".join(skill.get("categories", [])),
                    "标签": ", ".join(skill.get("tags", [])),
                    "版本": skill.get("latestVersion", ""),
                    "下载量": skill.get("downloads", 0),
                    "点赞": skill.get("likes", 0),
                    "创建时间": skill.get("createdAt", ""),
                    "技能链接": f"https://clawhub.ai/{skill.get('authorHandle', '')}/{skill.get('slug', '')}"
                }
                all_skills.append(skill_info)

            print(f"✅ 第 {page_num} 页 | 累计：{len(all_skills)} | 下游标：{next_cursor[:20] if next_cursor else '无'}")
            
            # 判断是否结束
            if not next_cursor:
                print("\n🎉 已到达最后一页！")
                break

            cursor = next_cursor
            page_num += 1
            time.sleep(DELAY)

        except Exception as e:
            print(f"❌ 第 {page_num} 页失败：{str(e)}")
            if "404" in str(e):
                print("💡 提示：接口可能再次变更，请检查官方文档或尝试搜索接口。")
                break
            time.sleep(DELAY * 2)
            continue

    return all_skills

def save_to_csv(skills_data, output_path):
    if not skills_data:
        print("⚠️ 无数据可保存")
        return
    df = pd.DataFrame(skills_data)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\n🎉 保存成功：{output_path}")
    print(f"📊 总技能数：{len(skills_data)}")

if __name__ == "__main__":
    skills_data = fetch_all_clawhub_skills()
    save_to_csv(skills_data, OUTPUT_FILE)