from Simulation.machines.simulation_machine import simulation_machine

class storage_station(simulation_machine):
    """
    存储站
    """

    def __init__(self, id, name, type):
        super().__init__(id, name, type)
