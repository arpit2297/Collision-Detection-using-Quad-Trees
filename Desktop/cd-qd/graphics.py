import pygame
import math
import random
from enum import Enum

pygame.init()


class Point:
	def __init__(self,x,y, fx = 1, fy = 1):
		self.x = x
		self.y = y
		self.fx = fx
		self.fy = fy

	def addPoint(self,p):
		return Point(self.x + p.x, self.y + p.y)

	def setX(self,x):
		self.x = x

	def setY(self,y):
		self.y = y

	def updateVelocity(self,velocity):
		self.velocity = velocity	

class Window:
	def __init__(self,windowScreen, width, height):
		self.windowScreen = windowScreen
		self.width = width
		self.height = height

	def getHeight(self):
		return self.height

	def getWidth(self):
		return self.width

	def getWindowReference(self):
		return self.windowScreen


class Color(Enum):
	WHITE = (255,255,255)
	GREEN = (0,255,0)
	BLACK = (0,0,0)
	RED = (255,0,0)
	BLUE = (0,0,255)

def contained(point, region):
	topLeft = region[0]
	lowerX = topLeft.x
	lowerY = topLeft.y
	bottomRight = region[1]
	higherX = bottomRight.x
	higherY = bottomRight.y

	checkX = (point.x >= lowerX) and (point.x <= higherX)
	checkY = (point.y >= lowerY) and (point.y <= higherY)
	return checkX and checkY


class QTNode:
	def __init__(self):
		self.children = []

	def isLeaf(self):
		for child in self.children:
			if child is not None:
				return False
		return True

class QuadTree:
	def __init__(self, boundingBox):
		self.root = None
		self.boundingBox = boundingBox # bounding box is a property of the QTree and not the QTNode
		self.points = []
		self.maxLimit = 2
		self.ptsInRegion = 0

	def isEmpty(self):
		return self.root == None

	def find(self,point):
		if (self.root.isLeaf): # invariant: if its a leaf, it has to be present in bounding box
			#print("always leaf")
			return self
		for i in range(4):
			q = self.root.children[i]
			if (contained(point, q.boundingBox)):
				print("contained")
				return find(q,point)

		return self # should never get here .. 

	def insert(self,point):
		if (not contained(point, self.boundingBox)):
			# print("not contained!")
			return

		if (self.isEmpty()):
			print("Quad tree empty. Making new root")
			self.root = QTNode()
			self.ptsInRegion = 1
			return

		q = self.find(point)
		if (not q):
			print("Null detect") # should never get here

		elif (q.root.isLeaf() and q.ptsInRegion < q.maxLimit):
			print("Appending")
			q.points.append(point)
			q.ptsInRegion += 1
			print(q.ptsInRegion)

		elif (q.root.isLeaf):
			print("gonna split")
			q.split()

		else: # not a leaf
			print("not a leaf")
			for child in q.root.children:
				child.insert(point)


	def split(self):
		if (self.isEmpty()):
			print("empty!!")
			return
		topLeft = self.boundingBox[0]
		lowerX = topLeft.x
		lowerY = topLeft.y
		bottomRight = self.boundingBox[1]
		higherX = bottomRight.x
		higherY = bottomRight.y

		meanX = (lowerX + higherX)/2
		meanY = (lowerY + higherY)/2
		q1 = QuadTree((Point(meanX, lowerY), Point(higherX, meanY)))
		q2 = QuadTree((Point(lowerX,lowerY), Point(meanX, meanY)))
		q3 = QuadTree((Point(lowerX, meanY), Point(meanX, higherY)))
		q4 = QuadTree((Point(meanX, meanY), Point(higherX, higherY)))
		flag = False
		for point in self.points:
			if (contained(point, q1.boundingBox)):
				print("q1 contains")
				q1.insert(point)
			elif (contained(point, q2.boundingBox)):
				print("q2 contains")
				q2.insert(point)
			elif (contained(point, q3.boundingBox)):
				print("q3 contains")
				q3.insert(point)
			elif (contained(point, q4.boundingBox)):
				print("q4 contains")
				q4.insert(point)

		self.root.children = [q1,q2,q3,q4]

def drawPointSizedObject(windowScreen, color, coords, rad,width):
	pygame.draw.circle(windowScreen,color,coords,rad,width)


def setWindowCaption(caption):
	pygame.display.set_caption(caption)

def main():
	window = Window(pygame.display.set_mode([700,500]), 700, 500)
	limit = 3

	setWindowCaption("Collision Detection Using Quad Trees")

	objects = list()

	for i in range(limit):
		x = int(round(random.uniform(0,window.width - 1)))
		y = int(round(random.uniform(0, window.height - 1)))
		ball = Point(x,y,1,1)
		vx = int(round(random.uniform(1,6)));
		vy = int(round(random.uniform(1,6)));
		velocity = Point(vx,vy)
		ball.updateVelocity(velocity)
		objects.append(ball)

	done = False
	clock = pygame.time.Clock()
	while not done:
		print("loop")
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

		# draw here
		window.getWindowReference().fill(Color.BLACK.value)

		for ball in objects:
			if ball.x == window.getWidth() or ball.x == 0:
				ball.fx = -1 * ball.fx

			if ball.y == window.getHeight() or ball.y == 0:
				ball.fy = -1 * ball.fy

			ball.setX(max(min(ball.x + ball.velocity.x*ball.fx, window.getWidth()),0))
			ball.setY(max(min(ball.y + ball.velocity.y*ball.fy, window.getHeight()),0))

			drawPointSizedObject(window.getWindowReference(),Color.BLUE.value,[ball.x,ball.y],2,0)
		
		pygame.display.flip()

		qTree = QuadTree((Point(0,0), Point(window.width, window.height)))
		for thing in objects:
			qTree.insert(thing)
		# Limit to 50 fps
		clock.tick(10)

	pygame.quit()


if __name__ == '__main__':
	main()