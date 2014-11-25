import pygame
import constants

class EntityDelegate :
	def get_all_entities () :
		pass

class Location :
	above = 2 << 1
	below = 2 << 2
	left = 2 << 3
	right = 2 << 4
	none = 2 << 5

class Entity (pygame.sprite.Sprite) :
	def __init__ (self,x=0, y=0,width=0,height=0,**images) :
		pygame.sprite.Sprite.__init__ (self)
		self.images = images
		self.width = width
		self.height = height
		self.physical = True
		self.affected_by_gravity = True
		self.velocity = (0,0)
		self.grounded = False
		self.sliding = True
		self.delegate = None
		self.image = None
		self.update_image ()
		self.rect = self.image.get_rect ()
		self.rect.move_ip (x,y)


	def get_delegate (self) :
		return self.delegate
	def set_delegate (self, delegate) :
		self.delegate = delegate

	def is_grounded (self) :
		return self.grounded

	def is_physical (self) :
		return self.physical
	def set_physical (self, physical) :
		self.physical = physical

	def is_affected_by_gravity (self) :
		return self.affected_by_gravity
	def set_affected_by_gravity (self, affected_by_gravity) :
		self.affected_by_gravity = affected_by_gravity

	def update (self) :

		v_x = self.velocity[0]
		v_y = self.velocity[1]
		self.grounded = False

		entities = self.delegate.get_all_entities ()

		if self.affected_by_gravity :
			v_y += constants.gravity

		if self.physical :

			#apply friction and test for collisions
			for entity in entities :
				if entity is self :
					continue

				touching = self.touching (entity)
				if Location.above == touching :
					self.grounded = True
					if self.sliding : 
						v_x *= .9
				elif Location.below == touching :
					if self.sliding :
						v_x *= .9
				elif Location.left == touching :
					pass
				elif Location.right == touching :
					pass

			#test for presence of nearby entities
			for entity in entities :
				if entity is self :
					continue
				
				location = self.location (entity)
				
				#horizontal
				if Location.left == location :
					v_x = min (v_x, entity.rect.left - self.rect.right)
				elif Location.right == location :
					v_x = max (v_x, entity.rect.right - self.rect.left)

				#vertical
				elif Location.above == location :
					v_y = min (v_y, entity.rect.top - self.rect.bottom)
				elif Location.below == location :
					v_y = max (v_y, entity.rect.bottom - self.rect.top)


		if self.grounded :
			assert (v_y <= 0)
			self.grounded = v_y == 0 #won't be grounded for next update if you're leaving the ground

		self.velocity = v_x, v_y
		self.rect.move_ip (*self.velocity)
		self.update_image ()

	def update_image (self) :
		if self.image == None :
			self.image = pygame.image.load (self.images['default'])
		if self.width != 0 or self.height != 0 :
			self.image = pygame.transform.scale (self.image, (self.width,self.height))

	def location (self, other) :
		result = 0
		if (self.rect.right <= other.rect.left) :
			result += Location.left
		if (self.rect.left >= other.rect.right) :
			result += Location.right
		if (self.rect.top >= other.rect.bottom) :
			result += Location.below
		if (self.rect.bottom <= other.rect.top) :
			result += Location.above
		return result

	def touching (self, other) :
		result = 0
		if (self.rect.right == other.rect.left and (self.rect.bottom <= other.rect.top and self.rect.top >= other.rect.bottom)) :
			result += Location.right
		if (self.rect.left == other.rect.right and (self.rect.bottom <= other.rect.top and self.rect.top >= other.rect.bottom)) :
			result += Location.left
		if (self.rect.top == other.rect.bottom and (self.rect.right >= other.rect.left and self.rect.left <= other.rect.right)) :
			result += Location.below
		if (self.rect.bottom == other.rect.top and (self.rect.right >= other.rect.left and self.rect.left <= other.rect.right)) :
			result += Location.above
		return result
