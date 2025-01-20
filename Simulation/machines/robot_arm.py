from Simulation.machines.simulation_machine import simulation_machine

class robot_arm(simulation_machine):
    """
    机械臂
    """

    def __init__(self, id, name, type):
        super().__init__(id, name, type)
