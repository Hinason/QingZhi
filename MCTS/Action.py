class Action():

    def __init__(self,task):
        self.task = task
    def __eq__(self, other):
        return self.task.id == other.task.id

    def __hash__(self):
        raise self.task.id
