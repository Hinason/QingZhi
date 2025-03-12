from Simulation.Machines.simulation_machine import simulation_machine
from Simulation import MAX_TIME


class capping_and_decapping_device(simulation_machine):
    """
    封盖、去盖
    """

    def __init__(self, id, name, type):
        super().__init__(id, name, type)
        # 存储每个位置上的盖子信息 {position_id: lid_id}
        self.lid_positions = {}

    def add_position(self, position):
        """添加位置，并初始化盖子信息"""
        super().add_position(position)
        if "plate" == position.sourcetype:
            # lid_positions 用于记录 position 上的 lid_id
            # 用于后续关盖的板盖匹配工作
            self.lid_positions[position.id] = None  # 初始化时机器上没有盖子


    def occupy(self, cur_time, last_time, occupied_position_id, occupied_position_type, plate=None, operation=None):
        """
        开关盖机器占用机器位置

        Args:
            cur_time: 当前时间
            last_time: 持续时间
            occupied_position_id: 被占用的位置ID
            occupied_position_type: 被占用的位置类型
            plate: 板子对象实例
            operation: 操作类型, "open" 或 "close"
        """
        # 如果是 "work" 类型, 处理开关盖操作
        if "work" == occupied_position_type:
            if self.busy:
                raise RuntimeError(f"Machine {self.id} is busy at Time {cur_time}")
            else:
                self.busy = True
                self.end_busy_time = MAX_TIME

                # 回顾 simulation_machine 中记录 position 状态的属性
                # self.positions是记录 position 状态的字典
                # 存储形式为 {position_id : [end_busy_time, plate]}
                # end_busy_time = -1 时表示未被占用, 其余表示占用状态结束时间
                # plate 表示占用该位置的板子实例，None表示没有板子

                # 如果提供了操作类型, 直接执行开关盖操作
                if operation == "open":
                    # 循环遍历 positions 字典里的所有 position, 只要有板子就打开其盖子
                    for position_id, value in self.positions.items():
                        if value[0] != -1:
                            plate = value[1]
                            if  not plate.has_lid:
                                raise RuntimeError(f"Plate {plate.id} does not have a lid to open at {self.id}")
                            # 调用 plate 中的开盖方法
                            lid_id = plate.open_lid(position_id)
                            self.lid_positions[position_id] = lid_id

                elif operation == "close":
                    # 循环遍历 positions 字典里的所有 position, 关盖时需要保证板子和盖子是对应的
                    for position_id, value in self.positions.items():
                        if value[0] != -1:
                            plate = value[1]
                            lid_id = self.lid_positions.get(position_id)
                            if lid_id is None:  # 当前 position上 是否有盖子
                                raise RuntimeError(f"No lid found at position {position_id} for plate {plate.id}")
                            if lid_id != plate.lid_id: # 盖子和板子不匹配
                                raise RuntimeError(f"Lid {lid_id} at position {position_id} does not match plate {plate.id}")
                            # 尝试关盖
                            plate.close_lid(lid_id)
                            self.lid_positions[position_id] = None
        # 如果是 其他("plate") 类型，使用基类的处理方式
        else:
            super().occupy(cur_time, last_time, occupied_position_id, occupied_position_type, plate)
