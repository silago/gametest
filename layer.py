
from cocos.director import director
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
		self.man.scale = 0.3
		self.add(self.man,1)
		self.collision_manager = cm.CollisionManagerBruteForce()
		self.collision_manager.add(self.man)
		#for i in range(randint(1,55)):
		for i in range((6)):
			Zombiing(self,self.man)
		
		#self.collision_manager.add(self.zoombie)
		
		self.prettybox = PrettyBox(self)
		self.add(self.prettybox,10)
		
		
		self.schedule(self.run_update)
		self.schedule_interval(self.each_second, 1)
	
		self.came_from = 	cocos.director.director.scene
		
		#self.gamover()

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
			elif isinstance(i,PrettyBox):
				try:
					self.man.weapon = i.holdeditem(self.man)
					i.kill()
				except:
					pass
				
	def run_update(self,some):
		pass
		if getattr(director,'caption',False):
			print director.caption
		#print self.menu
		#if getattr(self,'zoombie',False):
		
		#if self.zoombie in self.collision_manager.known_objs():
		#	if self.man.cshape.touches_point(self.zoombie.position[0],self.zoombie.position[1]):
		#		self.gamover()
		
	def gamover(self):
		self.menu.restart()

class PrettyBox(cocos.sprite.Sprite):
	def __init__(self,scene):
		self.scene = scene
		cocos.sprite.Sprite.__init__(self,'shotgun.png')
		#self.bonusitem = Shotgun(False)
		self.position = 100,100
		self.cshape = cm.CircleShape(eu.Vector2(100,100), 100)
		self.scene.collision_manager.add(self)
		self.holdeditem = Uzi
		#
		#
	
	#def bonus(self):
		
		
		
		"""
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
		"""
