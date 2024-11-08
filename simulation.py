def simulate(schedule, max_time):
    while schedule.current_time < max_time:
        # Check if any tasks can start
        for task in schedule.task_system.tasks:
            if task.status == "Pending" and can_start_task(task, schedule):
                start_task(task, schedule)

        # Update machine and task status
        update_status(schedule)

        # Increment time
        schedule.current_time += 1


def can_start_task(task, schedule):
    # Check if all required resources are available
    return all(is_resource_available(resource, schedule) for resource in task.resources)


def start_task(task, schedule):
    # Allocate resources and update task status
    task.status = "Running"
    task.start_time = schedule.current_time
    # Update machine status
    # This part needs more detailed implementation


def update_status(schedule):
    # Update task and machine status based on current time
    for task in schedule.tasks:
        if task.status == "Running" and schedule.current_time - task.start_time >= task.duration:
            task.status = "Completed"
            task.end_time = schedule.current_time
            # Release resources
            # This part needs more detailed implementation


def is_resource_available(resource, schedule):
    # Check if the required resource (machine) is available
    return any(machine.machine_id == resource and machine.status == "Idle" for machine in schedule.machine_system.machines)
