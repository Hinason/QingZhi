from config import DEBUG


class Machine:
    class BaseMachine:
        def __init__(self, id, name, type, category, category_text):
            self.id = id
            self.name = name
            self.type = type
            self.instrumentcategory = category
            self.instrumentcategorytext = category_text
            self.taskstoragedetail = []

    class PCRSimulator(BaseMachine):
        def __init__(self, id, name, category, category_text):
            super().__init__(id, name, "PCRSimulator", category, category_text)

    class CentrifugeLoader(BaseMachine):
        def __init__(self, id, name, category, category_text):
            super().__init__(id, name, "CentrifugeLoader", category, category_text)

    class TrashChute(BaseMachine):
        def __init__(self, id, name, category, category_text):
            super().__init__(id, name, "TrashChute", category, category_text)

    def __init__(self):
        self.machines = []

    def add_machine(self, machine_data):
        machine_type = machine_data['type']
        machine = None
        if machine_type == "PCRSimulator":
            machine = self.PCRSimulator(machine_data['id'], machine_data['name'],
                                        machine_data['instrumentcategory'],
                                        machine_data['instrumentcategorytext'])
        elif machine_type == "CentrifugeLoader":
            machine = self.CentrifugeLoader(machine_data['id'], machine_data['name'],
                                            machine_data['instrumentcategory'],
                                            machine_data['instrumentcategorytext'])
        elif machine_type == "TrashChute":
            machine = self.TrashChute(machine_data['id'], machine_data['name'],
                                      machine_data['instrumentcategory'],
                                      machine_data['instrumentcategorytext'])
        else:
            print(f"Unknown machine type: {machine_type}")

        if machine is not None:
            self.machines.append(machine)

    def get_all_machines(self):
        return self.machines
