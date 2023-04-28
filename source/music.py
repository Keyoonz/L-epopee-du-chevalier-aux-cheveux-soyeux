import pygame

pygame.mixer.init()

volume = 0
last_music = "game"
current_music = "game"

MUSIC = {
	'menu': pygame.mixer.Sound('audio/intro.mp3'),
	'game': pygame.mixer.Sound('audio/map.mp3'),
    'fight': pygame.mixer.Sound('audio/fight.mp3'),
}