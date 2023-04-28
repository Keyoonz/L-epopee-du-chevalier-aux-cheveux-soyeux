import pygame
from support import *
from data import *
from enemy import Enemy
from arrow import Arrow
from tile import Tile
from drop import drop
from boss import Rock

class Weapon(pygame.sprite.Sprite):
	def __init__(self, player, groups, weapon_type = 'sword', attackable_sprite = None, visible_sprites = None, attack_sprites = None, obstacle_sprites = None, inventory = None):
		super().__init__(groups)
		self.player = player
		self.sprite_type = 'weapon'
		self.direction = self.player.status.split('_')[0]
		self.frame_index = self.player.frame_index
		self.weapon_type = weapon_type
		self.attackable_sprite = attackable_sprite
		self.attack_sprites = attack_sprites
		self.visible_sprites = visible_sprites
		self.has_hit = False
		self.light = []

		self.inventory = inventory

		self.obstacle_sprites = obstacle_sprites

		if self.weapon_type == 'sword':
			self.image = pygame.image.load(f'graphics/swords/{player.sword}/{self.direction}/0.png')
		elif self.weapon_type == 'magic' :
			self.image = pygame.image.load(f'graphics/magics/{player.magic}/wand.png')
		elif self.weapon_type == 'bow' :
			self.image = pygame.image.load(f'graphics/bows/{player.bow}/{self.direction}.png')
		self.image = pygame.transform.scale(self.image, ((WIDTH/(1280/self.image.get_width())), (HEIGHT/(720/(self.image.get_height())))))
		if self.direction == 'right':
			self.rect = self.image.get_rect(midleft = self.player.rect.midright + pygame.math.Vector2(-14, 2))
		elif self.direction == 'left': 
			self.rect = self.image.get_rect(midright = self.player.rect.midleft + pygame.math.Vector2(0, 2))
		elif self.direction == 'down':
			self.rect = self.image.get_rect(midtop = self.player.rect.midbottom + pygame.math.Vector2(-47, -42))
			if self.weapon_type == 'magic':
				self.rect = self.image.get_rect(midleft = self.player.rect.bottomright + pygame.math.Vector2(-23, -36))
			if self.weapon_type == 'bow':
				self.rect = self.image.get_rect(midleft = self.player.rect.bottomright + pygame.math.Vector2(-52, 0))
		else:
			self.rect = self.image.get_rect(midbottom = self.player.rect.midtop + pygame.math.Vector2(-16, 30))
		self.hitbox = self.rect

		self.import_weapon_assets(player)
	

	def import_weapon_assets(self, player):
		if self.weapon_type == 'sword':
			weapon_path = f'graphics/swords/{player.sword}/'
		
			self.animations = {'up': [],'down': [],'left': [],'right': []}
		
			for animation in self.animations.keys():
					full_path = weapon_path + animation
					self.animations[animation] = import_folder(full_path)

	def update(self):
		self.frame_index = self.player.frame_index
		if self.weapon_type == 'sword':
			animation = self.animations[self.direction]
			self.image = animation[int(self.frame_index)]
			self.image = pygame.transform.scale(self.image, ((WIDTH/(1280/self.image.get_width())), (HEIGHT/(720/(self.image.get_height())))))
			match self.direction:
				case 'down':
					match int(self.frame_index):
						case 0:
							self.rect = self.image.get_rect(midtop = self.player.rect.midbottom + pygame.math.Vector2(WIDTH/-32, WIDTH/-36.5))
						case 1:
							self.rect = self.image.get_rect(midtop = self.player.rect.midbottom + pygame.math.Vector2(WIDTH/-46.5, WIDTH/-33.4))
						case 2:
							self.rect = self.image.get_rect(midtop = self.player.rect.midbottom + pygame.math.Vector2(WIDTH/70, WIDTH/-102))
						case 3:
							self.rect = self.image.get_rect(midtop = self.player.rect.midbottom + pygame.math.Vector2(WIDTH/35, WIDTH/-36.6))
						case 4:
							self.rect = self.image.get_rect(midtop = self.player.rect.midbottom + pygame.math.Vector2(WIDTH/25.6, WIDTH/-33.4))
				case 'right':
					match int(self.frame_index):
						case 0:
							self.rect = self.image.get_rect(midleft = self.player.rect.midright + pygame.math.Vector2(WIDTH/-109.7, WIDTH/768))
						case 1:
							self.rect = self.image.get_rect(midleft = self.player.rect.midright + pygame.math.Vector2(WIDTH/-109.7, 0))
						case 2:
							self.rect = self.image.get_rect(midleft = self.player.rect.midright + pygame.math.Vector2(WIDTH/-170.7, WIDTH/76.8))
						case 3:
							self.rect = self.image.get_rect(midleft = self.player.rect.midright + pygame.math.Vector2(WIDTH/-192, WIDTH/61.4))
						case 4:
							self.rect = self.image.get_rect(midleft = self.player.rect.midright + pygame.math.Vector2(WIDTH/-43.9, WIDTH/28))
				case 'left':
					match int(self.frame_index):
						case 0:
							self.rect = self.image.get_rect(midleft = self.player.rect.midleft + pygame.math.Vector2(0, WIDTH/768))
						case 1:
							self.rect = self.image.get_rect(midleft = self.player.rect.midleft + pygame.math.Vector2(WIDTH/-51.2, 0))
						case 2:
							self.rect = self.image.get_rect(midleft = self.player.rect.midleft + pygame.math.Vector2(WIDTH/-31.3, WIDTH/76.8))
						case 3:
							self.rect = self.image.get_rect(midleft = self.player.rect.midleft + pygame.math.Vector2(WIDTH/-32, WIDTH/61.4))
						case 4:
							self.rect = self.image.get_rect(midleft = self.player.rect.midleft + pygame.math.Vector2(WIDTH/-61.4, WIDTH/34.1))
				case 'up':
					match int(self.frame_index):
						case 0:
							self.rect = self.image.get_rect(midtop = self.player.rect.midtop + pygame.math.Vector2(WIDTH/153.6, 0))
						case 1:
							self.rect = self.image.get_rect(midtop = self.player.rect.midtop + pygame.math.Vector2(WIDTH/153.6, WIDTH/-102.4))
						case 2:
							self.rect = self.image.get_rect(midtop = self.player.rect.midtop + pygame.math.Vector2(WIDTH/-76.8, WIDTH/-102.4))
						case 3:
							self.rect = self.image.get_rect(midtop = self.player.rect.midtop + pygame.math.Vector2(WIDTH/-61.4, WIDTH/-153.6))
						case 4:
							self.rect = self.image.get_rect(midtop = self.player.rect.midtop + pygame.math.Vector2(WIDTH/-61.4, WIDTH/-153.6))
			self.hitbox = self.rect
		elif self.weapon_type == 'magic':
			min_distance = None
			if min_distance == None:
				for sprite in self.attackable_sprite:
					distance = sprite.get_player_distance_direction(self.player)[0]
					if min_distance == None:
						if distance < weapon_data['magic_range']:
							min_distance = sprite
					elif distance < min_distance.get_player_distance_direction(self.player)[0] and distance < weapon_data['magic_range']:
						min_distance = sprite
			if min_distance != None:
				minx,miny = min_distance.rect.x, min_distance.rect.y
				if int(self.frame_index) >=2:
					if len(self.light) < 1:
						self.light.append(Tile((minx, miny), [self.visible_sprites], "light_weapon", pygame.image.load("graphics/magics/general/light.png")	))
					if type(min_distance) == Enemy:
						self.light[0].rect.centerx = min_distance.rect.centerx
			if self.frame_index >= 3:
					for light in self.light:
						light.kill()
			if not self.has_hit:
				if int(self.frame_index) == 2:
					if min_distance != None:
						if type(min_distance) == Enemy or type(min_distance) == Rock:
							min_distance.get_damage(self.player, 'magic')
						elif type(min_distance) == Tile:
							items_available.append(drop((min_distance.rect.center), [self.visible_sprites], self.inventory))
							min_distance.kill()
						self.has_hit = True
						self.player.mana -=1
		elif self.weapon_type == 'bow' :
			if not self.has_hit:
				Arrow(self.rect.center, [self.visible_sprites, self.attack_sprites], self.player.last_direction, self.obstacle_sprites)
				self.has_hit = True