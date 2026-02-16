from dataclasses import dataclass, field
from datetime import datetime, timedelta
from typing import List, Optional, Set, Dict
from enum import IntEnum, Enum

class TaskStatus(Enum):
    BACKLOG = "backlog"
    TODO = "todo"
    IN_PROGRESS = "in_progress"
    REVIEW = "review"
    DONE = "done"

# Используем IntEnum, чтобы можно было сравнивать: Priority.HIGH > Priority.LOW
class Priority(IntEnum):
    LOWEST = 1
    LOW = 2
    MEDIUM = 3
    HIGH = 4
    CRITICAL = 5
    
class Seniority(IntEnum):
    JUNIOR = 1
    MIDDLE = 2
    SENIOR = 3

@dataclass
class Task:
    id: int
    title: str
    priority: Priority
    effort: float  # Оценка времени (в часах) для "среднего" разработчика
    status: TaskStatus
    created_at: datetime
    complexity: Seniority
    
    # Используем Set для быстрого поиска O(1)
    required_skills: Set[str] = field(default_factory=set)
    dependencies: List[int] = field(default_factory=list)
    
    assigned_to: Optional[int] = None
    deadline: Optional[datetime] = None

    def is_overdue(self) -> bool:
        if self.deadline and datetime.now() > self.deadline:
            return True
        return False

    def check_blocked(self, all_tasks_map: Dict[int, 'Task']) -> bool:
        """
        Проверяет, выполнены ли родительские задачи.
        Требует словарь всех задач для проверки статусов.
        """
        if not self.dependencies:
            return False
            
        for parent_id in self.dependencies:
            parent = all_tasks_map.get(parent_id)
            # Если родитель не найден или не готов — задача заблокирована
            if not parent or parent.status != TaskStatus.DONE:
                return True
        return False

@dataclass
class Developer:
    id: int
    name: str
    efficiency: float  # 0.5 - 1.5
    total_capacity: float # Общая емкость на спринт (например, 40 часов)
    level: Seniority
    
    current_tasks: List[Task] = field(default_factory=list) # Храним объекты задач, а не ID
    skills: Set[str] = field(default_factory=set)
    
    @property
    def used_capacity(self) -> float:
        """Считает занятое время с учетом эффективности разработчика"""
        # Время = Оценка / Эффективность
        # Если разработчик эффективный (1.5), он тратит меньше времени
        return sum(t.effort / self.efficiency for t in self.current_tasks)

    @property
    def remaining_capacity(self) -> float:
        """Сколько времени осталось реально"""
        rem = self.total_capacity - self.used_capacity
        return max(0.0, rem)

    def can_take_task(self, task: Task) -> bool:
        """Проверка по скиллам и времени"""
        # 1. Проверка скиллов (навыки задачи должны быть подмножеством навыков разраба)
        if not task.required_skills.issubset(self.skills):
            return False
        #if task.complexity > self.level:
        #    return False
            
        # 2. Проверка времени
        real_effort = task.effort / self.efficiency
        return real_effort <= self.remaining_capacity

@dataclass
class AssignmentResult:
    """Результат работы алгоритма для передачи обратно в Laravel"""
    task_id: int
    developer_id: int
    predicted_duration: float
    score: float # Насколько это назначение "хорошее" математически