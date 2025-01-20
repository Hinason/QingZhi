from Simulation.machines.simulation_machine import simulation_machine

class centrifuge(simulation_machine):
    """
    离心机
    """

    def __init__(self, id, name, type):
        super().__init__(id, name, type)
