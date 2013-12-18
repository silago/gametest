import cocos
from math import sin,cos,radians
import pyglet
from cocos.actions import *
from time import sleep
import threading

class Char(cocos.sprite.Sprite):
	#is_event_handler = True
	def __init__(self,img):
		cocos.sprite.Sprite.__init__(self,img)
		self.turning = True
		self.moving  = False
		self.direction = 0
		self.position = 420,340
		
	def move(self, some):
			print self.direction
			position = list(self.position)
			position[0]+=5*sin(radians(self.direction))
			position[1]+=5*cos(radians(self.direction))
			self.position = position[0],		position[1]
			print self.position
		
	def turn(self,some,direction):
		#d=0

		self.direction+=direction
		self.do(RotateBy(direction,0))
		
		
	
class Man(Char,img):
	def __init__(self,img):
		Char.__init__(self,img)
	
	
	def on_key_press(self, some, key):
		d = False
		if key == 97: d=-5
		if key == 100: d=5
		if d: 
			self.man.schedule(Char.turn, key)
		
	def on_key_release(self, key, modifiers):
		
		
	
	
class HelloWorld(cocos.layer.Layer):
	is_event_handler = True 
	def __init__(self):
		super( HelloWorld, self ).__init__()
		label = cocos.text.Label("hello",anchor_x='center', anchor_y='center')
		label.position = 320,240
		
		
		self.man = Person('char.png')
		self.man.scale = 0.3
		self.add(label)
		self.add(self.man)
	
	def on_key_press(self, key, modifiers):
		#if key in (97,100):
		#	self.man.schedule(self.man.turn, key)
		#if key == 119:
		#	self.man.schedule(self.man.move)



	def on_key_release(self, key, modifiers):
		#self.man.on_key_press(key)
		#if key in (97,100):
		#	self.man.unschedule(self.man.turn)
		#if key == 119:
		#	self.man.unschedule(self.man.move)
		
	#def on_key_press (self, key, modifiers):
	#	if key in (97,100):
	#		self.man.schedule(self.man.turn, key)
	#
	#
	#	if key == 119:
	#		position = list(self.man.position)
	#		print position
	#		position[0]+=10*sin(radians(self.man.direction))
	#		position[1]+=10*cos(radians(self.man.direction))
	#		self.man.position = position[0],		position[1]

cocos.director.director.init()
cocos.director.director.run( cocos.scene.Scene( HelloWorld() ) )
