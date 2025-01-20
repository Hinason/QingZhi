from Simulation.machines.simulation_machine import simulation_machine

class DENSO_RC8(simulation_machine):
    """
    DENSO_RC8是一个机械臂
    """

    def __init__(self, id, name, type):
        super().__init__(id, name, type)
