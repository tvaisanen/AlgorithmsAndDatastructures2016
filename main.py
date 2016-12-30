from data import Data
from settings import logging_level
from Classes import *
import re
import os, sys

logging.basicConfig(level=logging_level)
logger = logging.getLogger(__name__)

# RUN TESTS EVERY TIME

try:
    os.system("py.test")
except Exception as ex:
    logger.info("No testfiles in current directory.")

# ========================================================= #

data = Data()

def menu():
    """
    :return: return menu input
    """
    print("\n[1] Search agency")
    print("[2] Search driver")
    print("[3] Search customer")
    print("[4] Do something with travel information")
    print("[5] Additional functions")
    print("[0] EXIT\n")

    return menu_input()


def functions_menu():
    """
    :return: return menu input
    """
    print("\n[1] Customers travels")
    print("[2] Clients between dates")
    print("[3] Find drivers by customer")

    return menu_input()

def travel_menu():
    """
    :return: return menu input
    """
    print("\n[1] Search travel")
    print("[2] Add travel")
    print("[3] Delete travel")
    print("[0] Back")

    return menu_input()


def inserted_int(x):
    """
    :param x: checks can user input interpreted as int for deciding
              whether to search by id or name
    :return:  bool
    """
    try:
        return isinstance(int(x), int)
    except Exception as ex:
        return False

def menu_input():
    """
    Reads menu input from user.
    Accepts only integers.
    Integer validation must be handled by the caller
    :return: Integer inputted by user.
    """
    while True:
        try:
            return int(input(">>> "))
        except Exception as ex:
            print("invalid action, try again!")


def search(from_where, keyword, search_by='id', order_by='id', search_all=False):
    """
    "interface" for searching, user doesn't need to know anything about classes...
    :param from_where: defines from where
    :param keyword: defines what
    :param order_by: ordering by
    :return: results as a list
    """

    list_types = (Agencies, Travels)
    bst_types = (Customers, Drivers)
    is_linked_list = isinstance(from_where, list_types)
    is_bst = isinstance(from_where, bst_types)
    searching_int = inserted_int(keyword)

    logger.info("search: %s, %s as type: %s " % (search_by, keyword, type(keyword)))
    logger.info("from %s" % type(from_where))

    if searching_int:
        keyword = int(keyword)

    matching_to = search_by

    if search_all:
        results = from_where.search_all_key_of_T(keyword, T=matching_to)
    else:
        results = from_where.search_key_of_T(keyword, T=matching_to)

    logger.info(results)

    try:
        result_count = len(results[0])
        result_type = type(results[0])
    except Exception as ex:
        if results is not None:
            result_count = 1
            result_type = type(results)
        logger.info(str(ex))

    logger.info(" Found %d results." % result_count)
    logger.info(" Type of result objects: %s." % result_type)

    print("search results: ")
    try:
        print(results)
    except IndexError as ie:
        for result in results:
            print(result)
    except Exception as ex:
        logger.info(" Something went wrong?")
        logger.info(str(ex))

    return results

def input_int():
    while True:
        try:
            x = input("\n>>>")
            x = int(x)
            return x
        except Exception as ex:
            print("Invalid input, try again!")

def input_float():
    while True:
        try:
            x = input("\n>>>")
            x = float(x)
            return x
        except Exception as ex:
            print("Invalid input, try again!")

def input_date():
    print("Give date in format 'YYYY.DD.MM'")
    while True:
        try:
            date = input("\n>>>")
            if re.match(r'^\d{4}\.\d{2}\.\d{2}', date):
                return date
            else:
                raise Exception
        except Exception as ex:
            logger.info("\t" + str(ex))
            print("Invalid input, try again!")

def input_time():
    print("Give date in format 'HH:MM'")
    while True:
        try:
            time = input("\n>>>")
            if re.match(r'^\d{2}\:\d{2}', time):
                return time
            else:
                raise Exception
        except Exception as ex:
            logger.info("\t"+str(ex))
            print("Invalid input, try again!")


def add_travel():
    print("Add a new travel:")
    print("ID:")
    id = input_int()
    print("Driver ID:")
    driver_id = input_int()
    print("Customer ID:")
    customer_id = input_int()
    print("Date:")
    date = input_date()
    print("Time:")
    time = input_time()
    print("Location of departure:")
    source = input()
    print("Destination:")
    destination = input(),
    print("Price:")
    amount = input_float()
    travel = Travel(id=id, driver_id=driver_id, date=date, time=time, customer_id=customer_id,
                    source=source, destination=destination, amount=amount)
    driver = search(data.drivers, driver_id)
    # insert newly created travel also to drivers list, so
    # there's no need to traverse whole list for updating drivers list
    driver.travels.list_insert(travel)
    data.travels.list_insert(travel)


def search_all_by_obj(where, keyword, order_by='id'):
    """
    "interface" for searching, user doesn't need to know anything about classes...
    :param where: defines from where
    :param what: defines what
    :param order_by: ordering by
    :return: results as a list
    """

    logger.info("searching all by object instead of obj parameter\n")
    results = where.search_all_key_of_T(keyword)
    print(results)
    return results


def travel_actions_loop():
    """
    loop for handling travel actions: adding, deleting and searching
    :return: None
    """
    while True:
        action = travel_menu()
        if action == 0:
            break
        elif action == 1:
            keyword = input("Search customers travels:\n>>>")
            customer = search(data.customers, keyword)
            logger.info("found customer: %s" % customer)
            results = search(data.travels, keyword=customer.id, search_by='customer_id', search_all=True)
            results.sort(key=lambda x: x.date, reverse=True)
            logger.info(" returned results:")
            for i in results:
                print(i)
        elif action == 2:
            add_travel()
        elif action == 3:
            pass




def menu_loop():
    run = True
    while run:
        action = menu()

        if action == 1:
            print("search agency")
            where_to_search = data.agencies
        elif action == 2:
            print("search driver")
            where_to_search = data.drivers
        elif action == 3:
            print("search customer")
            where_to_search = data.customers


        if action == 0:
            print("\nExiting program...")
            run = False
        elif action == 4:
            travel_actions_loop()
        elif action == 5:
            functions_menu()
        elif action > 5:
            print("invalid action, try again!")
        else:
            keyword = input("Search: ")
            search(where_to_search, keyword)


def start_app():
    print("\nHELLO THERE! WHAT DO YOU WANT TO DO?")
    menu_loop()


if __name__ == '__main__':

    logger.info("\nStarting application")
    start_app()

    # TODO: KORJAA, Tää meni rikki ku siivosin nuita vitun parsesiivoushässäköitä tuolta konstruktoreista
    # TODO: ns. Palveluoperaatiot, asiakkaan matkat, asiakkaat päivämääriltä, asiakasta palvelleet kuljettajat

    """

    Funktio, joka muodostaa listan asiakkaista, jotka ovat hankkineet palveluita annettujen
    päivämäärien välisenä aikana.
    - timedeltaaa

    Funktio, joka muodostaa listan kuljettajista, jotka ovat palvelleet annettua asiakasta
    (tunnistetaan asiakastunnuksen perusteella). Kuljettajat listataan järjestyksessä nimen
    perusteella.
    """







