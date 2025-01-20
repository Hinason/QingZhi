# machine_loader.py
# 从json文件中读取machine的数据并创建对应的simulation_machine

import json
from machines import *

class MachineLoader:
    MACHINE_TYPES = {
        'DENSO_RC8': DENSO_RC8,
        'StorageCarousel_v2': StorageCarousel_v2,
        'Wellwash': Wellwash,
        'CentrifugeSimulator': CentrifugeSimulator
    }

    def __init__(self, json_file_path: str):
        self.json_file_path = json_file_path

    def load_machines(self):
        """
        从JSON文件加载机器数据并创建对应的模拟机器实例。
        """
        try:
            with open(self.json_file_path, 'r', encoding='utf-8') as file:
                data = json.load(file)
        except json.JSONDecodeError as e:
            raise ValueError(f"JSON文件格式不正确: {e}")
        except FileNotFoundError:
            raise FileNotFoundError(f"找不到指定的文件: {self.json_file_path}")

        machines =  {
            machine_data['id']: self.create_simulation_machine(machine_data)
            for machine_data in data
        }

        return machines


    @classmethod
    def create_simulation_machine(cls, machine_data):
        """
        根据机器数据创建相应的模拟机器实例。
        """
        machine_type = machine_data['type']
        machine_class = cls.MACHINE_TYPES.get(machine_type)

        if machine_class is None:
            raise ValueError(f"未知的机器类型: {machine_type}")

        return machine_class(
            id=machine_data['id'],
            name=machine_data['name'],
            type=machine_type
        )