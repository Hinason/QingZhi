from Simulation import MAX_TIME
from Simulation.Other.plate_manager import PlateManager


class simulation_machine:
    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type

        # busy = True 表示机器本身被占据, 也就是机器正在运行中
        # end_busy_time 表示机器结束运行的时间, 也就是释放占用时间
        self.busy = False
        self.end_busy_time = 0

        # positions是记录 position 状态的字典
        # 存储形式为 {position_id : [end_busy_time, plate]}
        # end_busy_time = -1 时表示未被占用, 其余表示占用状态结束时间
        # plate 表示占用该位置的板子，None表示没有板子
        self.positions = {}


    def __str__(self):
        return self.name

    def add_position(self, position):
        if "plate" == position.sourcetype:  # "plate" 说明是机器上的position
            self.positions[position.id] = [-1, None]    # [endBusyTime, plate_id]
        elif "work" == position.sourcetype:  # "work" 说明是机器本身
            self.busy = False

    def update(self, cur_time):
        """
        判断当前时间是否需要释放 machine 或 position
        :param cur_time: 当前时间
        :return: NULL
        """
        # 机器恢复未占用状态
        if cur_time >= self.end_busy_time:
            self.busy = False
        # position恢复未占用状态
        for key, value in self.positions.items():
            if cur_time >= value[0] != -1:
                if self.busy:
                    raise RuntimeError(f"Machine {self} is busy at Time {cur_time}, can't release position {key}")
                # 更新 position 的所有信息
                self.positions[key] = [-1, None]


    def occupy(self, cur_time, last_time, occupied_position_id, occupied_position_type, plate = None, operation = None):
        """
        处理机器占用逻辑
        :param cur_time: 当前时间
        :param last_time: 机器会被占用的时间
        :param occupied_position_id: 机器上被占用的 position 的 id
        :param occupied_position_type: 机器上被占用的 position 的 source_type
        :param plate: 存放在机器 position 上的实例
        :param operation: 机器本身 work 时的操作类型, 不同机器可能不同
        """
        if "work" == occupied_position_type:
            if self.busy:
                raise RuntimeError(f"Machine {self} is busy at Time {cur_time}")
            else:
                # 在行为合法时继续处理后续的占用逻辑
                self.busy = True
                self.end_busy_time = MAX_TIME
        elif "plate" == occupied_position_type:
            if self.busy:
                raise RuntimeError(f"Machine {self} is busy at Time {cur_time}")
            elif self.positions[occupied_position_id][0] != -1:
                raise RuntimeError(f"Machine {self} 's Position {occupied_position_id} is busy at Time {cur_time}")
            else:
                self.positions[occupied_position_id][0] = MAX_TIME
                if plate is not None:
                    self.positions[occupied_position_id][1] = plate



    def set_release(self, cur_time, last_time, occupied_position_id, occupied_position_type):
        """
        设置 release 时间, 对于有些 task, 在其结束时会释放 position, 因此我们可以根据这些 task 的结束时间设置对应 position 的释放时间
        :param cur_time: 当前时间
        :param last_time: 机器会被占用的时间
        :param occupied_position_id: 机器上被占用的 position 的 id
        :param occupied_position_type: 机器上被占用的 position 的 source_type
        """
        if "work" == occupied_position_type:
            if self.busy:
                self.end_busy_time = cur_time + last_time
            else:
                raise RuntimeError(f"Machine {self} is available at Time {cur_time}, can't release")
        elif "plate" == occupied_position_type:
            if self.positions[occupied_position_id][0] != -1:
                self.positions[occupied_position_id][0] = cur_time + last_time
            else:
                raise RuntimeError(f"Machine {self} 's Position {occupied_position_id} is available at Time {cur_time}, can't release")
        else:
            raise ValueError(f"Unknown position type: {occupied_position_type}")
