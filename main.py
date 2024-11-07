import json
from machine import Machine
from task import TaskSystem
from position import PositionSystem

from config import DEBUG



def load_machines_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    machine_system = Machine()

    for assay in data['assaysmodel']:
        for machine_data in assay['machines']:
            machine_system.add_machine(machine_data)

    return machine_system


def load_tasks_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    task_system = TaskSystem()

    for assay in data['assaysmodel']:
        for task_data in assay.get('tasks', []):
            task_system.add_task(task_data)

    return task_system


def load_positions_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)

    position_system = PositionSystem()

    for assay in data['assaysmodel']:
        for position_data in assay.get('positions', []):
            position_system.add_position(position_data)

    return position_system


if __name__ == "__main__":
    file_path = 'test.json'  # 替换正确的JSON文件路径
    machine_system = load_machines_from_json(file_path)
    task_system = load_tasks_from_json(file_path)
    position_system = load_positions_from_json(file_path)

    # 打印所有加载的机器
    if DEBUG:
        all_machines = machine_system.get_all_machines()
        for machine in all_machines:
            print(f"ID: {machine.id}, Name: {machine.name}, Type: {machine.type}")

        print("----------------------------------------------------------------------------------")
        i = 0
        for task in task_system.get_all_tasks():
            print(task)
            i = i + 1
            if i > 10:
                break

        print("\n----------------------------------------------------------------------------------")
        i = 0
        for position in position_system.get_all_positions():
            print(position)
            i = i + 1
            if i > 10:
                break