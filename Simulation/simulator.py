from Simulation.machine_loader import MachineLoader
from Simulation import MAX_TIME
from Simulation.Other.plate_manager import PlateManager
from Simulation.Machines import *


class simulator:

    def __init__(self, machine_system, position_system, tasks, max_time = MAX_TIME):
        self.curTime = 0
        self.maxTime = max_time
        self.tasks = sorted(tasks, key=lambda task: task.beginTime)
        self.curTaskIndex = 0
        self.machine_system = machine_system
        self.position_system = position_system
        # 初始化 machine 和 position
        self.machine_loader = MachineLoader(machine_system)
        self.machines = self.machine_loader.load_machines()
        self.machine_loader.load_position(position_system)
        self.plate_manager = PlateManager()
        # 记录每个位置上的板子
        self.position_plates = {}  # {position_id: plate_id}



    def run_simulation(self):
        while self.curTime < self.maxTime :
            # 当前时刻能够运行的任务
            ready_tasks = []
            for task in self.tasks[self.curTaskIndex:]:
                if task.beginTime <= self.curTime:
                    ready_tasks.append(task)
            self.curTaskIndex += len(ready_tasks)

            # 释放 machine 和 position
            for machine in self.machines.values():
                machine.update(self.curTime)

            # 处理已经就绪的 task
            # 判断机器 machine 和 position 是否可用
            for task in ready_tasks:
                # 判断任务类型，处理板子的创建、移动和销毁
                self._handle_plate_operations(task)
                for position_id in task.realOccupy:
                    position = self.position_system.get_position(position_id)
                    machine = self.machines[position.machine]
                    # 处理板子和一些机器的特殊操作
                    plate = None
                    operation = None
                    if position_id in self.position_plates and self.position_plates[position_id] is not None:
                        plate_id = self.position_plates[position_id]
                        plate = self.plate_manager.plates.get(plate_id)
                    # 只有开关盖机器才会有 operation 属性
                    if type(machine) is capping_and_decapping_device:
                        if "Open" == task.taskName:
                            operation = "open"
                        elif "Close" == task.taskName:
                            operation = "close"
                    machine.occupy(self.curTime, task.duration, position.id, position.sourcetype, plate, operation)
                print(f"{task.id} start at {self.curTime}")

            # 设置机器结束占用的时间
            # 部分 position 的占用和释放不在同一个 task 内
            for task in ready_tasks:
                for position_id in task.realRelease:
                    position = self.position_system.get_position(position_id)
                    machine = self.machines[position.machine]
                    machine.set_release(self.curTime, task.duration, position.id, position.sourcetype)

            self.curTime += 1

    def _handle_plate_operations(self, task):
        """处理板子的创建、移动和销毁操作"""
        # 检查是否是创建板子的任务 (Get From Hotel)
        if task.taskname == "Get From Hotel":
            # 创建新板子
            new_plate = self.plate_manager.create_new_plate()
            # 找到需要放置板子的位置
            # 判断逻辑是 source type 为 plate 的 position
            # 暂时认为在一个 task 的 realOccupy 中应该只有一个 plate 形式
            for position_id in task.realOccupy:
                position = self.position_system.get_position(position_id)
                if "plate" == position.sourcetype:
                    self.position_plates[position_id] = new_plate.id
        # 检查是否是销毁板子的任务 (Put In Hotel)
        elif task.taskname == "Put In Hotel":
            # 找到需要销毁的板子位置
            for position_id in task.realOccupy:
                position = self.position_system.get_position(position_id)
                if "plate" == position.sourcetype:
                    plate_id = self.position_plates[position_id]
                    self.position_plates[position_id] = None
                    self.plate_manager.delete_plate_by_id(plate_id)
        # 处理板子的移动
        else:
            # 检查是否有板子需要从release位置移动到occupy位置
            # 暂时认为移动均为一对一的行为
            for release_position_id in task.realRelease:
                if release_position_id in self.position_plates and self.position_plates[release_position_id] is not None:
                    plate_id = self.position_plates[release_position_id]
                    for occupy_position_id in task.realOccupy:
                        # 确保不是同一个位置
                        occupy_position = self.position_system.get_position(occupy_position_id)
                        if "plate" == occupy_position.sourcetype:
                            self.position_plates[release_position_id] = None
                            self.position_plates[occupy_position_id] = plate_id
                            break