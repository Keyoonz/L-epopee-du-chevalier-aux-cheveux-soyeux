import pygame, words
from data import *

class UI:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()

	def life(self, player):
		heart_empty = pygame.image.load('graphics/status/hempty.png').convert_alpha()
		heart_empty = pygame.transform.scale(heart_empty, ((WIDTH/(1280/heart_empty.get_width())), (HEIGHT/(720/heart_empty.get_height()))))
		heart_semi_full = pygame.image.load('graphics/status/hsemifull.png').convert_alpha()
		heart_semi_full = pygame.transform.scale(heart_semi_full, ((WIDTH/(1280/heart_semi_full.get_width())), (HEIGHT/(720/heart_semi_full.get_height()))))
		heart_full = pygame.image.load('graphics/status/hfull.png').convert_alpha()
		heart_full = pygame.transform.scale(heart_full, ((WIDTH/(1280/heart_full.get_width())), (HEIGHT/(720/heart_full.get_height()))))
		l = []
		for i in range(int(player.health)):
			l.append('f')
		for i in range(int((player.health-int(player.health))*2)):
			l.append('s')
		for i in range(int(player.stats['life']-player.health)):
			l.append('e')
		i = 0
		for elt in l:
			if i <= (WIDTH/30)*9:
				if elt == 'f':
					self.display_surface.blit(heart_full, heart_full.get_rect(topleft=((WIDTH/64)+i, HEIGHT/20)))
				elif elt == 's':
					self.display_surface.blit(heart_semi_full, heart_semi_full.get_rect(topleft=((WIDTH/64)+i, HEIGHT/20)))
				elif elt == 'e':
					self.display_surface.blit(heart_empty, heart_empty.get_rect(topleft=((WIDTH/64)+i, HEIGHT/20)))
				i += WIDTH/30
			else:
				if elt == 'f':
					self.display_surface.blit(heart_full, heart_full.get_rect(topleft=((WIDTH/64)+i-((WIDTH/30)*10), HEIGHT/9)))
				elif elt == 's':
					self.display_surface.blit(heart_semi_full, heart_semi_full.get_rect(topleft=((WIDTH/64)+i-((WIDTH/30)*10), HEIGHT/9)))
				elif elt == 'e':
					self.display_surface.blit(heart_empty, heart_empty.get_rect(topleft=((WIDTH/64)+i-((WIDTH/30)*10), HEIGHT/9)))
				i += WIDTH/30

	def current_object(self, heal_available, boots_use, mana, arrows):
		bg_image = pygame.image.load('graphics/menu/inventory_ui.png')
		bg_image = pygame.transform.scale(bg_image, ((WIDTH/(1280/bg_image.get_width())), (HEIGHT/(720/bg_image.get_height()))))
		bg_image_rect = bg_image.get_rect(topleft=(WIDTH/10*9, HEIGHT/17))
		if current_item != []:
			image = current_item[0].image
			image_rect = image.get_rect(center=bg_image_rect.center)
			self.display_surface.blit(bg_image, bg_image_rect)
			self.display_surface.blit(image, image_rect)
			if current_item[0].item_type == 'heartinventory':
				text = render(str(int(heal_available/0.5)), pygame.font.Font(UI_FONT, WIDTH//50))
				text_pos = bg_image_rect.bottomright
				text_rect = text.get_rect(bottomright=(text_pos[0]-WIDTH/200, text_pos[1]))
				self.display_surface.blit(text, text_rect)
			if current_item[0].item_type == 'boots':
				if boots_use:
					text = render('On', pygame.font.Font(UI_FONT, WIDTH//50))
				else:
					text = render('Off', pygame.font.Font(UI_FONT, WIDTH//50))
				text_pos = bg_image_rect.bottomright
				text_rect = text.get_rect(bottomright=(text_pos[0]-WIDTH/200, text_pos[1]))
				self.display_surface.blit(text, text_rect)
			if current_item[0].item_type == 'magic':
				text = render(str(int(mana)), pygame.font.Font(UI_FONT, WIDTH//50))
				text_pos = bg_image_rect.bottomright
				text_rect = text.get_rect(bottomright=(text_pos[0]-WIDTH/200, text_pos[1]))
				self.display_surface.blit(text, text_rect)
			if current_item[0].item_type == 'bow':
				text = render(str(int(arrows)), pygame.font.Font(UI_FONT, WIDTH//50))
				text_pos = bg_image_rect.bottomright
				text_rect = text.get_rect(bottomright=(text_pos[0]-WIDTH/200, text_pos[1]))
				self.display_surface.blit(text, text_rect)

	def display(self, player):
		self.life(player)
		self.current_object(player.heal_available, player.boots_use, player.mana, player.arrows)

class DialogueBox:
	def __init__(self, text):
		self.display_surface = pygame.display.get_surface()
		self.text = text
		self.back = None

	def update(self, offset):
		self.back = pygame.Surface((WIDTH/1.1, HEIGHT/3), pygame.SRCALPHA)
		self.back.fill((0, 0, 0, 150))
		blit_text(self.back, self.text, (WIDTH/50, HEIGHT/30), pygame.font.Font(UI_FONT, int(HEIGHT/24)))
		blit_text(self.back, words.words[words.current_language]['17'], (WIDTH/2 + offset, HEIGHT/4.5), pygame.font.Font(UI_FONT, int(HEIGHT/26)))
		self.display_surface.blit(self.back, (WIDTH/20, HEIGHT/3*2))

class Text_UI:
	def __init__(self, pos, text, font_size):
		self.font = pygame.font.Font(UI_FONT, int(HEIGHT/100*font_size))

		self.text = render(text, self.font)
		self.rect = self.text.get_rect(topleft = (pos[0], pos[1]))