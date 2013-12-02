# -*- coding: utf-8 -*-
from cocos.director import director
import cocos
from cocos.menu import *

import pyglet
from cocos.actions import *


from cocos.scenes.transitions import *
from random import randint
from layer import Game
from cocos.director import director
		
class TitleLayer(cocos.layer.Layer):
    def __init__(self):
        super(TitleLayer, self).__init__()

        w, h = director.get_window_size()
        self.font_title = {}

        self.font_title['font_name'] = 'Edit Undo Line BRK'
        self.font_title['font_size'] = 26
        #        self.font_title['color'] = (204,164,164,255)
        self.font_title['color'] = (255, 204, 204, 255)
        self.font_title['anchor_y'] = 'top'
        self.font_title['anchor_x'] = 'right'
        title = cocos.text.Label('Doke.', **self.font_title)
        title.position = (w - 10, 30)
        self.add(title, z=1)
		
		
class MainMenu(Menu):
	def __init__(self):
		super(MainMenu, self).__init__(str('Игрулька').decode('utf8'))
		self.name = "main menu"
		
		
		#self.select_sound = soundex.load('move.mp3')
		#self.title='s'
		self.font_title['font_name'] = 'Edit Undo Line BRK'
		self.font_title['font_size'] = 52	
		self.font_title['color'] = (255, 255, 255, 255)

		self.font_item['font_name'] = 'Edit Undo Line BRK',
		self.font_item['color'] = (32, 16, 32, 255)
		self.font_item['font_size'] = 32
		self.font_item_selected['font_name'] = 'Edit Undo Line BRK'
		self.font_item_selected['color'] = (32, 16, 32, 255)
		self.font_item_selected['font_size'] = 46

		#director.scene.add(label,z=1)
		
		#self.__super__.add(TitleLayer())
		
		self.menu_anchor_y = 100
		self.menu_anchor_x = 100
		
		
		
		items = list()
		#items.append(MenuItem(str('Новая игра').decode('utf8'), ))
		items.append(MenuItem(str('Новая игра').decode('utf8'), self.on_new_game1))
		items.append(MenuItem(str('Выход').decode('utf8'), self.on_quit))
		
		self.items = items
		
		
		self.create_menu(items, shake(), shake_back())
		#self.restart()
		#print self.title
	   # self.title = "Loooozer!!!"

	def restart(self):
		self.title = "Again?"
		#self.caption = "You loose"
		#  cocos.director.director.pop()
		self.create_menu(self.items, shake(), shake_back())
		cocos.director.director.replace (cocos.scene.Scene( self))

	def on_new_game1(self):
		
		s = cocos.scene.Scene()
		l = Game()
		l.menu = self
		s.add(l)
		
		#director.push(cocos.scene.Scene( self))
		director.push(FadeTransition(
			s, 1.0))
		
		print cocos.director.director.scene_stack

	def on_options( self ):
		self.parent.switch_to(1)

	def on_scores( self ):
		self.parent.switch_to(2)

	def on_quit(self):
		pyglet.app.exit()		
