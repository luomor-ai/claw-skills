import os
import re

def extract_skill_info(file_path):
    """
    从单个SKILL.md文件中提取name和description
    :param file_path: 文件路径
    :return: 字典 {name: xxx, description: xxx}
    """
    name = None
    description = None
    
    try:
        # 读取文件内容（兼容utf-8编码）
        with open(file_path, 'r', encoding='utf-8') as f:
            content = f.read()

        # 正则匹配规则（兼容多种写法：name: xxx / name：xxx / ## name: xxx）
        # 匹配 name
        name_match = re.search(r'name\s*[:：]\s*(.+)', content, re.IGNORECASE)
        if name_match:
            name = name_match.group(1).strip()

        # 匹配 description
        desc_match = re.search(r'description\s*[:：]\s*(.+)', content, re.IGNORECASE)
        if desc_match:
            description = desc_match.group(1).strip()

    except Exception as e:
        print(f"⚠️ 读取文件失败 {file_path}: {str(e)}")

    return {
        "file": file_path,
        "name": name if name else "未找到name",
        "description": description if description else "未找到description"
    }

def scan_all_skill_files(root_dir="."):
    """
    遍历所有目录，查找SKILL.md
    :param root_dir: 根目录（默认当前目录）
    :return: 所有skill信息列表
    """
    skill_list = []
    
    # 遍历目录
    for dirpath, dirnames, filenames in os.walk(root_dir):
        for filename in filenames:
            # 匹配所有SKILL.md（不区分大小写）
            if filename.lower() == "skill.md":
                file_path = os.path.join(dirpath, filename)
                skill_info = extract_skill_info(file_path)
                skill_list.append(skill_info)
                print(f"✅ 已处理: {file_path}")
    
    return skill_list

def save_to_file(skill_list, output_file="skill_result.txt"):
    """
    将提取结果保存到文件
    :param skill_list: skill信息列表
    :param output_file: 输出文件名
    """
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write("="*50 + "\n")
        f.write("SKILL信息提取结果\n")
        f.write("="*50 + "\n\n")
        
        for idx, skill in enumerate(skill_list, 1):
            # f.write(f"【第{idx}个文件】\n")
            # f.write(f"文件路径: {skill['file']}\n")
            f.write(f"【第{idx}个技能】\n")
            f.write(f"名称(name): {skill['name']}\n")
            f.write(f"描述(description): {skill['description']}\n")
            f.write("-"*50 + "\n\n")
    
    print(f"\n🎉 提取完成！结果已保存到: {output_file}")

if __name__ == "__main__":
    # 1. 扫描所有SKILL.md
    all_skills = scan_all_skill_files()
    
    # 2. 保存结果
    save_to_file(all_skills)