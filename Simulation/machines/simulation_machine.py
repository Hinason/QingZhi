from Simulation import MAX_TIME

class simulation_machine:
    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type
        # busy = True 表示机器本身被占据
        # 也就是机器正在运行中
        self.busy = False
        self.endBusyTime = 0
        # positions是记录 position 状态的字典
        # 存储形式为 {position_id : endBusyTime}
        # endBusyTime = -1 时表示未被占用, 其余表示占用状态结束时间
        self.positions = {}

    def __str__(self):
        return self.name

    def update(self, time):
        # 机器恢复未占用状态
        if time >= self.endBusyTime:
            self.busy = False
        # position恢复未占用状态
        if self.busy:
            raise RuntimeError(f"Machine {self} is busy at Time {time}, can't release position")
        for key, value in self.positions.items():
            if time >= value:
                self.positions[key] = -1


    def occupy(self, cur_time, last_time, occupied_position_id, occupied_position_type):
        """
        处理机器占用逻辑
        :param cur_time: 当前时间
        :param last_time: 机器会被占用的时间
        :param occupied_position_id: 机器上被占用的 position 的 id
        :param occupied_position_type: 机器上被占用的 position 的 source_type
        """
        if "work" == occupied_position_type:
            if self.busy:
                raise RuntimeError(f"Machine {self} is busy at Time {cur_time}")
            else:
                # 在行为合法时继续处理后续的占用逻辑
                self.busy = True
                self.endBusyTime = MAX_TIME
        elif "plate" == occupied_position_type:
            if self.busy:
                raise RuntimeError(f"Machine {self} is busy at Time {cur_time}")
            elif self.positions[occupied_position_id] != -1:
                raise RuntimeError(f"Machine {self} 's Position {occupied_position_id} is busy at Time {cur_time}")
            else:
                self.positions[occupied_position_id] = MAX_TIME

    def set_release(self, cur_time, last_time, occupied_position_id, occupied_position_type):
        """
        设置 release 时间, 对于有些 task, 在其结束时会释放 position, 因此想要确定何时释放, 只需要关注这些 task 即可
        :param cur_time: 当前时间
        :param last_time: 机器会被占用的时间
        :param occupied_position_id: 机器上被占用的 position 的 id
        :param occupied_position_type: 机器上被占用的 position 的 source_type
        """
        if "work" == occupied_position_type:
            if self.busy:
                self.endBusyTime = cur_time + last_time
            else:
                raise RuntimeError(f"Machine {self} is available at Time {cur_time}, can't release")
        elif "plate" == occupied_position_type:
            if self.positions[occupied_position_id] != -1:
                self.positions[occupied_position_id] = cur_time + last_time
            else:
                raise RuntimeError(f"Machine {self} 's Position {occupied_position_id} is available at Time {cur_time}, can't release")

