from datetime import datetime


class Model():
    def __init__(self, id: int):
        self.__id = id

    def setId(self, id: int):
        self.__id = id

    def getId(self):
        return self.__id


class eModel(Model):
    def __init__(self, id: int, name: str):
        super().__init__(id)
        self.__name = name

    def setName(self, name: str):
        self.__name = name

    def getName(self):
        return self.__name


class Equipment(eModel):
    def __init__(self, id: int, name: str):
        super().__init__(id, name)
        self.__reservations = []
        self.__hall = None

    def reserveEquipment(self, start: int, end: int):
        if not self.checkAvailibility(start, end):
            return False
        self.__reservations.append((start, end))
        return True

    def clearReservation(self, start: int, end: int):
        self.__reservations.remove((start, end))

    def checkAvailibility(self, start: int, end: int):
        for reserve in self.__reservations:
            if reserve[0] <= end and reserve[1] >= start:
                return False
        return True

    def getReservation(self):
        return self.__reservations.__iter__()

    def setHall(self, hall):
        self.__hall = hall

    def getHall(self):
        return self.__hall


class Trainer(eModel):
    def __init__(self, id: int, name: str, workStart: int = None, workEnd: int = None):
        super().__init__(id, name)
        self.__hall = None
        self.__workStart = workStart
        self.__workEnd = workEnd
        self.__assignments = []

    def setGymHall(self, hall):
        start, end = hall.getOpenTime()
        if self.__workStart <= start or self.__workEnd >= end:
            raise Exception("Trainer work time is incompatible with hall's open time")
        self.__hall = hall

    def getGymHall(self):
        return self.__hall

    def setWorkTimes(self, workStart: int, workEnd: int):
        start, end = self.getGymHall().getOpenTime()
        if self.__workStart <= start or self.__workEnd >= end:
            raise Exception("Trainer work time is incompatible with hall's open time")
        self.__workStart = workStart
        self.__workEnd = workEnd

    def getWorkTimes(self):
        return (self.__workStart, self.__workEnd)

    def getAssignments(self):
        return self.__assignments.__iter__()

    def assignToCustomer(self, start: int, end: int):
        if not self.checkAvailability(start, end):
            return False
        self.__assignments.append((start, end))
        return True
    
    def checkAvailability(self, start: int, end: int):
        if start <= self.__workStart or end >= self.__workEnd:
            return False
        for assignment in self.__assignments:
            if assignment[0] <= end and assignment[1] >= start:
                return False
        return True

    def clearAssignment(self, start: int, end: int):
        self.__assignments.remove((start, end))


class ExercisePlanItem(Model):
    def __init__(self, equipment: Equipment, duration: int, steps: list):
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
        return self.__planItems.__iter__()

    def getTrainer(self):
        return self.__trainer

    def getGymHall(self):
        return self.__trainer.getGymHall()


class GymHall(eModel):
    def __init__(self, id: int, name: str):
        super().__init__(id, name)
        self.__trainers = []
        self.__openStart = int()
        self.__openEnd = int()
        self.__equipments = []
        self.__exercisePlans = []

    def addTrainer(self, trainer: Trainer):
        self.__trainers.append(trainer)
        trainer.setGymHall(self)

    def removeTrainer(self, trainer: Trainer):
        self.__trainers.remove(trainer)
        trainer.setGymHall(None)

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
        equipement.setHall(self)

    def removeEquipment(self, equipment: Equipment):
        self.__equipments.remove(equipment)
        equipment.setHall(None)

    def getAllEquipments(self):
        return self.__equipments.__iter__()

    def addExercisePlan(self, plan: ExercisePlan):
        self.__exercisePlans.append(plan)

    def removeExercisePlan(self, plan: ExercisePlan):
        self.__exercisePlans.remove(plan)

    def getAllExercisePlans(self):
        return self.__exercisePlans.__iter__()


class Subscription(Model):
    def __init__(self, id: int, plan: ExercisePlan, reservationDate: datetime, dailyStart: int, dailyEnd: int):
        super().__init__(id)
        self.__plan = plan
        self.__reservationDate = reservationDate
        self.__dailyStart = dailyStart
        self.__dailyEnd = dailyEnd

    def getHall(self):
        return self.getTrainer().getGymHall()

    def getTrainer(self):
        return self.__plan.getTrainer()

    def getExercisePlan(self):
        return self.__plan

    def getReservationTime(self):
        return self.__reservationDate

    def getDailyTime(self):
        return (self.__dailyStart, self.__dailyEnd)


class Customer(eModel):
    def __init__(self, id: int, name: str):
        super().__init__(id, name)
        self.__subscriptions = []

    def subscribe(self, subscription: Subscription):
        self.__subscriptions.append(subscription)

    def cancelSubscribtion(self, subscription: Subscription):
        self.__subscriptions.remove(subscription)

    def getSubscribtions(self):
        return self.__subscriptions.__iter__()
