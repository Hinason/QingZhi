from Simulation.machines.simulation_machine import simulation_machine

class code_scanner(simulation_machine):
    """
    条码扫描仪
    """

    def __init__(self, id, name, type):
        super().__init__(id, name, type)
