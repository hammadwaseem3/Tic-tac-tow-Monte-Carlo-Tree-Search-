#!/usr/bin/python

import sys
import math
import copy
import random

sys.setrecursionlimit(10000)
class player:
	def __init__(self,PlayerSymbol):
		self.PlayerSymbol=PlayerSymbol
	
	def GetPlayerSymbol(self):
		return self.PlayerSymbol

class board:
	def __init__(self):
		self.grid = [['-' for x in range(3)] for y in range(3)] 
		self.positionleft=9
		#self.availablex=[x for x in range(0,3)]
		#self.availabley=[y for y in range(0,3)]
		self.available=[(0,0),(0,1),(0,2),(1,0),(1,1),(1,2),(2,0),(2,1),(2,2)]
	def CheckIfPlayerWins(self,symbol):
		#along x-axis
		if(self.grid[0][0] == symbol and self.grid[0][1] == symbol and self.grid[0][2] == symbol):
			return True

		if(self.grid[1][0] == symbol and self.grid[1][1] == symbol and self.grid[1][2] == symbol):
			return True

		if(self.grid[2][0] == symbol and self.grid[2][1] == symbol and self.grid[2][2] == symbol):
			return True

		#along y-axis
		if(self.grid[0][0] == symbol and self.grid[1][0] == symbol and self.grid[2][0] == symbol):
			return True

		if(self.grid[0][1] == symbol and self.grid[1][1] == symbol and self.grid[2][1] == symbol):
			return True

		if(self.grid[0][2] == symbol and self.grid[1][2] == symbol and self.grid[2][2] == symbol):
			return True

		#along diagonal
		if(self.grid[0][0] == symbol and self.grid[1][1] == symbol and self.grid[2][2] == symbol):
			return True

		if(self.grid[0][2] == symbol and self.grid[1][1] == symbol and self.grid[2][0] == symbol):
			return True

		return False

	def DisplayBoard(self):
		for i in range(3):
			print(self.grid[i][:]) 
	
	def MarkOnPosition(self,x,y,symbol):
		self.grid[x][y]=symbol
		self.positionleft=self.positionleft-1
		self.available.remove((x,y))
		


class game:
	def __init__(self):
		self.C_Board=board()
		self.computer=player('x')
		self.user=player('0')
		

	def Plays(self):
		computermove=MCTS(1000)
		self.C_Board.DisplayBoard()
			
		for i in range(4):
			print('Enter position (\'0\' base indexing)')
			x=input('Enter x:')
			y=input('Enter y:')
			self.C_Board.MarkOnPosition(x,y,self.user.GetPlayerSymbol())
			self.C_Board.DisplayBoard()
			print('Now its Computer turn\n')
			# here use monte carlo tree search
			x,y=computermove.getMove(self)
			self.C_Board.MarkOnPosition(x,y,self.computer.GetPlayerSymbol())
			self.C_Board.DisplayBoard()
			
		print('Enter position (\'0\' base indexing)')
		x=input('Enter x:')
		y=input('Enter y:')
		self.C_Board.DisplayBoard()
		if self.C_Board.CheckIfPlayerWins(self.computer.GetPlayerSymbol()):
			print('Computer Wins!!')
		else:
			if self.C_Board.CheckIfPlayerWins(self.user.GetPlayerSymbol()):
				print('User Wins!!')
			else:
				print('Draw !!')
		
		
				


class Node:
	def __init__(self,parent,children,unexploremove,moveusedforthisnode):
		self.parent=parent
		self.children=children
		self.unexploremove=unexploremove
		self.numSimulation=0
		self.winSimulation=0
		self.moveusedforthisnode=moveusedforthisnode

	def select(self):
		selectedNode=self
		maximum= (-sys.maxint - 1)
		for child in self.children :
			uctvalue=self.getUCTValue(child)
			if uctvalue > maximum :
				maximum=uctvalue
				selectedNode=child
				
		
		return selectedNode

	def expand(self,C_game):
		if C_game.C_Board.positionleft == 0 :
			return self
		x,y=random.choice(C_game.C_Board.available)
		if self.children is None:
			self.children=[]
		C_game.C_Board.MarkOnPosition(x,y,'x')
		child=Node(self,None,C_game.C_Board.available,[x,y])
		self.children.append(child)
		return child
#may be bug *******
	def backpropagate(self,reward):
		self.numSimulation=self.numSimulation+1
		self.winSimulation=self.winSimulation+reward
		if self.parent is not None :
			self.parent.backpropagate(reward)

		

	def getUCTValue(self,child):
		
		if child.numSimulation == 0:
			uctValue=1
		else:
			uctValue= (child.winSimulation/child.numSimulation) + (2*(math.log(self.numSimulation) / child.numSimulation))**(1/2)


		return uctValue

	def getMostVisitedNode(self):
		mostvisitcount=0
		bestChild=None
		for child in self.children:
			if child.numSimulation > mostvisitcount:
				bestChild=child
				mostvisitcount=child.numSimulation

		return bestChild	

class MCTS:
	def __init__(self,itr):
		self.maxiteration=itr
#parent,children,unexploremoveX,unexploremoveY,moveusedforthisnode
	def getMove(self,M_game):
		rootnode=Node(None,None,M_game.C_Board.available,None)
		for i in range(0,self.maxiteration):
			game_copy= copy.deepcopy(M_game)
			new_node=self.select(rootnode,game_copy)
			new_node=new_node.expand(game_copy)
			reward=self.rollout(game_copy)
			new_node.backpropagate(reward)

		mostVisitedChild=rootnode.getMostVisitedNode()
		return mostVisitedChild.moveusedforthisnode


	def select(self,t_node,t_game):
		while t_node.children is not None:
			t_node=t_node.select()

		return t_node

	def rollout(self,game_copy):
		symbol='0'
		while game_copy.C_Board.positionleft != 0:
			x,y=random.choice(game_copy.C_Board.available)
			game_copy.C_Board.MarkOnPosition(x,y,symbol)
			if symbol == '0':
				symbol='x'
			else:
				symbol='0'

		if game_copy.C_Board.CheckIfPlayerWins('x'):
			return 1
		else:
			return 0
			


obj= game()
obj.Plays()


#  Credits:	http://codegatherer.com/mcts_tic_tac_toe.php
