#!/usr/bin/python2.7
# -*- coding: utf-8 -*-

import cocos
#from cocos.director import director
from cocos.menu import *
from math import sin,cos,radians, atan2, pi
import pyglet
from cocos.actions import *
from time import sleep
import threading
from classchar import *
from classman import *
from zoombie import *
import cocos.euclid as eu
import cocos.collision_model as cm
from cocos.particle import ParticleSystem
from cocos.particle_systems import *
from cocos.scenes.transitions import *
from random import randint
from menu import MainMenu

#from pyglet.window import mouse

#import pymunk as pm


#window = pyglet.window.Window()


def run():	
	cocos.audio.pygame.mixer.init()	
	cocos.director.director.init(caption='game' )
	#cocos.director.director.run( cocos.scene.Scene( Game() ) )
	pyglet.clock.set_fps_limit(60)
	main = cocos.scene.Scene( MainMenu() )
	main.add(cocos.sprite.Sprite('bg.jpg',(320,240),0,1,30),-1)
	cocos.director.director.run( main,)
	
	
run()
