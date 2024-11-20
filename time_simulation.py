def time_simulate(schedule, scheduled_tasks):
    while True:
        print(f"current time : {schedule.current_time}")
        # finish_tasks 存储在 current_time 达到 end_time 的所有任务
        # ready_tasks 存储在 current_time 达到 start_time 的所有任务
        finish_tasks = []
        ready_tasks = []
        for scheduled_task in scheduled_tasks:
            if scheduled_task.start_time == schedule.current_time:
                ready_tasks.append(scheduled_task)
            if scheduled_task.end_time == schedule.current_time:
                finish_tasks.append(scheduled_task)

        # 首先处理到达 end_time 的任务, 只需要释放占用的 machine 和 position
        for task in finish_tasks:
            for machine_id in task.release_machine_id:
                machine = schedule.get_machine_by_id(machine_id)
                machine.occupied = False
            for position_id in task.release_position_id:
                position = schedule.get_position_by_id(position_id)
                position.occupied = False
            # 当一个任务到达 end_time, 说明该任务已经执行完毕, 剩余任务数量 - 1
            task.status = True
            schedule.remain_tasks_num = schedule.remain_tasks_num - 1
            print(f"task {task.task_id} is completed")

        # 然后处理到达 start_time 的任务，这里需要判断前置任务是否全部完成
        for task in ready_tasks:
            # 找到当前任务的所有前置任务, 要求前置任务全部完成且要满足时间约束
            prev_tasks = []
            for prev_task_id in task.prev_task_id:
                for prev_task in scheduled_tasks:
                    if prev_task.task_id == prev_task_id:
                        if not prev_task.status:
                            print(f"Error: Task {prev_task.task_id} is not completed, can't run Task {task.task_id} at time {schedule.current_time}")
                            return
                        if schedule.current_time - prev_task.start_time > task.time_limit:
                            print(f"Error: Task {prev_task.task_id} and Task {task.task_id} don't satisfy time limit at time {schedule.current_time}")
                            return
                        prev_tasks.append(prev_task)
                        break

            # 检查任务是否可以执行,task中的occupied_machine_id和occupied_position_id是一个列表,可能包含多个,也可能为空
            # 当前任务占用的机器可能是前置任务在占用，这种情况下任务可以进行
            occupied_machine = []
            occupied_position = []
            for machine_id in task.occupy_machine_id:
                machine = schedule.get_machine_by_id(machine_id)
                if machine.occupied and machine.occupied_assays_id != task.assays_id:
                    print(f"Error: Machine {machine_id} is occupied at time {schedule.current_time}")
                    return
                else:
                    occupied_machine.append(machine)
            for position_id in task.occupy_position_id:
                position = schedule.get_position_by_id(position_id)
                if position.occupied and position.occupied_assays_id != task.assays_id:
                    print(f"Error: Position {position_id} is occupied at time {schedule.current_time}")
                    return
                else:
                    occupied_position.append(position)

            # 执行任务,占用资源
            for machine in occupied_machine:
                machine.occupied = True
                machine.occupied_assays_id = task.assays_id
            for position in occupied_position:
                position.occupied = True
                position.occupied_assays_id = task.assays_id

            print(f"task {task.task_id} is working")

        # 判断任务是否全部完成
        if schedule.remain_tasks_num == 0:
            print(f"all tasks are completed, sum time: {schedule.current_time}")
            break

        schedule.current_time = schedule.current_time + 1
                    
    
    


