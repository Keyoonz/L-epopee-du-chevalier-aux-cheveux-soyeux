import pygame, words
from data import *
from entity import Entity
from support import *
from npc import NPC
import audio

class Boss(Entity):
    def __init__(self, pos, groups, name, damage_player, obstacle_sprites, visible_sprites):
        super().__init__(groups)
        self.display_surface = pygame.display.get_surface()
        self.sprite_type = 'boss'
        self.boss_name = name

        self.groups = groups
        self.obstacle_sprites = []
        self.os = obstacle_sprites

        self.visible_sprites = visible_sprites

        if self.boss_name == 'chevoeuil':
            self.animation_speed = 0.04

        self.status = 'idle'
        self.import_graphics(self.boss_name)
        self.image = self.animations[self.status][self.frame_index]
        self.image = pygame.transform.scale(self.image, ((WIDTH/(1280/self.image.get_width())), (HEIGHT/(720/(self.image.get_height())))))

        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(-50,-50)

        boss_info = boss_data[self.boss_name]
        self.attack_damage = boss_info['damage']
        self.health = boss_info['life']
        self.life = self.health
        self.speed = boss_info['speed']
        self.attack_radius = boss_info['attack_radius']
        self.notice_radius = boss_info['notice_radius']
        self.resistance = boss_info['resistance']

        self.can_attack = True
        self.attack_time = None
        self.attack_cooldown = 400
        self.damage_player = damage_player

        self.can_fall = False
        self.fall_time = 10000
        self.fall_cooldown = 10000
        self.falling = None

        self.ko_time = None
        self.ko_cooldown = 3000

        self.vulnerable = False
        self.hit_time = 0
        self.invicibility_duration = 300

        self.phase = 1
        self.rocks = []

    def import_graphics(self, name):
        self.animations = {'idle': [], 'right': [], 'left': [], 'ko': [], 'fall': []}
        main_path = f'graphics/boss/{name}/'
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
                self.status = 'left'
            else:
                self.status = 'right'
        else:
            self.status = 'idle'

        if self.falling == 'falling':
            self.status = 'fall'
        elif self.falling == 'ko':
            self.status = 'ko'

    def fall_damage(self, player):
        if self.hitbox.colliderect(player.hitbox) and self.status == 'fall':
            self.damage_player(player.health)

    def fall(self):
        if self.can_fall:
            self.fall_time = pygame.time.get_ticks()
            self.falling = 'falling'
            if int(self.frame_index) in [0, 1, 2]:
                self.hitbox.y -= HEIGHT/1000000
            elif int(self.frame_index) in [3, 4, 5, 6]:
                self.hitbox.y += 3
            if self.frame_index > 6:
                if not audio.hurt_channel.get_busy():
                    audio.hurt_channel.set_volume(audio.volume/5)
                    audio.hurt_channel.play(audio.EFFECTS['splash'])
                self.can_fall = False
                self.falling = 'ko'
                self.ko_time = pygame.time.get_ticks()

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

    def cooldowns(self):
        if not self.can_attack:
            current_time = pygame.time.get_ticks()
            if current_time - self.attack_time >= self.attack_cooldown:
                self.can_attack = True

        if self.falling == 'ko':
            current_time = pygame.time.get_ticks()
            if current_time - self.ko_time >= self.ko_cooldown:
                self.falling = 'None'

        if not self.vulnerable and self.falling == 'ko':
            current_time = pygame.time.get_ticks()
            if current_time - self.hit_time >= self.invicibility_duration:
                self.vulnerable = True

        if self.phase == 1:
            if not self.can_fall:
                current_time = pygame.time.get_ticks()
                if current_time - self.fall_time >= self.fall_cooldown:
                    self.can_fall = True

    def get_damage(self, player, weapon_type):
        if self.vulnerable:
            if self.phase == 1:
                if weapon_type == "sword":
                    self.health -= player.get_full_weapon_damage()
            else:
                if weapon_type == 'bow':
                    self.health -= player.get_full_weapon_damage(weapon_type) * 0.5
            self.hit_time = pygame.time.get_ticks()
            self.vulnerable = False

    def check_death(self):
        if self.health <= 0:
            NPC('tah_le_shamp', self.rect.center, [self.groups], [], self.groups[0])
            self.kill()
            return True

    def knockback(self):
        if not self.vulnerable:
            self.direction *= -self.resistance

    def life_bar(self):
        temp_font = pygame.font.Font(UI_FONT, int(HEIGHT/20))
        bg = pygame.Rect(WIDTH/10, (HEIGHT/10)*8.3, (WIDTH/10)*8, HEIGHT/25)
        life = bg.inflate(-20, -15)
        life.width = (life.width/self.life)*self.health
        pygame.draw.rect(self.display_surface, UI_BG_COLOR, bg, border_radius=5)
        pygame.draw.rect(self.display_surface, 'crimson', life)
        match words.current_language:
            case 'ENGLISH':
                prompt = 'The Chevoeuil'
            case 'FRENCH':
                prompt = 'Le Chevoeuil'
        text = render(prompt, temp_font)
        rect = text.get_rect(bottomright=(bg.topright))
        self.display_surface.blit(text, rect)

    def check_phase(self):
        if self.health < self.life/2 or self.phase == 2:
            self.phase = 2
            self.vulnerable = False
            self.rocks = [Rock((41*TILESIZE, 10*TILESIZE), self.groups, self.os, self.groups[1]),
                Rock((27*TILESIZE, 17*TILESIZE), [self.visible_sprites, self.groups[1]], self.os, self.groups[1]),
                Rock((48*TILESIZE, 22*TILESIZE), [self.visible_sprites, self.groups[1]], self.os, self.groups[1]),
                Rock((22*TILESIZE, 26*TILESIZE), [self.visible_sprites, self.groups[1]], self.os, self.groups[1]),
                Rock((30*TILESIZE, 26*TILESIZE), [self.visible_sprites, self.groups[1]], self.os, self.groups[1]),
                Rock((57*TILESIZE, 31*TILESIZE), [self.visible_sprites, self.groups[1]], self.os, self.groups[1]),
                Rock((45*TILESIZE, 36*TILESIZE), [self.visible_sprites, self.groups[1]], self.os, self.groups[1]),
                Rock((19*TILESIZE, 41*TILESIZE), [self.visible_sprites, self.groups[1]], self.os, self.groups[1]),
                Rock((36*TILESIZE, 39*TILESIZE), [self.visible_sprites, self.groups[1]], self.os, self.groups[1]),
                Rock((43*TILESIZE, 47*TILESIZE), [self.visible_sprites, self.groups[1]], self.os, self.groups[1])]

    def check_rocks(self):
        for elt in self.rocks:
            if elt.killed:
                elt.kill()
                self.rocks.remove(elt)
        if self.rocks == []:
            self.vulnerable = True
    
    def update(self):
        self.vulnerable = False
        # self.knockback()
        self.fall() 
        self.move(self.speed)
        self.animate()
        self.cooldowns()
        self.life_bar()
        if self.phase == 1:
            self.check_phase()
        elif self.phase == 2:
            self.check_rocks()
        self.check_death()

    def enemy_update(self,player):
        self.get_status(player)
        self.actions(player)
        self.fall_damage(player)

