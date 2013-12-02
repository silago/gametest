import cocos
from math import sin,cos,radians, atan2, pi, degrees
import pyglet
from cocos.actions import *
from time import sleep
from time import sleep
import threading
from classchar import Char
import cocos.collision_model as cm
import cocos.euclid as eu
from cocos.scenes.transitions import *
from random import randint
#from app.menu import MainMenu


class Bullet(cocos.sprite.Sprite):
	#is_event_handler = True
	def __init__(self,owner,speed=False,shuffle=False, distance=False):
		
		cocos.sprite.Sprite.__init__(self,'bullet.png')
		self.speed = 2			if not speed else speed
		self.distance= 1000 	if not distance else distance
		self.owner = owner 	
		self.shuffle = 0 		if not shuffle else shuffle
		self.cshape = cm.CircleShape(eu.Vector2(self.owner.position[0],self.owner.position[1]), 100)
		self.go()

		
		
	
	
		#self.flying = 
		

	def go(self):
		self.position = self.owner.position
		position = [self.distance*sin(radians(self.owner.rotation))+randint(0,self.shuffle),self.distance*cos(radians(self.owner.rotation))+randint(0,self.shuffle)]
		self.flying = self.do((MoveBy(position,self.speed) + Hide()))
		self.owner.parent.schedule(self.fly)
		self.owner.parent.collision_manager.add(self)

	def fly(self, some):
		if not self.flying.done():
			print "vzzz"
			self.cshape = cm.CircleShape(eu.Vector2(self.position[0],self.position[1]), 1)
			for i in self.owner.parent.collision_manager.objs_colliding(self):
				if i != self.owner and not isinstance(i,Bullet):
					if getattr(i,'hurt',False):
						i.hurt()
					
					
					try:
						self.owner.parent.unschedule(self.fly)
						self.owner.parent.collision_manager.remove_tricky(self)
						self.owner.parent.remove(self)
					except: 
						print "something wrong whith your bullets"
					
			
			
			
			#if self.man.cshape.touches_point(self.zoombie.position[0],self.zoombie.position[1]):
		else:
			
			print "end"
			#print "stop"
			self.owner.parent.unschedule(self.fly)
			self.owner.parent.collision_manager.remove_tricky(self)
			
			
		#some = False		
		#print some
		

class Weapon(object):
	is_event_handler = True 
	def __init__(self,owner):
		self.owner=owner
		self.distance=100
		self.speed = 100
		self.can_shoot = True
		self.weapon_speed = 1
		
	def enable_shoot(self,*args):
		self.can_shoot = True
		self.owner.parent.unschedule(self.enable_shoot)
		
	def shoot(self,*args):
		if self.can_shoot:	self.owner.parent.add(Bullet(self.owner),1)
				
	def p(self,some,bullet):
		pass
	
	def on_mouse_press(self, x,y,button,modifiers):
		if button==1:	self.shoot()	
		
	def on_mouse_release(self,x,y,button,modifiers):
		pass
		
	def on_key_press(self, key):
		pass
		
	def on_key_release(self, key):
		pass
		#print "s"
class Pistol(Weapon):
	is_event_handler = True 
	def __init__(self,owner):
		Weapon.__init__(self,owner)
		pass

		
		
		
class Shotgun(Weapon):
	def __init__(self,owner):
		Weapon.__init__(self,owner)
	
	def shoot(self,*args):
		if self.can_shoot:
			for _ in xrange(10):
				self.owner.parent.add(Bullet(self.owner,shuffle=200),1)
			self.can_shoot = False
			self.owner.parent.schedule_interval(self.enable_shoot,self.weapon_speed)
			
class Uzi(Weapon):
	def __init__(self,owner):
		self.shooting = False
		Weapon.__init__(self,owner)

	def shoot(self,*args):
		if self.can_shoot:	self.owner.parent.add(Bullet(self.owner,shuffle=200),1)
	
	def on_mouse_press(self, x,y,button,modifiers):
		if button==1 and not self.shooting:
			self.owner.parent.schedule_interval(self.shoot,0.1)
			self.shooting = True
			
			
	def on_mouse_release(self,x,y,button,modifiers):
		self.shooting = False
		if button==1:	self.owner.parent.unschedule(self.shoot)
		
	#self.schedule(self.move)	
		
		
class Man(Char):
	def __init__(self,img):
		Char.__init__(self,img)
		self.speed=5
		self.weapon = Pistol(self)
		
		#self.collision_type=0
		#self.shape.collision_type=3
	def die(self):
		self.parent.gamover()
	
	def shoot(self):
		self.weapon.shoot()
		
	def on_mouse_motion(self,x,y,dx,dy):
		a = list(self.position)
		b = list([x+dx,y+dy])
		
		#print randint(1,10)
		
		r = degrees(atan2(a[0] - b[0], a[1] - b[1]) )+180
		
		self.turn2(False,r)
		#self.move(False)
		
		
	def on_mouse_press(self, x,y,button,modifiers):
		self.weapon.on_mouse_press(x,y,button,modifiers)
		#print button
		
		if button==4:
			#self.schedule(self.on_mouse_motion, x,y, False,False)		
			self.on_key_press(119)
			
	def on_mouse_release(self,x,y,button,modifiers):
		self.weapon.on_mouse_release(x,y,button,modifiers)
		if button==4:
			self.on_key_release(119)
	
		
	def on_key_press(self, key):
		self.weapon.on_key_press(key)
		d = False
		if key == 97: d=-5
		if key == 100: d=5
		if d: self.schedule(self.turn, d)		
		if key == 119:	self.schedule(self.move)
		if key == 65507: self.shoot()
		
	def on_key_release(self, key):
		self.weapon.on_key_release(key)
		if key in (97,100):	self.unschedule(self.turn)
		if key == 119:		self.unschedule(self.move)
