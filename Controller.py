from Models import Trainer, GymHall, ExercisePlan, Customer, datetime, Subscription


class Controller():
    def __init__(self):
        self.__halls = []
        self.__customers = []

    def readFromFile(self, fileName):
        pass

    def writeToFile(self, fileName):
        pass

    def getAllHalls(self):
        return self.__halls.__iter__()

    def getAllCustomers(self):
        return self.__customers.__iter__()

    def createHall(self, name: str) -> GymHall:
        pass

    def createPlan(self, trainer: Trainer, equipment: list, duration: list, steps: list) -> ExercisePlan:
        pass

    def createTrainer(self, name: str, workStart: int, workEnd: int, hall: GymHall) -> Trainer:
        pass

    def createCustomer(self, name: str) -> Customer:
        pass

    def subscribeCustomer(self, customer: Customer, plan: ExercisePlan,
                                dailyStart: int, dailyEnd: int, reservationDate: datetime) -> bool:
        if not self.checkAvailability(plan, dailyStart, dailyEnd):
            return False
        plan.getTrainer().assignToCustomer(dailyStart, dailyEnd)
        for item in plan.getPlanItems():
            item.getEquipment().reserveEquipment(dailyStart, dailyEnd)
        subscription = Subscription(len(customer.getSubscribtions()), plan, reservationDate, dailyStart, dailyEnd)
        customer.subscribe(subscription)
        plan.getTrainer().addSubscribtion(subscription)

    def getSubscribtionsOfCustomer(self, customer: Customer):
        pass

    def checkAvailability(self, plan: ExercisePlan, start: int, end: int) -> bool:
        if not plan.getTrainer().checkAvailability(start, end):
            return False
        for item in plan.getPlanItems():
            if not item.getEquipment().checkAvailability(start, end):
                return False
        return True
