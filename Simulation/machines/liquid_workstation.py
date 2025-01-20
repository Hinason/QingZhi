from Simulation.machines.simulation_machine import simulation_machine

class liquid_workstation(simulation_machine):
    """
    液体工作站
    """

    def __init__(self, id, name, type):
        super().__init__(id, name, type)
