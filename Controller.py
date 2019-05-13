from Models import Trainer, GymHall, ExercisePlan, ExercisePlanItem, Customer, datetime
from Models import Subscription, SubscriptionType, SubscriptionTypeFactory, Equipment

class Controller():
    def __init__(self):
        self.__halls = []
        self.__customers = []

    def readFromFile(self, fileName: str):
        pass
        # try:
        #     file = open(fileName, "r")
        #     for line in file:
        #         for tokens in line.split(' '):
        #             pass
        # except:
        #     pass

    def writeToFile(self, fileName: str):
        return
        # trainers = []
        # equipment = []
        # for hall in self.__halls:
        #     trainers.extend(hall.getTrainers())
        #     equipment.extend(hall.getAllEquipments())
        # file = open(fileName, "w")
        # for hall in self.__halls:
        #     hallStart, hallFinish = hall.getOpenTime()
        #     file.write("{0} {1} {2} {3}\n".format(str(hall.getId()), hall.getName(), str(hallStart), str(hallFinish)))
        #     file.write("{0}\n".format(len(hall.getTrainers())))
        #     for trainer in hall.getTrainers():
        #         file.write()
        # file.write("customers\n")
        # for customer in self.__customers:
        #     file.write("{0} {1}\n".format(str(customer.getId()), str(customer.getName())))
        #     for sub in customer.getSubscribtions():
        #         file.write("{0}\n".format(sub.getId()))
        #     file.write("\n")
        
    def validateSubscriptions(self):
        for cust in self.__customers:
            for sub in cust.getSubscribtions():
                if not sub.validateExpiration():
                    cust.cancelSubscribtion(sub)

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
        trainer = Trainer(len(hall.getTrainers()), name, workStart, workEnd)
        trainer.setGymHall(hall)
        hall.addTrainer(trainer)
        return trainer

    def createCustomer(self, name: str, email: str) -> Customer:
        customer = Customer(len(self.__customers), name, email)
        self.__customers.append(customer)
        return customer

    def createEquipment(self, name: str, hall: GymHall):
        hall.addEquipment(Equipment(len(hall.getAllEquipments()), name))

    def deleteCustomer(self, customer: Customer):
        for sub in customer.getSubscribtions():
            sub.clearSubscription()
        self.__customers.remove(customer)

    def deleteHall(self, hall: GymHall):
        self.__halls.remove(hall)

    def cancelSubscribtion(self, customer: Customer, subscription: Subscription):
        subscription.clearSubscription()
        customer.cancelSubscribtion(subscription)

    def subscribeCustomer(self, customer: Customer, plan: ExercisePlan, subscriptionType: str,
                                dailyStart: int, dailyEnd: int, reservationDate: datetime) -> bool:
        if not self.checkAvailability(plan, dailyStart, dailyEnd):
            return False
        plan.getTrainer().assignToCustomer(dailyStart, dailyEnd)
        for item in plan.getPlanItems():
            item.getEquipment().reserveEquipment(dailyStart, dailyEnd)
        subscription = Subscription(len(customer.getSubscribtions()), plan, SubscriptionTypeFactory().create(subscriptionType),
                                    reservationDate, dailyStart, dailyEnd)
        customer.subscribe(subscription)
        plan.getTrainer().addSubscribtion(subscription)

    def checkAvailability(self, plan: ExercisePlan, start: int, end: int) -> bool:
        if plan.getTotalDuration() != (end - start):
            raise Exception(f"selected excersie plan requires {plan.getTotalDuration()} minutes, given interval is {end - start}")
        if not plan.getTrainer().checkAvailability(start, end):
            return False
        for item in plan.getPlanItems():
            duration = duration + item.getDuration()
            if not item.getEquipment().checkAvailability(start, end):
                return False
        return True
