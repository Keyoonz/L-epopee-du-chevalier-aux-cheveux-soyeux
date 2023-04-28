import pygame, music
from data import *
from support import *
from level import Level
from keybinds import keybinds
from tile import Tile
from text import Text
from quest import Quest, Subquest
from item import Item
from ui import DialogueBox
from debug import debug 

class Game:
	def __init__(self, inventory):
		self.display_surface = pygame.display.get_surface()
		self.current_map = 'map1'
		self.inventory = inventory
		self.spawn = pygame.math.Vector2(18*TILESIZE, 38*TILESIZE)
		self.can_continue = True
		self.first_launch = True

		#sample quest
		self.magician_quest = Quest("wizardquest", [Subquest('talk', 'mathis', 1, None),
												Subquest('collect', "fiole", 10, None),
		                                        Subquest('talk', 'mathis', 1, Item([], "magic"))], None, self.inventory)

		self.hunter_quest = Quest("hunterquest", [Subquest('talk', "althea", 1, None, self.magician_quest),
												Subquest("collect", 'magic', 1, None),
												Subquest('talk', "althea", 1, None),
												Subquest('kill', 'goblin', 5, None),
		                                     	Subquest("talk", "althea", 1, Item([], 'bow'))], None, self.inventory)

		self.main_quest = Quest("sirmadaquest", [Subquest("talk", "sirmada", 1, Item([], 'heartinventory')),
		                                           Subquest("kill", 'slime', 3, None),
		                                           Subquest("talk", "sirmada", 1, Item([], 'boots'), self.hunter_quest),
		                                           Subquest("collect", "bow", 1, None),
												   Subquest("talk", "sirmada", 1, None),
												   Subquest('talk', "tah_le_shamp", 1, None, end_game=True)], None, self.inventory)

		self.level = Level(self.current_map, self.spawn, 5, 0, self.inventory, 10, 20, self.main_quest, self.magician_quest, self.hunter_quest)

	def check_transitions(self, map, rec, id, n=0):
		transitions = import_csv_layout(f'maps/{map}/{map}_Transitions.csv')
		occ = {}
		for row_index, row in enumerate(transitions):
			for col_index, col in enumerate(row):
				if rec == 0:
					if col != '-1':
						try:
							occ[col] += 1
						except:
							occ[col] = 1
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if self.level.player.hitbox.colliderect(pygame.Rect(x, y, TILESIZE, TILESIZE)) and ((self.level.player.hitbox.x < -32 or self.level.player.hitbox.y <-32 or self.level.player.hitbox.x + self.level.player.hitbox.width > self.level.visible_sprites.floor_rect.width + 32 or self.level.player.hitbox.y + self.level.player.hitbox.height > self.level.visible_sprites.floor_rect.height + 32) or MT[col][3]):
							temp_data = MT[col]
							if self.current_map == temp_data[0]:
								self.can_continue = False
								if temp_data[4] != None:
									requirement = temp_data[4].split(":")
									if requirement[0] == "item":
										for item in self.inventory.items:
											if item.item_type == requirement[1]:
												self.can_continue = True
									elif requirement[0] == 'quest':
										for quest in quests:
											if quest.name_id == requirement[1]:
												self.can_continue = True
								else:
									self.can_continue = True
								if self.can_continue:
									if temp_data[3]:
										for event in pygame.event.get(pygame.KEYUP):	
											if event.key == keybinds['INTERACT']:
												self.current_map = temp_data[1]
												self.spawn = (39*TILESIZE, 42*TILESIZE)
												self.level = Level(self.current_map, self.spawn, self.level.player.health, self.level.player.heal_available, self.inventory, self.level.player.arrows, self.level.player.mana, self.main_quest, self.magician_quest, self.hunter_quest)
												items_available = []
									else:
											self.current_map = temp_data[1]
											self.spawn = self.check_transitions(self.current_map, 1, col, occ[col])
											self.level = Level(self.current_map, self.spawn, self.level.player.health, self.level.player.heal_available, self.inventory, self.level.player.arrows, self.level.player.mana, self.main_quest, self.magician_quest, self.hunter_quest)
											items_available = []
								else:
									direction = self.level.player.direction*-1
									self.level.player.hitbox.x += direction[0]*self.level.player.speed*10
									self.level.player.hitbox.y += direction[1]*self.level.player.speed*10
									self.level.player.is_in_dialogue_transition = True
									dialogue_box.insert(0, DialogueBox(temp_data[5]))
									self.level.player.interacting = True
							elif self.current_map == temp_data[1]:
									self.current_map = temp_data[0]
									self.spawn = self.check_transitions(self.current_map, 1, col, occ[col])
									self.level = Level(self.current_map, self.spawn, self.level.player.health, self.level.player.heal_available, self.inventory, self.level.player.arrows, self.level.player.mana, self.main_quest, self.magician_quest, self.hunter_quest)
									items_available = []
				elif col == str(id):
					try:
						occ[col] += 1
					except:
						occ[col] = 1
					if occ[col] == n:
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						return (x, y)

	def dead(self):
		if self.level.boss_fight:
			self.current_map = 'map1'
			self.spawn = pygame.math.Vector2(18*TILESIZE, 38*TILESIZE)
		if self.level.recreate_map:
			self.level = Level(self.current_map, self.spawn, self.level.player.stats['life'], 0, self.inventory, self.level.player.arrows, self.level.player.mana, self.main_quest, self.magician_quest, self.hunter_quest)
			self.level.boss_fight = False

	def run(self):
		if self.first_launch:
			self.level.player.is_in_dialogue_transition = True
			dialogue_box.insert(0, DialogueBox(words.words[current_language]["24"]))
			self.level.player.interacting = True
		self.first_launch = False
		self.level.run()
		self.check_transitions(self.current_map, 0, 0)
		self.inventory.items_update()
		self.dead()
