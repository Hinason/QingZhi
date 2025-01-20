from copy import deepcopy

from config import DEBUG

class Position:
    def __init__(self, position_data):
        self.id = position_data.get('id', '')
        self.status = position_data.get('status', 0)
        # 0 代表可用 1表示占用
        self.machine = position_data.get('machine', '')
        self.availableTime = 0
        self.positionname = position_data.get('positionname', '')
        self.machinename = position_data.get('machinename', '')
        # self.sourcetype = position_data.get('sourcetype', '')
        # self.occupied = False
        # self.occupied_assays_id =



    def __str__(self):
        return f"Position: {self.positionname} (ID: {self.id}) .AvailableTime: {self.availableTime}  ({self.status}) "

class PositionSystem:
    def __init__(self):
        self.positions = []
        self.positionDic = {}

    def __deepcopy__(self, memo):
        new = PositionSystem()
        new.positions = deepcopy(self.positions, memo)
        new.positionDic = deepcopy(self.positionDic, memo)
        return new

    def add_position(self, position_data):
        position = Position(position_data)
        self.positions.append(position)
        self.positionDic[position.id] = position

    def get_all_positions(self):
        return self.positions

    def get_position(self, position_id):
        return self.positionDic[position_id]

    def __str__(self):
        return f"PositionNumber: {len(self.positions)}"
