# -*- coding: utf-8 -*-
import cocos
from cocos.menu import *
from math import sin,cos,radians, atan2, pi
import pyglet
from cocos.actions import *
from time import sleep
import threading
from classchar import *
from zoombie import *
import cocos.euclid as eu
import cocos.collision_model as cm
from cocos.particle import ParticleSystem
from cocos.particle_systems import *
from cocos.scenes.transitions import *
from random import randint





# 
#
#
#

class Game(cocos.layer.Layer):
	is_event_handler = True 
	def __init__(self):
		super( Game, self ).__init__()
		self.name = "game layer"
		self.iteration=0
		bg_image = pyglet.image.load('dirt.jpg')
		bg = cocos.sprite.Sprite(bg_image)
		self.add(bg)
		self.man = Man('char.png')
		self.man.scale = 1.5
		self.add(self.man,2)
		self.collision_manager = cm.CollisionManagerBruteForce()
		self.collision_manager.add(self.man)
		self.score = 0
		self.score_text = cocos.text.Label(str(self.score),
							font_name='Times New Roman',
							font_size=32,
							anchor_x='center', anchor_y='center')
							
		#self.fps = cocos.text.Label(str(self.score),
		#					font_name='Times New Roman',
		#					font_size=32,
		#					anchor_x='center', anchor_y='center')
							
		self.score_text.position = 600,430
		self.add(self.score_text,100)
		#self.sound = cocos.audio.pygame.mixer.Sound('music.ogg')
		#self.sound.play()
		#for i in range(randint(1,55)):
		for i in range((6)):
			Zombiing(self,self.man)
		
		
		
		#self.prettybox = SpeedupBonus(self)
		#self.add(self.prettybox,10)
		
		
		self.schedule(self.run_update)
		self.schedule_interval(self.each_second, 1)
	
		self.collision_rules={self.man:(Zoombie,False,"hit")}
		
		#self.collision_rules =  (())
		#self.collision_rules+= [('name','name2','func')]
		#self.collision_rules+= [('name','name2','func')]
		#print self.collision_rules
		#self.came_from = 	cocos.director.director.scene
		
		#self.gamover()
		self.bonuses = [UziBonus,SpeedupBonus,ShotgunBonus]
		#self.bonuses = [UziBonus]
		self.schedule_interval(self.bonusing, 10)
		self.add(self.bonuses[0](self),20)
		
	def bonusing(self,*args):
		i = randint(0,2)
		bonus = self.bonuses[i](self)
		bonus.set_position(randint(10,400),randint(10,400))
		self.add(bonus,20)
		

	def on_mouse_motion( self, x, y, dx, dy):
		#print "s"
		self.man.on_mouse_motion(x,y,dx,dy)
		#pass
		#print "x="+x+" y="+y+" dx="+dx+" dy="+dy
		
		#self.man.on_key_press(key)
	def on_mouse_drag(self, x, y, dx, dy, buttons, modifiers):
		self.on_mouse_motion(x,y,dx,dy)
	
	def on_mouse_press(self, x, y, button, modifiers):
		self.man.on_mouse_press(x,y,button,modifiers)
		print "t"
		#self.man.on_mouse_press(x,y,button,modifiers)
	
	def on_mouse_release(self, x, y, button, modifiers):
		self.man.on_mouse_release(x,y,button,modifiers)
    
	def on_key_press(self, key, modifiers):
		print key
		self.man.on_key_press(key)

	def on_key_release(self, key, modifiers):
		self.man.on_key_release(key)
	
	def each_second(self,some):
		#	for element in self.collision_rules:
		#		for i in self.collision_manager.objs_colliding(element):
		#			print key
					#if isinstance(i,element[0]):
					#	getattr(i, element[2])()
		#cocos.director.director.show_FPS()
		
		
		for i in self.collision_manager.objs_colliding(self.man):
			if isinstance(i,Zoombie):
				i.hit(self.man)
			#elif isinstance(i,PrettyBox):
			#	try:
			#		self.man.weapon = i.holdeditem(self.man)
			#		self.collision_manager.remove_tricky(i)
			#		i.kill()
			#	except:
			#		pass
				
	def run_update(self,some):
		pass
		if getattr(cocos.director.director,'caption',False):
			print cocos.director.director.caption
		
	def gamover(self):
		self.menu.restart()

#def Bonusing(scene):
	#scene.self.schedule_interval(self.uneffect,50,obj)
#	pass


#class PrettyBox(cocos.sprite.Sprite):
#	def __init__(self,scene):
#		self.scene = scene
#		cocos.sprite.Sprite.__init__(self,'u.jpg')
#		#self.bonusitem = Shotgun(False)
#		self.position = 100,100
#		self.cshape = cm.CircleShape(eu.Vector2(100,100), 100)
#		self.scene.collision_manager.add(self)
#		self.holdeditem = Uzi
	
	

	
class Bonus(cocos.sprite.Sprite):
		def __init__(self,scene):
			self.scene = scene
			cocos.sprite.Sprite.__init__(self,'bonus.jpg')
			self.position = 100,100
			self.cshape = cm.CircleShape(eu.Vector2(100,100), 20)
			self.scene.collision_manager.add(self)
			self.schedule(self.wait_for_pickup)
		
		def set_position(self,x,y):
			self.position = x,y
			self.cshape = cm.CircleShape(eu.Vector2(x,y), 20)
		
		def wait_for_pickup(self,*args):
			for i in self.scene.collision_manager.objs_colliding(self):
				if isinstance(i,Man):
						self.effect(i)
						self.unschedule(self.wait_for_pickup)
						try:
							self.scene.remove(self)
							self.scene.collision_manager.remove_tricky(self)
						except: print "something go wrong when deleting picked up object"
						break
		def effect(self,obj):
			pass
		

class ShotgunBonus(Bonus):
	def __init__(self,scene):
		Bonus.__init__(self,scene)
		
	def effect(self,obj):
		obj.weapon = Shotgun(obj)
		
class UziBonus(Bonus):
	def __init__(self,scene):
		Bonus.__init__(self,scene)
		
	def effect(self,obj):
		obj.weapon = Uzi(obj)
		
class SpeedupBonus(Bonus):
	def __init__(self,scene):
		Bonus.__init__(self,scene)		
		
	def effect(self,obj):
			obj.speed+=10
			self.schedule_interval(self.uneffect,15,obj)
			self.scene.remove(self)

	def uneffect(self,obj,*args):
			obj.speed-=10
			self.unsheldule(self.uneffect)		

#class bonusBox(object):
#		self.__init__(self):
#			pass
		
		
		#
		#
	
	#def bonus(self):
		
		
