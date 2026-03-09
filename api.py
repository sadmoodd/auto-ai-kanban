from fastapi import FastAPI
from pydantic import BaseModel
from typing import List, Set
from solver import Solver
from models import Developer, Task, TaskStatus, Priority, Seniority
import uvicorn
from datetime import datetime
import logging


logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

app = FastAPI()

class TaskRequest(BaseModel):
    id: int
    title: str
    priority: int  # 1-5
    effort: float
    complexity: int # 1-3
    required_skills: Set[str]
    dependencies: List[int] = []

class DevRequest(BaseModel):
    id: int
    name: str
    efficiency: float
    total_capacity: float
    level: int
    skills: Set[str]

@app.get("/api/health")
def health():
    return '{"health": "ok"}'



@app.post("/api/optimize")
def optimize_kanban(devs_in: List[DevRequest], tasks_in: List[TaskRequest]):
    logger.info(f"Получен запрос на оптимизацию: {len(tasks_in)} задач, {len(devs_in)} разработчиков")
    
    try:
        # 1. Конвертируем входящие данные в объекты твоих dataclasses
        developers = [
            Developer(
                id=d.id,
                name=d.name,
                efficiency=d.efficiency,
                total_capacity=d.total_capacity,
                level=Seniority(d.level),
                skills=d.skills
            ) for d in devs_in
        ]
        
        tasks = [
            Task(
                id=t.id,
                title=t.title,
                priority=Priority(t.priority),
                effort=t.effort,
                complexity=Seniority(t.complexity),
                status=TaskStatus.BACKLOG,
                created_at=datetime.now(),
                required_skills=t.required_skills,
                dependencies=t.dependencies
            ) for t in tasks_in
        ]
        
        # 2. Инициализируем твой Solver и запускаем расчет
        solver = Solver()
        result = solver.optimize(developers, tasks)
        
        logger.info(f"Оптимизация завершена. Назначено задач: {len(result)}")
        return result

    except Exception as e:
        logger.error(f"Ошибка при оптимизации: {str(e)}")
        return {"error": str(e)}, 500


if __name__ == '__main__':
    uvicorn.run(app, host='127.0.0.1', port=5050)