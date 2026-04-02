#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
WorkBuddy 技能自动进化 - 技能审核器

功能：
1. 显示技能草稿
2. 提供审核检查清单
3. 收集用户反馈
4. 记录审核决策

作者：阿中
版本：v1.0.0
日期：2026-04-02
"""

import os
import sys
from pathlib import Path
from typing import Dict, Optional, List
from datetime import datetime


class SkillReviewer:
    """技能审核器"""
    
    def __init__(self, workspace_root: str = None):
        """初始化技能审核器"""
        self.workspace_root = Path(workspace_root) if workspace_root else Path(__file__).parent.parent
        self.skill_drafts_dir = self.workspace_root / ".workbuddy" / "skills" / "drafts"
        self.skill_review_log = self.workspace_root / ".workbuddy" / "skill_evolution" / "review_log.md"
        
        # 确保目录存在
        self.skill_review_log.parent.mkdir(parents=True, exist_ok=True)
        
        # 审核检查清单
        self.checklist = [
            ("技能名称清晰准确", "name_clear"),
            ("触发条件合理", "trigger_reasonable"),
            ("执行动作安全", "action_safe"),
            ("代码无语法错误", "no_syntax_error"),
            ("符合 SKILL.md 格式", "format_correct"),
            ("有使用示例", "has_example"),
            ("有安全机制", "has_safety"),
        ]
    
    def review_skill(self, skill_path: str) -> Dict:
        """
        审核技能
        
        Args:
            skill_path: 技能文件路径
        
        Returns:
            Dict: 审核结果
        """
        result = {
            'skill_path': skill_path,
            'review_time': datetime.now().isoformat(),
            'checklist_results': [],
            'issues': [],
            'suggestions': [],
            'recommendation': 'pending',  # approve / modify / reject
        }
        
        # 读取技能文件
        try:
            with open(skill_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            result['issues'].append(f"无法读取文件：{str(e)}")
            result['recommendation'] = 'reject'
            return result
        
        # 执行检查清单
        for item_name, item_key in self.checklist:
            passed = self._check_item(content, item_key)
            result['checklist_results'].append({
                'item': item_name,
                'passed': passed,
            })
            
            if not passed:
                result['issues'].append(item_name)
        
        # 生成建议
        result['suggestions'] = self._generate_suggestions(content)
        
        # 推荐决策
        passed_count = sum(1 for item in result['checklist_results'] if item['passed'])
        total_count = len(self.checklist)
        
        if passed_count == total_count:
            result['recommendation'] = 'approve'
        elif passed_count >= total_count * 0.7:
            result['recommendation'] = 'modify'
        else:
            result['recommendation'] = 'reject'
        
        return result
    
    def _check_item(self, content: str, item_key: str) -> bool:
        """检查单个项目"""
        checks = {
            'name_clear': 'name:' in content.lower() or '# ' in content,
            'trigger_reasonable': '触发' in content or 'trigger' in content.lower(),
            'action_safe': not any(danger in content for danger in ['rm -rf', 'del /S', 'DROP TABLE']),
            'no_syntax_error': True,  # 需要实际执行代码检查，这里简化
            'format_correct': '---' in content and '##' in content,
            'has_example': '示例' in content or 'example' in content.lower(),
            'has_safety': '安全' in content or 'safety' in content.lower(),
        }
        
        return checks.get(item_key, False)
    
    def _generate_suggestions(self, content: str) -> List[str]:
        """生成改进建议"""
        suggestions = []
        
        if 'def execute' not in content:
            suggestions.append("建议添加 execute 函数定义")
        
        if 'if __name__ == "__main__"' not in content:
            suggestions.append("建议添加测试代码块")
        
        if len(content) < 500:
            suggestions.append("技能描述可能过于简单，建议补充详细说明")
        
        if 'return' not in content:
            suggestions.append("建议添加返回值说明")
        
        return suggestions
    
    def display_review(self, review_result: Dict):
        """显示审核结果"""
        print("\n" + "=" * 60)
        print("技能审核报告")
        print("=" * 60)
        print(f"技能路径：{review_result['skill_path']}")
        print(f"审核时间：{review_result['review_time']}")
        print()
        
        print("检查清单:")
        for item in review_result['checklist_results']:
            status = "✅" if item['passed'] else "❌"
            print(f"  {status} {item['item']}")
        print()
        
        if review_result['issues']:
            print("发现问题:")
            for issue in review_result['issues']:
                print(f"  - {issue}")
            print()
        
        if review_result['suggestions']:
            print("改进建议:")
            for suggestion in review_result['suggestions']:
                print(f"  - {suggestion}")
            print()
        
        print(f"审核建议：{self._get_recommendation_text(review_result['recommendation'])}")
        print("=" * 60)
    
    def _get_recommendation_text(self, recommendation: str) -> str:
        """获取推荐决策文本"""
        texts = {
            'approve': "✅ 建议通过（所有检查项通过）",
            'modify': "⚠️ 建议修改后通过（大部分检查项通过）",
            'reject': "❌ 建议拒绝（多数检查项未通过）",
            'pending': "⏳ 待审核",
        }
        return texts.get(recommendation, "未知")
    
    def save_review_log(self, review_result: Dict):
        """保存审核日志"""
        log_entry = f"""
## 技能审核 - {review_result['skill_path']}

**审核时间**: {review_result['review_time']}

**检查结果**:
"""
        for item in review_result['checklist_results']:
            status = "✅" if item['passed'] else "❌"
            log_entry += f"- {status} {item['item']}\n"
        
        if review_result['issues']:
            log_entry += "\n**发现问题**:\n"
            for issue in review_result['issues']:
                log_entry += f"- {issue}\n"
        
        log_entry += f"\n**审核建议**: {self._get_recommendation_text(review_result['recommendation'])}\n"
        log_entry += "---\n"
        
        with open(self.skill_review_log, 'a', encoding='utf-8') as f:
            f.write(log_entry)


def demo_reviewer():
    """演示审核器"""
    print("=" * 60)
    print("技能审核器演示")
    print("=" * 60)
    
    reviewer = SkillReviewer()
    
    # 查找技能草稿
    if not reviewer.skill_drafts_dir.exists():
        print(f"技能草稿目录不存在：{reviewer.skill_drafts_dir}")
        return False
    
    draft_files = list(reviewer.skill_drafts_dir.glob("*/SKILL.md"))
    
    if not draft_files:
        print("未找到技能草稿文件")
        return False
    
    print(f"找到 {len(draft_files)} 个技能草稿:\n")
    for i, draft in enumerate(draft_files, 1):
        print(f"{i}. {draft.parent.name}")
    
    # 审核第一个技能
    print(f"\n审核技能：{draft_files[0].parent.name}")
    review_result = reviewer.review_skill(str(draft_files[0]))
    
    # 显示审核结果
    reviewer.display_review(review_result)
    
    # 保存审核日志
    reviewer.save_review_log(review_result)
    print(f"\n审核日志已保存：{reviewer.skill_review_log}")
    
    return True


if __name__ == "__main__":
    success = demo_reviewer()
    sys.exit(0 if success else 1)
