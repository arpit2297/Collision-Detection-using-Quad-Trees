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
	lowerX = topLeft[0]
	lowerY = topLeft[1]
	bottomRight = region[1]
	higherX = bottomRight[0]
	higherY = bottomRight[1]

	checkX = (point.x >= lowerX) and (point.x <= higherX)
	checkY = (point.y >= lowerY) and (point.y <= higherY)
	return checkX and checkY


class QuadTree:
	def __init__(self, boundingBox):
		self.maxLimit = 2
		self.ptsInRegion = 0
		self.boundingBox = boundingBox
		self.points = []
		self.children = []

	def isEmpty(self):
		return self == None

	def isLeaf(self):
		for child in self.children:
			if child is not None:
				return False
		return True

	def find(self,point):
		if (self.isEmpty):
			return None # should never reach here
		if (self.isLeaf): # invariant: if its a leaf, it has to be present in bounding box
			return self
		for i in range(4):
			q = self.children[i]
			if (contained(point, q.boundingBox)):
				return find(q,point)
		return self # should never get here .. 

	def insert(self,point):
		if (not contained(point, q.boundingBox)):
			return None

		q = find(point)
		if (not q):
			print("Null detect") # should never get here

		if (q.isLeaf() and q.ptsInRegion < q.maxLimit):
			q.points.append(point)
			q.ptsInRegion += 1

		elif (q.isLeaf):
			q.split()
			for child in q.children:
				child.insert(point)
		else: # not a leaf
			for child in q.children:
				child.insert(point)


	def split(self):
		if (self.isEmpty):
			return
		topLeft = boundingBox[0]
		lowerX = topLeft[0]
		lowerY = topLeft[1]
		bottomRight = boundingBox[1]
		higherX = bottomRight[0]
		higherY = bottomRight[1]

		meanX = (lowerX + higherX)/2
		meanY = (lowerY + higherY)/2
		q1 = Quad((meanX, lowerY), (higherX, meanY))
		q2 = Quad((lowerX,lowerY), (meanX, meanY))
		q3 = Quad((lowerX, meanY), (meanX, lowerX))
		q4 = Quad((meanX, meanY), (higherX, higherY))
		for point in points:
			if (contained(point, q1.boundingBox)):
				q1.points.append(point)
				q1.ptsInRegion += 1
			elif (contained(point, q2.boundingBox)):
				q2.points.append(point)
				q2.ptsInRegion += 1
			elif (contained(point, q3.boundingBox)):
				q3.points.append(point)
				q3.ptsInRegion += 1
			elif (contained(point, q3.boundingBox)):
				q4.points.append(point)
				q4.ptsInRegion += 1

		self.children = [q1,q2,q3,q4]

def detectCollisions(root, objects, cnt):
	if (root.isEmpty):
		return cnt


def drawPointSizedObject(windowScreen, color, coords, rad,width):
	pygame.draw.circle(windowScreen,color,coords,rad,width)


def setWindowCaption(caption):
	pygame.display.set_caption(caption)

def main():
	window = Window(pygame.display.set_mode([700,500]), 700, 500)
	limit = 250

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

		root = QuadTree(((0,0), (window.width, window.height)))
		# Limit to 50 fps
		clock.tick(50)

	pygame.quit()


if __name__ == '__main__':
	main()