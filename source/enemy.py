import pygame
from data import *
from entity import Entity
from support import *
from drop import drop
import audio

class Enemy(Entity):
    def __init__(self, monster_name, pos, groups, obstacle_sprites, damage_player, visible_sprites, inventory):
        super().__init__(groups)
        self.sprite_type = 'enemy'

        self.animation_speed = 0.04

        self.inventory = inventory

        self.import_graphics(monster_name)
        self.status = 'idle'
        self.image = self.animations[self.status][self.frame_index]

        self.visible_sprites = visible_sprites

        self.rect = self.image.get_rect(topleft = pos)
        self.hitbox = self.rect.inflate(0,-35)
        self.obstacle_sprites = obstacle_sprites

        self.monster_name = monster_name
        monster_info = monster_data[self.monster_name]
        self.attack_damage = monster_info['damage']
        self.health = monster_info['life']
        self.speed = monster_info['speed']
        self.attack_radius = monster_info['attack_radius']
        self.notice_radius = monster_info['notice_radius']
        self.resistance = monster_info['resistance']

        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player

        self.vulnerable = True
        self.hit_time = None
        self.invicibility_duration = 300

    def import_graphics(self, name):
        self.animations = {'idle': [], 'left': [], 'right': []}
        main_path = f'graphics/foes/{name}/'
        for animation in self.animations.keys():
            self.animations[animation] = import_folder(main_path + animation)

    def get_player_distance_direction(self, player):
        enemy_vec = pygame.math.Vector2(self.rect.center)
        player_vec = pygame.math.Vector2(player.rect.center)
        distance = (player_vec - enemy_vec).magnitude()

        if distance > 0:
            direction = (player_vec - enemy_vec).normalize()
        else:
            direction = pygame.math.Vector2()

        return (distance,direction)

    def get_status(self, player):
        distance = self.get_player_distance_direction(player)[0]
        if distance <= self.attack_radius and self.can_attack:
            if not 'attack' in self.status:
                self.frame_index = 0
            if self.direction[0] < 0:
                self.status = 'attack_left'
            else:
                self.status = 'attack_right'
        elif distance <= self.notice_radius:
            if self.direction[0] < 0:
                if self.vulnerable:
                    self.status = 'left'
                else:
                    self.status = 'right'
            else:
                if self.vulnerable:
                    self.status = 'right'
                else:
                    self.status = 'left'
        else:
            self.status = 'idle'

    def actions(self,player):
        if 'attack' in self.status:
            self.attack_time = pygame.time.get_ticks()
            self.damage_player(self.attack_damage)
        elif self.status == 'left' or self.status == 'right':
            self.direction = self.get_player_distance_direction(player)[1]
        else:
            self.direction = pygame.math.Vector2()

    def animate(self):
        if 'attack' in self.status:
            animation = self.animations[self.status.split('_')[1]]
        else:
            animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            if 'attack' in self.status:
                self.can_attack = False
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, ((WIDTH/(1280/self.image.get_width())), (HEIGHT/(720/(self.image.get_height())))))
        self.rect = self.image.get_rect(center = self.hitbox.center)

        if not self.vulnerable:
            alpha = self.wave_value()
            self.image.set_alpha(alpha)
        else:
            self.image.set_alpha(255)

    def cooldowns(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if not self.vulnerable:
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time >= self.invicibility_duration:
                self.vulnerable = True

    def get_damage(self, player, weapon_type = "sword"):
        if not audio.ennemy_channel.get_busy():
            audio.hurt_channel.set_volume(audio.volume/10)
            audio.hurt_channel.play(audio.EFFECTS['uh_enemy'])
        if self.vulnerable:
            self.direction = self.get_player_distance_direction(player)[1]
            if weapon_type == "sword":
                self.health -= player.get_full_weapon_damage()
            else:
                self.health -= player.get_full_weapon_damage(weapon_type) * 0.5
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            if self.monster_name == 'slime':
                items_available.append(drop(self.hitbox.center, [self.visible_sprites], self.inventory))

            self.kill()
            return True
        return False

    def knockback(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def update(self):
        self.knockback()
        self.move(self.speed)
        self.animate()
        self.cooldowns()

    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)
        if self.check_death():
            for quest in quests:
                quest.check_quest(self.monster_name, "kill")