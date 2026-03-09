from typing import List
from models import Developer, Task
from ortools.linear_solver import pywraplp
from tests import create_simple_test_data
import logging

logging.basicConfig(level=logging.INFO, format='%(asctime)s | %(levelname)s | %(message)s')
logger = logging.getLogger(__name__)

class Solver():
    def __init__(self):
        self.assignments = [] # присвоения - кому какая задача
        self.solver = pywraplp.Solver.CreateSolver('SCIP')
        
        
    def optimize(self, developers: List[Developer], tasks: List[Task]): 
        logger.info("Начало оптимизации...")       
        if not self.solver:
            return
        
        x = {}
        for i, task in enumerate(tasks):
            for j, dev in enumerate(developers):
                # Создаем бинарную переменную для каждой возможной пары
                x[i, j] = self.solver.IntVar(0, 1, f'task_{task.id}_dev_{dev.id}')
      
        # Ограничение на задачи (каждую задачу берет не более 1 человека) 
        for i, task in enumerate(tasks):
            valid_vars_for_task = []
            for j, dev in enumerate(developers):
                if dev.can_take_task(task):
                    valid_vars_for_task.append(x[i, j])
                else:
                    self.solver.Add(x[i, j] == 0) # Скиллов нет — работать нельзя
                    
            if valid_vars_for_task:
                self.solver.Add(self.solver.Sum(valid_vars_for_task) <= 1)

        # Ограничение на разработчиков (не работать больше лимита) 
        for j, dev in enumerate(developers):
            # Собираем всё время, которое этот разработчик (j) может потратить на все задачи (i)
            # Время = Оценка / Эффективность
            developer_load = [
                x[i, j] * (tasks[i].effort / dev.efficiency) 
                for i in range(len(tasks))
            ]
            self.solver.Add(self.solver.Sum(developer_load) <= dev.remaining_capacity)
                    
        # Целевая функция 
        objective_terms = []
        for i, task in enumerate(tasks):
            for j, dev in enumerate(developers):
                diff = dev.level - task.complexity
        
                if diff == 0:
                    match_factor = 1.2  # Бонус за соответствие
                elif diff > 0:
                    match_factor = 0.6  # Оверквалификация (сеньор на мелкой задаче)
                else:
                    match_factor = 0.3  # Недостаток квалификации
                
                # Просто добавляем слагаемое в список
                weight = (dev.efficiency * task.priority) / task.effort * match_factor
                objective_terms.append(x[i, j] * weight)
                
        # Устанавливаем цель ОДИН раз для всей задачи
        self.solver.Maximize(self.solver.Sum(objective_terms))
        
        # Решение и извлечение данных 
        status = self.solver.Solve()
        
        results = []
        if status == pywraplp.Solver.OPTIMAL or status == pywraplp.Solver.FEASIBLE:
            for i, task in enumerate(tasks):
                for j, dev in enumerate(developers):
                    # Проверяем, выбрал ли солвер эту пару (значение будет 1.0)
                    if x[i, j].solution_value() > 0.5:
                        results.append({
                            "task_id": task.id,
                            "task_title": task.title,
                            "developer": dev.name,
                            "real_effort": round(task.effort / dev.efficiency, 2)
                        })
            logger.info("Решение найдено успешно")
            return results
        else:
            logger.error("Решение не найдено.")
            return []
                  
        
        
s = Solver()
print(s.optimize(*create_simple_test_data()))
