class Task:
    def __init__(self, task_id: int, duration: int, dependencies=None):
        self.task_id = task_id
        self.duration = duration
        self.dependencies = dependencies if dependencies else []

class Scheduler:
    def __init__(self):
        self.tasks = {}

    def add_task(self, task: Task):
        self.tasks[task.task_id] = task

    def find_completion_time(self, task_id: int) -> int:
        memo = {}  # Cache to store computed times
        visited = set()  # Set to track the current path for cycle detection
        total_time = self._dfs(task_id, memo, visited)
        if total_time == float('inf'):
            print(Exception("Cycle detected in task dependencies"))
            return 101
        return total_time

    def _dfs(self, task_id: int, memo: dict, visited: set) -> int:
        if task_id in visited:
            return float('inf')  # Cycle detected

        if task_id in memo:
            return memo[task_id]

        visited.add(task_id)

        task = self.tasks.get(task_id)
        if not task:
            visited.remove(task_id)
            return 0

        total_time = task.duration
        for dep_id in task.dependencies:
            dep_time = self._dfs(dep_id, memo, visited)
            if dep_time == float('inf'):
                return float('inf')  # Propagate cycle detection
            total_time += dep_time

        visited.remove(task_id)
        memo[task_id] = total_time
        return total_time

# Example usage
scheduler = Scheduler()
scheduler.add_task(Task(1, 3, [2, 3]))
scheduler.add_task(Task(2, 2))
scheduler.add_task(Task(3, 4))

print(scheduler.find_completion_time(1))  # Output: 9 (3 + 2 + 4)

# Adding a cycle to test cycle detection
scheduler.add_task(Task(4, 1, [1]))
scheduler.add_task(Task(5, 1, [4]))
scheduler.add_task(Task(6, 1, [5, 6]))  # Cycle 6 -> 5 -> 4 -> 1 -> 6

try:
    print(scheduler.find_completion_time(6))
except Exception as e:
    print(e)  # Output: Cycle detected in task dependencies
