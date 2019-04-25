class Model():
    def __init__(self, id: int):
        self.__id = id
    def setId(self, id : int):
        self.__id = id
    def getId(self):
        return self.__id

class eModel(Model):
    def __init__(self, id: int, name: str):
        super().__init__(id)
        self.__name = name
    def setName(self, name : str):
        self.__name = name
    def getName(self):
        return self.__name

class Equipment(eModel):
    def __init__(self, id: int, name : str):
        super().__init__(id, name)
        self.__reservations = []
    def reserveEquipment(self, start: int, end: int):
        for reserve in self.__reservations:
            if reserve[0] <= end and reserve[1] >= start:
                return False
        self.__reservations.append((start, end))
        return True
    def getReservation(self):
        return self.__reservations.__iter__()
    
class Trainer(eModel):
    def __init__(self, id: int, name: str, workStart : int = None, workEnd : int = None):
        super().__init__(id, name)
        self.__workStart = workStart
        self.__workEnd = workEnd
        self.__assignments = []
    def setWorkTimes(self, workStart: int, workEnd: int):
        self.__workStart = workStart
        self.__workEnd = workEnd
    def getWorkTimes(self):
        return (self.__workStart, self.__workEnd)
    def getAssignments(self):
        return self.__assignments.__iter__()
    def assignToCustomer(self, start: int, end: int):
        for assignment in self.__assignments:
            if assignment[0] <= end and assignment[1] >= start:
                return False
        self.__assignments.append((start, end))
        return True

class ExercisePlanItem(Model):
    def __init__(self, equipment : Equipment, duration : int, steps : list):
        self.__equipment = equipment
        self.__duraton = duration
        self.__steps = list(steps)
    def getEquipment(self):
        return self.__equipment
    def getDuration(self):
        return self.__duraton
    def getSteps(self):
        return self.__steps

class ExercisePlan(Model):
    def __init__(self, id: int, planItems: list, trainer: Trainer):
        super().__init__(id)
        self.__planItems = list(planItems)
        self.__trainer = trainer
    def getPlanItems(self):
        return self.__planItems
    def getTrainer(self):
        return self.__trainer

class GymHall(Model):
    def __init__(self):
        self.__trainers = []
        self.__openStart = int()
        self.__openEnd = int()
        self.__equipments = []
    def addTrainer(self, trainer: Trainer):
        self.__trainers.append(trainer)
    def removeTrainer(self, trainer: Trainer):
        i = self.__trainers.index(trainer)
        self.__trainers.pop(i)
    def getTrainers(self):
        return self.__trainers.__iter__()
    def setOpenTime(self, start: int, end: int):
        if end - start != 12:
            raise Exception("A hall has to be open for exactly 12 hours")
        self.__openStart = start
        self.__openEnd = end
    def getOpenTime(self):
        return (self.__openStart, self.__openEnd)
    def addEquipment(self, equipement: Equipment):
        self.__equipments.append(equipement)
    def removeEquipment(self, equipment: Equipment):
        i = self.__equipments.index(equipment)
        self.__equipments.pop(i)
    def getAllEquipments(self):
        return self.__equipments.__iter__()

class Controller():
    pass
