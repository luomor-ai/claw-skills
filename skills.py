import os
import re

def extract_skill_info(file_path):
    """
    从SKILL.md提取 name 和 description（支持跨多行）
    任意字段不存在则返回 None，表示跳过
    """
    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            lines = f.readlines()

    except Exception as e:
        print(f"❌ 读取失败: {file_path} | {str(e)}")
        return None

    name = None
    description = None
    capture_description = False
    desc_lines = []

    # 逐行解析（支持换行）
    for line in lines:
        stripped = line.strip()

        # ========== 匹配 name ==========
        if not name and re.match(r'^name\s*[:：]', stripped, re.IGNORECASE):
            # 去掉 name: 后面的内容
            name_val = re.sub(r'^name\s*[:：]\s*', '', stripped, flags=re.IGNORECASE).strip()
            if name_val:
                name = name_val

        # ========== 匹配 description（支持换行） ==========
        elif not description and re.match(r'^description\s*[:：]', stripped, re.IGNORECASE):
            # 第一行 description
            first_line = re.sub(r'^description\s*[:：]\s*', '', stripped, flags=re.IGNORECASE).strip()
            desc_lines.append(first_line)
            capture_description = True  # 开始捕获后续行

        elif capture_description:
            # 遇到空行 / 下一个字段 停止捕获
            if not stripped or stripped.startswith(('name', 'description', '#', '-', '*')):
                capture_description = False
                continue
            desc_lines.append(stripped)

    # 拼接 description
    if desc_lines:
        description = ' '.join([x.strip() for x in desc_lines if x.strip()])

    # ========== 关键规则：任意一个不存在则跳过 ==========
    if not name or not description:
        return None

    return {
        "file": file_path,
        "name": name,
        "description": description
    }

def scan_all_skill_files(root_dir="."):
    skill_list = []
    for dirpath, _, filenames in os.walk(root_dir):
        for filename in filenames:
            if filename.lower() == "skill.md":
                file_path = os.path.join(dirpath, filename)
                info = extract_skill_info(file_path)
                if info:
                    skill_list.append(info)
                    print(f"✅ 已提取: {file_path}")
                else:
                    print(f"⏭️  已跳过: {file_path}（字段不完整）")
    return skill_list

def save_to_file(skill_list, output="skill_result.txt"):
    with open(output, 'w', encoding='utf-8') as f:
        f.write("=" * 50 + "\n")
        f.write("SKILL 信息提取结果（已跳过不完整字段）\n")
        f.write("=" * 50 + "\n\n")

        for idx, skill in enumerate(skill_list, 1):
            f.write(f"【{idx}】\n")
            f.write(f"文件路径: {skill['file']}\n")
            f.write(f"名称: {skill['name']}\n")
            f.write(f"描述: {skill['description']}\n")
            f.write("-" * 50 + "\n\n")

    print(f"\n🎉 提取完成！共 {len(skill_list)} 条有效数据 | 已保存到 {output}")

if __name__ == "__main__":
    skills = scan_all_skill_files()
    save_to_file(skills)