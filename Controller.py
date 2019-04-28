import Models


class Controller():
    def __init__(self):
        self.__halls = []
        self.__equipments = []
        self.__customers = []

    def readFromFile(self, fileName):
        pass

    def writeToFile(self, fileName):
        pass

    def getAllHalls(self):
        pass

    def getAllTrainersInHall(self, hall: Models.GymHall):
        pass

    def getAllEquipmentsInHall(self, hall: Models.GymHall):
        pass

    def getAllPlansOfTrainer(self, trainer: Models.Trainer):
        pass

    def createHall(self, name: str) -> Models.GymHall:
        pass

    def createPlan(self, trainer: Models.Trainer, equipment: list, duration: list, steps: list) -> Models.ExercisePlan:
        pass

    def createTrainer(self, name: str, workStart: int, workEnd: int, hall: Models.GymHall):
        pass

    def createCustomer(self, name: str):
        pass

    def subscribeCustomer(self, customer: Models.Customer, plan: Models.ExercisePlan,
                                dailyStart: int, dailyEnd: int, reservationDate: Models.datetime) -> bool:
        if not self.checkAvailability(plan, dailyStart, dailyEnd):
            return False
        plan.getTrainer().assignToCustomer(dailyStart, dailyEnd)
        for item in plan.getPlanItems():
            for equipment in item.getEquipment():
                equipment.reserveEquipment(dailyStart, dailyEnd)
        subscription = Models.Subscription(len(customer.getSubscribtions()), plan, reservationDate, dailyStart, dailyEnd)
        customer.subscribe(subscription)

    def getSubscribtionsOfCustomer(self, customer: Models.Customer):
        pass

    def checkAvailability(self, plan: Models.ExercisePlan, start: int, end: int):
        if not plan.getTrainer().checkAvailability(start, end):
            return False
        for item in plan.getPlanItems():
            for equipment in item.getEquipment():
                if not equipment.checkAvailability(start, end):
                    return False
        return True
