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
from bullet import *
from weapon import *
from weapons import *


		
class Man(Char):
	def __init__(self,img):
		Char.__init__(self,img)
		self.speed=10
		self.weapon = Pistol(self)
		
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
		
		
		#self.collision_type=0
		#self.shape.collision_type=3
	def die(self):
		self.parent.gamover()
	
	def shoot(self):
		self.weapon.shoot()
	
		
	def on_mouse_motion(self,x,y,dx,dy):
		#print "m"
		#print self.position
		a = list(self.position)
		b = list([x+dx,y+dy])
		
		r = degrees(atan2(a[0] - b[0], a[1] - b[1]) )+180
		#print r 
		for i in self.directions: i.opacity = 0
		
		
		
		if (0			<=r<67.5 or r > 292): self.directions[3].opacity=255# print "1"
		elif 67.5		<=r<112.5:			 self.directions[2].opacity=255  # |
		elif 112.5		<=r<157.5: 			 self.directions[5].opacity=255
		elif 157.5		<=r<202.5:			 self.directions[0].opacity=255
		elif 202.5		<=r<247.5: 			 self.directions[4].opacity=255 #
		elif 247.5		<r<292.5: 			 self.directions[1].opacity=255
		self.weapon_sprite.rotation = r+180
		#self.move(False)
		self.r = r		
		
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



