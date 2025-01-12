import json

from MCTS.State import State
from machine import MachineSystem
from task import TaskSystem
from position import PositionSystem
from schedule import Schedule, ScheduledTask
from task_simulation import task_simulate
from time_simulation import time_simulate
from config import DEBUG
from MCTS.mcts import  mcts


def load_machines_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    machine_system = MachineSystem()
    for assay in data['assaysmodel']:
        for machine_data in assay['machines']:
            machine_system.add_machine(machine_data)
    return machine_system


def load_tasks_from_json(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        data = json.load(file)
    task_system = TaskSystem()
    for assay in data['assaysmodel']:
        assays_id = assay.get('assaysid', '')
        for task_data in assay.get('tasks', []):
            task_system.add_task(task_data, assays_id)
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
    for pos in position_system.get_all_positions():
        machine_system.get_machine(pos.machine).addPos(pos)
    schedule = Schedule(task_system, machine_system, position_system)

    # 从 json 文件获取的 task 转变为 schedule_tasks
    # schedule_tasks 是算法和仿真运行的输入
    scheduled_tasks = schedule.get_schedule_tasks()

    scheduleState = State(task_system,position_system,machine_system)
    mcts = mcts(timeLimit=2000)
    action = mcts.search(scheduleState)
    print(action)
    # 此处使用算法调度scheduled_tasks
    # 主要是给每一个 task 确定开始时间(start_time)以及结束时间(end_time)
    # 由于 duration 是一个固定值, 因此只需要确定 start_time 即可, end_time=start_time+duration
    pass

    # 手动创建test1.json的ScheduledTask
    # scheduled_tasks = [
    #     ScheduledTask("a4389c1d88194dbca0a1d94626450e57",
    #                   0, 5, 5,
    #                   [], ["11a7fd397e2c45a1b37b0b7b5bdafc25"],
    #                   ["2A1ED471BA87491A9349656CBF55CDF8",],
    #                   ["e93ef43bc4b3493e9b7cd27252dc0331","6ED7448DEA49411981D06807F4656F27"],
    #                   ["2A1ED471BA87491A9349656CBF55CDF8",],
    #                   ["e93ef43bc4b3493e9b7cd27252dc0331","6ED7448DEA49411981D06807F4656F27"],
    #                   "3426392A4D16413E87819B003585EE82"),
    #     ScheduledTask("11a7fd397e2c45a1b37b0b7b5bdafc25",
    #                   10, 10, 20,
    #                   ["a4389c1d88194dbca0a1d94626450e57"], ["31e096523e114b08b6b6eb96a621c828"],
    #                   ["8DA254642C2C4FFF94C39B298B65A9BE","AA8E524389BE4EAB9D1BFE626C7937A7"],
    #                   ["4E43EF8C7F154ADBBEE4DDEDAC66DE5A","0672F2FEB135489CB952D8AAED313EF8"],
    #                   ["8DA254642C2C4FFF94C39B298B65A9BE","AA8E524389BE4EAB9D1BFE626C7937A7"],
    #                   ["4E43EF8C7F154ADBBEE4DDEDAC66DE5A","0672F2FEB135489CB952D8AAED313EF8"],
    #                   "3426392A4D16413E87819B003585EE82"),
    #     ScheduledTask("31e096523e114b08b6b6eb96a621c828",
    #                   20, 5, 25,
    #                   ["11a7fd397e2c45a1b37b0b7b5bdafc25"], [],
    #                   ["8DA254642C2C4FFF94C39B298B65A9BE"],
    #                   ["5b0482266a2f467da9bc387740da22de"],
    #                   ["8DA254642C2C4FFF94C39B298B65A9BE"],
    #                   ["5b0482266a2f467da9bc387740da22de"],
    #                   "3426392A4D16413E87819B003585EE82"),
    # ]

    # time_simulate(schedule, scheduled_tasks)
