from config import DEBUG

class Position:
    def __init__(self, position_data):
        self.id = position_data.get('id', '')
        self.status = position_data.get('status', 0)
        self.machine = position_data.get('machine', '')
        self.positionname = position_data.get('positionname', '')
        self.machinename = position_data.get('machinename', '')
        self.sourcetype = position_data.get('sourcetype', '')
        self.occupied = False
        self.occupied_task_id = None

    def __str__(self):
        return f"Position: {self.positionname} (ID: {self.id})"

class PositionSystem:
    def __init__(self):
        self.positions = []

    def add_position(self, position_data):
        position = Position(position_data)
        self.positions.append(position)

    def get_all_positions(self):
        return self.positions

    def get_position_by_id(self, position_id):
        for position in self.positions:
            if position.id == position_id:
                return position
        return None

    def __str__(self):
        return f"PositionNumber: {len(self.positions)}"
