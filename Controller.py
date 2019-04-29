from Models import Trainer, GymHall, ExercisePlan, ExercisePlanItem, Customer, datetime, Subscription


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
        hall = GymHall(len(self.__halls), name)
        self.__halls.append(hall)
        return hall

    def createPlan(self, trainer: Trainer, equipment: list, duration: list, steps: list) -> ExercisePlan:
        ExerciseItem = []
        for i in range(len(equipment)):
            ExerciseItem.append(ExercisePlanItem(equipment[i], duration[i], steps[i]))
        Plan = ExercisePlan(len(trainer.getGymHall().getAllExercisePlans()), ExerciseItem, trainer)
        trainer.addExercisePlan(Plan)
        return Plan

    def createTrainer(self, name: str, workStart: int, workEnd: int, hall: GymHall) -> Trainer:
        trainer = Trainer(len(hall.getTrainers()), name, workStart, workStart)
        trainer.setGymHall(hall)
        hall.addTrainer(trainer)
        return trainer

    def createCustomer(self, name: str) -> Customer:
        customer = Customer(len(self.__customers), name)
        self.__customers.append(customer)
        return customer

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

    def checkAvailability(self, plan: ExercisePlan, start: int, end: int) -> bool:
        if not plan.getTrainer().checkAvailability(start, end):
            return False
        for item in plan.getPlanItems():
            if not item.getEquipment().checkAvailability(start, end):
                return False
        return True
