from Simulation.machine_loader import MachineLoader
from Simulation import MAX_TIME

class simulator:

    def __init__(self, machine_system, position_system, tasks, max_time = MAX_TIME):
        self.curTime = 0
        self.maxTime = max_time
        self.tasks = sorted(tasks, key=lambda task: task.beginTime)
        self.machine_system = machine_system
        self.position_system = position_system
        # 初始化 machine 和 position
        self.machine_loader = MachineLoader(machine_system)
        self.machines = self.machine_loader.load_machines()
        self.machine_loader.load_position(position_system)



    def run_simulation(self):
        while self.curTime < self.maxTime :
            # 当前时刻能够运行的任务
            ready_tasks = []
            for task in self.tasks:
                if task.beginTime == self.curTime:
                    ready_tasks.append(task)

            # 释放 machine 和 position
            for machine in self.machines.values():
                machine.update(self.curTime)


            # 处理已经就绪的 task
            # 判断机器 machine 和 position 是否可用
            for task in ready_tasks:
                for position_id in task.realOccupy:
                    position = self.position_system.get_position(position_id)
                    position_machine_id = position.machine
                    machine = self.machines[position_machine_id]
                    machine.occupy(self.curTime, task.duration, position.id, position.sourcetype)
                print(f"{task.id} start at {self.curTime}")

            # 设置机器结束占用的时间
            # 部分 position 的占用和释放不在同一个 task 内
            for task in ready_tasks:
                for position_id in task.realRelease:
                    position = self.position_system.get_position(position_id)
                    position_machine_id = position.machine
                    machine = self.machines[position_machine_id]
                    machine.set_release(self.curTime, task.duration, position.id, position.sourcetype)

            self.curTime += 1