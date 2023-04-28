import pygame, random
from tile import Tile
from item import Item

def drop(pos, groups, inventory):
    a = random.randint(1, 4)
    if a != 1:
        return False
    b = random.randint(1, 10)
    if b in [1, 2, 3, 4, 5] and len(inventory.items) > 0:
        return Tile(pos, groups, 'heart', pygame.image.load('graphics/items/heart.png'))
    elif b in [6, 7, 8] and len(inventory.items) > 2:
        return Tile(pos, groups, 'mana', pygame.image.load('graphics/items/mana.png'))
    elif b in [9, 10] and len(inventory.items) > 3:
        return Tile(pos, groups, 'arrow', pygame.image.load('graphics/items/arrow.png'))