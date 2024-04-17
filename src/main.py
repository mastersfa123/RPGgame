import pygame
from core.location import Location
from core.entity import Player

pygame.init()
WIDTH = 800
HEIGHT = 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
icon = pygame.image.load('assets/RPGIcon.png')
pygame.display.set_icon(icon)
pygame.display.set_caption('RPGgame')
location = Location()
player = Player()


running = True
while running:
    location.update(screen, player)
    keys = pygame.key.get_pressed()
    event_list = pygame.event.get()
    player.update(keys, screen, event_list, location)
    for event in event_list:
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
    pygame.display.update()
    clock.tick(20)
