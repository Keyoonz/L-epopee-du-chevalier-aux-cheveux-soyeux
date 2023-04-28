import pygame
from data import *

class Tile(pygame.sprite.Sprite):
	def __init__(self, pos, groups, sprite_type, surface = pygame.Surface((TILESIZE, TILESIZE)), alpha = 255, col=None):
		super().__init__(groups)
		self.sprite_type = sprite_type
		y_offset = HITBOX_OFFSET[sprite_type]
		self.image = surface
		self.image.set_alpha(alpha)
		if sprite_type != 'invisible':
			self.image = pygame.transform.scale(self.image, ((WIDTH/(1280/self.image.get_width())), (HEIGHT/(720/self.image.get_height()))))
			self.x_offset = 0
		if sprite_type == 'object':
			self.rect = self.image.get_rect(topleft=(pos[0], pos[1]-TILESIZE))
			if col == 18:
				self.rect = self.image.get_rect(bottomleft=(pos[0], pos[1]-TILESIZE))
			self.x_offset = -30
		elif sprite_type == 'heart':
			self.amount = .5
			self.rect = self.image.get_rect(center=pos)
			self.x_offset = 0
		elif sprite_type == 'mana':
			self.amount = 1
			self.rect = self.image.get_rect(center=pos)
			self.x_offset = 0
		elif sprite_type == 'arrow':
			self.amount = 1
			self.rect = self.image.get_rect(center=pos)
			self.x_offset = 0
		else:
			self.rect = self.image.get_rect(topleft=pos)
			self.x_offset = 0
		self.hitbox = self.rect.inflate(self.x_offset, y_offset)
		if col == 18:
			self.hitbox = self.rect.inflate(self.x_offset, -(self.rect.height/10)*7)
			self.hitbox.bottom = self.rect.bottom

	def get_player_distance_direction(self, player):
		enemy_vec = pygame.math.Vector2(self.rect.center)
		player_vec = pygame.math.Vector2(player.rect.center)
		distance = (player_vec - enemy_vec).magnitude()

		if distance > 0:
			direction = (player_vec - enemy_vec).normalize()
		else:
			direction = pygame.math.Vector2()

		return (distance,direction)