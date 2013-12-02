import cocos
from math import sin,cos,radians, atan2, pi
import pyglet
from cocos.actions import *
from time import sleep
import threading
from classchar import *
from classman import *
from random import randint

def Zombiing(scene,victim):
	if not getattr(scene,'zoombies',False):
		scene.zoombies = []
	z = Zoombie()
	z.position = randint(-10,500),randint(10,20)*-1
	#z.scale = randint(2,5)/10
	z.scale = 0.2
	z.victim = victim
	z.hunt()
	scene.zoombies.append(z)
	scene.add(z)
	scene.collision_manager.add(z)
	
	

class Zoombie(Char):
	def __init__(self):
		Char.__init__(self,'zoombie.png')
		self.victim = False
		self.position = 220,240
		self.speed = 1
		#self.shape.collision_type=2
	
	def hit(self, target):		
		target.hurt()
		
	def hunt(self):
		if not self.victim:
			print "nothing to hunt"
		else:
			self.schedule(self.look_to_victim)
			#self.look_to_victim(False)
	
	def die(self):
		
		for i in range((randint(1,2))):
			Zombiing(self.parent,self.victim)
		Char.die(self)
		
		
		
	def look_to_victim(self,some):
		a = list(self.position)
		b = list(self.victim.position)
		
		r = atan2(a[1] - b[1], a[0] - b[0]) / pi * 180
		r = r + 90
		r = r * -1
		if (r<0):	r+=360
		r = (r-self.rotation)
		self.turn(False,r)
		self.move(False)
		#print r
