import pygame

from entity import EntityDelegate
from camera import Camera
from notificationcenter import NotificationCenter

import perishableentity
import character
import firearm
import pointofinterest
import resource

class Positioning :
	absolute = 0
	relative = 1

def clear_rect (surf, rect) :
	color = 255,255,255
	surf.fill (color, rect)

class Game (EntityDelegate) :
	def __init__(self, width=800, height=400, camera=None) :
		pygame.init()
		resource.set_images_path (".")
		self.last_update_time = pygame.time.get_ticks ()
		self.time_since_last_update = 0
		self.screen = pygame.display.set_mode((width, height), pygame.HWSURFACE | pygame.DOUBLEBUF | pygame.RESIZABLE)
		self.clock = pygame.time.Clock ()
		self.all_entities = pygame.sprite.LayeredUpdates ()
		self.camera = camera
		self.log_message = None
		self.log_message_duration = None
		self.in_settings = False
		self.defend_points = []
		self.enemies = []

		self._log_message_rect = pygame.Rect (0,0,0,0)
		self._fps_rect = pygame.Rect (0,0,0,0)

		#settings stuff
		self.settings_button_needs_reset = False

		#register for notifications
		notification_names = self.get_notification_names ()
		for notification_name in notification_names :
			NotificationCenter.shared_center().add_observer (self, notification_name)

	#notification handling
	def notify (self, poster, notification_name, **info) :
		main_entity = self.get_main_entity ()
		if character.character_cannot_drop_weapon_notification == notification_name and poster == main_entity:
			self.log ("Cannot drop weapon here")
		elif perishableentity.perishable_entity_died_notification == notification_name :
			if poster == self.get_main_entity () :
				self.log ("You lost!")
			else :
				pass
		elif character.character_picked_up_weapon_notification == notification_name and poster == main_entity :
			self.log (main_entity.get_weapon().get_description ())
		elif firearm.firearm_out_of_ammo_notification == notification_name and poster.get_owner () == main_entity :
			self.log ("Out of ammo!")
		elif pointofinterest.point_of_interest_reached_notification == notification_name :
			entity = info['entity']
			if poster in self.get_defend_points () and entity in self.get_enemies () :
				self.log ("You lose!")

	#notification names for which the game registers
	def get_notification_names (self) :
		return [
			character.character_cannot_drop_weapon_notification,
			perishableentity.perishable_entity_died_notification,
			character.character_picked_up_weapon_notification,
			firearm.firearm_out_of_ammo_notification,
			pointofinterest.point_of_interest_reached_notification]

	#the camera used to scroll the screen
	def get_camera (self) :
		return self.camera
	def set_camera (self, camera) :
		self.camera = camera

	#the main entity in the game. this is the entity that the camera follows.
	def get_main_entity (self) :
		return self.camera.get_target ()
	def set_main_entity (self, entity) :
		self.camera.set_target (entity)

	#the enemies in the game. if the enemies reach the defend points,
	#	the player loses
	def get_enemies (self) :
		return self.enemies
	def set_enemeies (self, enemies) :
		self.enemies = enemies

	#if enemies reach these points, the player loses
	def get_defend_points (self) :
		return self.defend_points
	def set_defend_points (self, defend_points) :
		self.defend_points = defend_points

	#log a message to the top of the game screen
	def log (self, message) :
		self.log_message = message
		self.log_message_duration = 0

	def run (self) :

		clear_rect (self.screen, self.screen.get_rect ())

		while 1:

			#quit or resize screen
			pygame.event.pump ()
			events = pygame.event.get ()
			for event in events :
				if event.type == pygame.QUIT :
					pygame.quit ()
					return
				elif event.type==pygame.VIDEORESIZE:
					size = event.dict['size']
					screen=pygame.display.set_mode(size,pygame.HWSURFACE|pygame.DOUBLEBUF|pygame.RESIZABLE)
					clear_rect (screen, screen.get_rect ())
					self.camera.set_state ((0,0,size[0],size[1]))

			#user input
			keys = pygame.key.get_pressed ()
			if keys[pygame.K_1] :
				if not self.settings_button_needs_reset :
					self.in_settings = not self.in_settings
					self.settings_button_needs_reset = True
			else :
				self.settings_button_needs_reset = False
			
			if self.in_settings :
				self.update_settings ()
			else :
				self.update_game ()

			#framerate stuff
			self.clock.tick (60)
			clear_rect (self.screen, self._fps_rect)
			font = pygame.font.Font (None, 36)
			color = (0, 0, 0)
			text = font.render ('FPS: ' + str (int (self.clock.get_fps ())), False, color, (255,255,255))
			text.set_colorkey ((255,255,255))
			textpos = text.get_rect ()
			textpos.topright = self.screen.get_rect().topright
			self.screen.blit (text, textpos)
			self._fps_rect = textpos
	
			pygame.display.flip ()


	def update_settings (self) :
		pass

	def update_game (self) :

		#update entities
		self.all_entities.update ()

		#camera
		assert self.camera != None
		self.camera.update ()
		for entity in self.all_entities :
			if entity.positioning == Positioning.relative :
				self.camera.apply (entity)

		self.all_entities.clear (self.screen, clear_rect)
		self.all_entities.draw (self.screen)

		clear_rect (self.screen, self._log_message_rect)
		if self.log_message != None :
			percent = min (1.0, self.log_message_duration/60.0)
			if percent < 1 :
				font = pygame.font.Font (None, 36)
				color = (100, 100, 100)
				text = font.render (self.log_message, False, color, (255,255,255))
				text.set_colorkey ((255,255,255))
				textpos = text.get_rect ()
				textpos.centerx = self.screen.get_rect().centerx
				self.screen.blit (text, textpos)
				self.log_message_duration += 1
				self._log_message_rect = textpos
			else :
				log_message = None

	###########################
	#EntityDelegate methods /
	#	entity spawning methods
	###########################

	def get_all_entities (self) :
		return self.all_entities

	def spawn_entity (self, entity) :
		self.all_entities.add (entity)
		entity.set_delegate (self)
		entity.positioning = Positioning.relative
	def spawn_entity_absolute (self, entity) :
		self.spawn_entity (entity)
		entity.positioning = Positioning.absolute
	def despawn_entity (self, entity) :
		self.all_entities.remove (entity)