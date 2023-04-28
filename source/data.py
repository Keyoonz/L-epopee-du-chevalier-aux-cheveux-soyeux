import json, pygame, tkinter, pygame.font, pygame.image, words
from pygame.locals import *
from words import *

# game data
root = tkinter.Tk()
WIDTH = root.winfo_screenwidth()
HEIGHT = root.winfo_screenheight()
# WIDTH = 1280
# HEIGHT = 720
FPS = 120
UI_FONT = 'graphics/font/font.ttf'
UI_BG_COLOR = '#222222'
UI_BORDER_COLOR = '#111111'
TEXT_COLOR = '#EEEEEE'
UI_BORDER_COLOR_ACTIVE = 'gold'
TILESIZE = WIDTH/20
HITBOX_OFFSET = {
    'player': -36,
    'object': -40,
    'grass': -10,
    'invisible': 0,
    'heart': 0,
    'semiheart': 0,
    'interactive_ui': 0,
    'light_weapon': 0,
    'arrow': 0,
    'mana': 0}

load_words()
load_dialogues()

# maps transitions
MT = {
    '0': ['map1', 'map2', 'lr', False, "item:heartinventory", words.words[words.current_language]['19']],
    '1': ['map1', 'map3', 'bt', False, "item:bow", words.words[words.current_language]['20']],
    '2': ['map1', 'map4', 'rl', False, "item:heartinventory", words.words[words.current_language]['19']],
    '3': ['map4', 'map5', 'bt', False, "quest:wizardquest", words.words[words.current_language]['21']],
    '4': ['map2', 'map6', 'lr', False, "item:boots", words.words[words.current_language]['22']],
    '5': ['map3', 'map7', 'io', True, None]
}

# weapon data
weapon_data = {
    'sword1': {'damage': 1},
    'magic1': {'damage': 1},
    'magic_range': 400,
    'bow1': {'damage': 4},
    'arrow_speed': HEIGHT/100
}

# foes data
monster_data = {
    'slime': {'damage': .5, 'life': 2, 'speed': HEIGHT/400, 'attack_radius': WIDTH/30, 'notice_radius': WIDTH/4.27, 'resistance': .8},
    'goblin': {'damage': 1, 'life': 4, 'speed': HEIGHT/300, 'attack_radius': WIDTH/20, 'notice_radius': WIDTH/4, 'resistance': .1}
}

boss_data = {
    'chevoeuil': {'damage': 2, 'life': 60, 'speed': HEIGHT/400, 'attack_radius': WIDTH/20, 'notice_radius': 100000, 'resistance': .8}
}

#hearts_available
items_available = []

#font
_circle_cache = {}
def _circlepoints(r):
    r = int(round(r))
    if r in _circle_cache:
        return _circle_cache[r]
    x, y, e = r, 0, 1 - r
    _circle_cache[r] = points = []
    while x >= y:
        points.append((x, y))
        y += 1
        if e < 0:
            e += 2 * y - 1
        else:
            x -= 1
            e += 2 * (y - x) - 1
    points += [(y, x) for x, y in points if x > y]
    points += [(-x, y) for x, y in points if x]
    points += [(x, -y) for x, y in points if y]
    points.sort()
    return points

def render(text, font, gfcolor=pygame.Color('white'), ocolor=(0, 0, 0), opx=3):
    textsurface = font.render(text, True, gfcolor).convert_alpha()
    w = textsurface.get_width() + 2 * opx
    h = font.get_height()

    osurf = pygame.Surface((w, h + 2 * opx)).convert_alpha()
    osurf.fill((0, 0, 0, 0))

    surf = osurf.copy()

    osurf.blit(font.render(text, True, ocolor).convert_alpha(), (0, 0))

    for dx, dy in _circlepoints(opx):
        surf.blit(osurf, (dx + opx, dy + opx))

    surf.blit(textsurface, (opx, opx))
    return surf

def blit_text(surface, text, pos, font, color=pygame.Color('black')):
    words = [word.split(' ') for word in text.splitlines()]
    space = font.size(' ')[0]
    max_width, max_height = surface.get_size()
    x, y = pos
    for line in words:
        for word in line:
            word_surface = render(word, font)
            word_width, word_height = word_surface.get_size()
            if x + word_width >= max_width:
                x = pos[0]
                y += word_height
            surface.blit(word_surface, (x, y))
            x += word_width + space
        x = pos[0]
        y += word_height

#dialogue box
dialogue_box = []

current_item = []

quests = []