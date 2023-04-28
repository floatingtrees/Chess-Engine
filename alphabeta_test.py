#Example node:
#min: 1,3,5,7,9,11,13,15
#max: 3,7,11,15
#min: 3,11
#max: 11
#tree_arr = [1,2,3,4,5,6,7,8,9,10,11,12,13,14,15,16]

#Example node 2:
#min: -1,5,3,-3,-5,0,-5,-8
#max: 5,3,0,-5
#min: 3,-5
#max: 3
tree_arr = [-1,2,13,5,7,3,4,-3,-5,6,1,0,-2,-5,8,-8]

import math

class Node:
	#left and right indexes are for tree
	def __init__(self, depth, left_index, right_index):
		self.depth = depth
		self.children = []
		self.left_index = left_index
		self.right_index = right_index

	def create_children(self):
		self.children.extend([
			Node(self.depth + 1, self.left_index, self.left_index + int((self.right_index - self.left_index) / 2)),
			Node(self.depth + 1, self.left_index + int((self.right_index - self.left_index) / 2) + 1, self.right_index)
		])

		#keep recursively making children branches until depth is reached
		if self.depth < math.log(len(tree_arr), 2) - 1:
			self.children[0].create_children()
			self.children[1].create_children()

	def display_depth_first(self):
		if len(self.children) == 0:
			print(tree_arr[self.left_index])
		else:
			for i in self.children:
				i.display_depth_first()



tree = Node(0, left_index=0, right_index=len(tree_arr) - 1)
tree.create_children()
#tree.display_depth_first()

#minimax without pruning
def minimax(node, maximizing):
	if len(node.children) == 0:
		return tree_arr[node.left_index]
	if maximizing:
		maximum = -999
		for child in node.children:
			val = minimax(child, False)
			if val > maximum:
				maximum = val
		print(f"returning {maximum}")
		return maximum
	else:
		minimum = 999
		for child in node.children:
			val = minimax(child, True)
			if val < minimum:
				minimum = val
		print(f"returning {minimum}")
		return minimum

#alphabeta
def alphabeta(node, alpha, beta, maximizing):
	if len(node.children) == 0:
		return tree_arr[node.left_index]
	if maximizing:
		val = -999
		for child in node.children:
			val = max(val, alphabeta(child, alpha, beta, False))
			if val > beta:
				print(f"throwing out {val}")
				break
			alpha = max(alpha, val)

		print(f"returning {val}")
		return val
	else:
		val = 999
		for child in node.children:
			val = min(val, alphabeta(child, alpha, beta, True))
			if val < alpha:
				print(f"throwing out {val}")
				break
			beta = min(beta, val)

		print(f"returning {val}")
		return val

print(minimax(tree, True))
print(alphabeta(tree, -999, 999, True))