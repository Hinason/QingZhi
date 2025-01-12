from config import DEBUG


class Machine:
    def __init__(self, id, name, type, category, category_text):
        self.id = id
        self.name = name
        self.type = type
        self.instrumentcategory = category
        self.instrumentcategorytext = category_text
        self.taskstoragedetail = []
        self.positions = []
        self.occupied = False
        self.occupied_assays_id = None
        self.status = 0 # 空闲

    def addPos(self,position):
        self.positions.append(position)

    def updateState(self):
        # 这里注意不同机器的pos与status的对应关系
        self.status = 0
        for position in self.positions:
            if position.status == 1:
                self.status = 1
                return


class MachineSystem:
    def __init__(self):
        self.machines = []
        self.machinesDict = {}

    def add_machine(self, machine_data):
        machine = Machine(machine_data['id'], machine_data['name'], machine_data['type'],
                          machine_data['instrumentcategory'],
                          machine_data['instrumentcategorytext'])
        self.machines.append(machine)
        self.machinesDict[machine.id] = machine

    def get_all_machines(self):
        return self.machines

    def get_machine(self, id):
        return self.machinesDict[id]

    def add_position(self, position):
        for machine in self.machines:
            if machine.id == position.machine:
                machine.positions.append(position)
                break

    def __str__(self):
        return f"MachineNumber: {len(self.machines)}"