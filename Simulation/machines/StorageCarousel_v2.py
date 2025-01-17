from Simulation.machines.simulation_machine import simulation_machine

class StorageCarousel_v2(simulation_machine):
    """
    StorageCarousel_v2是一个存储站
    """

    def __init__(self, id, name, type):
        super().__init__(id, name, type)

    def update(self, time):
        if time > self.endBusyTime:
            self.busy = False

    def occupy(self, curTime, lastTime, occupyPositions):
        assert (self.busy == False, "Busy Machine " + str(self) + " at Time " + str(curTime))
        for positionName in occupyPositions:
            assert (self.positions[positionName].occupy == False, "")

    def check(self):
        pass