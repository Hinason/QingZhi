class Schedule:
    def __init__(self, task_system, machine_system, position_system):
        self.task_system = task_system
        self.machine_system = machine_system
        self.position_system = position_system
        self.current_time = 0


    def get_task_by_id(self, task_id):
        for task in self.task_system.tasks:
            if task.id == task_id:
                return task
        return None

    def get_machine_by_id(self, machine_id):
        for machine in self.machine_system.machines:
            if machine.id == machine_id:
                return machine
        return None

    def get_position_by_id(self, position_id):
        for position in self.position_system.positions:
            if position.id == position_id:
                return position
        return None

    def __str__(self):
        return f"Schedule(taskNumber: {self.task_system}, machines: {self.machine_system}, current_time: {self.current_time})"



class ScheduledTask:
    def __init__(self, start_time, task_id, prev_task_id, next_task_id, occupy_machine_id, occupy_position_id, release_machine_id, release_position_id):
        self.start_time = start_time
        self.task_id = task_id
        self.prev_task_id = prev_task_id
        self.next_task_id = next_task_id
        self.occupy_machine_id = occupy_machine_id
        self.occupy_position_id = occupy_position_id
        self.release_machine_id = release_machine_id
        self.release_position_id = release_position_id
        self.status = False

        '''
        start_time : 开始时间
        task_id : 任务ID
        prev_task_id : 该任务所有前置任务
        next_task_id : 该任务的后续任务
        occupy_machine_id : 执行该任务需要哪些机器
        occupy_position_id : 执行该任务需要哪些位置
        release_machine_id : 执行完毕后释放哪些机器
        release_position_id : 执行完毕后释放哪些位置
        status : 该任务是否已经完成
        '''


