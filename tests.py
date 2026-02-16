from models import *

def create_simple_test_data():
    """3 задачи, 2 разработчика - проверка приоритетов и эффективности"""
    
    # Разработчики
    devs = [
        Developer(
            id=1,
            name="Анна (эффективный)",
            efficiency=1.2,
            total_capacity=20,
            level = 2,
            current_tasks=[],  # пустой список задач
            skills={"python", "sql", "fastapi"}
        ),
        Developer(
            id=2,
            name="Борис (новичок)",
            level = 1,
            efficiency=0.7,
            total_capacity=20,
            current_tasks=[],
            skills={"python", "sql"}
        ),
        Developer(
            id=2,
            name="Андрей (сеньор)",
            level = 3,
            efficiency=1.35,
            total_capacity=40,
            current_tasks=[],
            skills={"python", "sql", "fastapi"}
        )
    ]
    
    # Задачи
    tasks = [
        Task(
            id=1,
            title="Рефакторинг модуля аутентификации",
            priority=Priority.CRITICAL,
            complexity=2,
            effort=8,
            status=TaskStatus.BACKLOG,
            created_at=datetime.now() - timedelta(days=2),
            required_skills={"python", "sql"}
        ),
        Task(
            id=2,
            title="Написать тесты для API",
            priority=Priority.HIGH,
            complexity=3,
            effort=25,
            status=TaskStatus.BACKLOG,
            created_at=datetime.now() - timedelta(days=1),
            required_skills={"python", "fastapi"}
        ),
        Task(
            id=3,
            title="Обновить документацию",
            priority=Priority.LOW,
            effort=4,
            complexity=1,
            status=TaskStatus.BACKLOG,
            created_at=datetime.now() - timedelta(days=3),
            required_skills={"sql"}  # не требует python
        )
    ]
    
    return devs, tasks

# Ожидаемый результат: 
# Задача 1 (CRITICAL) → Анна (1.5 * 5/8 = 0.94)
# Задача 2 (HIGH) → Анна (1.5 * 4/12 = 0.5) или Борис (0.7 * 4/12 = 0.23) → Анна лучше
# Задача 3 (LOW) → Борис (0.7 * 1/4 = 0.175) - единственный вариант