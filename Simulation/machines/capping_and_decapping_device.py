from Simulation.machines.simulation_machine import simulation_machine

class capping_and_decapping_device(simulation_machine):
    """
    封盖、去盖
    """

    def __init__(self, id, name, type):
        super().__init__(id, name, type)
