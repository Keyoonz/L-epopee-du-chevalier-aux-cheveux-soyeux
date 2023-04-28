import pygame, keybinds, audio, time
from data import *
from support import import_folder
from entity import Entity
from random import choice
from debug import debug
import states
import music

class Player(Entity):
	def __init__(self, pos, health, heal_available, arrows, mana, groups, obstacle_sprites, create_attack, destroy_attack):
		super().__init__(groups)
		self.image = pygame.image.load('graphics/player/down_idle/idle_down.png').convert_alpha()
		self.image = pygame.transform.scale(self.image, ((WIDTH/(1280/self.image.get_width())), (HEIGHT/(720/(self.image.get_height())))))
		self.rect = self.image.get_rect(topleft = pos)
		self.hitbox = self.rect.inflate(-6, HITBOX_OFFSET['player'])
		self.hitbox.x, self.hitbox.y = pos[0], pos[1]

		self.can_interact_with = []
		self.interacting = False

		self.import_player_assets()
		self.status = 'down'

		self.attacking = False
		self.can_attack = True
		self.attack_cooldown = 350
		self.can_attack_cooldown = 600
		self.attack_time = None
		self.obstacle_sprites = obstacle_sprites
		self.last_direction = 'down'

		self.using_magic = False
		self.shooting  = False

		self.sword = 'sword1'
		self.magic = 'magic1'
		self.bow = 'bow1'
		self.create_attack = create_attack
		self.destroy_attack = destroy_attack

		self.vulnerable = True
		self.hurt_time = None
		self.invulnerability_duration = 500

		self.stats = {'speed': HEIGHT/240, 'life': 5}
		self.health = health
		self.heal_available = heal_available
		self.speed = self.stats['speed']

		self.mana = mana

		self.ending_game = False
		self.end_time = None
		self.end = False

		self.arrows = arrows

		self.can_use_item = True
		self.item_use_cooldown = 250
		self.boots_use = False

		self.recreate_map = False

		self.is_in_dialogue_transition = False

	def import_player_assets(self):
		character_path = 'graphics/player/'
		self.animations = {'up': [],'down': [],'left': [],'right': [],
			'right_idle':[],'left_idle':[],'up_idle':[],'down_idle':[],
			'right_attack':[],'left_attack':[],'up_attack':[],'down_attack':[],
			'up_magic': [], 'down_magic': [], 'left_magic': [], 'right_magic': [],
			'up_bow': [], 'down_bow': [], 'left_bow': [], 'right_bow': [], 'dead': [],
			'up_damage': [], 'down_damage': [], 'left_damage': [], 'right_damage': []}

		for animation in self.animations.keys():
			full_path = character_path + animation
			self.animations[animation] = import_folder(full_path)

	def input(self):
		keys = pygame.key.get_pressed()

		if keys[keybinds.keybinds['INTERACT']] and self.is_in_dialogue_transition and not self.ending_game:
				self.is_in_dialogue_transition = False
				dialogue_box.clear()
				self.interacting = False
		if self.ending_game and self.is_in_dialogue_transition:
			if pygame.time.get_ticks() - self.end_time > 1000:
				states.current_state = states.MENU
				music.MUSIC[music.current_music].stop()
				music.MUSIC['menu'].set_volume(music.volume/10)
				music.MUSIC['menu'].play()
				self.end = True
		if not self.attacking and not self.interacting and not self.using_magic and not self.shooting and self.status != 'dead':

			# movement
			if keys[keybinds.keybinds['UP']]:
				self.direction.y = -1
				self.status = 'up'
				self.last_direction = 'up'
			elif keys[keybinds.keybinds['DOWN']]:
				self.direction.y = 1
				self.status = 'down'
				self.last_direction = 'down'
			else:
				self.direction.y = 0

			if keys[keybinds.keybinds['RIGHT']]:
				self.direction.x = 1
				self.status = 'right'
				self.last_direction = 'right'
			elif keys[keybinds.keybinds['LEFT']]:
				self.direction.x = -1
				self.status = 'left'
				self.last_direction = 'left'
			else:
				self.direction.x = 0

			# attack input 
			if keys[keybinds.keybinds['ATTACK']]:
				if self.can_attack:
					self.attacking = True
					self.attack_time = pygame.time.get_ticks()
					self.create_attack()
					self.frame_index = 0
					self.can_attack = False

			if len(current_item) > 0:
				if keys[keybinds.keybinds['USE_ITEM']]:
					if self.can_use_item:
						match current_item[0].item_type:
							case 'heartinventory':
								if self.heal_available > 0:
									self.heal(0.5)
									self.can_use_item = False
									self.heal_available -= .5
									self.item_use_time = pygame.time.get_ticks()
							case 'boots':
								if not self.boots_use:
									self.boots_use = True
								else:
									self.boots_use = False
								self.can_use_item = False
								self.item_use_time = pygame.time.get_ticks()
							case 'magic':
								if self.can_attack and self.mana > 0:
									self.using_magic = True
									self.attack_time = pygame.time.get_ticks()
									self.create_attack('magic')
									self.frame_index = 0
									self.can_attack = False
							case 'bow':
								if self.can_attack and self.arrows > 0:
									self.arrows -= 1
									self.shooting = True
									self.attack_time = pygame.time.get_ticks()
									self.create_attack('bow')
									self.frame_index = 0
									self.can_attack = False

		if self.status == 'dead':
			keys = pygame.key.get_pressed()
			if keys[pygame.K_RETURN]:
				self.recreate_map = True

	def get_status(self):
		if self.direction.x == 0 and self.direction.y == 0:
			if not 'idle' in self.status and not 'attack' in self.status and not 'magic' in self.status and not 'bow' in self.status and self.vulnerable:
				self.status = self.status + '_idle'

		if self.interacting:
			self.direction.x = 0
			self.direction.y = 0

		if self.attacking and not self.using_magic and not self.shooting:
			self.direction.x = 0
			self.direction.y = 0
			if not 'attack' in self.status:
				if 'idle' in self.status:
					if 'idle' in self.status:
						self.status = self.status.replace('_idle', '_attack')
					else:
						self.status = self.status + '_attack'
		else:
			if 'attack' in self.status:
				self.status = self.status.replace('_attack', '')
		
		if not self.attacking and self.using_magic and not self.shooting:
			self.direction.x = 0
			self.direction.y = 0
			if not 'magic' in self.status:
				if 'idle' in self.status:
					if 'idle' in self.status:
						self.status = self.status.replace('_idle', '_magic')
					else:
						self.status = self.status + '_magic'
		else:
			if 'magic' in self.status:
				self.status = self.status.replace('_magic', '')
		
		if not self.attacking and not self.using_magic and self.shooting:
			self.direction.x = 0
			self.direction.y = 0
			if not 'bow' in self.status:
				if 'idle' in self.status:
					if 'idle' in self.status:
						self.status = self.status.replace('_idle', '_bow')
					else:
						self.status = self.status + '_bow'
		else:
			if 'bow' in self.status:
				self.status = self.status.replace('_bow', '')

		if self.health <= 0:
			self.status = 'dead'

		if not self.vulnerable and not self.attacking and not self.using_magic and not self.shooting:
			self.direction.x = 0
			self.direction.y = 0
			if not 'damage' in self.status:
				if 'idle' in self.status:
					if 'idle' in self.status:
						self.status = self.status.replace('_idle', '_damage')
					else:
						self.status = self.status + '_damage'
		else:
			if 'damage' in self.status:
				self.status = self.status.replace('_damage', '')

	def walk_audio(self):
		if not '_' in self.status:
			if not audio.effects_channel.get_busy():
				audio.effects_channel.play(audio.EFFECTS['step1'])
			if not audio.effects_channel.get_busy():
				audio.effects_channel.play(audio.EFFECTS['step2'])

	def animate(self):
		animation = self.animations[self.status]
		if 'magic' in self.status:
			animation = 4*self.animations[self.status]
		if 'attack' in self.status or 'magic' in self.status or 'bow' in self.status:
			self.animation_speed = 0.1
		else:
			self.animation_speed = 0.11
		self.frame_index += self.animation_speed
		if self.frame_index >= len(animation):
			self.frame_index = 0
		self.image = animation[int(self.frame_index)]
		self.image = pygame.transform.scale(self.image, ((WIDTH/(1280/self.image.get_width())), (HEIGHT/(720/(self.image.get_height())))))
		self.rect = self.image.get_rect(center=self.hitbox.center)
		if not self.vulnerable and not self.status == 'dead':
			alpha = self.wave_value()
			self.image.set_alpha(alpha)
		else:
			self.image.set_alpha(255)

	def cooldowns(self):
		current_time = pygame.time.get_ticks()

		if self.attacking:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.attacking = False
				self.destroy_attack()

		if self.using_magic:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.using_magic = False
				self.destroy_attack()

		if self.shooting:
			if current_time - self.attack_time >= self.attack_cooldown:
				self.shooting = False
				self.destroy_attack()

		if not self.can_attack:
			if current_time - self.attack_time >= self.can_attack_cooldown:
				self.can_attack = True

		if not self.vulnerable:
			if current_time - self.hurt_time >= self.invulnerability_duration:
				self.vulnerable = True

		if not self.can_use_item:
			if current_time - self.item_use_time >= self.item_use_cooldown:
				self.can_use_item = True

	def get_full_weapon_damage(self, weapon_type = 'sword'):
		if weapon_type == 'sword':
			return weapon_data[self.sword]['damage']
		elif weapon_type == 'bow':
			return weapon_data[self.bow]['damage']
		return weapon_data[self.magic]['damage']

	def heal(self, amount):
		self.health += amount
		if self.health > self.stats['life']:
			self.health = self.stats['life']

	def dead(self):
		if self.status == 'dead':
			self.vulnerable = False

	def update(self):
		self.input()
		self.move(self.speed)
		self.get_status()
		if not self.status == 'dead':
			self.walk_audio()
		self.animate()
		self.cooldowns()
		for quest in quests:
			quest.update()
		if self.boots_use:
			self.speed = self.stats['speed']*1.5
		else:
			self.speed = self.stats['speed']
		if current_item != []:
			if current_item[0].item_type != 'boots':
				self.boots_use = False
		self.dead()

	def interact(self):
		if self.status != 'dead':
			for obj in self.can_interact_with:
				obj.interact(self)

	def move(self,speed):
		if self.direction.magnitude() != 0:
			self.direction = self.direction.normalize()
		self.hitbox.x += self.direction.x * speed
		self.collision('horizontal')
		self.hitbox.y += self.direction.y * speed
		self.collision('vertical')
		self.rect.center = self.hitbox.center