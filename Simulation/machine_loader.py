# machine_loader.py
# 从 machine_system 中读取machine的数据并创建对应的simulation_machine

from Simulation.machines import *

class MachineLoader:
    MACHINE_TYPES = {
        'DENSO RC8': robot_arm,
        'StorageCarousel v2': storage_station,
        'Wellwash': liquid_separator,
        'CentrifugeSimulator': centrifuge,
        'LiquidJanusG3.v2': liquid_workstation,
        'PlateLidOpenAndClose': capping_and_decapping_device,
        'PCRSimulator': pcr,
        'Storage Universal': storage_station,
        'CenerifugeSunWang DW-4': centrifuge,
        '1D Code Scanner': code_scanner,
        'SealerAndPeelIOmicsSP100': sealer_and_peel_device,
        'a4S Sealer': sealer_and_peel_device,
    }

    def __init__(self, machine_system):
        self.machine_system = machine_system
        self.machines = None

    def load_machines(self):
        """
        从 machine_system 加载机器数据并创建对应的模拟机器实例。

        该方法从 machine_system 获取所有机器数据，为每台机器创建模拟实例，
        并将它们存储在一个以机器ID为键的字典中。

        Returns:
            dict: 一个包含模拟机器实例的字典，其中键为机器ID，值为对应的机器实例。
        """
        machines_data = self.machine_system.get_all_machines()
        self.machines =  {
            machine_data.id : self.create_simulation_machine(machine_data)
            for machine_data in machines_data
        }

        return self.machines


    @classmethod
    def create_simulation_machine(cls, machine_data):
        """
        根据机器数据创建相应的模拟机器实例。
        """
        machine_type = machine_data.type
        machine_class = cls.MACHINE_TYPES.get(machine_type)

        if machine_class is None:
            raise ValueError(f"未知的机器类型: {machine_type}")

        return machine_class(
            id=machine_data.id,
            name=machine_data.name,
            type=machine_type
        )

    def load_position(self, position_system):
        positions = position_system.get_all_positions()
        for position in positions:
            if "plate" == position.sourcetype:            # "plate" 说明是机器上的position
                self.machines[position.machine].positions[position.id] = 0
            elif "work" == position.sourcetype:            # "work" 说明是机器本身
                self.machines[position.machine].busy = False
