import copy
from copy import deepcopy

from config import DEBUG


class Task:
    def __init__(self, task_data, assays_id):
        self.id = task_data.get('id', '')
        self.occupy = task_data.get('occupy', [])
        self.realOccupy = []
        self.release = task_data.get('release', [])
        self.occupy_dependency = task_data.get('occupy_dependency', [])
        self.release_dependency = task_data.get('release_dependency', [])
        self.dependency2 = task_data.get('dependency2', -1)
        self.status = task_data.get('status', 0)
        self.duration = task_data.get('time', 0)
        self.beginTime = 0
        self.endTime = 0
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
        self.assays_id = assays_id

        ## 添加锁定逻辑 task在某些情况多选1的时候 这之后也必须选同一个

    def __str__(self):
        return f"Task: {self.taskname} (ID: {self.id})"

class TaskSystem:
    def __init__(self):
        self.tasks = []
        self.taskDic = {}

    def __deepcopy__(self, memo):
        new = TaskSystem()
        new.tasks = deepcopy(self.tasks, memo)
        new.taskDic = deepcopy(self.taskDic, memo)
        return new

    def add_task(self, task_data, assays_id):
        task = Task(task_data, assays_id)
        self.tasks.append(task)
        self.taskDic[task.id] = task

    def get_all_tasks(self):
        return self.tasks

    def get_tasks_num(self):
        return len(self.tasks)

    def get_task(self,taskID):
        return self.taskDic[taskID]

    def __str__(self):
        return f"TaskNumber: {len(self.tasks)}"

    def __hash__(self):
        return hash(self.tasks)
