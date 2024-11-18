def simulate(schedule, scheduled_tasks):
    for scheduled_task in scheduled_tasks:
        # 当前时间设置为任务开始时间
        schedule.current_time = scheduled_task.start_time

        # 找到当前任务的所有前置任务，前置任务必须全部已经完成
        prev_tasks = []
        for prev_task_id in scheduled_task.prev_task_id:
            for p in scheduled_tasks:
                if p.task_id == prev_task_id:
                    if not p.status:
                        print(f"Error: Task {p.task_id} is not completed, can't run Task {scheduled_task.task_id}")
                        prev_tasks.clear()
                        return
                    prev_tasks.append(p)
                    break

        # 检查任务是否可以执行,task中的occupied_machine_id和occupied_position_id是一个列表,可能包含多个,也可能为空
        # 当前任务占用的机器可能是前置任务在占用，这种情况下任务可以进行
        occupied_machine = []
        occupied_position = []
        for machine_id in scheduled_task.occupy_machine_id:
            machine = schedule.get_machine_by_id(machine_id)
            if machine.occupied and machine.occupied_task_id not in scheduled_task.prev_task_id:
                print(f"Error: Machine {machine_id} is occupied at time {schedule.current_time}")
                occupied_machine.clear()
                return
            else:
                occupied_machine.append(machine)

        for position_id in scheduled_task.occupy_position_id:
            position = schedule.get_position_by_id(position_id)
            if position.occupied and position.occupied_task_id not in scheduled_task.prev_task_id:
                print(f"Error: Position {position_id} is occupied at time {schedule.current_time}")
                occupied_position.clear()
                return
            else:
                occupied_position.append(position)

        # 释放前一个任务的资源
        for prev_task in prev_tasks:
            for machine_id in prev_task.release_machine_id:
                machine = schedule.get_machine_by_id(machine_id)
                machine.occupied = False
            for position_id in prev_task.release_position_id:
                position = schedule.get_position_by_id(position_id)
                position.occupied = False

        # 执行任务,占用资源
        scheduled_task.status = True
        for machine in occupied_machine:
            machine.occupied = True
            machine.occupied_task_id = scheduled_task.task_id
        for position in occupied_position:
            position.occupied = True
            position.occupied_task_id = scheduled_task.task_id

        print(f"Executing task {scheduled_task.task_id} at time {schedule.current_time}")

    print("Simulation completed")

