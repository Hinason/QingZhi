from Simulation.Machines.simulation_machine import simulation_machine
from Simulation import MAX_TIME


class centrifuge(simulation_machine):
    """
    离心机，继承自simulation_machine，需满足对称性才能启动工作状态
    """

    def __init__(self, id, name, type):
        super().__init__(id, name, type)
        self.positions_list = []  # 记录所有类型为 plate 的 position 的 id

    def add_position(self, position):
        """
        添加 position 并维护 positions_list 的顺序从而实现对称性检查
        """
        super().add_position(position)
        if position.sourcetype == "plate":
            if position.id not in self.positions_list:
                self.positions_list.append(position.id)


    def occupy(self, cur_time, last_time, occupied_position_id, occupied_position_type, plate = None, operation = None):
        """
        处理离心机的占用逻辑，启动工作前需验证对称性。
        """
        if occupied_position_type == "work":
            if self.busy:
                raise RuntimeError(f"Centrifuge {self} is busy at Time {cur_time}.")

            occupied_positions = [
                pos_id for pos_id, value in self.positions.items()
                if value[0] != -1
            ]
            if not occupied_positions:
                raise RuntimeError(f"Centrifuge {self} cannot start with no occupied positions.")

            if len(self.positions_list) % 2 != 0:
                raise RuntimeError(f"Centrifuge {self} has an odd number of positions, invalid.")

            # 验证是否满足对称性质
            n = len(self.positions_list)
            for pos_id in occupied_positions:
                if pos_id not in self.positions_list:
                    raise ValueError(f"Position {pos_id} not in machine {self} position list.")

                idx = self.positions_list.index(pos_id)
                sym_idx = (idx + n // 2) % n
                sym_pos_id = self.positions_list[sym_idx]

                if sym_pos_id not in occupied_positions:
                    raise RuntimeError(
                        f"Position {pos_id} lacks symmetric pair {sym_pos_id}. "
                        "Cannot start centrifuge."
                    )

            # 所有检查通过，设置工作状态
            self.busy = True
            self.end_busy_time = MAX_TIME

        elif occupied_position_type == "plate":
            # 直接调用父类方法处理position占用
            super().occupy(cur_time, last_time, occupied_position_id, occupied_position_type, plate)

        else:
            raise ValueError(f"Unknown position type: {occupied_position_type}")