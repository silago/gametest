from cocos.particle_systems import *
from cocos.particle import ParticleSystem, Color
from cocos.euclid import Point2
import cocos.collision_model as cm
import pyglet
class Trace( ParticleSystem ):

  
    # total particles
    total_particles = 50

    # duration
    duration = 1

    # gravity
    gravity = Point2(000,0)

    # angle11
    angle = 00.0
    angle_var = 0.0

    # speed of particles
    speed = 250.0
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
    life = 1
    life_var = 0.0

    # size, in pixels
    size = 2.0
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

    pic = pyglet.image.load('bullet.png', file=pyglet.resource.file('bullet.png'))
    texture = pic.get_texture()
