import pygame, time, states, words
from data import *

class Language:
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
				states.current_state = states.OPTIONS
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

	def en_button(self):
		if self.active == 'eb':
			text_color = TEXT_COLOR
			border_color = UI_BORDER_COLOR_ACTIVE
			if pygame.key.get_pressed()[pygame.K_RETURN]:
				words.current_language = 'ENGLISH'
		else:
			text_color = 'gold'
			border_color = UI_BORDER_COLOR
		temp_font = pygame.font.Font(UI_FONT, int(HEIGHT/21))
		text = temp_font.render(words.words[words.current_language]['10'], False, text_color)
		en_rect = pygame.Rect(0.05*WIDTH, 0.4*HEIGHT, 0.4*WIDTH, 0.2*HEIGHT)
		en_rect_border = en_rect.inflate(9, 9)
		rect = text.get_rect(center = en_rect.center)
		pygame.draw.rect(self.display_surface, border_color, en_rect_border, border_radius=5)
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, en_rect, border_radius=5)
		self.display_surface.blit(text, rect)
    
	def fr_button(self):
		if self.active == 'fb':
			text_color = TEXT_COLOR
			border_color = UI_BORDER_COLOR_ACTIVE
			if pygame.key.get_pressed()[pygame.K_RETURN]:
				words.current_language = 'FRENCH'
		else:
			text_color = 'gold'
			border_color = UI_BORDER_COLOR
		temp_font = pygame.font.Font(UI_FONT, int(HEIGHT/21))
		text = temp_font.render(words.words[words.current_language]['11'], False, text_color)
		fr_rect = pygame.Rect(0.55*WIDTH, 0.4*HEIGHT, 0.4*WIDTH, 0.2*HEIGHT)
		fr_rect_border = fr_rect.inflate(9, 9)
		rect = text.get_rect(center = fr_rect.center)
		pygame.draw.rect(self.display_surface, border_color, fr_rect_border, border_radius=5)
		pygame.draw.rect(self.display_surface, UI_BG_COLOR, fr_rect, border_radius=5)
		self.display_surface.blit(text, rect)

	def selection_keys(self, key):
		match key:
			case pygame.K_DOWN:
				match self.active:
					case None:
						self.active = 'eb'
					case 'back':
						self.active = 'eb'
					case 'eb':
						self.active = 'fb'
					case 'fb':
						pass
			case pygame.K_UP:
				match self.active:
					case None:
						self.active = 'eb'
					case 'back':
						pass
					case 'eb':
						self.active = 'back'
					case 'fb':
						self.active = 'eb'
			case pygame.K_RIGHT:
				match self.active:
					case None:
						self.active = 'eb'
					case 'back':
						pass
					case 'fb':
						pass
					case 'eb':
						self.active = 'fb'
			case pygame.K_LEFT:
				match self.active:
					case None:
						self.active = 'eb'
					case 'back':
						pass
					case 'eb':
						pass
					case 'fb':
						self.active = 'eb'
		save_language()
    
	def run(self):
		self.general_appearance()
		self.back_button()
		self.en_button()
		self.fr_button()
		MT['0'][5] = words.words[words.current_language]['19']
		MT['1'][5] = words.words[words.current_language]['20']
		MT['2'][5] = words.words[words.current_language]['19']
		MT['3'][5] = words.words[words.current_language]['21']
		MT['4'][5] = words.words[words.current_language]['22']