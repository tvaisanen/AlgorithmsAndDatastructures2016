
from Classes import *


class Data:

    def __init__(self):
        self.load_data()

    def load_data(self):

        print("\nInitializing data...\n")

        try:
            self.agencies = Agencies()
            # self.agencies.print_list()
            print("\u2713\tAgencies linked list")
        except Exception as ex:
            logger.debug(str(ex))
            print("\u2718\tAgencies linked list")

        try:
            self.travels = Travels()
            # self.travels.print_list()
            print("\u2713\tTravels linked list")
        except Exception as ex:
            logger.debug(str(ex))
            print("\u2718\tTravels linked list")

        try:
            self.drivers = Drivers()
            self.drivers.Load(self.travels)
            # self.drivers.print_inorder()
            print("\u2713\tDrivers linked list")
        except Exception as ex:
            logger.debug(str(ex))
            print("\u2718\tDrivers linked list")

        try:
            self.customers = Customers()
            # self.customers.print_inorder()
            print("\u2713\tCustomers binary search tree")
        except Exception as ex:
            logger.debug(str(ex))
            print("\u2718\tCustomers binary search tree")