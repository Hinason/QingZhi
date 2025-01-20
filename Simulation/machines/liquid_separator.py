from Simulation.machines.simulation_machine import simulation_machine

class liquid_separator(simulation_machine):
    """
    分液、清洗
    """

    def __init__(self, id, name, type):
        super().__init__(id, name, type)
