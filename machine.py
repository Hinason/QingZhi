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


class MachineSystem:
    def __init__(self):
        self.machines = []

    def add_machine(self, machine_data):
        machine = Machine(machine_data['id'], machine_data['name'], machine_data['type'],
                          machine_data['instrumentcategory'],
                          machine_data['instrumentcategorytext'])
        self.machines.append(machine)

    def get_all_machines(self):
        return self.machines

    def add_position(self, position):
        for machine in self.machines:
            if machine.id == position.machine:
                machine.positions.append(position)
                break

    def __str__(self):
        return f"MachineNumber: {len(self.machines)}"