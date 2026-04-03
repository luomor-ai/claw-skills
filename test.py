import requests
import time
import json
from bs4 import BeautifulSoup
from urllib.parse import urljoin

# 基础配置
BASE_URL = "https://clawhub.com"
SKILLS_LIST_URL = urljoin(BASE_URL, "/skills")  # 技能列表页
HEADERS = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
}
REQUEST_DELAY = 1  # 每次请求间隔1秒，遵守爬虫友好原则

def get_all_skill_links():
    """获取所有技能的名称和详情链接"""
    try:
        response = requests.get(SKILLS_LIST_URL, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        skills = []
        # 匹配技能卡片/链接（根据页面结构调整）
        skill_items = soup.select("a[href*='/skills/']")  # 包含 /skills/ 的链接
        
        for item in skill_items:
            skill_name = item.get_text(strip=True)
            skill_url = urljoin(BASE_URL, item["href"])
            
            # 去重 + 过滤空名称
            if skill_name and skill_url not in [s["url"] for s in skills]:
                skills.append({
                    "name": skill_name,
                    "url": skill_url
                })
        
        print(f"✅ 成功获取到 {len(skills)} 个技能")
        return skills
    
    except Exception as e:
        print(f"❌ 获取技能列表失败：{str(e)}")
        return []

def get_skill_intro(skill_url):
    """爬取单个技能的简介/描述"""
    try:
        time.sleep(REQUEST_DELAY)  # 请求延时
        response = requests.get(skill_url, headers=HEADERS, timeout=10)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, "html.parser")
        
        # 匹配简介区域（根据页面实际结构调整选择器）
        intro_elem = soup.select_one(".skill-description, .intro, .content p")
        intro = intro_elem.get_text(strip=True) if intro_elem else "暂无简介"
        
        # 清洗空内容
        if not intro or len(intro) < 5:
            intro = "暂无简介"
        
        return intro
    
    except Exception as e:
        print(f"❌ 爬取 {skill_url} 简介失败：{str(e)}")
        return "爬取失败"

def crawl_all_skills():
    """主函数：爬取所有技能 + 简介"""
    # 1. 获取所有技能列表
    skill_list = get_all_skill_links()
    if not skill_list:
        return
    
    # 2. 逐个爬取简介
    print("\n开始爬取技能简介...")
    result = []
    for idx, skill in enumerate(skill_list, 1):
        name = skill["name"]
        url = skill["url"]
        intro = get_skill_intro(url)
        
        skill_data = {
            "id": idx,
            "skill_name": name,
            "skill_url": url,
            "introduction": intro
        }
        result.append(skill_data)
        
        print(f"{idx:03d} | {name} | {intro[:30]}...")
    
    # 3. 保存结果
    save_to_json(result)
    save_to_markdown(result)
    print("\n🎉 爬取完成！数据已保存为 skills.json 和 skills.md")

def save_to_json(data):
    """保存为 JSON 文件"""
    with open("skills.json", "w", encoding="utf-8") as f:
        json.dump(data, f, ensure_ascii=False, indent=2)

def save_to_markdown(data):
    """保存为 Markdown 文档（带格式）"""
    md_content = "# Clawhub 技能图谱大全\n\n> 爬取时间：2026年\n| 序号 | 技能名称 | 简介 |\n| ---- | -------- | ---- |\n"
    
    for item in data:
        md_content += f"| {item['id']} | {item['skill_name']} | {item['introduction']} |\n"
    
    with open("skills.md", "w", encoding="utf-8") as f:
        f.write(md_content)

if __name__ == "__main__":
    crawl_all_skills()