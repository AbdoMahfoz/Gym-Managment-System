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

    def subscribeCustomer(self, customer: Models.Customer, plan: Models.ExercisePlan) -> bool:
        pass

    def getSubscribtionsOfCustomer(self, customer: Models.Customer):
        pass

    def checkAvailability(self, trainer: Models.Trainer, plan: Models.ExercisePlan, start: int, end: int):
        pass
