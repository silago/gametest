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
		self.cshape = cm.CircleShape(eu.Vector2(self.position[0],self.position[1]), 25)
		self.cshape.position=self.position
		self.health = 100
		self.iteration = 0
		self.alive = True
		
		#self.body = pm.Body(1,1666)
		#self.body.position = self.position		
		#self.shape = pm.Segment(self.body,(-80,0),(80,0),10)
		#self.shape.collision_type=1
		#if space:
		#	space.add(self.body)
		##	print "adding to space" 
		#else: print "doesnt'n add to space"
		
		
		
	def hurt(self,damage=False):
		print self.health
		if not damage: damage = 10
		
		self.health-=damage
		if self.health<=0:
			self.die()
		#print self.health
		#print "uhh"
	
	def update_cshape(self):
		self.cshape = cm.CircleShape(eu.Vector2(self.position[0],self.position[1]), 25)
		pass
		
	def die(self):
		self.speed = 0
		self.parent.collision_manager.remove_tricky(self)
		self.parent.remove(self)		
		print "dead"
		try: 
			self = None
		except: pass
			
	def move(self, some):
			position = list(self.position)
			self.update_cshape()
			if (getattr(self,'r',False)):			
				position[0]+=self.speed*sin(radians(self.r))
				position[1]+=self.speed*cos(radians(self.r))
			else:
				position[0]+=self.speed*sin(radians(self.rotation))
				position[1]+=self.speed*cos(radians(self.rotation))				
			#self.position = position[0],		position[1]
			self.do(MoveTo((position[0],		position[1]),0.05))
			#self.cshape = cm.CircleShape(eu.Vector2(self.position[0],self.position[1]), 25)
			#self.body.position = self.position
			
			
			#print self.position
	def turn2(self,some,direction):
		self.rotation = direction
		self.update_cshape()
		#self.cshape = cm.CircleShape(eu.Vector2(self.position[0],self.position[1]), 25)
		#self.direction=direction

	
	def turn(self,some,direction):
		self.do(Rotate(direction,0.0001))
		self.update_cshape()
		#pass
		#self.cshape = cm.CircleShape(eu.Vector2(self.position[0],self.position[1]), 25)
		#self.direction+=direction
		
		#self.direction+=direction
