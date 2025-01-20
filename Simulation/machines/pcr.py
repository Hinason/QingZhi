from Simulation.machines.simulation_machine import simulation_machine

class pcr(simulation_machine):
    """
    热循环器
    """

    def __init__(self, id, name, type):
        super().__init__(id, name, type)
