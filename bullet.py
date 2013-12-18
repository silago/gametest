from random import randint
import cocos
from cocos.particle_systems import *
from cocos.particle import ParticleSystem, Color
from cocos.euclid import Point2
import cocos.collision_model as cm			
import cocos.euclid as eu
from weaponEffects import *
from math import sin,cos,radians, atan2, pi, degrees
from cocos.actions import *

class Bullet(cocos.sprite.Sprite):
	#is_event_handler = True
	def __init__(self,owner,speed=False,shuffle=False, distance=False,damage=False):		
		cocos.sprite.Sprite.__init__(self,'bullet.png')
		self.speed = 2		if not speed else speed
		#self.speed 		= 10
		self.damage 	= 10		if not damage else damage
		self.distance	= 1000 		if not distance else distance
		self.owner		= owner 	
		self.scale		=	1
		self.shuffle = randint(1,2) if not shuffle else randint(-shuffle,shuffle)
		
		self.position = self.owner.position[0],self.owner.position[1]
		self.cshape = cm.CircleShape(eu.Vector2(self.position[0],self.position[1]), 5)
		#self.cshape.position=self.position
		
		
		self.go()
		self.parent=self.owner
		#self.rotation = self.owner.rotation
		#print self.rotation
		
	
	
		#self.flying = 
	def trace(self,position):
		pass
		#for _ in (xrange(155)):
		#	position = [(self.distance-((_)*10))*sin(radians(self.owner.rotation))+(self.shuffle),(self.distance-((_)*10))*cos(radians(self.owner.rotation))+(self.shuffle)]
		#	t = cocos.sprite.Sprite('bullet.png',self.owner.position,1,1,155-_)
		#	self.owner.parent.add(t)
		
		#print self.effect
			
	def go(self):
		if not (getattr(self.owner,'effect',False)):	self.effect = Trace()
		else: self.effect = self.owner.effect
		ri = randint(-self.shuffle,-self.shuffle)
		self_owner_r = self.owner.r
		self_owner_weapon_sprite_rotation = self.owner.weapon_sprite.rotation
		self_rotation = self.rotation
		
		self.owner.r = self.owner.r+ri
		self.owner.weapon_sprite.rotation = self.owner.weapon_sprite.rotation+ri
		self.rotation = self.owner.r+450
		
		#self.position = [self.owner.position[0]+25*sin(radians(self.rotation-450)),self.owner.position[1]+50*cos(radians(self.rotation-450))]
		#self.effect.gravity = Point2(self.owner.position[0],self.owner.position[1])
		self.effect.gravity = Point2(-25,000)
		
		
		#self.effect.gravity = Point2(-200,-200)
		#self.effect.rotation = 0
		#self.effect.rotation = self.rotation
		#self.effect.size = 50
		self.add(self.effect,200)
		#self.effect.rotation = self.owner.r+450
		#self.effect.rotation = self.owner.r+20
		#self.effect.transform_anchor = 00, 2000
		#	print self.effect.parent
		#self.position = self.owner.position
		
		#position = [self.distance*sin(radians(self.owner.r))+(self.shuffle),self.distance*cos(radians(self.owner.r))+(self.shuffle)]
		position = [self.distance*sin(radians(self.owner.r)),self.distance*cos(radians(self.owner.r))]
		
		
		#a = list(self.position)
		#b = position		
		#r = degrees(atan2(a[0] - b[0], a[1] - b[1]) )+180
		#self.rotation = r+73.5	
		
		self.flying = ((self.do((MoveBy(position,self.speed) ))))
		self.owner.parent.schedule(self.fly)
		self.owner.parent.collision_manager.add(self)
		self.trace(position)

		#self.owner.r = self_owner_r
		#self.owner.weapon_sprite.rotation = self_owner_weapon_sprite_rotation
		#self.rotation = self_rotation

	def fly(self, some):
		self.cshape = cm.CircleShape(eu.Vector2(self.position[0],self.position[1]), 5)
		#print self.flying.done()
		if not self.flying.done():
			#print "vzzz"
			#self.effect.rotation = 
			#self.position = self.owner.position
			self.cshape.position = self.position
			#print self.owner.parent.collision_manager.objs_colliding(self)
			for i in self.owner.parent.collision_manager.objs_colliding(self):			
				if i != self.owner and not isinstance(i,Bullet):
					if getattr(i,'hurt',False):
						i.hurt(self.damage)					
					try:	self.effect.remove()
					except: print "self.effect.remove()"
					#try:	self.remove(self.effect)
					#except: print "self.remove(self.effect)"
					
					self.owner.parent.unschedule(self.fly)
			
					try:	self.owner.parent.collision_manager.remove_tricky(self)
					except: print "self.owner.parent.collision_manager.remove_tricky(self)"
					
					try:	self.owner.parent.remove(self)
					except: "self.owner.parent.remove(self)"
					
		else:		
					self.owner.parent.unschedule(self.fly)
					self.owner.parent.collision_manager.remove_tricky(self)
					self.owner.parent.remove(self)
