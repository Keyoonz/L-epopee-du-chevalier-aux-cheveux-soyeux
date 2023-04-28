import pygame, words
from entity import Entity
from tile import Tile
from data import *
from support import *
from text import Text
from ui import DialogueBox

class NPC(Entity):
    def __init__(self, npc_name, pos, groups, quests, important_sprites):
        super().__init__(groups)

        self.display_surface = pygame.display.get_surface()

        self.sprite_type = "npc"

        self.quests = quests
        self.current_quest = 0

        self.import_graphics(npc_name)
        self.status = "idle"
        self.animation_speed = 0.04
        self.image = self.animations[self.frame_index]

        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0, -35)
        self.arrows = []
        self.arrow_height = 1
        self.arrow_speed = 0.2

        self.important_sprites = important_sprites

        self.npc_name = npc_name
        self.dialogues = words.dialogues[words.current_language][self.npc_name]

        self.text = []

        self.dialogue_index = 1
        self.can_skip = False

    def import_graphics(self, name):
        self.animations = import_folder(f'graphics/npc/{name}')

    def animate(self):
        animation = self.animations

        self.arrow_height += self.arrow_speed
        if self.arrow_height >= 10 or self.arrow_height <= 0:
            self.arrow_speed = -self.arrow_speed

        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0
        
        self.image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, ((WIDTH/(1280/self.image.get_width())), (HEIGHT/(720/(self.image.get_height())))))
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def get_player_distance(self, player):
        npc_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - npc_vec).magnitude()

        return distance

    def update(self):
        self.animate()
        self.input()
        self.can_skip_cooldown()
        
    def npc_update(self, player):
        if self.status != "talking":
            if self.npc_name != 'tah_le_shamp':
                self.dialogues = words.dialogues[words.current_language][self.npc_name][str(self.quests[self.current_quest].current_subquest)]
            else:
                self.dialogues = words.dialogues[words.current_language][self.npc_name]['1']
        if self.get_player_distance(player) < 150 and self.status != "talking":
            self.purpose_talk()
            if not self in player.can_interact_with:
                player.can_interact_with.append(self)
        else :
            if self in player.can_interact_with:
                player.can_interact_with.remove(self)
            for arrow in self.arrows:
                arrow.kill()
            self.arrows = []
            for text in self.text:
                text.kill()
            self.text = []
        
        if self.status == "talking":
            self.dialogue(player)

    def purpose_talk(self):
        if len(self.arrows)==0:
            self.arrows.append(Tile(self.rect.move(0,-30).topleft, self.important_sprites, 'interactive_ui', pygame.image.load("graphics/npc/general/arrow.png")))
            self.arrows[0].rect.centerx = self.rect.centerx
            if self.npc_name != 'tah_le_shamp':
                self.text.append(Text(self.rect.move(75, -85), self.important_sprites, words.words[words.current_language]['16']))
            else:
                self.text.append(Text(self.rect.move(75, -85), self.important_sprites, words.words[words.current_language]['23']))
            self.text[0].rect.centerx = self.rect.centerx
        else:
            self.arrows[0].kill()
            self.arrows = [Tile(self.rect.move(0,-30-self.arrow_height).topleft, self.important_sprites, 'interactive_ui', pygame.image.load("graphics/npc/general/arrow.png"))]
            self.arrows[0].rect.centerx = self.rect.centerx
            self.text[0].kill()
            if self.npc_name != 'tah_le_shamp':
                self.text = [Text(self.rect.move(0, -85), self.important_sprites, words.words[words.current_language]['16'])]
            else:
                self.text = [Text(self.rect.move(0, -85), self.important_sprites, words.words[words.current_language]['23'])]
            self.text[0].rect.centerx = self.rect.centerx

    def interact(self, player):
        self.status = 'talking'
        self.dialogue_time = pygame.time.get_ticks()
        player.interacting = True

    def input(self):
        keys = pygame.key.get_pressed()

        if self.can_skip and keys[pygame.K_SPACE]:
            self.dialogue_time = pygame.time.get_ticks()
            self.dialogue_index += 1
            self.can_skip = False

    def can_skip_cooldown(self):
        current_time = pygame.time.get_ticks()

        if self.status == 'talking':
            if current_time - self.dialogue_time > 200:
                self.can_skip = True

    def dialogue(self, player):
        for quest in quests:
            quest.check_quest(self.npc_name, "talk")
        if self.dialogue_index <= len(self.dialogues) and self.npc_name != 'tah_le_shamp':
            dialogue_box.insert(0, DialogueBox(self.dialogues[str(self.dialogue_index)]))
        elif self.dialogue_index <= len(self.dialogues) and self.npc_name == 'tah_le_shamp':
            dialogue_box.insert(0, DialogueBox(self.dialogues))
            player.ending_game = True
            player.is_in_dialogue_transition = True
            if player.end_time == None:
                player.end_time = pygame.time.get_ticks()
        else:
            dialogue_box.clear()
            self.dialogue_index = 1
            self.status = 'idle'
            if not self.quests[self.current_quest] in quests and not self.npc_name != "tah_le_shamp":
                quests.append(self.quests[self.current_quest])
            player.interacting = False