import sys, pygame, time
from game import Game
from character import Character
from entity import Entity
from camera import Camera
from userinputentitycontroller import UserInputEntityController
from aientitycontroller import AIEntityController
from firearm import Firearm
from bomb import Bomb
from statusdisplay import StatusDisplay
from bullet import Bullet
from explosivebullet import ExplosiveBullet
from pointofinterest import PointOfInterest
from perishableentity import PerishableEntity
from shotgunshell import ShotgunShell
from moveableentity import MoveableEntity
from automaticfirearm import AutomaticFirearm
from entityspawner import EntitySpawner


##
#
#	GUN SPRITES
#
#	http://dustination.deviantart.com/gallery/33496765/Gun-Sprites
#
##

class LevelReader :
	def __init__ (self) :
		self.current_platform = None

	def read (self, file_path) :
		file = open (file_path, 'r')
		
		game = Game (800, 450)
		game.set_camera (Camera (800,450))


		current_entity = None
		
		for line in file :
			line = line.strip ()
			line = line.split (':')
			line = map (lambda string : string.strip (), line)

			if line[0] == '' or line[0][0] == "#":
				continue

			###############
			#player
			###############
			elif line[0] == 'player' :
				assert game.get_main_entity () == None
				assert current_entity == None

				player = Character (
					default = 'images/mario_stand.png',
					stand='images/mario_stand.png',
					walk='images/mario_walk.png',
					run='images/mario_run.png',
					jump='images/mario_jump.png',)
				player.set_name ("Main")
				player.set_controller (UserInputEntityController ())
				game.spawn_entity (player)
				game.set_main_entity (player)
				status_display = StatusDisplay (10,340)
				status_display.set_client (player)
				game.spawn_entity_absolute (status_display)

				current_entity = player



			######
			#enemy
			######
			elif line[0] == 'enemy' :
				assert len (game.get_defend_points ()) > 0
				assert current_entity == None
				player_ai = Character (
					default = 'images/mario_stand.png',
					stand='images/mario_stand.png',
					walk='images/mario_walk.png',
					run='images/mario_run.png',
					jump='images/mario_jump.png',)
				player_ai.set_name ("AI")
				player_ai.set_hostile (True)
				player_ai_c = AIEntityController ()
				player_ai.set_controller (player_ai_c)
				player_ai_c.set_target_entity (game.get_defend_points ()[0])
				game.spawn_entity (player_ai)
				game.get_enemies().append (player_ai)
				player_ai.set_status_display (StatusDisplay (100,50))

				current_entity = player_ai


			#########
			#platform
			#########
			elif line[0] == 'platform' :
				assert current_entity == None
				platform = Entity (default='images/platform.png')
				game.spawn_entity (platform)

				current_entity = platform


			##################
			#destructible wall
			##################
			elif line[0] == 'destructible_wall' :
				assert current_entity == None
				wall = PerishableEntity (default='images/platform.png')
				game.spawn_entity (wall)

				current_entity = wall


			#######
			#firearm
			#######
			elif line[0] == 'firearm' :
				gun = Firearm (default='images/platform.png')
				gun.set_anchor_points (muzzle=(0,0))
				magazine = []

				for ammo in line[1].split (',') :
					info = ammo.split ('*')
					info = map (lambda string : string.strip (), info)
					count = int (info[0])
					if info[1] == 'explosive_bullet' :
						for i in range (count) :
							projectile = ExplosiveBullet (default='images/platform.png')
							magazine.append (projectile)
					elif info[1] == 'bullet' :
						for i in range (count) :
							projectile = Bullet (default='images/platform.png')
							magazine.append (projectile)
					elif info[1] == 'shotgun_shell' :
						for i in range (count) :
							projectile = ShotgunShell (default='images/platform.png')
							magazine.append (projectile)
					else :
						assert (False)

				gun.set_magazine (magazine)
				game.spawn_entity (gun)

				current_entity = gun

			#################
			#automaticfirearm
			#################
			elif line[0] == 'autofirearm' :
				autogun = AutomaticFirearm (default='images/m60.png')
				autogun.set_anchor_points (muzzle=(175,17))
				magazine = []

				for ammo in line[1].split (',') :
					info = ammo.split ('*')
					info = map (lambda string : string.strip (), info)
					count = int (info[0])
					if info[1] == 'explosive_bullet' :
						for i in range (count) :
							projectile = ExplosiveBullet (default='images/platform.png')
							magazine.append (projectile)
					elif info[1] == 'bullet' :
						for i in range (count) :
							projectile = Bullet (default='images/platform.png')
							magazine.append (projectile)
					elif info[1] == 'shotgun_shell' :
						for i in range (count) :
							projectile = ShotgunShell (default='images/platform.png')
							magazine.append (projectile)
					else :
						assert (False)

				autogun.set_magazine (magazine)
				game.spawn_entity (autogun)

				current_entity = autogun


			#####
			#bomb
			#####
			elif line[0] == 'bomb' :
				bomb = Bomb (default='images/platform.png')
				game.spawn_entity (bomb)

				current_entity = bomb

			#############
			#defend point
			#############
			elif line[0] == 'defend_point' :
				point_of_interest = PointOfInterest ()
				game.spawn_entity (point_of_interest)
				game.get_defend_points().append (point_of_interest)
				current_entity = point_of_interest


			###############
			#entity spawner
			###############
			elif line[0] == 'entity_spawner' :
				entity_spawner = EntitySpawner ()
				entities_list = []

				for entities in line[1].split (',') :
					info = entities.split ('*')
					info = map (lambda string : string.strip (), info)
					count = int (info[0])
					if info[1] == 'enemy' :
						for i in range (count) :

							player_ai = Character (
								default = 'images/mario_stand.png',
								stand='images/mario_stand.png',
								walk='images/mario_walk.png',
								run='images/mario_run.png',
								jump='images/mario_jump.png',)
							player_ai.set_name ("AI")
							player_ai.set_hostile (True)
							player_ai_c = AIEntityController ()
							player_ai.set_controller (player_ai_c)
							player_ai.set_status_display (StatusDisplay ())
							player_ai_c.set_target_entity (game.get_defend_points ()[0])
							game.get_enemies().append (player_ai)
							entities_list.append (player_ai)
					else :
						assert (False)

				entity_spawner.set_entities (entities_list)
				game.spawn_entity (entity_spawner)
				current_entity = entity_spawner


			#######################################
			#coordinates for entity location
			#######################################
			else :
				coords = line[0].split ()
				assert (len (coords) == 4)
				coords = map (lambda string : int (string), coords)
				x,y,width,height = coords
				current_entity.rect = pygame.Rect (*coords)
				current_entity.width, current_entity.height = width, height
				current_entity = None


		return game