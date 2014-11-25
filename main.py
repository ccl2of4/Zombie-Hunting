import sys, pygame, time
import constants
from Game import Game
from Player import Player
from Entity import Entity


game = Game ()

player = Player (50,0,46,80, stand_left='images/mario_stand_left.png',stand_right='images/mario_stand_right.png',walk_left='images/mario_walk_left.png',walk_right='images/mario_walk_right.png',run_left='images/mario_run_left.png',run_right='images/mario_run_right.png')
player.set_delegate (game)

platform = Entity (0,300,500,20,default='images/platform.png')
platform.set_affected_by_gravity (False)
platform.set_delegate (game)

platform1 = Entity (600,280,500,20,default='images/platform.png')
platform1.set_affected_by_gravity (False)
platform1.set_delegate (game)

platform2 = Entity (450,200,20,100,default='images/platform.png')
platform2.set_affected_by_gravity (False)
platform2.set_delegate (game)

game.add_entity (player)
game.add_entity (platform)
game.add_entity (platform1)
game.add_entity (platform2)

game.run ()