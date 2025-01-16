class simulation_machine:
    def __init__(self,positions):
        self.busy = False
        self.endBusyTime = 0
        self.positions = positions #dict
        self.name = ""

    def __str__(self):
        return self.name

    def update(self,time):
        if time > self.endBusyTime:
            self.busy = False

    def occupy(self,curTime,lastTime,occupyPositions):
        assert (self.busy == False , "Busy Machine "+ str(self) + " at Time "+ str(curTime))
        for positionName in occupyPositions:
            assert(self.positions[positionName].occupy == False ,"")
