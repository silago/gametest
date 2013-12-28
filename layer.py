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
from weaponEffects import *




# 
#
#
#

class HUD(cocos.layer.Layer):
	def __init__(self):
		super(HUD, self ).__init__()
		self.score = 0
		self.scull = cocos.sprite.Sprite('images/scull.png')
		self.scull.scale = 0.7
		self.scull.position = 30,430
		self.add(self.scull,100)
		self.score_text = cocos.text.Label(str(self.score),	font_name='Ubuntu',	font_size=16)
		self.score_text.position = 50,420
		self.add(self.score_text,100)
		
		
		self.heart = cocos.sprite.Sprite('images/heart.png')
		self.heart.position = 30,390
		self.heart.scale = 0.4
		self.add(self.heart,100)
		
		self.health = cocos.text.Label('100%',	font_name='Ubuntu',	font_size=16)
		self.health.position = 50,385
		self.add(self.health,100)
		
		
		self.weapon_icon 	= False
		self.bullets 		= False
		self.bonuses 		= False
		self.level 			= False
		
		
		

class Game(cocos.layer.Layer):
	is_event_handler = True 
	def __init__(self):
		super( Game, self ).__init__()
		#self.score = 0
		#self.scull
		#self.score_text = cocos.text.Label(str(self.score),
		#					font_name='Times New Roman',
		#					font_size=32,
		#					anchor_x='center', anchor_y='center')
		
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
		
							
		#self.fps = cocos.text.Label(str(self.score),
		#					font_name='Times New Roman',
		#					font_size=32,
		#					anchor_x='center', anchor_y='center')
							
		
		self.sound = cocos.audio.pygame.mixer.Sound('music.ogg')
		self.sound.play()
		#for i in range(randint(1,55)):
		for i in xrange((100)):
			Zombiing(self,self.man)
		
		
		
		#self.prettybox = SpeedupBonus(self)
		#self.add(self.prettybox,10)
		
		
		#self.schedule(self.run_update)
		self.schedule_interval(self.each_second, 1)
	
		self.collision_rules={self.man:(Zoombie,False,"hit")}
		
		#self.collision_rules =  (())
		#self.collision_rules+= [('name','name2','func')]
		#self.collision_rules+= [('name','name2','func')]
		#print self.collision_rules
		#self.came_from = 	cocos.director.director.scene
		
		#self.gamover()
		self.bonuses = [UziBonus,SpeedupBonus,ShotgunBonus,BombBonus]
		#self.bonuses = [BombBonus]
		#self.bonuses = [UziBonus]
		self.schedule_interval(self.bonusing, 10)
		#self.add(self.bonuses[0](self),20)
		
	def bonusing(self,*args):
		#Элемент случайности
		if (randint(0,1)>-1):
			i = randint(0,3)
			#i=0
			bonus = self.bonuses[i](self)
			bonus.set_position(randint(10,400),randint(10,400))
			self.add(bonus,20)
		else:
			pass
		

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
		for i in self.collision_manager.objs_colliding(self.man):
			if isinstance(i,Zoombie):
				i.hit(self.man)
				
	def run_update(self,some):
		pass
		#if getattr(cocos.director.director,'caption',False):
		#	print cocos.director.director.caption
		
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
		self.image = pyglet.image.load('shotgun.png')
		
	def effect(self,obj):
		obj.weapon = Shotgun(obj)
		
class UziBonus(Bonus):
	def __init__(self,scene):
		Bonus.__init__(self,scene)
		self.image = pyglet.image.load('uzi.png')
		
	def effect(self,obj):
		obj.weapon = Uzi(obj)
		
class SpeedupBonus(Bonus):
	def __init__(self,scene):
		Bonus.__init__(self,scene)		
		self.image = pyglet.image.load('speed.png')
		
	def effect(self,obj):
			obj.speed+=10
			self.schedule_interval(self.uneffect,15,obj)
			self.scene.remove(self)

	def uneffect(self,obj,*args):
			obj.speed-=10
			self.unsheldule(self.uneffect)
			
class BombBonus(Bonus):
	def __init__(self,scene):
		Bonus.__init__(self,scene)		
		self.image = pyglet.image.load('bomb.png')
		self.scene = scene
		self.sound = cocos.audio.pygame.mixer.Sound('sounds/bomb.wav')
		self.radius = 200
		self.damage = 110
		
	def effect(self,obj):
		self.sound.play()
		bps = BombParticleSystem()
		bps.position = self.position
		self.scene.add(bps,100)
		#objects_in_screen = 
		
		for i in self.scene.collision_manager.objs_into_box(self.position[0]-self.radius,self.position[0]+self.radius,self.position[1]-self.radius,self.position[1]+self.radius):
			if isinstance(i,Zoombie):
					i.hurt(self.damage)
			
	def uneffect(self,obj,*args):
		pass
			#obj.speed-=10
			#self.unsheldule(self.uneffect)		
