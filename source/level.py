import pygame, music
from data import *
from support import *
from tile import Tile
from player import Player
from random import choice
from ui import UI
from weapon import Weapon
from enemy import Enemy
from npc import NPC
from drop import drop
from quest import Quest
from quest import Subquest
from item import Item
from arrow import Arrow
from enter_tile import Enter_Tile
from boss import Boss, Rock
import audio

class Level:
	def __init__(self, map, spawn, health, heal_available, inventory, arrows, mana, main_quest, magician_quest, hunter_quest):
		self.display_surface = pygame.display.get_surface()

		self.main_quest = main_quest
		self.hunter_quest = hunter_quest
		self.magician_quest = magician_quest

		self.visible_sprites = YSortCameraGroup(map)
		self.obstacle_sprites = pygame.sprite.Group()
		self.important_sprites = pygame.sprite.Group()
		self.transition_update = pygame.sprite.Group()

		self.current_attack = None
		self.attack_sprites = pygame.sprite.Group()
		self.attackable_sprites = pygame.sprite.Group()

		self.spawn = spawn
		self.health = health
		self.arrows = arrows
		self.mana = mana
		self.heal_available = heal_available

		self.skip_text_offset = 0
		self.skip_text_offset_parameter = 0

		self.ui = UI()
		self.inventory = inventory

		self.map = map

		self.boss_fight = False
		self.last_music = "game"
		self.current_music = "game"

		if not self.main_quest in quests:
			quests.append(self.main_quest)

		self.create_map(self.map, self.health)
		self.recreate_map = False


	def create_map(self, map, player_health):
		layouts = {
			'boundary': import_csv_layout(f'maps/{map}/{map}_FloorBlocks.csv'),
			'grass': import_csv_layout(f'maps/{map}/{map}_Grass.csv'),
			'object': import_csv_layout(f'maps/{map}/{map}_Objects.csv'),
			'entities': import_csv_layout(f'maps/{map}/{map}_Entities.csv'),
			'transitions': import_csv_layout(f'maps/{map}/{map}_Transitions.csv')
		}
		graphics = {
			'grass': import_folder('graphics/Grass'),
			'objects': import_folder('graphics/objects')
		}

		for style, layout in layouts.items():
			for row_index, row in enumerate(layout):
				for col_index, col in enumerate(row):
					if col != '-1':
						x = col_index * TILESIZE
						y = row_index * TILESIZE
						if style == 'boundary':
							Tile((x, y), [self.obstacle_sprites], 'invisible')
						if style == 'grass':
							random_grass_image = choice(graphics['grass'])
							Tile((x, y), [self.visible_sprites, self.obstacle_sprites, self.attackable_sprites], 'grass', random_grass_image)
						if style == 'object':
							surf = graphics['objects'][int(col)]
							if col == "18":
								Tile((x, y), [self.important_sprites, self.obstacle_sprites], 'object', surf, col=int(col))
							else:
								Tile((x, y), [self.visible_sprites, self.obstacle_sprites], 'object', surf, col=int(col))	
						if style == 'entities':
							if col == '4':
								Enemy('slime', (x, y), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_player, self.visible_sprites, self.inventory)
							elif col == '5':
								Enemy('goblin', (x, y), [self.visible_sprites, self.attackable_sprites], self.obstacle_sprites, self.damage_player, self.visible_sprites, self.inventory)
							elif col == '0':
								NPC('sirmada', (x, y), [self.visible_sprites, self.obstacle_sprites], [self.main_quest], self.important_sprites)
							elif col == '1':
								NPC('althea', (x, y), [self.visible_sprites, self.obstacle_sprites], [self.hunter_quest], self.important_sprites)
							elif col == '2':
								NPC('mathis', (x, y), [self.visible_sprites, self.obstacle_sprites], [self.magician_quest], self.important_sprites)
							if col == '6':
								Enter_Tile((x,y), [self.transition_update], self.important_sprites)
							if col == '3':
								self.boss_fight = True
								Boss((x,y), [self.visible_sprites, self.attackable_sprites], 'chevoeuil', self.damage_player, self.obstacle_sprites, self.visible_sprites)

		self.player = Player(self.spawn, player_health, self.heal_available, self.arrows, self.mana, [self.visible_sprites], self.obstacle_sprites, self.create_attack, self.destroy_attack)

	def create_attack(self, weapon_type = 'sword'):
		audio.effects_channel.set_volume(audio.volume/10)
		audio.effects_channel.play(audio.EFFECTS['rah'])
		if weapon_type == 'sword':
			self.current_attack = Weapon(self.player,[self.visible_sprites, self.attack_sprites], inventory=self.inventory)
			audio.effects_channel.set_volume(audio.volume/10)
			audio.effects_channel.play(audio.EFFECTS['sword'])
		elif weapon_type == 'magic':
			self.current_attack = Weapon(self.player,[self.visible_sprites], weapon_type, self.attackable_sprites, self.visible_sprites, inventory=self.inventory)
		elif weapon_type == 'bow':
			self.current_attack = Weapon(self.player, [self.visible_sprites], weapon_type, self.attackable_sprites, self.visible_sprites, self.attack_sprites, self.obstacle_sprites, inventory=self.inventory)

	def destroy_attack(self):
		if self.current_attack.weapon_type == 'magic':
			for light in self.current_attack.light:
				light.kill()
		if self.current_attack:
			self.current_attack.kill()
		self.current_attack = None

	def check_regen(self):
		for elt in items_available:
			if not elt:
				items_available.remove(elt)
			else:
				if elt.hitbox.colliderect(self.player.hitbox):
					if elt.sprite_type == 'heart':
						self.player.heal_available += elt.amount
						for quest in quests:
							quest.check_quest('fiole', 'collect')
					elif elt.sprite_type == 'mana':
						self.player.mana += elt.amount
					elif elt.sprite_type == 'arrow':
						self.player.arrows += elt.amount
					elt.kill()
					items_available.remove(elt)

	def player_attack_logic(self):
		if self.attack_sprites:
			for attack_sprite in self.attack_sprites:
				collision_sprites = pygame.sprite.spritecollide(attack_sprite, self.attackable_sprites, False)
				if collision_sprites:
					for target_sprite in collision_sprites:
						if target_sprite.sprite_type == 'grass':
							if not type(attack_sprite) == Arrow:
								items_available.append(drop((target_sprite.rect.center), [self.visible_sprites], self.inventory))
								target_sprite.kill()
							else :
								attack_sprite.kill()
						else:
							if type(attack_sprite) == Weapon:
								target_sprite.get_damage(self.player, 'sword')
							elif type(attack_sprite) == Arrow:
								target_sprite.get_damage(self.player, 'bow')
								attack_sprite.kill()

	def damage_player(self, amount):
		if not audio.hurt_channel.get_busy() and self.player.status != 'dead' and self.player.health > 0:
			audio.hurt_channel.set_volume(audio.volume/10)
			audio.hurt_channel.play(audio.EFFECTS['uh'])
		if self.player.vulnerable:
			if self.player.health - amount <= 0:
				self.player.health = 0
			else:
				self.player.health -= amount
			self.player.vulnerable = False
			self.player.hurt_time = pygame.time.get_ticks()

	def dead(self):
		self.recreate_map = self.player.recreate_map

	def run(self):
		if self.boss_fight:
			music.current_music = 'fight'
			music.MUSIC['fight'].set_volume(music.volume/10)
		else:
			music.current_music = 'game'
			music.MUSIC['game'].set_volume(music.volume/10)

		if music.last_music != music.current_music:
			music.MUSIC[music.last_music].stop()
			music.MUSIC[music.current_music].set_volume(music.volume/10)
			music.MUSIC[music.current_music].play(loops=-1)
			music.last_music = music.current_music
		
		self.visible_sprites.custom_draw(self.player, self.obstacle_sprites, self.important_sprites)
		self.visible_sprites.update()
		self.visible_sprites.enemy_update(self.player)
		self.visible_sprites.npc_update(self.player)
		self.transition_update.update(self.player)
		self.check_regen()
		self.player_attack_logic()
		self.ui.display(self.player)
		if self.player.interacting:
			dialogue_box[0].update(self.skip_text_offset)
			if self.skip_text_offset > -WIDTH/4000*50 and self.skip_text_offset < WIDTH/4000*50:
				if self.skip_text_offset_parameter == 0:
					self.skip_text_offset += WIDTH/4000
				else:
					self.skip_text_offset -= WIDTH/4000
			elif self.skip_text_offset >= WIDTH/4000*50:
				self.skip_text_offset_parameter = 1
				self.skip_text_offset -= WIDTH/4000
			else:
				self.skip_text_offset_parameter = 0
				self.skip_text_offset += WIDTH/4000
			if len(dialogue_box) == 0:
				self.player.interacting = False

		for attack_sprite in self.attack_sprites:
			if type(attack_sprite) == Arrow:
				if attack_sprite.has_stopped_moving:
					attack_sprite.kill()
		self.dead()

