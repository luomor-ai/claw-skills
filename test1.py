import requests
import pandas as pd
import time

# ===================== 修复配置 =====================
BASE_URL = "https://clawhub.ai/api/v1/search"  # 新API地址
PAGE_SIZE = 50
OUTPUT_FILE = "clawhub_all_skills.csv"
DELAY = 1.5
# ====================================================

def fetch_all_clawhub_skills():
    all_skills = []
    page_num = 1
    print("🚀 开始抓取 ClawHub.ai 所有技能...")

    while True:
        try:
            # 新接口参数
            payload = {
                "q": "",          # 空字符串=搜索全部
                "limit": PAGE_SIZE,
                "offset": (page_num - 1) * PAGE_SIZE,
                "sort": "newest"
            }
            
            response = requests.post(BASE_URL, json=payload, timeout=15)
            response.raise_for_status()
            data = response.json()

            skills_list = data.get("skills", [])
            if not skills_list:
                print(f"\n📌 第 {page_num} 页无数据，抓取完成！")
                break

            for skill in skills_list:
                skill_info = {
                    "技能ID": skill.get("id", ""),
                    "名称": skill.get("name", ""),
                    "描述": skill.get("description", "").replace("\n", " "),
                    "作者": skill.get("author", {}).get("handle", ""),
                    "分类": ", ".join(skill.get("categories", [])),
                    "标签": ", ".join(skill.get("tags", [])),
                    "版本": skill.get("latestVersion", {}).get("version", ""),
                    "下载量": skill.get("downloads", 0),
                    "点赞": skill.get("likes", 0),
                    "创建时间": skill.get("createdAt", ""),
                    "技能链接": f"https://clawhub.ai/skill/{skill.get('id', '')}"
                }
                all_skills.append(skill_info)

            print(f"✅ 第 {page_num} 页完成 | 累计：{len(all_skills)}")
            page_num += 1
            time.sleep(DELAY)

        except Exception as e:
            print(f"❌ 第 {page_num} 页失败：{str(e)}")
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