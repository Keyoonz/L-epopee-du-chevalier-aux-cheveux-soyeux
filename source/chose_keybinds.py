import pygame, states, time, words
from data import *
from keybinds import *

class Keybinds:
    def __init__(self):
        self.display_surface = pygame.display.get_surface()
        self.chosing_keybind = False
        self.chosen_keybind = None
        self.active = None
        self.draw_message_auth = (False, 0)

    def general_appearance(self):
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
    
    def keybinds(self):
        Y_OFFSET = 0.2*HEIGHT
        for i in range(len(possible_keybinds)):
            if self.active == f'kb{i}':
                text_color = TEXT_COLOR
                border_color = UI_BORDER_COLOR_ACTIVE
                if pygame.key.get_pressed()[pygame.K_RETURN]:
                    self.draw_message_auth = (True, (0.1*HEIGHT*i +Y_OFFSET))
                    self.chosing_keybind = True
                    self.chosen_keybind = possible_keybinds[i]
            else:
                text_color = 'gold'
                border_color = UI_BORDER_COLOR
            temp_font = pygame.font.Font(UI_FONT, int(HEIGHT/24))
            text = temp_font.render(possible_keybinds[i], False, text_color)
            key_rect = pygame.Rect(0.05*WIDTH, 0.1*HEIGHT*i +Y_OFFSET, 0.2*WIDTH, 0.06*HEIGHT)
            key_rect_border = key_rect.inflate(9, 9)
            rect = text.get_rect(center=key_rect.center)
            pygame.draw.rect(self.display_surface, border_color, key_rect_border, border_radius=5)
            pygame.draw.rect(self.display_surface, UI_BG_COLOR, key_rect, border_radius=5)
            self.display_surface.blit(text, rect)
            
            key_text = temp_font.render(pygame.key.name(keybinds[possible_keybinds[i]]), False, TEXT_COLOR)
            key_back_rect = pygame.Rect(0.27*WIDTH, 0.1*HEIGHT*i +Y_OFFSET, 0.2*WIDTH, 0.06*HEIGHT)
            key_back_rect_border = key_back_rect.inflate(9, 9)
            key_rect = key_text.get_rect(center=key_back_rect.center)
            pygame.draw.rect(self.display_surface, UI_BORDER_COLOR, key_back_rect_border, border_radius=5)
            pygame.draw.rect(self.display_surface, UI_BG_COLOR, key_back_rect, border_radius=5)
            self.display_surface.blit(key_text, key_rect)
        
        if self.chosing_keybind:
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN:
                    keybinds[self.chosen_keybind] = event.key
                    for key in keybinds:
                        if keybinds[key] == event.key and key != self.chosen_keybind:
                            keybinds[key] = -1
                    self.chosing_keybind = False
                    self.chosen_keybind = None
                    self.draw_message_auth = (False, 0)
                    saveKeybinds()

    def draw_message(self):
        if self.draw_message_auth[0]:
            temp_font = pygame.font.Font(UI_FONT, 25)
            text = temp_font.render(words.words[words.current_language]['9'], False, UI_BG_COLOR)
            rect = text.get_rect(topleft=(0.5*WIDTH, self.draw_message_auth[1]))
            self.display_surface.blit(text, rect)
            
    def selection_keys(self, key):
        match key:
            case pygame.K_DOWN:
                match self.active:
                    case None:
                        self.active = 'kb0'
                    case 'back':
                        self.active = 'kb0'
                    case 'kb0':
                        self.active = 'kb1'
                    case 'kb1':
                        self.active = 'kb2'
                    case 'kb2':
                        self.active = 'kb3'
                    case 'kb3':
                        self.active = 'kb4'
                    case 'kb4':
                        self.active = 'kb5'
                    case 'kb5':
                        self.active = 'kb6'
                    case 'kb6':
                        self.active = 'kb7'
                    case 'kb7':
                        pass
            case pygame.K_UP:
                match self.active:
                    case None:
                        self.active = 'kb0'
                    case 'back':
                        pass
                    case 'kb0':
                        self.active = 'back'
                    case 'kb1':
                        self.active = 'kb0'
                    case 'kb2':
                        self.active = 'kb1'
                    case 'kb3':
                        self.active = 'kb2'
                    case 'kb4':
                        self.active = 'kb3'
                    case 'kb5':
                        self.active = 'kb4'
                    case 'kb6':
                        self.active = 'kb5'
                    case 'kb7':
                        self.active = 'kb6'

    def run(self):
        self.general_appearance()
        self.back_button()
        self.keybinds()
        self.draw_message()