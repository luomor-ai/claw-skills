import requests
import pandas as pd
import time
 
# ===================== 配置参数 =====================
BASE_URL = "https://api.clawhub.com/skills"  # ClawHub Skills 核心接口
PAGE_SIZE = 20  # 每页数据量（接口默认值）
OUTPUT_FILE = "clawhub_all_skills.csv"  # 输出文件名
DELAY = 1  # 请求间隔（秒），避免请求过快被限制
# ====================================================
 
def fetch_all_clawhub_skills():
    """抓取 ClawHub 所有 Skills 数据"""
    all_skills = []
    page_num = 1
    print("🚀 开始抓取 ClawHub Skills 数据...")
 
    while True:
        try:
            # 构造请求参数
            params = {
                "page": page_num,
                "size": PAGE_SIZE
            }
            # 发送 GET 请求
            response = requests.get(BASE_URL, params=params, timeout=10)
            response.raise_for_status()  # 抛出请求异常
            data = response.json()
 
            # 提取当前页技能列表
            skills_list = data.get("data", {}).get("records", [])
            if not skills_list:
                print(f"\n📌 第 {page_num} 页无数据，抓取完成！")
                break
 
            # 清洗核心字段（按需增减）
            for skill in skills_list:
                skill_info = {
                    "技能ID": skill.get("id", ""),
                    "技能名称": skill.get("name", ""),
                    "技能描述": skill.get("description", "").replace("\n", " ").replace("\r", ""),
                    "作者": skill.get("author", ""),
                    "分类": skill.get("category", ""),
                    "标签": ", ".join(skill.get("tags", [])),
                    "创建时间": skill.get("createTime", ""),
                    "更新时间": skill.get("updateTime", ""),
                    "点赞数": skill.get("likeCount", 0),
                    "下载数": skill.get("downloadCount", 0),
                    "技能链接": f"https://clawhub.com/skill/{skill.get('id', '')}"
                }
                all_skills.append(skill_info)
 
            print(f"✅ 成功抓取第 {page_num} 页，当前累计：{len(all_skills)} 条")
            page_num += 1
            time.sleep(DELAY)  # 友好延时
 
        except Exception as e:
            print(f"❌ 第 {page_num} 页抓取失败：{str(e)}")
            time.sleep(DELAY * 2)
            continue
 
    return all_skills
 
def save_to_csv(skills_data, output_path):
    """保存数据到 CSV 文件"""
    if not skills_data:
        print("⚠️ 无数据可保存")
        return
 
    df = pd.DataFrame(skills_data)
    df.to_csv(output_path, index=False, encoding="utf-8-sig")
    print(f"\n🎉 数据保存成功！文件路径：{output_path}")
    print(f"📊 总抓取技能数量：{len(skills_data)} 条")
 
if __name__ == "__main__":
    # 执行抓取
    skills_data = fetch_all_clawhub_skills()
    # 保存文件
    save_to_csv(skills_data, OUTPUT_FILE)

