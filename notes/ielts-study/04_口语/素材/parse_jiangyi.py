#!/usr/bin/env python3
"""
解析讲义.md，生成排版好的口语题库Markdown
支持多种格式的Part
"""

import re

def extract_question(line):
    """提取英文问题部分（去掉中文翻译）"""
    line = line.strip()
    if '?' not in line:
        return None

    q_parts = line.split('?')
    question_part = q_parts[0]

    question_words = ['When', 'What', 'How', 'Do', 'Does', 'Did', 'Are', 'Is', 'Has', 'Have', 'Can', 'Would', 'Should', 'Why', 'Who', 'Where', 'Which', 'If', 'Tell', 'Describe']
    for word in question_words:
        if question_part.strip().startswith(word):
            return question_part.strip() + '?'

    if len(re.findall(r'[a-zA-Z]', question_part)) > 20:
        return question_part.strip() + '?'

    return None

def is_topic_line_part1(line):
    """Part 1的话题格式：英文开头+中文结尾"""
    line = line.strip()
    if not line or len(line) < 5:
        return False
    if '?' in line:
        return False

    en_match = re.match(r'^([A-Za-z][a-z]*)\s+', line)
    if not en_match:
        return False

    cn_chars = re.findall(r'[\u4e00-\u9fff]', line)
    if not cn_chars:
        return False

    if len(line) > 50:
        return False

    return True

def is_topic_line_part3(line):
    """Part 3的话题格式：数字编号开头 + 英文"""
    line = line.strip()
    if not line:
        return False

    if re.match(r'^\d+\.\s+[A-Za-z]', line):
        return True

    return False

def is_part2_question(line):
    """Part 2的描述题格式：Describe开头"""
    line = line.strip()
    return line.startswith('Describe ')

def clean_answer_line(line):
    """清理答案行"""
    line = line.strip()

    # 跳过话题行
    if is_topic_line_part1(line):
        return None
    if is_topic_line_part3(line):
        return None

    cn = len(re.findall(r'[\u4e00-\u9fff]', line))
    en = len(re.findall(r'[a-zA-Z]', line))

    if cn > 0 and cn >= en * 0.5:
        return None

    result = ""
    for char in line:
        if char.isascii() or char in ' .,!?\'"-':
            result += char
        elif char == ' ':
            result += ' '

    return result.strip() if result.strip() else None

def merge_sentences(lines):
    """合并断行的英文句子"""
    if not lines:
        return ""

    result = []
    buffer = ""

    for line in lines:
        line = clean_answer_line(line)
        if not line:
            continue

        if buffer:
            if buffer[-1].isalpha() and buffer[-1].islower():
                if buffer[-1] not in '.!?':
                    buffer += " " + line
                    continue

        if buffer:
            result.append(buffer)
        buffer = line

    if buffer:
        result.append(buffer)

    return " ".join(result)

def parse_file():
    """解析讲义.md"""
    input_path = "/Users/baojian/Desktop/IELTS/04_口语/素材/讲义.md"

    with open(input_path, 'r', encoding='utf-8') as f:
        lines = f.read().split('\n')

    # 找Part边界
    part_positions = []
    for i, line in enumerate(lines):
        if re.search(r'Part\s*[123]', line):
            part_positions.append((i, line.strip()))

    all_sections = []

    for idx in range(len(part_positions)):
        pos, part_title = part_positions[idx]

        # 确定Part编号
        if re.search(r'Part\s*1', part_title) and not re.search(r'Part\s*[23]', part_title):
            part_num = 1
        elif re.search(r'Part\s*2', part_title):
            part_num = 2
        elif re.search(r'Part\s*3', part_title):
            part_num = 3
        else:
            part_num = 0

        if idx + 1 < len(part_positions):
            end_pos = part_positions[idx + 1][0]
        else:
            end_pos = len(lines)

        print(f"处理 Part {part_num}: 行 {pos+1}-{end_pos}")

        if part_num == 1:
            topics_data = parse_part1(lines, pos, end_pos)
        elif part_num == 2:
            topics_data = parse_part2(lines, pos, end_pos)
        else:
            topics_data = parse_part3(lines, pos, end_pos)

        print(f"  -> {len(topics_data)} 个话题, {sum(len(qs) for _, qs in topics_data)} 道题")

        all_sections.append({
            'part': f'Part {part_num}',
            'topics': topics_data
        })

    return all_sections

