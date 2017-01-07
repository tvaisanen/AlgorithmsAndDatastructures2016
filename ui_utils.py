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

def print_menu():
    print("\nPrint:")
    print("[1] Agencies")
    print("[2] Customers")
    print("[3] Drivers")
    print("[4] Travels")
    print("[0] Back")
    return menu_input()


def print_actions_loop():
    """
    loop for handling list printing
    :return: None
    """
    while True:
        action = print_menu()

        if action == 0:
            break
        elif action == 1:
            data.agencies.print_list()
        elif action == 2:
            data.customers.print_inorder()
        elif action == 3:
            data.drivers.print_inorder()
        elif action == 4:
            data.travels.print_list()
        else:
            pass

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