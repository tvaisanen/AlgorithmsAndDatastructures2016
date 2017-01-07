import logging
from settings import LOGGING_LEVEL, DATE_FORMAT
from time import strptime

# Implementation of binary search tree


logging.basicConfig(level=LOGGING_LEVEL)
logger = logging.getLogger(__name__)

# Node in the tree
class BSTNode:
    data = None
    left = None
    right = None
    parent = None
    count = 0

    def __init__(self, d, p=None, l=None, r=None):
        self.data = d
        self.parent = p
        self.left = l
        self.right = r
        self.count += 1

    def print(self):
        print(self.data)

    def __str__(self):
        return "data: %" % self.data


# The tree: its root
class BST(object):
    root = None

    # Minimum and maximum values of tre
    def bst_min(self):
        x = self.root
        if x == None:
            return None

        while x.left != None:
            x = x.left

        return x

    def bst_max(self):
        x = self.root

        if x == None:
            return None

        while x.right != None:
            x = x.right

        return x

    # Searches a node according to key
    # and returns a pointer to found node
    def bst_search(self, key):
        node = self.root

        while (node != None) and (node.data != key):
            if node.data < key:
                node = node.right
            else:
                node = node.left;

        return node

    def search_key_of_T(self, key, T):

        node = self.root
        found = False
        data = None
        searching_string = isinstance(key, str)

        # handle upper-lower case collisions
        if searching_string:
            key.lower()

        while (node is not None) and (not found):
            data = node.__dict__['data']
            matching_to = data.__dict__[T]  # use the original datatype of instance

            if searching_string:
                matching_to = matching_to.lower()

            if key == matching_to:
                return data
            if matching_to < key:
                node = node.right
            else:
                node = node.left;

        return None

    def search_all_key_of_T(self, key, T):

        logger.info("\tsearch: %s: %s\n" %(T, key))
        node = self.root
        results = []
        data = None
        searching_string = isinstance(key, str)

        # handle upper-lower case collisions
        if searching_string:
            key.lower()

        while node is not None:
            data = node.__dict__['data']
            matching_to = data.__dict__[T]  # use the original datatype of instance

            logger.info("\n\tBinary Search Tree data:")
            logger.info(data.__dict__)
            logger.info("\t\n")

            if searching_string:
                logger.info("Lowering")
                matching_to = matching_to.lower()

            logger.info("\tkey:\t%s\nmatching_to:\t%s" %(key, matching_to))

            if key == matching_to:
                results.append(data)
            if matching_to < key:
                node = node.right
            else:
                node = node.left;

        logger.info("\t\nFOUND: ")
        logger.info(results)
        logger.info("\t\n")
        return results

    def search_all_between_dates(self, date0, date1):

        node = self.root
        results = []

        while node is not None:
            data = node.__dict__['data']
            matching_to = data.__dict__['date']  # use the original datatype of instance

            left = node.left
            right = node.right

            logger.info("\n\tBinary Search Tree data:")
            logger.info(data.__dict__)
            logger.info(data.date)
            logger.info("%s <= %s <= %s" % date0, data.date, date1)

            if date0 <= data.date <= date1:
                results.append(data)
            if matching_to < date1:
                node = node.right
            else:
                node = node.left;

        logger.info("\t\nFOUND: ")
        logger.info(results)
        logger.info("\t\n")
        return results

    # Prints a node
    def print_node(self, n):
        if n is not None:
            print(' ', n.data, ' ')

    def print_inorder(self, node=None):
        if node is not None:
            self.print_inorder(node.left)
            self.print_node(node)
            self.print_inorder(node.right)

    # Prints the whole tree inorder
    def print_tree_inorder(self):
        self.print_inorder(self.root)

    # Allocates a node with data key
    # and inserts it in the tree

    # TODO: Try to find more generic solution!
    def bst_insert(self, key):
        self.count += 1
        n = BSTNode(key)
        x = self.root
        y = None

        try:
            while x != None:
                y = x
                if key.id < x.data.id:
                    x = x.left
                else:
                    if key.id > x.data.id:
                        x = x.right
                    else:
                        return
        except Exception as ex:
            logger.critical(" bst_insert(): %s" % str(ex))

        n.parent = y
        if y == None:
            self.root = n
        else:
            if key.id < y.data.id:
                y.left = n
            else:
                y.right = n

    # Subroutine for removing
    def bst_transplant(self, u, v):
        if u.parent == None:
            self.root = v
        else:
            if u == (u.parent).left:
                (u.parent).left = v
            else:
                (u.parent).right = v

        if v != None:
            v.parent = u.parent

    # Searches a node according to key
    # and removes it from the tree
    def bst_remove(self, key):
        x = self.bst_search(self, key)

        if (x == None):
            return False

        if x.left == None:
            self.bst_transplant(x, x.right)
        else:
            if x.right == None:
                self.bst_transplant(x, x.left)
            else:
                y = self.bst_min(x.right)

                if y.parent != x:
                    self.bst_transplant(y, y.right)
                    y.right = x.right
                    (y.right).parent = y

                self.bst_transplant(x, y)
                y.left = x.left
                (y.left).parent = y
        self.count -= 1
        return True
