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
from cocos.particle_systems import *
from cocos.particle import ParticleSystem, Color
from cocos.euclid import Point2

class Bullet(cocos.sprite.Sprite):
	#is_event_handler = True
	def __init__(self,owner,speed=False,shuffle=False, distance=False,damage=False):		
		cocos.sprite.Sprite.__init__(self,'bullet.png')
		
		self.speed = 3		if not speed else speed
		#self.speed 		= 10
		self.damage 	= 10		if not damage else damage
		self.distance	= 1000 		if not distance else distance
		self.owner		= owner 	
		self.scale		=	1
		self.shuffle = randint(1,2) if not shuffle else randint(1,shuffle)
		
		#self.position = self.owner.position
		self.cshape = cm.CircleShape(eu.Vector2(self.position[0],self.position[1]), 5)
		self.cshape.position=self.position
		
		self.go()
		self.parent=self.owner
		self.opacity = 0
	
	
		#self.flying = 
	def trace(self,position):
		pass
			
	def go(self):
		self.effect = Trace()
		if (self.owner,'r',False):		self.rotation = self.owner.r+450
		else:	self.rotation = self.owner.rotation+450
		self.position = [self.owner.position[0]+50*sin(radians(self.rotation-450))+(self.shuffle),self.owner.position[1]+50*cos(radians(self.rotation-450))+(self.shuffle)]
		self.opacity = 5
		self.effect.gravity = Point2(self.owner.position[0],self.owner.position[1])
		self.effect.gravity = Point2(200,00)
		#self.effect.size = 50
		self.add(self.effect,20)
		print self.position
		print self.position
		#self.position = self.owner.position
		position = [self.distance*sin(radians(self.rotation-450))+(self.shuffle),self.distance*cos(radians(self.rotation-450))+(self.shuffle)]
		
		self.flying = ((self.do((MoveBy(position,self.speed) + Hide()))))
		self.owner.parent.schedule(self.fly)
		self.owner.parent.collision_manager.add(self)
		self.trace(position)

	def fly(self, some):
		self.cshape = cm.CircleShape(eu.Vector2(self.position[0],self.position[1]), 5)
		if not self.flying.done():
			#print "vzzz"
			#self.effect.rotation = 
			self.position = self.owner.position
			self.cshape.position = self.position
			#print self.owner.parent.collision_manager.objs_colliding(self)
			for i in self.owner.parent.collision_manager.objs_colliding(self):
			
				if i != self.owner and not isinstance(i,Bullet):
					print "#"
					print i
					if getattr(i,'hurt',False):
						i.hurt(self.damage)					
					#try:	self.effect.remove()
					#except: print "self.effect.remove()"
					#try:	self.remove(self.effect)
					#except: print "self.remove(self.effect)"
					
					self.owner.parent.unschedule(self.fly)
					try:	self.owner.parent.unschedule(self.fly)
					except: print "self.owner.parent.unschedule(self.fly)"
					
					try:	self.owner.parent.collision_manager.remove_tricky(self)
					except: print "self.owner.parent.collision_manager.remove_tricky(self)"
					
					try:	self.owner.parent.remove(self)
					except: "self.owner.parent.remove(self)"
					
		else:
						try:	
							self.effect.remove()
							self.remove(self.effect)
							self.owner.parent.unschedule(self.fly)
							self.owner.parent.collision_manager.remove_tricky(self)
							self.owner.parent.remove(self.effect)
							self.owner.parent.remove(self)
						except: pass
			
			
		#some = False		
		#print some
		

class Weapon(object):
	is_event_handler = True 
	def __init__(self,owner):
		self.owner=owner
		
		#print "####"
		#print owner
		self.distance=10
		self.speed = 1
		self.can_shoot = True
		self.weapon_speed = 2
		
	def enable_shoot(self,*args):
		self.can_shoot = True
		self.owner.parent.unschedule(self.enable_shoot)
		
	def shoot(self,*args):
		if self.can_shoot:	self.owner.parent.add(Bullet(self.owner),20)
				
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
		self.damage = 100
		self.shooting = False
		Weapon.__init__(self,owner)
		
		
	def shoot(self,*args):
		if self.can_shoot:	self.owner.parent.add(Bullet(self.owner,speed=2,shuffle=1,damage=self.damage),1)
	
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
		self.speed=10
		self.weapon = Pistol(self)
		self.opacity = 255
		self.r = 0
		self.directions = (
							cocos.sprite.Sprite('char/1.png'), #down
							cocos.sprite.Sprite('char/2.png'), #left
							cocos.sprite.Sprite('char/3.png'), #right
							cocos.sprite.Sprite('char/4.png'), #top
							cocos.sprite.Sprite('char/5.png'), #leftdown
							cocos.sprite.Sprite('char/6.png'), #rightdown
							cocos.sprite.Sprite('char/1.png'), #allother
						  )
		for i in self.directions: self.add(i,255)
		self.weapon_sprite = cocos.sprite.Sprite('char/weapon.png')
		self.add(self.weapon_sprite,254)
		self.add(cocos.sprite.Sprite('char/body.png'),253)
		#self.scale=20
		#self.add(cocos.sprite.Sprite('char/1.png',(0,0),1,0,255),10000) #allother
		
	def turn(self,some,rotation):
		print rotation
		#r = self.rotation = 
		#self.do(Rotate(direction,0.0001))
		#self.update_cshape()
		
		#self.collision_type=0
		#self.shape.collision_type=3
	def die(self):
		self.parent.gamover()
	
	def shoot(self):
		self.weapon.shoot()
	
		
	def on_mouse_motion(self,x,y,dx,dy):
		a = list(self.position)
		b = list([x+dx,y+dy])
		
		r = degrees(atan2(a[0] - b[0], a[1] - b[1]) )+180
		print r 
		for i in self.directions: i.opacity = 0
		
		
		
		if (0			<=r<67.5 or r > 292): self.directions[3].opacity=255# print "1"
		elif 67.5		<=r<112.5:			 self.directions[2].opacity=255  # |
		elif 112.5		<=r<157.5: 			 self.directions[5].opacity=255
		elif 157.5		<=r<202.5:			 self.directions[0].opacity=255
		elif 202.5		<=r<247.5: 			 self.directions[4].opacity=255 #
		elif 247.5		<r<292.5: 			 self.directions[1].opacity=255
		self.weapon_sprite.rotation = r+180
		
		#else: self.directions[5].opacity=255
		
		#self.positions
		#0-90
		#90-180
		
		
		self.r = r
		#self.turn2(False,r)
		
		
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





class Trace( ParticleSystem ):

  
    # total particles
    total_particles = 50

    # duration
    duration = 1

    # gravity
    gravity = Point2(-200,100)

    # angle
    angle = 0.0
    angle_var = 0.0

    # speed of particles
    speed = 100.0
    speed_var = 0.0

    # radial
    radial_accel = 0
    radial_accel_var = 0

    # tangential
    tangential_accel = 0.0
    tangential_accel_var = 0.0

    # emitter variable position
    pos_var = Point2(0,0)

    # life of particles
    life = 1.2
    life_var = 0.2

    # size, in pixels
    size = 5.0
    size_var = 0.0

    # emits per frame
    emission_rate = total_particles / life

    # color of particles
    start_color = Color(0.2, 0.1, 0.1, 0.5)
    start_color_var = Color(0.0, 0.0, 0.0, 0.0)
    end_color = Color(0.0, 0.0, 0.0, 0.0)
    end_color_var = Color(0.0, 0.0, 0.0, 0.0)

    # blend additive
    blend_additive = False

    # color modulate
    color_modulate = False
