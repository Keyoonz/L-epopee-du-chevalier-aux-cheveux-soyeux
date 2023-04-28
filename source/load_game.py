import pygame, states, time, words, music
from data import *

class Load:
	def __init__(self) -> None:
		self.display_surface = pygame.display.get_surface()
		self.active = None

	def general_appearance(self) -> None:
		bg = pygame.Rect(0, 0, WIDTH, HEIGHT)
		pygame.draw.rect(self.display_surface, '#2c2d2c', bg)

	def back_button(self):
		if self.active == 'back':
			text_color = TEXT_COLOR
			border_color = UI_BORDER_COLOR_ACTIVE
			if pygame.key.get_pressed()[pygame.K_RETURN]:
				states.current_state = states.MENU
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

	def load_button_1(self):
		if self.active == 'lb1':
			text_color = TEXT_COLOR
			border_color = UI_BORDER_COLOR_ACTIVE
			if pygame.key.get_pressed()[pygame.K_RETURN]:
				music.MUSIC['menu'].stop()
				music.MUSIC['game'].set_volume(music.volume/10)
				music.MUSIC['game'].play(loops=-1)
				states.current_state = states.PLAYING
		else:
			text_color = 'gold'
			border_color = UI_BORDER_COLOR
		temp_font = pygame.font.Font(UI_FONT, int(HEIGHT/24))
		text = temp_font.render(words.words[words.current_language]['5'], False, text_color)
		lb1_rect = pygame.Rect(0.1*WIDTH, 0.23*HEIGHT, 0.8*WIDTH, 0.15*HEIGHT)
		lb1_rect_border = lb1_rect.inflate(9, 9)
		rect = text.get_rect(center=lb1_rect.center)
		pygame.draw.rect(self.display_surface, border_color, lb1_rect_border, border_radius=5)
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, lb1_rect, border_radius=5)
		self.display_surface.blit(text, rect)

	def load_button_2(self):
		if self.active == 'lb2':
			text_color = TEXT_COLOR
			border_color = UI_BORDER_COLOR_ACTIVE
		else:
			text_color = 'gold'
			border_color = UI_BORDER_COLOR
		temp_font = pygame.font.Font(UI_FONT, int(HEIGHT/24))
		text = temp_font.render(words.words[words.current_language]['5'], False, text_color)
		lb2_rect = pygame.Rect(0.1*WIDTH, 0.5*HEIGHT, 0.8*WIDTH, 0.15*HEIGHT)
		lb2_rect_border = lb2_rect.inflate(9, 9)
		rect = text.get_rect(center=lb2_rect.center)
		pygame.draw.rect(self.display_surface, border_color, lb2_rect_border, border_radius=5)
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, lb2_rect, border_radius=5)
		self.display_surface.blit(text, rect)

	def load_button_3(self):
		if self.active == 'lb3':
			text_color = TEXT_COLOR
			border_color = UI_BORDER_COLOR_ACTIVE
		else:
			text_color = 'gold'
			border_color = UI_BORDER_COLOR
		temp_font = pygame.font.Font(UI_FONT, int(HEIGHT/24))
		text = temp_font.render(words.words[words.current_language]['5'], False, text_color)
		lb3_rect = pygame.Rect(0.1*WIDTH, 0.75*HEIGHT, 0.8*WIDTH, 0.15*HEIGHT)
		lb3_rect_border = lb3_rect.inflate(9, 9)
		rect = text.get_rect(center=lb3_rect.center)
		pygame.draw.rect(self.display_surface, border_color, lb3_rect_border, border_radius=5)
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, lb3_rect, border_radius=5)
		self.display_surface.blit(text, rect)


	def selection_keys(self, key):
		match key:
			case pygame.K_DOWN:
				match self.active:
					case None:
						self.active = 'lb1'
					case 'back':
						self.active = 'lb1'
					case 'lb1':
						self.active = 'lb2'
					case 'lb2':
						self.active = 'lb3'
					case 'lb3':
						pass
			case pygame.K_UP:
				match self.active:
					case None:
						self.active = 'lb1'
					case 'back':
						pass
					case 'lb1':
						self.active = 'back'
					case 'lb2':
						self.active = 'lb1'
					case 'lb3':
						self.active = 'lb2'

	def run(self):
		self.general_appearance()
		self.back_button()
		self.load_button_1()
		self.load_button_2()
		self.load_button_3()