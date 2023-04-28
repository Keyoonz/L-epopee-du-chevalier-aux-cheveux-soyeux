import pygame
import states
import time
import words
import music
import audio
import json
from data import *


class Volume:
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
                states.current_state = states.OPTIONS
                time.sleep(0.3)
        else:
            text_color = 'gold'
            border_color = UI_BORDER_COLOR
        temp_font = pygame.font.Font(UI_FONT, int(HEIGHT/29))
        text = temp_font.render(
            words.words[words.current_language]['4'], False, text_color)
        back_rect = pygame.Rect(0.05*WIDTH, 0.07*HEIGHT,
                                0.1*WIDTH, 0.06*HEIGHT)
        back_rect_border = back_rect.inflate(9, 9)
        rect = text.get_rect(center=back_rect.center)
        pygame.draw.rect(self.display_surface, border_color,
                         back_rect_border, border_radius=5)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR,
                         back_rect, border_radius=5)
        self.display_surface.blit(text, rect)

    def music_volume_slider(self):
        cursor_position = 0.15*WIDTH + music.volume*(0.7*WIDTH/10)
        if self.active == 'mvs':
            border_color = UI_BORDER_COLOR_ACTIVE
            cursor_color = 'gold'
            text_color = TEXT_COLOR
        else:
            border_color = UI_BORDER_COLOR
            cursor_color = '#949494'
            text_color = '#949494'

        bg_rect = pygame.Rect(0.1*WIDTH, 0.2*HEIGHT, 0.8*WIDTH, 0.3*HEIGHT)
        bg_rect_border = bg_rect.inflate(7, 7)
        pygame.draw.rect(self.display_surface, border_color, bg_rect_border)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        line_rect = pygame.Rect(0.15*WIDTH, 0.34*HEIGHT,
                                0.7*WIDTH, 0.02*HEIGHT)
        pygame.draw.rect(self.display_surface, '#949494', line_rect)

        cursor = pygame.Rect(cursor_position, 0.32*HEIGHT,
                             0.01*WIDTH, 0.06*HEIGHT)
        pygame.draw.rect(self.display_surface, cursor_color, cursor)

        music_volume_mute = pygame.image.load(
            'graphics/icon/volume-mute-icon.png').convert_alpha()
        music_volume_mute = pygame.transform.scale(
            music_volume_mute, (WIDTH/24, HEIGHT/17))
        music_volume_up = pygame.image.load(
            'graphics/icon/volume-icon.png').convert_alpha()
        music_volume_up = pygame.transform.scale(
            music_volume_up, (WIDTH/24, HEIGHT/18))
        music_volume_mute_rect = music_volume_mute.get_rect(
            topleft=(0.025*WIDTH, 0.315*HEIGHT))
        music_volume_up_rect = music_volume_up.get_rect(
            topleft=(0.925*WIDTH, 0.315*HEIGHT))
        self.display_surface.blit(music_volume_mute, music_volume_mute_rect)
        self.display_surface.blit(music_volume_up, music_volume_up_rect)

        temp_font = pygame.font.Font(UI_FONT, int(HEIGHT/18))
        text = temp_font.render(
            words.words[words.current_language]['12'], False, text_color)
        rect = text.get_rect(midbottom=(
            bg_rect_border.midtop[0], bg_rect_border.midtop[1] + 75))
        self.display_surface.blit(text, rect)

    def effects_volume_slider(self):
        cursor_position = 0.15*WIDTH + audio.volume*(0.7*WIDTH/10)
        if self.active == 'evs':
            border_color = UI_BORDER_COLOR_ACTIVE
            cursor_color = 'gold'
            text_color = TEXT_COLOR
        else:
            border_color = UI_BORDER_COLOR
            cursor_color = '#949494'
            text_color = '#949494'

        bg_rect = pygame.Rect(0.1*WIDTH, 0.6*HEIGHT, 0.8*WIDTH, 0.3*HEIGHT)
        bg_rect_border = bg_rect.inflate(7, 7)
        pygame.draw.rect(self.display_surface, border_color, bg_rect_border)
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg_rect)

        line_rect = pygame.Rect(0.15*WIDTH, 0.74*HEIGHT,
                                0.7*WIDTH, 0.02*HEIGHT)
        pygame.draw.rect(self.display_surface, '#949494', line_rect)

        cursor = pygame.Rect(cursor_position, 0.72*HEIGHT,
                             0.01*WIDTH, 0.06*HEIGHT)
        pygame.draw.rect(self.display_surface, cursor_color, cursor)

        effects_volume_mute = pygame.image.load(
            'graphics/icon/volume-mute-icon.png').convert_alpha()
        effects_volume_mute = pygame.transform.scale(
            effects_volume_mute, (WIDTH/24, HEIGHT/17))
        effects_volume_up = pygame.image.load(
            'graphics/icon/volume-icon.png').convert_alpha()
        effects_volume_up = pygame.transform.scale(
            effects_volume_up, (WIDTH/24, HEIGHT/18))
        effects_volume_mute_rect = effects_volume_mute.get_rect(
            topleft=(0.025*WIDTH, 0.715*HEIGHT))
        effects_volume_up_rect = effects_volume_up.get_rect(
            topleft=(0.925*WIDTH, 0.715*HEIGHT))
        self.display_surface.blit(
            effects_volume_mute, effects_volume_mute_rect)
        self.display_surface.blit(effects_volume_up, effects_volume_up_rect)

        temp_font = pygame.font.Font(UI_FONT, int(HEIGHT/18))
        text = temp_font.render(
            words.words[words.current_language]['13'], False, text_color)
        rect = text.get_rect(midbottom=(
            bg_rect_border.midtop[0], bg_rect_border.midtop[1] + 75))
        self.display_surface.blit(text, rect)

    def input(self, key):
        if self.active == 'mvs':
            match key:
                case pygame.K_LEFT:
                    if music.volume > 0:
                        music.volume -= 1
                    else:
                        pass
                case pygame.K_RIGHT:
                    if music.volume < 10:
                        music.volume += 1
                    else:
                        pass
        if self.active == 'evs':
            match key:
                case pygame.K_LEFT:
                    if audio.volume > 0:
                        audio.volume -= 1
                    else:
                        pass
                case pygame.K_RIGHT:
                    if audio.volume < 10:
                        audio.volume += 1
                    else:
                        pass
        saveAudio()

    def selection_keys(self, key):
        match key:
            case pygame.K_DOWN:
                match self.active:
                    case None:
                        self.active = 'mvs'
                    case 'back':
                        self.active = 'mvs'
                    case 'mvs':
                        self.active = 'evs'
                    case 'evs':
                        pass
            case pygame.K_UP:
                match self.active:
                    case None:
                        self.active = 'mvs'
                    case 'evs':
                        self.active = 'mvs'
                    case 'mvs':
                        self.active = 'back'
                    case 'back':
                        pass

    def run(self):
        music.MUSIC['menu'].set_volume(music.volume/10)
        music.MUSIC['game'].set_volume(music.volume/10)
        self.general_appearance()
        self.back_button()
        self.music_volume_slider()
        self.effects_volume_slider()


def saveAudio():
    audio_file = open('settings/volume.json', 'w')
    audio_settings = {"music": music.volume, "audio": audio.volume}
    json.dump(audio_settings, audio_file)
    audio_file.close()

def getAudio():
    audio_file = open('settings/volume.json', 'r')
    audio_settings = json.load(audio_file)
    music.volume = audio_settings['music']
    audio.volume = audio_settings['audio']
    audio_file.close()
