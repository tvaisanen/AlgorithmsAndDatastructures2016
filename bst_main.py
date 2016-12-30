import time
import random
from bst import *

def main():
	# Empty tree
	coll = BST() 
	coll.root=None
	
	# Insert random numbers into tree
	for i in range(0,50):
		bst_insert(coll,random.randint(1,1000))
			
	print('Tree after inserting keys:')
	print_tree_inorder(coll)
	
	limit = 500 
	print('Removing keys less than', limit)
	# Remove some keys
	for i in range(0,limit):
		bst_remove(coll,i)
		
	print('Tree after removing keys:')
	print_tree_inorder(coll)
		
	
main()