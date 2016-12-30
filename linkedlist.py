import logging
from settings import logging_level

logging.basicConfig(level=logging_level)
logger = logging.getLogger(__name__)

# Implementation of linked list

# Node in the lis
class Node(object):
    data = None
    next = None

    def __init__(self, d, n=None):
        self.data = d
        self.next = n

    def __str__(self):
        return "data: %s" % self.data


# The list: its head
class LinkedList(object):
    head = None
    count = 0

    # Inserts a key into list
    # inserted to head
    def list_insert(self, key):
        self.count += 1
        n = Node(key)
        n.data = key
        n.next = self.head
        self.head = n

    def __str__(self):
        self.print_list()

    # more generic search which allows subclass
    # to specify what kind of parameter we're searching
    def search_key_of_T(self, key, T):
        logger.info("search: %s: %s" %(T, key))
        node = self.head
        found = False

        data = None

        searching_string = isinstance(key, str)

        # handle upper-lower case collisions
        if searching_string:
            key = key.lower()

        while (node is not None) and (not found):
            data = node.__dict__['data']

            logger.info("\nLinkedList data:")
            logger.info(data.__dict__)
            logger.info("\n")

            matching_to = data.__dict__[T]  # use the original data type of instance

            if searching_string:
                matching_to.lower()

            if matching_to == key:
                found = True
                return data
            else:
                node = node.next
                data = None

        return data

    def search_all_key_of_T(self, key, T=None):
        """
        :param key: What we are looking for
        :param T:  To what we are comparing the key we are looking for
        :return: array of data objects, no node elements
        """
        node = self.head

        logger.info(" method: search_all_key_of_T()")
        logger.info(" search keyword: %s as type %s" % (str(key), type(key)))
        logger.info(" searching from data type:")
        logger.info(node.__dict__['data'])



        results = []

        while node is not None:
            data = node.__dict__['data']

            # this allows search by object itself instead of searching by objects parameter
            if T is None:
                matching_to = data
            else:
                matching_to = data.__dict__[T]

            if matching_to == key:
                results.append(node.data)

            node = node.next

        return results

    def get_subset_list(self, key, T):
        """
        :param key: subset of elements containing the key
        :param T:  element id to compare key
        :return: search results as a linked list, this is not a real copy
        """
        node = self.head
        results = LinkedList()
        key = str(key)

        while node is not None:
            try:
                data = node.__dict__['data']
                matching_to = str(data.__dict__[T])

                if matching_to == key:
                    results.list_insert(node)

                node = node.next
            except Exception as ex:
                logger.critical(str(ex))
        return results

    # Searches and returns a node with
    # the given key
    def search(self, key):
        node = self.head
        found = False

        while node is not None and not found:
            if node.data == key:
                found = True
            else:
                node = node.next

        return node



    # Searches and removes a node with
    # the given key
    def list_remove(self, key):
        node = self.search(key)

        if node is not None:
            self.count -= 1
            # Check if head node deleted
            if node == self.head:
                self.head = node.next
            else:
                # Find predecessor
                pred = self.head

                while pred.next != node:
                    pred = pred.next

                pred.next = node.next;

    # Prints node by taking print_node() from subclass


    # Prints list starting from head
    def print_list(self):
        node = self.head
        while node is not None:
            print(node.data)
            node = node.next;



    def get_count(self):
        return self.count




