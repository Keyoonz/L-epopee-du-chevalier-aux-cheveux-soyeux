import pygame
import states
import time
import words
import sys
from data import *
import music


class Pause:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.active = None

    def general_appearance(self):
        bg = pygame.image.load('graphics/temp.png').convert_alpha()
        bg.set_alpha(50)
        self.display_surface.blit(bg, bg.get_rect())

    def back_button(self):
        if self.active == 'back':
            text_color = TEXT_COLOR
            border_color = UI_BORDER_COLOR_ACTIVE
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                states.current_state = states.PLAYING
                time.sleep(0.2)
        else:
            text_color = 'gold'
            border_color = UI_BORDER_COLOR
        temp_font = pygame.font.Font(UI_FONT, int(HEIGHT/21))
        text = temp_font.render(
            words.words[words.current_language]['14'], False, text_color)
        back_rect = pygame.Rect(0.5*WIDTH-((WIDTH/2.3)/2),
                                0.15*HEIGHT, WIDTH/2.3, HEIGHT/7.2)
        back_rect_border = back_rect.inflate(15, 15)
        rect = text.get_rect(center=back_rect.center)
        pygame.draw.rect(self.display_surface, border_color,
                         back_rect_border, border_radius=20)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         back_rect, border_radius=20)
        self.display_surface.blit(text, rect)

    def settings_button(self):
        if self.active == 'settings':
            text_color = TEXT_COLOR
            border_color = UI_BORDER_COLOR_ACTIVE
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                states.current_state = states.OPTIONS
                time.sleep(0.2)
        else:
            text_color = 'gold'
            border_color = UI_BORDER_COLOR
        temp_font = pygame.font.Font(UI_FONT, int(HEIGHT/21))
        text = temp_font.render(
            words.words[words.current_language]['2'], False, text_color)
        settings_rect = pygame.Rect(
            0.5*WIDTH-((WIDTH/2.3)/2), 0.45*HEIGHT, WIDTH/2.3, HEIGHT/7.2)
        settings_rect_border = settings_rect.inflate(15, 15)
        rect = text.get_rect(center=settings_rect.center)
        pygame.draw.rect(self.display_surface, border_color,
                         settings_rect_border, border_radius=20)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         settings_rect, border_radius=20)
        self.display_surface.blit(text, rect)

    def quit_button(self):
        if self.active == 'quit':
            text_color = TEXT_COLOR
            border_color = UI_BORDER_COLOR_ACTIVE
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                states.current_state = states.MENU
                music.MUSIC[music.current_music].stop()
                music.MUSIC['menu'].set_volume(music.volume/10)
                music.MUSIC['menu'].play()
                time.sleep(0.2)
        else:
            text_color = 'gold'
            border_color = UI_BORDER_COLOR
        temp_font = pygame.font.Font(UI_FONT, int(HEIGHT/21))
        text = temp_font.render(
            words.words[words.current_language]['15'], False, text_color)
        quit_rect = pygame.Rect(0.5*WIDTH-((WIDTH/2.3)/2),
                                0.75*HEIGHT, WIDTH/2.3, HEIGHT/7.2)
        quit_rect_border = quit_rect.inflate(15, 15)
        rect = text.get_rect(center=quit_rect.center)
        pygame.draw.rect(self.display_surface, border_color,
                         quit_rect_border, border_radius=20)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         quit_rect, border_radius=20)
        self.display_surface.blit(text, rect)

    def selection_keys(self, key):
        match key:
            case pygame.K_DOWN:
                match self.active:
                    case None:
                        self.active = 'back'
                    case 'back':
                        self.active = 'settings'
                    case 'settings':
                        self.active = 'quit'
                    case 'quit':
                        pass
            case pygame.K_UP:
                match self.active:
                    case None:
                        self.active = 'back'
                    case 'quit':
                        self.active = 'settings'
                    case 'settings':
                        self.active = 'back'
                    case 'back':
                        pass

    def run(self):
        self.general_appearance()
        self.back_button()
        self.settings_button()
        self.quit_button()
