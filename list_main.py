from linkedlist import *


def main():
    # Empty linked list
    coll = LinkedList()
    coll.head = None

    # Insert 0..9 into list
    for i in range(10):
        list_insert(coll, i)

    print('Original list:')
    print_list(coll)

    # Remove even keys
    L = [2 * x for x in range(5)]

    for i in L:
        list_remove(coll, i)

    print('List after removing even keys:')
    print_list(coll)

    # Remove odd keys
    L = [9 - 2 * x for x in range(5)]

    for i in L:
        list_remove(coll, i)

    print('List after removing odd keys:')
    print_list(coll)


main()
