class Action():

    def __init__(self,task,beginTime):
        self.task = task
        self.beginTime = beginTime

    def __eq__(self, other):
        return self.task.id == other.task.id

    def __str__(self):
        return str(self.task) +" begin at Time " +str(self.beginTime)

    def __hash__(self):
        return hash(self.task.id)
