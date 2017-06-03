import pygame
import math
import random
import gc
from enum import Enum

pygame.init()


class Point:
	def __init__(self,x,y, fx = 1, fy = 1, radius = 2):
		self.x = x
		self.y = y
		self.fx = fx
		self.fy = fy
		self.rad = radius

	def addPoint(self,p):
		return Point(self.x + p.x, self.y + p.y)

	def setX(self,x):
		self.x = x

	def setY(self,y):
		self.y = y

	def updateVelocity(self,velocity):
		self.velocity = velocity	

class Window:
	width = 800
	height = 500
	windowScreen = pygame.display.set_mode([width,height])

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

def detectCircleCollision(point1, point2):
	# point1, point2 are the circles
	dx = point2.x - point1.x
	dy = point2.y - point1.y
	combinedRadii = point1.rad + point2.rad

	# Distance formula
	if ((dx * dx) + (dy * dy) < combinedRadii * combinedRadii):
		return True
	return False

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
		self.collisions = 0

	def isEmpty(self):
		return self.root == None

	def find(self,qtree,point):
		if (qtree.root.isLeaf()): # invariant: if its a leaf, it has to be present in bounding box
			#print("always leaf")
			return self
		for i in range(4):
			q = qtree.root.children[i]
			if (contained(point, q.boundingBox)):
				if (q.isEmpty()):
					return q
				return q.find(q,point)

		return self # should never get here .. 

	def insert(self,point):
		if (not contained(point, self.boundingBox)):
			#print("not contained!")
			return

		if (self.isEmpty()):
			#print("Quad tree empty. Making new root")
			self.root = QTNode()
			self.points.append(point)
			return

		q = self.find(self, point)
		if (q.isEmpty()):
			q.root = QTNode()
			q.points.append(point)

		elif (q.root.isLeaf() and len(q.points) < q.maxLimit):
			#print("Appending")
			q.points.append(point)

		elif (q.root.isLeaf()):
			#print("gonna split")
			q.points.append(point)
			q.split()

		else: # not a leaf
			for child in q.root.children:
				child.insert(point)


	def split(self):
		if (self.isEmpty()):
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

		drawLine(Window().getWindowReference(), Color.WHITE.value, (meanX, lowerY), (meanX, higherY))
		drawLine(Window().getWindowReference(), Color.WHITE.value, (lowerX, meanY), (higherX, meanY))

		assert len(self.points) > self.maxLimit
		for point in self.points:
			if (contained(point, q1.boundingBox)):
				q1.insert(point)
			elif (contained(point, q2.boundingBox)):
				q2.insert(point)
			elif (contained(point, q3.boundingBox)):
				q3.insert(point)
			elif (contained(point, q4.boundingBox)):
				q4.insert(point)

		self.root.children = [q1,q2,q3,q4]

	def countCollisions(self):
		# dfs
		if (self.isEmpty()):
			return self.collisions
		if (self.root.isLeaf()):
			# a leaf can contain maximum maxLimit # of objects. So, an n^2 approach here is ok
			i = 0
			numPoints = len(self.points)
			while (i < numPoints):
				j = i + 1
				while (j < numPoints):
					if (detectCircleCollision(self.points[i], self.points[j])):
						self.collisions += 1
					j += 1
				i += 1
			return self.collisions

		for i in range(4):
			self.collisions += self.root.children[i].countCollisions()
		return self.collisions


def drawLine(windowScreen, color, point1, point2):
	#print("been here")
	pygame.draw.line(windowScreen, color, point1,point2)

def drawPointSizedObject(windowScreen, color, coords, rad,width):
	pygame.draw.circle(windowScreen,color,coords,rad,width)


def setWindowCaption(caption):
	pygame.display.set_caption(caption)

def main():
	window = Window()
	limit = 400
	setWindowCaption("Collision Detection Using Quad Trees")

	objects = []

	for i in range(limit):
		x = int(round(random.uniform(0,window.width - 1)))
		y = int(round(random.uniform(0, window.height - 1)))
		point = Point(x,y,1,1,2)
		vx = int(round(random.uniform(1,6)));
		vy = int(round(random.uniform(1,6)));
		velocity = Point(vx,vy)
		point.updateVelocity(velocity)
		objects.append(point)

	done = False
	clock = pygame.time.Clock()
	window.getWindowReference().fill(Color.BLACK.value)
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

		# draw here
		window.getWindowReference().fill(Color.BLACK.value)
		qTree = QuadTree((Point(0,0), Point(window.width, window.height)))
		for point in objects:
			if point.x == window.getWidth() or point.x == 0:
				point.fx = -1 * point.fx

			if point.y == window.getHeight() or point.y == 0:
				point.fy = -1 * point.fy

			point.setX(max(min(point.x + point.velocity.x*point.fx, window.getWidth()),0))
			point.setY(max(min(point.y + point.velocity.y*point.fy, window.getHeight()),0))

			drawPointSizedObject(window.getWindowReference(),Color.BLUE.value,[point.x,point.y],2,0)
			qTree.insert(point)

		pygame.display.flip()

		qTree.countCollisions()
		print(qTree.collisions)
		# Limit to 50 fps
		gc.collect() # free any unreferenced memory
		clock.tick(50)

	pygame.quit()


if __name__ == '__main__':
	main()