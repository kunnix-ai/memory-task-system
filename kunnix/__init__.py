"""
Kunnix Memory & Task Scheduling System

让 AI 拥有永久记忆与任务调度能力
Give Your AI Assistant Memory & Task Scheduling

Version: 1.0.0
Author: Kunnix Team
"""

__version__ = "1.0.0"
__author__ = "Kunnix Team"
__description__ = "Advanced AI Memory & Task Scheduling System"

from .memory import MemorySystem
from .task import TaskOrchestrator
from .skill import SkillEvolution

__all__ = [
    "MemorySystem",
    "TaskOrchestrator", 
    "SkillEvolution",
]
