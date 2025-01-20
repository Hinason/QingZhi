from Simulation.machines.simulation_machine import simulation_machine

class sealer_and_peel_device(simulation_machine):
    """
    封膜、撕膜
    """

    def __init__(self, id, name, type):
        super().__init__(id, name, type)
