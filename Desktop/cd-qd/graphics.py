import pygame
import math
import random

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


class Color:
	WHITE = (255,255,255)
	GREEN = (0,255,0)
	BLACK = (0,0,0)
	RED = (255,0,0)
	BLUE = (0,0,255)

def drawPointSizedObject(windowScreen, color, coords, rad,width):
	pygame.draw.circle(windowScreen,color,coords,rad,width)


def setWindowCaption(caption):
	pygame.display.set_caption(caption)

def main():
	window = Window(pygame.display.set_mode([700,500]), 700, 500)
	limit = 25

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
		window.getWindowReference().fill(Color.BLACK)

		for ball in objects:
			if ball.x == window.getWidth() or ball.x == 0:
				ball.fx = -1 * ball.fx

			if ball.y == window.getHeight() or ball.y == 0:
				ball.fy = -1 * ball.fy

			ball.setX(max(min(ball.x + ball.velocity.x*ball.fx, window.getWidth()),0))
			ball.setY(max(min(ball.y + ball.velocity.y*ball.fy, window.getHeight()),0))

			drawPointSizedObject(window.getWindowReference(),Color.BLUE,[ball.x,ball.y],4,0)
		
		pygame.display.flip()

		# Limit to 20 fps
		clock.tick(50)

	pygame.quit()


if __name__ == '__main__':
	main()