class YSortCameraGroup(pygame.sprite.Group):
	def __init__(self, map) -> None:
		super().__init__()
		self.display_surface = pygame.display.get_surface()
		self.half_width = self.display_surface.get_size()[0]//2
		self.half_height = self.display_surface.get_size()[1]//2
		self.offset = pygame.math.Vector2()

		self.floor_surf = pygame.image.load(f'maps/{map}/floor.png').convert()
		self.floor_surf = pygame.transform.scale(self.floor_surf, (self.floor_surf.get_width()*WIDTH/1280, self.floor_surf.get_height()*HEIGHT/720))
		self.floor_rect = self.floor_surf.get_rect(topleft=(0, 0))

		self.show_hitboxes = False

	def custom_draw(self, player, obstacle_sprites, important_sprites):
		self.offset.x = player.rect.centerx - self.half_width
		if self.offset.x < 0:
			self.offset.x = 0
		elif self.offset.x > self.floor_rect.width - self.display_surface.get_size()[0]:
			self.offset.x = self.floor_rect.width - self.display_surface.get_size()[0]
		self.offset.y = player.rect.centery - self.half_height
		if self.offset.y < 0:
			self.offset.y = 0
		elif self.offset.y > self.floor_rect.height - self.display_surface.get_size()[1]:
			self.offset.y = self.floor_rect.height - self.display_surface.get_size()[1]
		floor_offset_pos = self.floor_rect.topleft - self.offset
		self.display_surface.blit(self.floor_surf, floor_offset_pos)

		for sprite in sorted(self.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image, offset_pos)
			if self.show_hitboxes and type(sprite) != "ParticleEffect":
				if type(sprite) != 'weapon':
					pygame.draw.rect(self.display_surface, (255, 0, 0), sprite.hitbox.move(-self.offset), 1)
				else:
					pygame.draw.rect(self.display_surface, (255, 0, 0), sprite.rect.move(-self.offset), 1)

		for sprite in sorted(important_sprites.sprites(), key = lambda sprite: sprite.rect.centery):
			offset_pos = sprite.rect.topleft - self.offset
			self.display_surface.blit(sprite.image, offset_pos)

		for sprite in sorted(obstacle_sprites.sprites(), key = lambda sprite: sprite.rect.centery):
			if self.show_hitboxes:
				pygame.draw.rect(self.display_surface, (0, 255, 0), sprite.hitbox.move(-self.offset), 1)

	def enemy_update(self,player):
		enemy_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and (sprite.sprite_type == 'enemy' or sprite.sprite_type == 'boss')]
		for enemy in enemy_sprites:
			enemy.enemy_update(player)

	def npc_update(self,player):
		npc_sprites = [sprite for sprite in self.sprites() if hasattr(sprite,'sprite_type') and sprite.sprite_type == 'npc']
		for npc in npc_sprites:
			npc.npc_update(player)