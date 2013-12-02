import cocos
from math import sin,cos,radians
import pyglet
from cocos.actions import *
from time import sleep
import threading
import cocos.euclid as eu
import cocos.collision_model as cm



#import pymunk as pm

class Char(cocos.sprite.Sprite):
	#is_event_handler = True
	def __init__(self,img):
		cocos.sprite.Sprite.__init__(self,img)
		self.turning = True
		self.moving  = False
		self.direction = 0
		self.position = 420,440
		self.speed = 1
		self.cshape = cm.CircleShape(eu.Vector2(self.position[0],self.position[1]), 10)
		self.health = 100
		self.iteration = 0
		
		
		#self.body = pm.Body(1,1666)
		#self.body.position = self.position		
		#self.shape = pm.Segment(self.body,(-80,0),(80,0),10)
		#self.shape.collision_type=1
		#if space:
		#	space.add(self.body)
		##	print "adding to space" 
		#else: print "doesnt'n add to space"
	def hurt(self):
		print self.health
		self.health-=10
		if self.health<=0:
			self.die()
		#print self.health
		#print "uhh"
		
	def die(self):
		self.speed = 0
		self.parent.collision_manager.remove_tricky(self)
		self.parent.remove(self)		
		print "dead"
		
			
	def move(self, some):
			position = list(self.position)
			self.cshape = cm.CircleShape(eu.Vector2(self.position[0],self.position[1]), 10)
			position[0]+=self.speed*sin(radians(self.rotation))
			position[1]+=self.speed*cos(radians(self.rotation))
			#self.position = position[0],		position[1]
			self.do(MoveTo((position[0],		position[1]),0.05))
			
			#self.body.position = self.position
			
			
			#print self.position
	def turn2(self,some,direction):
		self.rotation = direction
		#self.direction=direction

	
	def turn(self,some,direction):
		#self.direction+=direction
		self.do(Rotate(direction,0.0001))
		#self.direction+=direction
