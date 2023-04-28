from entity import Entity
import pygame
from data import *
from debug import debug

class Arrow(Entity):
    def __init__(self, pos, groups, direction, obstacle_sprites):
        super().__init__(groups)

        self.display_surface = pygame.display.get_surface()
        self.obstacle_sprites = obstacle_sprites
        self.direction = direction
        self.image = pygame.image.load('graphics/bows/general/arrow.png')
        if self.direction == 'up':
            self.direction = pygame.math.Vector2(0, -1)
            self.image = pygame.transform.rotate(self.image, 90)
        elif self.direction == 'down':
            self.direction = pygame.math.Vector2(0, 10)
            self.image = pygame.transform.rotate(self.image, -90)
        elif self.direction == 'left':
            self.direction = pygame.math.Vector2(-1, 0)
            self.image = pygame.transform.rotate(self.image, 180)
        elif self.direction == 'right':
            self.direction = pygame.math.Vector2(10, 0)
        self.rect = self.image.get_rect(center= pos)
        self.hitbox = self.rect
        self.last_hitbox = self.hitbox.copy()
        self.has_stopped_moving = False
        
        
    def update(self):
        self.move(weapon_data['arrow_speed'])
        if self.last_hitbox.x == self.hitbox.x and self.last_hitbox.y == self.hitbox.y:
            self.has_stopped_moving = True
        self.last_hitbox = self.hitbox.copy()
        
        
        