class Vehicle:
    def __init__(self, name, car_type, power, cost):
        self.name = name
        self.car_type = car_type
        self.power = power
        self.cost = cost
    def description(self):
        desc_str = "The " + self.name + " is a(n) " + self.car_type + " with " + str(self.power) + "hp and costs $" + str(self.cost) + "."
        return desc_str

car1 = Vehicle("Merc E 330", "sedan", 400, 40000)
car2 = Vehicle("Caterham A5", "sports car", 700, 75000)

choice = input("Model Name: ")

if choice == car1.name:
    print(car1.description())
elif choice == car2.name:
    print(car2.description())
else:
    print("That car is not registered in the system")