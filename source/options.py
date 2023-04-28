import pygame, states, time, words
from data import *

class Settings:
	def __init__(self) -> None:
		self.display_surface = pygame.display.get_surface()
		self.active = None

	def general_appearance(self):
		bg = pygame.Rect(0, 0, WIDTH, HEIGHT)
		pygame.draw.rect(self.display_surface, '#2c2d2c', bg)

	def back_button(self):
		if self.active == 'back':
			text_color = TEXT_COLOR
			border_color = UI_BORDER_COLOR_ACTIVE
			if pygame.key.get_pressed()[pygame.K_RETURN]:
				if states.before_options == 'M':
					states.current_state = states.MENU
				elif states.before_options == 'P':
					states.current_state = states.PAUSE
				time.sleep(0.2)
		else:
			text_color = 'gold'
			border_color = UI_BORDER_COLOR
		temp_font = pygame.font.Font(UI_FONT, int(HEIGHT/29))
		text = temp_font.render(words.words[words.current_language]['4'], False, text_color)
		back_rect = pygame.Rect(0.05*WIDTH, 0.07*HEIGHT, 0.1*WIDTH, 0.06*HEIGHT)
		back_rect_border = back_rect.inflate(9, 9)
		rect = text.get_rect(center=back_rect.center)
		pygame.draw.rect(self.display_surface, border_color, back_rect_border, border_radius=5)
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, back_rect, border_radius=5)
		self.display_surface.blit(text, rect)

	def chose_keybinds_button(self):
		if self.active == 'ckb':
			text_color = TEXT_COLOR
			border_color = UI_BORDER_COLOR_ACTIVE
			if pygame.key.get_pressed()[pygame.K_RETURN]:
				states.current_state = states.CHOSE_KEYBINDS
				time.sleep(0.2)
		else:
			text_color = 'gold'
			border_color = UI_BORDER_COLOR
		temp_font = pygame.font.Font(UI_FONT, int(HEIGHT/24))
		text = temp_font.render(words.words[words.current_language]['6'], False, text_color)
		ckb_rect = pygame.Rect(0.3*WIDTH, 0.15*HEIGHT, WIDTH*0.4, HEIGHT*0.15)
		ckb_rect_border = ckb_rect.inflate(15, 15)
		rect = text.get_rect(center=ckb_rect.center)
		pygame.draw.rect(self.display_surface, border_color, ckb_rect_border, border_radius=20)
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, ckb_rect, border_radius=20)
		self.display_surface.blit(text, rect)

	def music_volume_button(self):
		if self.active == 'mv':
			text_color = TEXT_COLOR
			border_color = UI_BORDER_COLOR_ACTIVE
			if pygame.key.get_pressed()[pygame.K_RETURN]:
				states.current_state = states.VOLUME
				time.sleep(0.2)
		else:
			text_color = 'gold'
			border_color = UI_BORDER_COLOR
		temp_font = pygame.font.Font(UI_FONT, int(HEIGHT/24))
		text = temp_font.render(words.words[words.current_language]['7'], False, text_color)
		mv_rect = pygame.Rect(0.3*WIDTH, 0.45*HEIGHT, WIDTH*0.4, HEIGHT*0.15)
		mv_rect_border = mv_rect.inflate(15, 15)
		rect = text.get_rect(center=mv_rect.center)
		pygame.draw.rect(self.display_surface, border_color, mv_rect_border, border_radius=20)
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, mv_rect, border_radius=20)
		self.display_surface.blit(text, rect)

	def chose_language_button(self):
		if self.active == 'clb':
			text_color = TEXT_COLOR
			border_color = UI_BORDER_COLOR_ACTIVE
			if pygame.key.get_pressed()[pygame.K_RETURN]:
				states.current_state = states.CHOSE_LANGUAGE
				time.sleep(0.2)
		else:
			text_color = 'gold'
			border_color = UI_BORDER_COLOR
		temp_font = pygame.font.Font(UI_FONT, int(HEIGHT/24))
		text = temp_font.render(words.words[words.current_language]['8'], False, text_color)
		clb_rect = pygame.Rect(0.3*WIDTH, 0.74*HEIGHT, WIDTH*0.4, HEIGHT*0.15)
		clb_rect_border = clb_rect.inflate(15, 15)
		rect = text.get_rect(center=clb_rect.center)
		pygame.draw.rect(self.display_surface, border_color, clb_rect_border, border_radius=20)
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, clb_rect, border_radius=20)
		self.display_surface.blit(text, rect)

	def selection_keys(self, key):
		match key:
			case pygame.K_DOWN:
				match self.active:
					case None:
						self.active = 'ckb'
					case 'back':
						self.active = 'ckb'
					case 'ckb':
						self.active = 'mv'
					case 'mv':
						self.active = 'clb'
					case 'clb':
						pass
			case pygame.K_UP:
				match self.active:
					case None:
						self.active = 'ckb'
					case 'clb':
						self.active = 'mv'
					case 'mv':
						self.active = 'ckb'
					case 'ckb':
						self.active = 'back'
					case 'back':
						pass

	def run(self):
		self.general_appearance()
		self.back_button()
		self.chose_keybinds_button()
		self.music_volume_button()
		self.chose_language_button()