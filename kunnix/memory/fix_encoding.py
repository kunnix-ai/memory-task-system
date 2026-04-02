#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""修复 performance_test.py 的编码问题"""

import re

# 读取文件
with open('performance_test.py', 'r', encoding='utf-8') as f:
    content = f.read()

# 替换所有非 ASCII 字符
replacements = {
    '→': '->',
    '≤': '<=',
    '≥': '>=',
    '×': 'x',
    '÷': '/',
    'λ': 'lambda',
    'Σ': 'sum',
    'α': 'alpha',
    'β': 'beta',
    'γ': 'gamma',
    'δ': 'delta',
    'ε': 'epsilon',
}

for old, new in replacements.items():
    content = content.replace(old, new)

# 移除所有剩余的 emoji（如果还有）
emoji_pattern = re.compile("["
    u"\U0001F600-\U0001F64F"  # emoticons
    u"\U0001F300-\U0001F5FF"  # symbols & pictographs
    u"\U0001F680-\U0001F6FF"  # transport & map symbols
    u"\U0001F1E0-\U0001F1FF"  # flags
    "]+", flags=re.UNICODE)

content = emoji_pattern.sub('', content)

# 写回文件
with open('performance_test.py', 'w', encoding='utf-8') as f:
    f.write(content)

print("修复完成！")
