from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import json

# 配置浏览器选项
chrome_options = Options()
chrome_options.add_argument('--headless')
chrome_options.add_argument('--disable-gpu')
chrome_options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36')

# 初始化驱动
driver = webdriver.Chrome(options=chrome_options)
url = "https://cn.clawhub-mirror.com/skills"
driver.get(url)
time.sleep(2)

# 模拟滚动加载全部数据
last_height = driver.execute_script("return document.body.scrollHeight")
while True:
    # 滚动到底部
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(2)
    # 计算新高度
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# 提取所有技能信息
skill_list = []
items = driver.find_elements(By.CSS_SELECTOR, '.card')

for item in items:
    try:
        title = item.find_element(By.CSS_SELECTOR, '.card-title').text.strip()
        desc = item.find_element(By.CSS_SELECTOR, '.card-text').text.strip()
        author = item.find_element(By.CSS_SELECTOR, '.card-author').text.strip()
        skill_list.append({
            "标题": title,
            "描述": desc,
            "作者": author
        })
    except Exception:
        continue

driver.quit()

# 保存数据
with open("clawhub_skills.json", "w", encoding="utf-8") as f:
    json.dump(skill_list, f, ensure_ascii=False, indent=2)

# 打印预览
for idx, skill in enumerate(skill_list, 1):
    print(f"{idx}. {skill['标题']}")
    print(f"   介绍：{skill['描述']}")
    print(f"   作者：{skill['作者']}\n")