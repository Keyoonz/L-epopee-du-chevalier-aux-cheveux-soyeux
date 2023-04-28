import pygame, states, words, keybinds
from weapon import Weapon
from data import *
from ui import Text_UI

class Inventory:
	def __init__(self):
		self.display_surface = pygame.display.get_surface()
		self.alpha = 255
		self.intro = True

		self.animation_move_speed_x = WIDTH/25
		self.animation_move_speed_y = HEIGHT/25

		self.a = WIDTH/8.5
		self.b = self.a + WIDTH/1.3 - WIDTH/2.7
		self.c = HEIGHT/1.4

		self.d = self.a - 5*self.animation_move_speed_x
		self.e = self.b + 5*self.animation_move_speed_x
		self.f = self.c + 5*self.animation_move_speed_y

		self.inventory1_rect_pos = pygame.math.Vector2(self.d, HEIGHT/12)
		self.inventory2_rect_pos = pygame.math.Vector2(self.e, HEIGHT/12)
		self.inventory3_rect_pos = pygame.math.Vector2(WIDTH/8.5, self.f)

		self.inventory1_height_capacity = 2
		self.inventory1_width_capacity = 2

		self.items = []

		self.selected_item = 0
		

	def general_appearance(self):
		self.bg.set_alpha(self.alpha)
		self.display_surface.blit(self.bg, self.bg.get_rect(topleft=(0, 0)))

		inventory1_surf = pygame.image.load('graphics/menu/inventory1.png')
		inventory1_surf = pygame.transform.scale(inventory1_surf, (WIDTH/3.2, WIDTH/3.2))
		inventory1_rect = inventory1_surf.get_rect(topleft=(self.inventory1_rect_pos.x, self.inventory1_rect_pos.y))
		self.display_surface.blit(inventory1_surf, inventory1_rect)

		inventory2_surf = pygame.image.load('graphics/menu/inventory2.png')
		inventory2_surf = pygame.transform.scale(inventory2_surf, (WIDTH/2.7, WIDTH/3.2))
		inventory2_rect = inventory2_surf.get_rect(topleft=(self.inventory2_rect_pos.x, self.inventory2_rect_pos.y))
		self.display_surface.blit(inventory2_surf, inventory2_rect)

		inventory3_surf = pygame.image.load('graphics/menu/inventory3.png')
		inventory3_surf = pygame.transform.scale(inventory3_surf, (WIDTH/1.3, HEIGHT/5.5))
		inventory3_rect = inventory3_surf.get_rect(topleft=(self.inventory3_rect_pos.x, self.inventory3_rect_pos.y))
		self.display_surface.blit(inventory3_surf, inventory3_rect)

		self.show_quests(inventory2_rect)

	def run(self):
		self.items_update()
		self.general_appearance()
		self.show_items()
		if self.intro:
			if self.inventory1_rect_pos.x < self.a:
				self.inventory1_rect_pos.x += self.animation_move_speed_x
			if self.inventory2_rect_pos.x > self.b:
				self.inventory2_rect_pos.x -= self.animation_move_speed_x
			if self.inventory3_rect_pos.y > self.c:
				self.inventory3_rect_pos.y -= self.animation_move_speed_y

			if self.alpha > 100:
				self.alpha -= 10
		else:
			if self.inventory1_rect_pos.x > self.d:
				self.inventory1_rect_pos.x -= self.animation_move_speed_x
			if self.inventory2_rect_pos.x < self.e:
				self.inventory2_rect_pos.x += self.animation_move_speed_x
			if self.inventory3_rect_pos.y < self.f:
				self.inventory3_rect_pos.y += self.animation_move_speed_y
			else:
				states.current_state = states.PLAYING

			if self.alpha < 255:
				self.alpha += 10

	def show_items(self):
		for itemIndex, item in enumerate(self.items):
			image = pygame.transform.scale(item.image, (item.image.get_width()*2.5, item.image.get_height()*2.5))
			itemWidth = image.get_width()
			itemHeight = image.get_height()
			itemRect = image.get_rect(topleft=(self.inventory1_rect_pos.x+0.3*itemWidth + itemWidth*(itemIndex%self.inventory1_width_capacity) +25*(itemIndex%self.inventory1_width_capacity), self.inventory1_rect_pos.y+0.3*itemHeight + itemWidth*((itemIndex)//self.inventory1_width_capacity) + 25*(itemIndex//self.inventory1_width_capacity)))
			if itemIndex == self.selected_item:
				pygame.draw.rect(self.display_surface, 'gold', itemRect, 5, border_radius=5)
			self.display_surface.blit(image, itemRect)

	def show_quests(self, inventory_2_rect):
		for i, quest in enumerate(quests):
			quest_text = Text_UI((inventory_2_rect.x + inventory_2_rect.width/10, inventory_2_rect.y + inventory_2_rect.height/20 + i*inventory_2_rect.width/6), f"{quest.dialogue} : ({quest.current_subquest}/{quest.number_of_subquests})", 3)
			self.display_surface.blit(quest_text.text, quest_text.rect)
			subquest_text = Text_UI((inventory_2_rect.x + inventory_2_rect.width/8, quest_text.rect.bottom), f"{quest.subquests[quest.current_subquest].dialogue} : ({quest.subquests[quest.current_subquest].current_objective_amount}/{quest.subquests[quest.current_subquest].objective_amount})", 2)
			self.display_surface.blit(subquest_text.text, subquest_text.rect)

	def selection_keys(self, key):
		if key == keybinds.keybinds['LEFT']:
			if not self.selected_item % self.inventory1_width_capacity == 0:
				self.selected_item-=1
		if key ==  keybinds.keybinds['RIGHT']:
			if not self.selected_item % self.inventory1_width_capacity == 5:
				if not self.selected_item+1 >= len(self.items):
					self.selected_item+=1
		if key ==  keybinds.keybinds['UP']:
			if not self.selected_item // self.inventory1_height_capacity == 0:
				self.selected_item-= self.inventory1_width_capacity
		if key == keybinds.keybinds['DOWN']:
			if not self.selected_item // self.inventory1_height_capacity == 5:
				if not self.selected_item+self.inventory1_height_capacity >= len(self.items):
					self.selected_item+= self.inventory1_width_capacity

	def items_update(self):
		for item in self.items:
			for quest in quests:
				quest.check_quest(item.item_type, 'collect')