def parse_part1(lines, start_line, end_line):
    """解析Part 1区域"""
    topics_data = []
    current_topic = None
    current_questions = []

    i = start_line

    while i < end_line:
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        # 检测话题行
        if is_topic_line_part1(line):
            if current_topic and current_questions:
                topics_data.append((current_topic, current_questions))
            current_topic = line
            current_questions = []

        # 检测问句
        question = extract_question(line)
        if question:
            answer_lines = []
            j = i + 1

            while j < end_line:
                next_line = lines[j].strip()

                if extract_question(next_line):
                    break
                if is_topic_line_part1(next_line):
                    break

                cleaned = clean_answer_line(next_line)
                if cleaned and len(cleaned) > 5:
                    answer_lines.append(cleaned)

                j += 1

            answer = merge_sentences(answer_lines)
            if answer:
                current_questions.append({'question': question, 'answer': answer})

            i = j
            continue

        i += 1

    if current_topic and current_questions:
        topics_data.append((current_topic, current_questions))

    return topics_data

def parse_part2(lines, start_line, end_line):
    """解析Part 2区域 - 串题格式"""
    topics_data = []
    current_topic = None
    current_questions = []

    i = start_line

    while i < end_line:
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        # 检测话题分类标题（中文开头，无问号）
        if re.match(r'^[\u4e00-\u9fff]', line) and '?' not in line and len(line) < 30:
            if current_topic and current_questions:
                topics_data.append((current_topic, current_questions))
            current_topic = line
            current_questions = []

        # 检测Describe题目
        if is_part2_question(line):
            full_question = line
            prompt_lines = []
            j = i + 1

            while j < end_line:
                next_line = lines[j].strip()
                if is_part2_question(next_line) or (re.match(r'^[\u4e00-\u9fff]', next_line) and '?' not in next_line):
                    break
                if next_line.startswith('You ') or next_line.startswith('And '):
                    prompt_lines.append(next_line)
                j += 1

            if prompt_lines:
                full_question = line + '\n\n' + '\n'.join(prompt_lines)

            current_questions.append({'question': full_question, 'answer': '(见原讲义视频)'})
            i = j
            continue

        i += 1

    if current_topic and current_questions:
        topics_data.append((current_topic, current_questions))

    return topics_data

def parse_part3(lines, start_line, end_line):
    """解析Part 3区域 - 带编号的话题"""
    topics_data = []
    current_topic = None
    current_questions = []

    i = start_line

    while i < end_line:
        line = lines[i].strip()

        if not line:
            i += 1
            continue

        # 检测话题编号行
        topic_match = is_topic_line_part3(line)
        if topic_match:
            if current_topic and current_questions:
                topics_data.append((current_topic, current_questions))
            current_topic = line
            current_questions = []
        elif current_topic:
            # 只有在有当前话题时才收集问句
            question = extract_question(line)
            if question:
                answer_lines = []
                j = i + 1

                while j < end_line:
                    next_line = lines[j].strip()

                    if extract_question(next_line):
                        break

                    cleaned = clean_answer_line(next_line)
                    if cleaned and len(cleaned) > 5:
                        answer_lines.append(cleaned)

                    j += 1

                answer = merge_sentences(answer_lines)
                if answer:
                    current_questions.append({'question': question, 'answer': answer})

                i += 1
                continue

        i += 1

    if current_topic and current_questions:
        topics_data.append((current_topic, current_questions))

    return topics_data

def generate_markdown():
    """生成排版好的Markdown"""
    data = parse_file()

    md = """---
created: 2026-05-13
updated: 2026-05-13
tags:
  - IELTS
  - 口语
  - 题库
  - 麦门讲义
type: 口语练习题库
---

# 口语完整题库

> 来源：麦门雅思2026年1~4月口语大讲义
>
> 使用方法：
> 1. 先看题目，自己尝试回答
> 2. 填写「初次口述」
> 3. 对照「参考答案」学习表达
> 4. 优化自己的答案，填写「最终答案」

---

"""

    total_questions = 0

    for section in data:
        part = section.get('part', '')
        topics = section.get('topics', [])

        md += f"\n## {part}\n\n"

        topic_num = 0
        for topic_name, questions in topics:
            topic_num += 1
            md += f"### 话题 {topic_num}: {topic_name}\n\n"

            for q in questions:
                total_questions += 1
                question = q.get('question', '')
                answer = q.get('answer', '')

                md += f"""#### 题目 {total_questions}

**{question}**

---

##### 初次口述

（在此处填写你的回答）

---

##### 参考答案

{answer}

---

"""

    return md, total_questions

if __name__ == "__main__":
    md, total = generate_markdown()
    output = "/Users/baojian/Desktop/IELTS/04_口语/题库/口语完整题库.md"
    with open(output, 'w', encoding='utf-8') as f:
        f.write(md)

    print(f"\n✓ 已生成: {output}")
    print(f"✓ 共 {total} 道题目")