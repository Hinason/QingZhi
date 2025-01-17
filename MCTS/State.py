from copy import deepcopy

import task
import position
import machine
from  MCTS.Action import Action

class State:

    def __init__(self,taskSystem,positionSystem,machineSystem):
        # param :
        # 注意一下 这里要考虑动态调度问题 所以拿到的task不一定全都是未安排时间的
        # 在考虑状态转移的时候确认一下
        # 那么问题来了 如何用这种带初始条件的task融入我的MDP过程
        # 需不需要考虑没做完的动作呢？
        # 目前可以认为全部输出的动作都已经做完
        self.finishTask = 0
        self.taskSystem = taskSystem
        self.positionSystem = positionSystem
        self.machineSystem = machineSystem
        self.preAvailableAction = None # 这里的available只是前后关系的 机器上的阻塞另外考虑
        # 这么处理为了降低复杂度提高效率
        self.needDetails = True
        self.dfsTask()

    def __deepcopy__(self,memo):
        newState = State(deepcopy(self.taskSystem,memo),deepcopy(self.positionSystem,memo),deepcopy(self.machineSystem,memo))
        newState.finishTask = self.finishTask
        newState.preAvailableAction = self.preAvailableAction
        newState.needDetails = self.needDetails
        newState.dfsTask()
        return newState


    def dfsTask(self):
        tasks = self.taskSystem.get_all_tasks()
        self.finishTask = 0
        # status 代表任务是否完成
        # 0 未开始 1 已完成
        self.preAvailableAction = []
        for task in tasks:
            if task.status ==1 :
                self.finishTask += 1
                continue
            pre = task.pre
            allPreFinishFlag = True
            for preTaskId in pre:
                preTask = self.taskSystem.get_task(preTaskId)
                if preTask.status != 1:
                    allPreFinishFlag = False
            if allPreFinishFlag:
                self.preAvailableAction.append(task)




    def getCurrentPlayer(self):
        return 0

    def getEarliestPosition(self,occupySourceIDList):
        selectPos = None
        earliestTime = 1000000
        # 在可选集合中选取一个
        for occupySourceID in occupySourceIDList:
            occupySource = self.positionSystem.get_position(occupySourceID)
            if occupySource.status == 0 and occupySource.availableTime < earliestTime:
                selectPos = occupySource
                earliestTime = occupySource.availableTime
        return selectPos,earliestTime

    def getPossibleActions(self):
        possibleActions = []
        for task in self.preAvailableAction:
            beginTime = 0
            hasAvailablePos = False
            for preTaskId in task.pre:
                beginTime = max(beginTime,self.taskSystem.get_task(preTaskId).endTime)
            for occupySourceIDList in task.occupy:
                selectPos ,earliestTime = self.getEarliestPosition(occupySourceIDList)
                if selectPos is not None:
                    hasAvailablePos = True
                    beginTime = max(beginTime,earliestTime)
                else:
                    continue
            if hasAvailablePos:
                possibleActions.append(Action(task,beginTime))
        if self.needDetails:
            print("state Stage : %d "%(self.finishTask))
            for action in possibleActions:
                print(action)
        assert (len(possibleActions)>0,"死锁")
        return  possibleActions

    def takeAction(self, action):
        newState = deepcopy(self)
        task = newState.taskSystem.get_task(action.task.id)
        beginTime = action.beginTime
        realOccupy = []
        selPos = [ ]
        for preTaskId in task.pre:
            beginTime = max(beginTime, self.taskSystem.get_task(preTaskId).endTime)

        for occupySourceIDList in task.occupy:
            selectPos, earliestTime = self.getEarliestPosition(occupySourceIDList)
            if selectPos is None:
                print('>')
            selectPos.status = 1 # 占据

            beginTime = max(beginTime,earliestTime)
            realOccupy.append(selectPos.id)
            selPos.append(selectPos)
        task.realOccupy += realOccupy #可能有上一个机器的占据依赖残留
        task.beginTime = beginTime
        task.endTime = task.beginTime + task.duration
        realOccupy = task.realOccupy
        if self.needDetails:
            print('task begin At '+str(task.beginTime) + ' end At '+str(task.endTime)+" occupy: "+str(realOccupy))
        for pos in selPos:
            pos.availableTime = task.endTime
        for releaseIDList in task.release:
            for releaseID in releaseIDList:
                if releaseID not in realOccupy:
                    continue
                position = self.positionSystem.get_position(releaseID)
                position.status = 0  # 释放
                realOccupy.remove(releaseID)
                if self.needDetails:
                    print('task release '+str(releaseID))
                # self.machineSystem.get_machine(position.machine).updateState()
                # 应该是可有可无目前看来
        if len(realOccupy) >=1:
            for taskID in task.next:
                nextTask = newState.taskSystem.get_task(taskID)
                nextTask.realOccupy  += realOccupy

        task.status = 1 # 完成
        ## 重新找到可运行的任务
        newState.dfsTask()
        ## 部分工作需要锁定！
        ## 设置锁定时间

        return newState

    def isTerminal(self):
        for task in self.taskSystem.get_all_tasks():
            if task.status == 0:
                return False
        return True


    def getReward(self):
        # only needed for terminal states
        time = 0
        for task in self.taskSystem.get_all_tasks():
            time = max(time,task.endTime)
        return -time

    def __eq__(self, other):
        return self.taskSystem.get_hash() == other.taskSystem.get_hash()
