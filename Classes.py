import os
import os.path
from linkedlist import *
from bst import *
from time import strptime
from settings import DATE_FORMAT


class Customer(object):
    def __init__(self, id=0, name='', address='', phone=''):
        self.id = id
        self.name = name.replace('\t', '')
        self.address = address.replace('\t', '')
        self.phone = phone.replace('\t', '')

    def __str__(self):
        return '%5d\t %10s\t %10s\t %10s\n' % \
              (self.id, self.name, self.address, self.phone)


class Driver(object):
    def __init__(self, id=0, agency_id='', name='', date_hired='', car_model='', travels=None):
        self.id = id
        self.name = name
        self.carModel = car_model
        self.travels = travels
        self.date_hired = strptime(date_hired, DATE_FORMAT)


    def __str__(self):
        date = "%d.%d.%d" % (self.date_hired.tm_year, self.date_hired.tm_mon, self.date_hired.tm_mday)
        return '%5d\t %10s\t %10s\t %10s travels: %s\n' % \
              (self.id, self.name, date, self.carModel, self.travels.count)

    def get_date_hired_str(self):
        return "%d.%d.%d" % (self.date_hired.tm_year, self.date_hired.tm_mon, self.date_hired.tm_mday)

class Travel(object):
    def __init__(self,
                 id=0,
                 driver_id='',
                 date='',
                 time='',
                 customer_id=0,
                 source='',
                 destination='',
                 amount=0.0):
        self.id = id
        self.driver_id = driver_id
        self.date = strptime(date, '%Y.%m.%d')
        self.time = strptime(time, '%H:%M')  # in hour:min format
        self.customer_id = int(customer_id)
        self.source = source
        self.destination = destination
        self.amount = amount

    def date_str(self):
        return "%d.%d.%d" % (self.date.tm_year, self.date.tm_mon, self.date.tm_mday)

    def __str__(self):
        # format date and time for printing
        date = "%d.%d.%d" % (self.date.tm_year, self. date.tm_mon, self.date.tm_mday)
        time = "%d:%d" % (self.time.tm_hour, self.time.tm_min)
        return "Id: %d\tdriver: %s\tcustomer: %s\tdate/time: %s / %s\tfrom: %s\tto: %s" \
               % (self.id, self.driver_id, self.customer_id, date, time, self.source, self.destination)

    def __lt__(self, other):
        if self.date < other.date and self.time < other.time:
            return True
        else:
            return False

    def __gt__(self, other):
        if self.date > other.date and self.time > other.time:
            return True
        else:
            return False


class Agency(object):

    def __init__(self, id=0, name='', date_reg='', staff_count=0, manager_name=''):
        self.id = id
        self.name = name
        self.regDate = date_reg
        self.staffCount = staff_count
        self.managerName = manager_name

    def print(self):
        print('%5d\t %10s\t %10s\t %6d\t %10s\n' % \
              (self.id, self.name, self.regDate, self.staffCount, self.managerName))

    def __str__(self):
        return '%5d\t %10s\t %10s\t %6d\t %10s\n' % \
              (self.id, self.name, self.regDate, self.staffCount, self.managerName)



# Agencies Linked List.
# Modify or implement accordingly

class Agencies(LinkedList):
    def __init__(self):
        # super(LinkedList, self).__init__()
        self.head = LinkedList.head
        if not os.path.exists('agencies.txt'):
            f = open('agencies.txt', 'w')
            f.close()
        self.Load()

    def Load(self):
        f = open('agencies.txt', 'r')
        c = None
        try:
            for line in f.readlines():
                data = line.replace('\n', '').split('\t')
                if len(data) > 1:
                    # clean up readed data
                    id = int(data[0])
                    name = data[1].replace('\t', '')
                    date_reg = data[2].replace('\t', '')
                    staff_count = int(data[3])
                    manager_name = data[4].replace('\t', '')

                    agency = Agency(id=id,
                                    name=name,
                                    date_reg=date_reg,
                                    staff_count=staff_count,
                                    manager_name=manager_name)

                    self.list_insert(agency)

        except Exception as ex:
            logger.info("exception with loading data from agencies.txt")
            logger.info(str(ex))

        f.close()


    def print_list(self):
        print('%5s\t %10s\t %10s\t %6s\t %10s\n' % ('ID', 'Name', 'RegDate', '#Staff', 'Manager'))
        node = self.head
        while node is not None:
            node.data.print()
            node = node.next

    # Required implementations
    def findById(self, id):
        return self.search_key_of_T(id, "id")

    def findByName(self, name):
        return self.search_key_of_T(id, "name")

    # -------------------------------------------- #

    # extra methods that you might need
    def methodName(self, pars):
        pass


