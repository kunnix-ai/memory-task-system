#!/usr/bin/env python3
# 快速检查技能系统
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

from skill_evolution.skill_reviewer import SkillReviewer
from skill_evolution.skill_publisher import SkillPublisher

print("=" * 60)
print("鲲凰技能系统检查")
print("=" * 60)

reviewer = SkillReviewer()

# 查找技能草稿
draft_files = list(reviewer.skill_drafts_dir.glob("*/SKILL.md"))
print(f"\n找到 {len(draft_files)} 个技能草稿:\n")

for i, draft in enumerate(draft_files, 1):
    print(f"{i}. {draft.parent.name}")

if draft_files:
    # 审核第一个技能
    print(f"\n审核技能：{draft_files[0].parent.name}")
    review_result = reviewer.review_skill(str(draft_files[0]))
    reviewer.display_review(review_result)
    
    # 保存审核日志
    reviewer.save_review_log(review_result)
    print(f"\n审核日志已保存：{reviewer.skill_review_log}")

print("\n" + "=" * 60)
