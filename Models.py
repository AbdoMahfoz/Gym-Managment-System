from datetime import datetime, timedelta
from abc import ABC
from abc import abstractmethod

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
        self.__subscribtions = []
        self.__excersiePlans = []

    def setGymHall(self, hall):
        start, end = hall.getOpenTime()
        if self.__workStart <= start or self.__workEnd >= end:
            raise Exception("Trainer work time is incompatible with hall's open time")
        self.__hall = hall

    def getGymHall(self):
        return self.__hall

    def setWorkTimes(self, workStart: int, workEnd: int):
        start, end = self.getGymHall().getOpenTime()
        if workStart <= start or workEnd >= end:
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
    
    def addSubscribtion(self, subscription):
        self.__subscribtions.append(subscription)

    def removeSubscribtion(self, subscription):
        self.__subscribtions.remove(subscription)

    def getAllSubscribtions(self):
        return self.__subscribtions.__iter__()
    
    def checkAvailability(self, start: int, end: int):
        if start <= self.__workStart or end >= self.__workEnd:
            return False
        for assignment in self.__assignments:
            if assignment[0] <= end and assignment[1] >= start:
                return False
        return True

    def clearAssignment(self, start: int, end: int):
        self.__assignments.remove((start, end))

    def addExercisePlan(self, plan):
        self.__excersiePlans.append(plan)

    def getAllExcercisePlans(self):
        return self.__excersiePlans.__iter__()

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

    def getTotalDuration(self):
        res = 0
        for item in self.__planItems:
            res = res + item.getDuration()
        return res

class GymHall(eModel):
    def __init__(self, id: int, name: str):
        super().__init__(id, name)
        self.__trainers = []
        self.__openStart = int()
        self.__openEnd = int()
        self.__equipments = []

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

    def getAllExercisePlans(self):
        res = []
        for trainer in self.__trainers:
            res.extend(trainer.getAllExcercisePlans())
        return res.__iter__()


class SubscriptionType(ABC):
    @abstractmethod
    def checkExpiration(self, reservationDate: datetime):
        pass

class SilverSubscription(SubscriptionType):
    def checkExpiration(self, reservationDate: datetime):
        if (datetime.now() - reservationDate) >= timedelta(days=30):
            return False
        return True

class GoldSubscription(SubscriptionType):
    def checkExpiration(self, reservationDate: datetime):
        if (datetime.now() - reservationDate) >= timedelta(days=45):
            return False
        return True

class SubscriptionTypeFactory():
    def create(self, subscriptionType: str) -> SubscriptionType:
        if subscriptionType == "gold":
            return GoldSubscription()
        elif subscriptionType == "silver":
            return SilverSubscription()
        else:
            raise Exception("Invalid selection, only available two options are gold and silver")

class SubscriptionState(ABC):
    @abstractmethod
    def getHall(self, hall):
        pass

    @abstractmethod
    def getTrainer(self, trainer):
        pass
    
    @abstractmethod
    def getExercisePlan(self, plan):
        pass

    @abstractmethod
    def getReservationTime(self, reservationDate):
        pass

    @abstractmethod
    def getDailyTime(self, dailyStart, dailyEnd):
        pass

class ActiveSubscription(SubscriptionState):
    def getHall(self, hall):
        return hall
    
    def getDailyTime(self, dailyStart, dailyEnd):
        return (dailyStart, dailyEnd)
    
    def getExercisePlan(self, plan):
        return plan
    
    def getReservationTime(self, reservationDate):
        return reservationDate

    def getTrainer(self, trainer):
        return trainer

class ExpiredSubscription(SubscriptionState):
    def getHall(self, hall):
        return None
    
    def getDailyTime(self, dailyStart, dailyEnd):
        return None
    
    def getExercisePlan(self, plan):
        return None
    
    def getReservationTime(self, reservationDate):
        return None

    def getTrainer(self, trainer):
        return None

class Subscription(Model):
    def __init__(self, id: int, subscriptionType: SubscriptionType, plan: ExercisePlan,
                                reservationDate: datetime, dailyStart: int, dailyEnd: int):
        super().__init__(id)
        self.__state = ActiveSubscription()
        self.__subscriptionType = subscriptionType
        self.__plan = plan
        self.__reservationDate = reservationDate
        self.__dailyStart = dailyStart
        self.__dailyEnd = dailyEnd

    def validateExpiration(self):
        if type(self.__state) == type(ExpiredSubscription()):
            return False
        if not self.__subscriptionType.checkExpiration(self.__reservationDate):
            self.clearSubscription()
            return False
        return True

    def clearSubscription(self):
        self.__plan.getTrainer().clearAssignment(self.__dailyStart, self.__dailyEnd)
        for equipment in self.__plan.getPlanItems():
            equipment.getEquipment().clearReservation(self.__dailyStart, self.__dailyEnd)
        self.__state = ExpiredSubscription()

    def getHall(self):
        return self.__state.getHall(self.__plan.getGymHall())

    def getTrainer(self):
        return self.__state.getTrainer(self.__plan.getTrainer())

    def getExercisePlan(self):
        return self.__state.getExercisePlan(self.__plan)

    def getReservationTime(self):
        return self.__state.getReservationTime(self.__reservationDate)

    def getDailyTime(self):
        return self.__state.getDailyTime(self.__dailyStart, self.__dailyEnd)

class Customer(eModel):
    def __init__(self, id: int, name: str, email: str):
        super().__init__(id, name)
        self.__subscriptions = []
        self.__email = email

    def subscribe(self, subscription: Subscription):
        self.__subscriptions.append(subscription)

    def notify(self, office: str):
        #Email SMTP mn ra4ad
        pass

    def cancelSubscribtion(self, subscription: Subscription):
        self.__subscriptions.remove(subscription)

    def getEmail(self):
        return self.__email

    def setEmail(self, email):
        self.__email = email

    def getSubscribtions(self):
        return self.__subscriptions.__iter__()

class Offers():
    def __init__(self):
        self.__observers = []
        self.__offers = []

    def addOffer(self, offer: str):
        self.__offers.append(offer)
        for observer in self.__observers:
            observer.notify(offer)

    def addObserver(self, observer: Customer):
        self.__observers.append(observer)
        
    def removeOffer(self, offer: str):
        self.__offers.remove(offer)

    def getOffers(self):
        return self.__offers.__iter__()

    def getObservers(self):
        return self.__observers.__iter__()

class Admin():
    __instance = None
    __admins = []

    def __init__(self, userName: str, password: str):
        if not (Admin.__instance is None):
            raise Exception("An instance is already created")
        Admin.__instance = self
        self.__userName = userName
        self.__password = password

    def getUsername(self):
        return self.__userName

    def getPassword(self):
        return self.__password

    @staticmethod
    def fill(admins):
        Admin.__admins.extend(admins)

    @staticmethod
    def get():
        return Admin.__instance
    
    @staticmethod
    def login(userName: str, password: str):
        for admin in Admin.__admins:
            if admin == (userName, password):
                return Admin(userName, password)
        return None
