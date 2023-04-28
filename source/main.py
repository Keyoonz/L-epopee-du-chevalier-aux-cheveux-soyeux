import pygame, sys, states, audio, keybinds
from data import *
from menu import Menu
from words import *
from options import Settings
from chose_keybinds import Keybinds
from volume import Volume
import volume
from chose_language import Language
from load_game import Load
from game import Game
from pause import Pause
from inventory import Inventory
from item import Item

class Main:
    def __init__(self) -> None:
        pygame.init()
        pygame.font.init()
        pygame.mixer.set_num_channels(4)
        pygame.mouse.set_visible(0)
        self.screen = pygame.display.set_mode((WIDTH,HEIGHT))
        pygame.display.set_caption('L\'Epopee du Chevalier aux Cheveux Soyeux')
        pygame.display.set_icon(pygame.image.load('graphics/icon/icon.png').convert_alpha())
        self.clock = pygame.time.Clock()

        self.menu = Menu()
        self.settings = Settings()
        self.chose_keybinds = Keybinds()
        self.volume = Volume()
        self.chose_language = Language()
        self.inventory = Inventory()
        self.game = Game(self.inventory)
        self.load = Load()
        self.pause = Pause()

        volume.getAudio()

    def run(self) -> None:
        while True:
            for event in pygame.event.get():
                match event.type:
                    case pygame.QUIT:
                        pygame.quit()
                        sys.exit()
                    case pygame.KEYDOWN:
                        if states.current_state == states.INVENTORY:
                            self.inventory.selection_keys(event.key)
                        if event.key == pygame.K_F3 and states.current_state == states.PLAYING:
                            self.game.level.visible_sprites.show_hitboxes = not self.game.level.visible_sprites.show_hitboxes
                        if (event.key == pygame.K_UP or event.key == pygame.K_DOWN) and not self.chose_keybinds.chosing_keybind and states.current_state != states.PLAYING:
                            audio.effects_channel.set_volume(audio.volume/10)
                            audio.effects_channel.play(audio.EFFECTS['menu_selection'])
                            if states.current_state == states.MENU:
                                self.menu.selection_keys(event.key)
                            elif states.current_state == states.OPTIONS:
                                self.settings.selection_keys(event.key)
                            elif states.current_state == states.CHOSE_KEYBINDS:
                                self.chose_keybinds.selection_keys(event.key)
                            elif states.current_state == states.VOLUME:
                                self.volume.selection_keys(event.key)
                            elif states.current_state == states.LOAD:
                                self.load.selection_keys(event.key)
                            elif states.current_state == states.CHOSE_LANGUAGE:
                                self.chose_language.selection_keys(event.key)
                            elif states.current_state == states.PAUSE:
                                self.pause.selection_keys(event.key)
                        if (event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT) and states.current_state != states.PLAYING:
                            if states.current_state == states.VOLUME or states.current_state == states.CHOSE_LANGUAGE:
                                audio.effects_channel.set_volume(audio.volume/10)
                                audio.effects_channel.play(audio.EFFECTS['menu_selection'])
                                self.volume.input(event.key)
                                self.chose_language.selection_keys(event.key)
                        if event.key == pygame.K_ESCAPE:
                            match states.current_state:
                                case states.PAUSE:
                                    states.current_state = states.PLAYING
                                case states.PLAYING:
                                    pygame.image.save_extended(self.screen, 'graphics/temp.png')
                                    states.current_state = states.PAUSE
                        if event.key == pygame.K_RETURN and states.current_state != states.PLAYING:
                            audio.effects_channel.play(audio.EFFECTS['menu_enter'])
                        if event.key == pygame.K_TAB and not self.game.level.player.interacting:
                            if states.current_state == states.INVENTORY:
                                self.inventory.intro = False
                            elif states.current_state == states.PLAYING:
                                pygame.image.save_extended(self.screen, 'graphics/temp.png')
                                self.inventory.bg = pygame.image.load('graphics/temp.png')
                                self.inventory.intro = True
                                states.current_state = states.INVENTORY
                        if event.key == keybinds.keybinds['INTERACT'] and states.current_state == states.PLAYING:
                            self.game.level.player.interact()

            current_item.clear()
            if self.inventory.items != []:
                current_item.append(self.inventory.items[self.inventory.selected_item])

            match states.current_state:
                case states.MENU:
                    self.screen.fill('black')
                    self.menu.run()
                case states.PLAYING:
                    self.screen.fill('black')
                    self.game.run()
                case states.OPTIONS:
                    self.screen.fill('black')
                    self.settings.run()
                case states.CHOSE_KEYBINDS:
                    self.screen.fill('black')
                    self.chose_keybinds.run()
                case states.VOLUME:
                    self.screen.fill('black')
                    self.volume.run()
                case states.LOAD:
                    self.screen.fill('black')
                    self.load.run()
                case states.CHOSE_LANGUAGE:
                    self.screen.fill('black')
                    self.chose_language.run()
                case states.PAUSE:
                    states.before_options = 'P'
                    self.screen.fill('black')
                    self.pause.run()
                case states.INVENTORY:
                    self.screen.fill('black')
                    self.inventory.run()

            if self.game.level.player.end:
                self.reset()
            
            pygame.display.update()
            self.clock.tick(FPS)

    def reset(self) -> None:
        self.menu = Menu()
        self.settings = Settings()
        self.chose_keybinds = Keybinds()
        self.volume = Volume()
        self.chose_language = Language()
        self.inventory = Inventory()
        self.game = Game(self.inventory)
        self.load = Load()
        self.pause = Pause()

if __name__ == '__main__':
    main = Main()
    main.run()