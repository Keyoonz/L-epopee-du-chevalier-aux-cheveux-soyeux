import pygame
import words
from data import *

class Text(pygame.sprite.Sprite):
	def __init__(self, pos, groups, text):
		super().__init__(groups)
		self.font = pygame.font.Font(UI_FONT, int(HEIGHT/23))

		self.sprite_type = "interactive_ui"
		y_offset = HITBOX_OFFSET[self.sprite_type]
		self.image = render(text, self.font)
		self.rect = self.image.get_rect(topleft = (pos[0], pos[1] - y_offset))
		self.hitbox = self.rect