import cocos
from math import sin,cos,radians, atan2, pi
import pyglet
from cocos.actions import *
from time import sleep
import threading
from classchar import *
from classman import *
from random import randint

#from pyglet import image
pic = pyglet.image.load('zoombie_dead.png')

#dead_zombie_sprite = cocos.sprite.Sprite('zoombie_dead.png')


def Zombiing(scene,victim):
	if not getattr(scene,'zoombies',False):
		scene.zoombies = []
	z = Zoombie()
	
	probaly_pos = (
					(650, randint(0,480)),
					(randint(0,480), 500),
					(-10, randint(0,480)),
					(randint(0,480), -10))
	pos = probaly_pos[randint(0,3)]
	z.position = pos[0],pos[1]
	#z.scale = float(randint(15,30))/100
	z.scale = 1
	z.victim = victim
	z.hunt()
	scene.zoombies.append(z)
	scene.add(z,2)
	scene.collision_manager.add(z)
	
	

class Zoombie(Char):
	def __init__(self):
		Char.__init__(self,'zoombie.png')
		self.victim = False
		self.position = 220,240
		self.speed = 1
		self.stepping_aside = False
		#self.shape.collision_type=2
	
	def move(self, some):
		return 1
		to_step = False
		
		if self.parent.collision_manager.objs_colliding(self):
			for i in self.parent.collision_manager.objs_colliding(self):
				if i!=self and isinstance(i,Zoombie):
					to_step = True
					break
		if (to_step): self.step_aside(i)
		else: Char.move(self,some)
		#else: pass
	
	def step_aside(self,obj):
			return 1
			self.stepping_aside = True
			x = (self.position[0]-obj.position[0])
			y = (self.position[1]-obj.position[1])
			self.do(MoveBy((x,y),2))
			self.update_cshape()
	
	def hit(self, target):		
		return 1
		target.hurt()
		
	def hunt(self):
		if not self.victim:
			print "nothing to hunt"
		else:
			self.schedule_interval(self.look_to_victim,0.1)
			#self.look_to_victim(False)
	
	def die(self):
		self.parent.parent.get('hud').score_text.element.text=str(int(self.parent.parent.get('hud').score_text.element.text)+1)
		self.unschedule(self.look_to_victim)
		self.parent.add(cocos.sprite.Sprite(pic,self.position,randint(1,360),5,100),1)
		#self.image = pyglet.image.load('zoombie_dead.png')
		for i in range((randint(1,2))):
			Zombiing(self.parent,self.victim)
		Char.die(self)
		
	
		
		
	def look_to_victim(self,some):
		print self.parent.parent.get_rect()
		#print self.x
		#return 1
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
