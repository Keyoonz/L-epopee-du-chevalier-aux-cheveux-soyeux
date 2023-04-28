import pygame

pygame.mixer.init()

volume = 2
effects_channel = pygame.mixer.Channel(1)
hurt_channel = pygame.mixer.Channel(2)
ennemy_channel = pygame.mixer.Channel(3)
EFFECTS = {
	'menu_selection': pygame.mixer.Sound('audio/effects/menu_selection.wav'),
	'menu_enter': pygame.mixer.Sound('audio/effects/menu_enter.wav'),
	'step1': pygame.mixer.Sound('audio/effects/step1.wav'),
	'step2': pygame.mixer.Sound('audio/effects/step2.wav'),
    'sword': pygame.mixer.Sound('audio/effects/sword.mp3'),
    'rah': pygame.mixer.Sound('audio/effects/rah.mp3'),
    'uh': pygame.mixer.Sound('audio/effects/uh.mp3'),
    'uh_enemy': pygame.mixer.Sound('audio/effects/uh_enemy.mp3'),
    'splash': pygame.mixer.Sound('audio/effects/splash.mp3')
}