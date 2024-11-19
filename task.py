from config import DEBUG


class Task:
    def __init__(self, task_data):
        self.id = task_data.get('id', '')
        self.occupy = task_data.get('occupy', [])
        self.release = task_data.get('release', [])
        self.occupy_dependency = task_data.get('occupy_dependency', [])
        self.release_dependency = task_data.get('release_dependency', [])
        self.dependency2 = task_data.get('dependency2', -1)
        self.status = task_data.get('status', 0)
        self.priority = task_data.get('priority', 0)
        self.time = task_data.get('time', 0)
        self.robotgettime = task_data.get('robotgettime', 0)
        self.robotputtime = task_data.get('robotputtime', 0)
        self.estduration = task_data.get('estduration', 0)
        self.pre = task_data.get('pre', [])
        self.next = task_data.get('next', [])
        self.machine = task_data.get('machine', '')
        self.position = task_data.get('position', '')
        self.release_machine = task_data.get('release_machine', [])
        self.release_position = task_data.get('release_position', [])
        self.dependency = task_data.get('dependency', -1)
        self.available = task_data.get('available', 0)
        self.start_time = task_data.get('start_time', 0)
        self.heuristic = task_data.get('heuristic', 0)
        self.taskname = task_data.get('taskname', '')
        self.plateprocess = task_data.get('plateprocess', '')
        self.stepplatename = task_data.get('stepplatename', '')
        self.taskplatename = task_data.get('taskplatename', '')
        self.stepname = task_data.get('stepname', '')
        self.sequnceid = task_data.get('sequnceid', '')
        self.steps = task_data.get('steps', [])
        self.sequncestepid = task_data.get('sequncestepid', '')
        self.procedurids = task_data.get('procedurids', [])
        self.nodeid = task_data.get('nodeid', '')
        self.processtype = task_data.get('processtype', 0)
        self.processtypetext = task_data.get('processtypetext', '')
        self.taskplates = task_data.get('taskplates', [])
        self.timeout = task_data.get('timeout', 0)
        self.zone = task_data.get('zone', '')

    def __str__(self):
        return f"Task: {self.taskname} (ID: {self.id})"

class TaskSystem:
    def __init__(self):
        self.tasks = []

    def add_task(self, task_data):
        task = Task(task_data)
        self.tasks.append(task)

    def get_all_tasks(self):
        return self.tasks

    def get_tasks_num(self):
        return len(self.tasks)

    def __str__(self):
        return f"TaskNumber: {len(self.tasks)}"
