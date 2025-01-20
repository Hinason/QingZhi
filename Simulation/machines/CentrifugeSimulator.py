from Simulation.machines.simulation_machine import simulation_machine

class CentrifugeSimulator(simulation_machine):
    """
    CentrifugeSimulator是一个离心机
    """

    def __init__(self, id, name, type):
        super().__init__(id, name, type)
