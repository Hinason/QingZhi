from machine_loader import MachineLoader


class simulator:
    def __init__(self, file_path, tasks, max_time = 1000):
        self.curTime = 0
        self.maxTime = max_time
        self.tasks = tasks.sort(key=lambda task: task.beginTime)
        self.machine_loader = MachineLoader(file_path)
        self.machines = self.machine_loader.load_machines()

    def run_simulation(self):
        while self.curTime < self.maxTime :
            ready_tasks = []
            for task in self.tasks:
                if task.beginTime == self.curTime:
                    ready_tasks.append(task)


            self.curTime += 1
        pass