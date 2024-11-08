class Schedule:
    def __init__(self, task_system, machine_system):
        self.task_system = task_system
        self.machine_system = machine_system
        self.current_time = 0


    def __repr__(self):
        return f"Schedule(taskNumber: {self.task_system}, machines: {self.machine_system}, current_time: {self.current_time})"
