from random import randint
#from app.menu import MainMenu
from cocos.particle_systems import *
from cocos.particle import ParticleSystem, Color
from cocos.euclid import Point2
from bullet import *
from weapon import Weapon



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
				self.owner.parent.add(Bullet(self.owner,shuffle=100),1)
			self.can_shoot = False
			self.owner.parent.schedule_interval(self.enable_shoot,self.weapon_speed)
			
class Uzi(Weapon):
	def __init__(self,owner):
		self.damage = 70
		self.shooting = False
		Weapon.__init__(self,owner)
		
		
	def shoot(self,*args):
		if self.can_shoot:
			self.owner.parent.add(Bullet(self.owner,speed=2,shuffle=5,damage=self.damage),1)
			self.sound_effect()
			self.fire_effect()
	
	
	def on_mouse_press(self, x,y,button,modifiers):
		if button==1 and not self.shooting:
			self.owner.parent.schedule_interval(self.shoot,0.1)
			self.shooting = True
			
			
	def on_mouse_release(self,x,y,button,modifiers):
		self.shooting = False
		if button==1:	self.owner.parent.unschedule(self.shoot)
		
	#self.schedule(self.move)	
		
