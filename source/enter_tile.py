from entity import Entity
import pygame, words
from data import *
from support import *
from text import Text
from tile import Tile

class Enter_Tile(Entity):
    def __init__(self, pos, groups, visible_sprites):
        super().__init__(groups)

        self.display_surface = pygame.display.get_surface()

        self.rect = pygame.Rect(pos, (50, 50))

        self.arrows = []
        self.arrow_height = 1
        self.arrow_speed = 0.2

        self.visible_sprites = visible_sprites

        self.text = []
        
        
    def update(self, player):
        self.arrow_height += self.arrow_speed
        if self.arrow_height >= 10 or self.arrow_height <= 0:
            self.arrow_speed = -self.arrow_speed
        if self.rect.colliderect(player.hitbox):
            self.purpose_enter()
        else :
            for arrow in self.arrows:
                arrow.kill()
            self.arrows = []
            for text in self.text:
                text.kill()
            self.text = []

    def purpose_enter(self):
        if len(self.arrows)==0:
            self.arrows.append(Tile(self.rect.move(0,-30-TILESIZE).topleft, self.visible_sprites, 'interactive_ui', pygame.image.load("graphics/npc/general/arrow.png")))
            self.arrows[0].rect.centerx = self.rect.centerx
            self.text.append(Text(self.rect.move(75, -85-TILESIZE), self.visible_sprites, words.words[words.current_language]['18']))
            self.text[0].rect.centerx = self.rect.centerx
        else:
            self.arrows[0].kill()
            self.arrows = [Tile(self.rect.move(0,-30-TILESIZE-self.arrow_height).topleft, self.visible_sprites, 'interactive_ui', pygame.image.load("graphics/npc/general/arrow.png"))]
            self.arrows[0].rect.centerx = self.rect.centerx
            self.text[0].kill()
            self.text = [Text(self.rect.move(0, -85-TILESIZE), self.visible_sprites, words.words[words.current_language]['18'])]
            self.text[0].rect.centerx = self.rect.centerx