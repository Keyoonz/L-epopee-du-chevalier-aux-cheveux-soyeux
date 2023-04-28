import pygame
import sys
import time
import words
import states
import music
import audio
from data import *


class Menu:
    def __init__(self) -> None:
        self.font = pygame.font.Font(UI_FONT, int(HEIGHT/13))
        self.display_surface = pygame.display.get_surface()

        self.active = None

        self.hero_animation_frame = 0

        music.MUSIC['menu'].set_volume(music.volume)
        music.MUSIC['menu'].play(loops=-1)

    def hero_image(self) -> None:
        if self.hero_animation_frame > 240 and self.hero_animation_frame < 245:
            hero = pygame.image.load('graphics/menu/hero1.png').convert_alpha()
        elif self.hero_animation_frame > 245 and self.hero_animation_frame < 250:
            hero = pygame.image.load('graphics/menu/hero2.png').convert_alpha()
        elif self.hero_animation_frame > 250 and self.hero_animation_frame < 255:
            hero = pygame.image.load('graphics/menu/hero3.png').convert_alpha()
        elif self.hero_animation_frame > 255 and self.hero_animation_frame < 260:
            hero = pygame.image.load('graphics/menu/hero4.png').convert_alpha()
        elif self.hero_animation_frame > 260 and self.hero_animation_frame < 265:
            hero = pygame.image.load('graphics/menu/hero4.png').convert_alpha()
        else:
            hero = pygame.image.load('graphics/menu/hero.png').convert_alpha()
        hero = pygame.transform.scale(hero, (HEIGHT, HEIGHT))
        hero_rect = hero.get_rect(topleft=(0, 0))
        self.display_surface.blit(hero, hero_rect)

    def main_title(self):
        main_title = pygame.image.load(
            'graphics/menu/main_title.png').convert_alpha()
        main_title_rect = main_title.get_rect(topleft=(10, 10))
        self.display_surface.blit(main_title, main_title_rect)

    def overlay(self):
        overlay = pygame.image.load('graphics/menu/image_overlay.png')
        overlay = pygame.transform.scale(overlay, (HEIGHT, HEIGHT))
        overlay_rect = overlay.get_rect(topleft=(0, 0))
        self.display_surface.blit(overlay, overlay_rect)

    def button_part(self):
        half_window = pygame.Rect(0.56*WIDTH, 0, 0.56*WIDTH, HEIGHT)
        pygame.draw.rect(self.display_surface, '#2c2d2c', half_window)

    def play_button(self):
        if self.active == 'play':
            text_color = TEXT_COLOR
            border_color = UI_BORDER_COLOR_ACTIVE
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                music.MUSIC['menu'].stop()
                music.MUSIC['game'].set_volume(music.volume/10)
                music.MUSIC['game'].play(loops=-1)
                states.current_state = states.PLAYING
                time.sleep(0.2)
        else:
            text_color = 'gold'
            border_color = UI_BORDER_COLOR
        text = self.font.render(
            words.words[words.current_language]['1'], False, text_color)
        play_rect = pygame.Rect(0.63*WIDTH, 0.16*HEIGHT, WIDTH/3.2, HEIGHT/7.2)
        play_rect_border = play_rect.inflate(15, 15)
        rect = text.get_rect(center=play_rect.center)
        pygame.draw.rect(self.display_surface, border_color,
                         play_rect_border, border_radius=20)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         play_rect, border_radius=20)
        self.display_surface.blit(text, rect)

    def settings_button(self):
        if self.active == 'settings':
            text_color = TEXT_COLOR
            border_color = UI_BORDER_COLOR_ACTIVE
            if pygame.key.get_pressed()[pygame.K_RETURN]:
                states.current_state = states.OPTIONS
                before_options = 'M'
                time.sleep(0.2)
        else:
            text_color = 'gold'
            border_color = UI_BORDER_COLOR
        text = self.font.render(
            words.words[words.current_language]['2'], False, text_color)
        settings_rect = pygame.Rect(
            0.63*WIDTH, 0.45*HEIGHT, WIDTH/3.2, HEIGHT/7.2)
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
                pygame.quit()
                sys.exit()
        else:
            text_color = 'gold'
            border_color = UI_BORDER_COLOR
        text = self.font.render(
            words.words[words.current_language]['3'], False, text_color)
        quit_rect = pygame.Rect(0.63*WIDTH, 0.74*HEIGHT, WIDTH/3.2, HEIGHT/7.2)
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
                        self.active = 'play'
                    case 'play':
                        self.active = 'settings'
                    case 'settings':
                        self.active = 'quit'
                    case 'quit':
                        pass
            case pygame.K_UP:
                match self.active:
                    case None:
                        self.active = 'play'
                    case 'quit':
                        self.active = 'settings'
                    case 'settings':
                        self.active = 'play'
                    case 'play':
                        pass

    def run(self) -> None:
        music.MUSIC['menu'].set_volume(music.volume/10)
        self.hero_image()
        self.main_title()
        self.overlay()
        self.button_part()
        self.play_button()
        self.settings_button()
        self.quit_button()
        self.hero_animation_frame += 1
        if self.hero_animation_frame > 270:
            self.hero_animation_frame = 0