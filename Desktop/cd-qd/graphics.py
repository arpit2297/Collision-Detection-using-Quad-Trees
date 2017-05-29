import pygame
import math
pygame.init()


class Point:
	def __init__(self,x,y):
		self.x = x
		self.y = y

	def addPoint(self,p):
		return Point(self.x + p.x, self.y + p.y)

	def getX(self):
		return self.x		

	def getY(self):
		return self.y

	def setX(self,x):
		self.x = x

	def setY(self,y):
		self.y = y


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


class Color:
	WHITE = (255,255,255)
	BLACK = (0,0,0)
	RED = (255,0,0)
	BLUE = (0,0,255)

def drawPointSizedObject(windowScreen, color, coords, rad,width):
	pygame.draw.circle(windowScreen,color,coords,rad,width)


def setWindowCaption(caption):
	pygame.display.set_caption(caption)

def main():
	flipx = 1
	flipy = 1
	window = Window(pygame.display.set_mode([700,500]), 700, 500)

	setWindowCaption("Collision Detection Using Quad Trees")

	ball = Point(50,50)
	velocity = Point(3,3) # increase x,y by 3 always

	done = False
	clock = pygame.time.Clock()
	while not done:
		for event in pygame.event.get():
			if event.type == pygame.QUIT:
				done = True

		# draw here
		window.getWindowReference().fill(Color.WHITE)

		if ball.getX() == window.getWidth() or ball.getX() == 0:
			flipx = -1 * flipx

		if ball.getY() == window.getHeight() or ball.getY() == 0:
			flipy = -1 * flipy

		ball.setX(max(min(ball.getX() + velocity.getX()*flipx, window.getWidth()),0))
		ball.setY(max(min(ball.getY() + velocity.getY()*flipy, window.getHeight()),0))

		drawPointSizedObject(window.getWindowReference(),Color.BLACK,[ball.getX(),ball.getY()],4,0)
		
		pygame.display.flip()

		# Limit to 20 fps
		clock.tick(50)

	pygame.quit()


if __name__ == '__main__':
	main()