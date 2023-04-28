import pygame
from data import *

class Item(pygame.sprite.Sprite):
	def __init__(self, groups, item_type):
		super().__init__(groups)
		self.sprite_type = 'item'
		self.item_type = item_type
		self.image = pygame.image.load(f'graphics/items/{item_type}.png')		
		self.image = pygame.transform.scale(self.image, ((WIDTH/(1280/self.image.get_width())), (HEIGHT/(720/(self.image.get_height())))))
		self.rect = self.image.get_rect()
		self.hitbox = self.rect