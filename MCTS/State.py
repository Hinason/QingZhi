import task
import position
import machine


class State:

    def __init__(self,taskSystem,positionSystem,machineSystem):
        # param :
        # 懒得写了
        # 注意一下 这里要考虑动态调度问题 所以拿到的task不一定全都是未安排时间的
        # 在考虑状态转移的时候确认一下
        # 那么问题来了 如何用这种带初始条件的task融入我的MDP过程
        # 需不需要考虑没做完的动作呢？
        # 目前可以认为全部输出的动作都已经做完
        self.taskSystem = taskSystem
        self.positionSystem = positionSystem
        self.machineSystem = machineSystem
        self.curAvailableAction = None # 这里的available只是前后关系的 机器上的阻塞另外考虑
        # 这么做是为了降低复杂度
        self.dfsTask()

    def dfsTask(self):
        tasks = self.taskSystem.get_all_tasks()
        # status 代表任务是否完成
        # 0 未开始 1 已完成
        self.curAvailableAction = []
        for task in tasks:
            pre = task.pre
            allPreFinishFlag = True
            for preTaskId in pre:
                preTask = self.taskSystem.get_task(preTaskId)
                if preTask.status != 1:
                    allPreFinishFlag = False
            if allPreFinishFlag:
                self.curAvailableAction.append(task)




    def getCurrentPlayer(self):
        return 0

    def getPossibleActions(self):
        raise NotImplementedError()

    def takeAction(self, action):
        raise NotImplementedError()

    def isTerminal(self):
        raise NotImplementedError()

    def getReward(self):
        # only needed for terminal states
        raise NotImplementedError()

    def __eq__(self, other):
        raise NotImplementedError()
