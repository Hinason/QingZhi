def simulate(schedule, scheduled_tasks):
    for scheduled_task in scheduled_tasks:
        # 当前时间设置为任务开始时间
        schedule.current_time = scheduled_task.start_time

        # 找到当前任务的前一个任务,暂时默认只有一个前一个任务
        prev_task = None
        if scheduled_task.prev_task_id:
            for p in scheduled_tasks:
                if p.task_id == scheduled_task.prev_task_id:
                    prev_task = p
                    break

        # 检查任务是否可以执行,task中的occupied_machine_id和occupied_position_id是一个列表,可能包含多个,也可能为空
        occupied_machine = []
        occupied_position = []
        for machine_id in scheduled_task.occupy_machine_id:
            machine = schedule.get_machine_by_id(machine_id)
            if machine.occupied and machine_id not in prev_task.occupy_machine_id:
                print(f"Error: Machine {machine_id} is occupied at time {schedule.current_time}")
                return
            else:
                occupied_machine.append(machine)

        for position_id in scheduled_task.occupy_position_id:
            position = schedule.get_position_by_id(position_id)
            if position.occupied and position_id not in prev_task.occupy_position_id:
                print(f"Error: Position {position_id} is occupied at time {schedule.current_time}")
                return
            else:
                occupied_position.append(position)

        # 释放前一个任务的资源
        if scheduled_task.prev_task_id:
            if prev_task:
                for machine_id in prev_task.release_machine_id:
                    machine = schedule.get_machine_by_id(machine_id)
                    machine.occupied = False
                for position_id in prev_task.release_position_id:
                    position = schedule.get_position_by_id(position_id)
                    position.occupied = False

        # 执行任务,占用资源
        for machine in occupied_machine:
            machine.occupied = True
        for position in occupied_position:
            position.occupied = True

        print(f"Executing task {scheduled_task.task_id} at time {schedule.current_time}")

    print("Simulation completed")

