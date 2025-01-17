class simulation_machine:
    def __init__(self, id, name, type):
        self.id = id
        self.name = name
        self.type = type
        self.busy = False
        self.endBusyTime = 0
        self.positions = {}  #dict

    def __str__(self):
        return self.name

    def update(self, time):
        if time > self.endBusyTime:
            self.busy = False

    def occupy(self, curTime, lastTime, occupyPositions):
        if self.busy:
            raise RuntimeError(f"Machine {self} is busy at Time {curTime}")

        for positionName in occupyPositions:
            if self.positions[positionName].occupy:
                raise RuntimeError(f"Position {positionName} is already occupied at Time {curTime}")

        # 继续处理占用逻辑
        self.busy = True
        for positionName in occupyPositions:
            self.positions[positionName].occupy = True

        # 可能还需要设置其他状态或记录日志

    def check(self):
        pass
