# 技能自动化

> 从重复工作中自动生成技能

## 🤖 场景说明

识别重复工作流，自动生成自动化技能。

## 🚀 使用示例

```python
from kunnix import SkillEvolution

skill_system = SkillEvolution()

# 从历史任务中学习
patterns = skill_system.extract_patterns(
    task_archives=["./tasks/archives"],
    min_cluster_size=3,
    threshold=0.5
)

# 生成技能
skill = skill_system.generate_skill(patterns[0])

# 审核发布
review_result = skill_system.review_skill(skill["path"])
if review_result["status"] == "approved":
    skill_system.publish_skill(skill["path"])
    print(f"✅ 技能已发布：{skill['skill_name']}")
```

## 📖 相关示例

- [基础示例](/examples/basic)
- [项目管理](/examples/project-management)
