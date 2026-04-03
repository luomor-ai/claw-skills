import requests
from bs4 import BeautifulSoup
import re

# 目标页面
url = "https://cn.clawhub-mirror.com/skills"
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
}

# 请求页面
resp = requests.get(url, headers=headers)
soup = BeautifulSoup(resp.text, "html.parser")

# 提取所有技能卡片
skills = []
a_tags = soup.find_all("a", class_="btn")

for i in range(0, len(a_tags), 3):
    try:
        title = a_tags[i].get_text(strip=True)
        desc = a_tags[i+1].get_text(strip=True) if i+1 < len(a_tags) else ""
        author = a_tags[i+2].get_text(strip=True) if i+2 < len(a_tags) else ""
        skills.append({
            "title": title,
            "desc": desc,
            "author": author
        })
    except:
        continue

# 输出结果
for idx, s in enumerate(skills, 1):
    print(f"{idx}. {s['title']}")
    print(f"   介绍：{s['desc']}")
    print(f"   {s['author']}\n")