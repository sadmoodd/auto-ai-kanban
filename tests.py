from models import *
import requests


def create_simple_test_data():
    """3 задачи, 3 разработчика - проверка приоритетов и эффективности"""
    
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
            id=3,
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


from tests import create_simple_test_data # Импортируем твою функцию с данными

def test_api_optimization():
    url = "http://127.0.0.1:5050/api/optimize"
    
    # 1. Получаем данные из твоих тестов
    devs, tasks = create_simple_test_data()
    
    # 2. Подготавливаем данные в формате JSON (Pydantic ожидает именно такие ключи)
    # Важно: превращаем Set в List, так как JSON не поддерживает множества
    payload = {
        "devs_in": [
            {
                "id": d.id,
                "name": d.name,
                "efficiency": d.efficiency,
                "total_capacity": d.total_capacity,
                "level": int(d.level),
                "skills": list(d.skills)
            } for d in devs
        ],
        "tasks_in": [
            {
                "id": t.id,
                "title": t.title,
                "priority": int(t.priority),
                "effort": t.effort,
                "complexity": int(t.complexity),
                "required_skills": list(t.required_skills),
                "dependencies": t.dependencies
            } for t in tasks
        ]
    }

    print(f"Отправка запроса на {url}...")
    
    try:
        # 3. Посылаем POST запрос
        response = requests.post(url, json=payload)
        
        # 4. Анализируем ответ
        if response.status_code == 200:
            print("Успех! Результат оптимизации:")
            assignments = response.json()
            print("RAW JSON", assignments)
            for a in assignments:
                print(f"  - Задача: {a['task_title']} -> Разработчик: {a['developer']} (Время: {a['real_effort']}ч)")
        else:
            print(f"Ошибка {response.status_code}: {response.text}")
        
    except requests.exceptions.ConnectionError:
        print("Ошибка: Не удалось подключиться к серверу. Убедись, что main.py запущен!")

if __name__ == "__main__":
    test_api_optimization()