class Rock(Entity):
    def __init__(self, pos, groups, obstacle_sprites, attackable_sprites):
        super().__init__(groups)
        self.sprite_type = 'rock'

        self.status = 'falling'

        self.obstacle_sprites = obstacle_sprites
        self.attackable_sprites = attackable_sprites

        self.animation_speed = 0.04

        self.import_graphics()

        self.image = self.animations[self.status][self.frame_index]
        self.image = pygame.transform.scale(self.image, ((WIDTH/(1280/self.image.get_width())), (HEIGHT/(720/(self.image.get_height())))))

        self.rect = self.image.get_rect(center = pos)
        self.hitbox = self.rect.inflate(0,-35)

        self.killed = False
    
    def import_graphics(self):
        self.animations = {'falling': [], 'ground': []}
        main_path = f'graphics/boss/chevoeuil/rock/'
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
    
    def update(self):
        self.animate()
        self.get_status()

    def animate(self):
        if self.status == 'ground':
            self.image = self.animations[self.status][0]
        animation = self.animations[self.status]
        
        self.frame_index += self.animation_speed
        if self.frame_index >= len(animation):
            self.frame_index = 0

        self.image = animation[int(self.frame_index)]
        self.image = pygame.transform.scale(self.image, ((WIDTH/(1280/self.image.get_width())), (HEIGHT/(720/(self.image.get_height())))))
        self.rect = self.image.get_rect(center = self.hitbox.center)

    def get_status(self):
        if self.animations[self.status][int(self.frame_index)] == self.animations['falling'][-1]:
            self.status = 'ground'
            self.add(self.obstacle_sprites)
            self.add(self.attackable_sprites)

    def get_damage(self, player, weapon_type):
        if weapon_type == 'magic':
            self.killed = True