# implement classes
class Customers(BST):

    def __init__(self):
        self.root = BST.root
        self.count = 0
        self.load()

    def load(self):
        f = open('customers.txt', 'r')
        c = None
        try:
            for line in f.readlines():
                data = line.replace('\n', '').split('\t')
                if len(data) > 1:
                    id = int(data[0])
                    name = data[1]
                    address = data[2]
                    phone = data[3]
                    customer = Customer(id=id,
                                        name=name,
                                        address=address,
                                        phone=phone)
                    self.bst_insert(customer)
            f.close()
        except Exception as ex:
            logger.critical(str(ex))

    def print_node(self, node):
        print(node.data)




class Drivers(BST):
    def __init__(self):
        self.head = BST.root
        self.count = 0
        if not os.path.exists('drivers.txt'):
            f = open('drivers.txt', 'w')
            f.close()

    # for now when loading drivers we must have travel information already
    def Load(self, travels):
        f = open('drivers.txt', 'r')
        c = None
        try:
            for line in f.readlines():
                data = line.replace('\n', '').split('\t')
                if len(data) > 1:
                    driver_id = int(data[0])
                    agency_id = int(data[1])
                    driver_name = data[2].replace('\t', '')
                    date_hired = data[3].replace('\t', '')
                    car_model = data[4].replace('\t', '')
                    travels_for_driver = self.load_travels(driver_id, travels)
                    driver = Driver(
                                    id=driver_id,
                                    agency_id=agency_id,
                                    name=driver_name,
                                    date_hired=date_hired,
                                    car_model=car_model,
                                    travels=travels_for_driver
                                )
                    self.bst_insert(driver)
        except Exception as ex:
            logger.critical(str(ex))

        f.close()

    def load_travels(self, id, travels):
        """
        This is just a wrapper to general search method of linkedlist
        :param id:
        :param travels:
        :return:
        """
        return travels.get_subset_list(id, 'driver_id')

    def print_list(self):
        print('%5s\t %10s %10s\t %10s\t %6s\n' % ('ID', 'Agency', 'Name', 'hireDate', 'carModel'))
        node = self.head
        while node is not None:
            print(node.data)
            node = node.next

    # Implement
    def find_by_id(self, id):
        return self.search_key_of_T(id, "id")

    def find_by_name(self, name):
        return self.search_key_of_T(id, "name")


class Travels(LinkedList):
    def __init__(self):
        self.root = LinkedList.head
        if not os.path.exists('travels.txt'):
            f = open('travels.txt', 'w')
            f.close()
        self.Load()

    def Load(self):
        f = open('travels.txt', 'r')
        c = None
        for line in f.readlines():
            data = line.replace('\n', '').split('\t')
            try:
                if len(data) > 1:
                    id = int(data[0])
                    driver_id = int(data[1].replace('\t', ''))
                    date, time = data[2].split(' ')
                    customer_id = int(data[3])
                    source = data[4].replace('\t', '')
                    destination = data[5].replace('\t', '')
                    amount = float(data[6])
                    travel = Travel(id=id,
                                    driver_id=driver_id,
                                    date=date,
                                    time=time,
                                    customer_id=customer_id,
                                    source=source,
                                    destination=destination,
                                    amount=amount
                                    )
                    self.list_insert(travel)
            except Exception as ex:
                logger.debug(str(ex))
        f.close()


