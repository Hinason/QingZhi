from Simulation.machines.simulation_machine import simulation_machine

class Wellwash(simulation_machine):
    """
    Wellwash是一个分液、清洗机器
    """

    def __init__(self, id, name, type):
        super().__init__(id, name, type)
