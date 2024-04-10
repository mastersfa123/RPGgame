from .entity import Enemy
import pygame


class Tiles(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect(topleft=(x, y))


class Decoration(pygame.sprite.Sprite):
    def __init__(self, x, y, img):
        super().__init__()
        self.image = pygame.image.load(img)
        self.rect = self.image.get_rect(bottomleft=(x, y))


class Building(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        self.animation = [
            pygame.image.load(f'assets/shop/shop{i}.png') for i in range(1, 7)
        ]
        self.current_frame = 0
        self.image = self.animation[self.current_frame]
        self.rect = self.animation[self.current_frame].get_rect(bottomleft=(x, y))

    def update(self):
        self.current_frame = (self.current_frame + 1) % len(self.animation)

    def draw(self, screen):
        screen.blit(self.animation[self.current_frame], self.rect)
        self.update()


class Location:
    def __init__(self):
        self.width = 800
        self.height = 600
        self.bg = [
            pygame.image.load('assets/background/background1.png'),
            pygame.image.load('assets/background/background2.png'),
            pygame.image.load('assets/background/background3.png'),
        ]
        self.tiles = pygame.sprite.Group()
        self.tiles.add(Tiles(0, 570, 'assets/tiles/ground2.png'))
        self.tiles.add(Tiles(75, 570, 'assets/tiles/ground2.png'))
        self.tiles.add(Tiles(150, 570, 'assets/tiles/ground3.png'))
        self.tiles.add(Tiles(225, 570, 'assets/tiles/ground3.png'))
        self.tiles.add(Tiles(300, 570, 'assets/tiles/ground3.png'))
        self.tiles.add(Tiles(375, 570, 'assets/tiles/ground3.png'))
        self.tiles.add(Tiles(450, 570, 'assets/tiles/ground3.png'))
        self.tiles.add(Tiles(525, 570, 'assets/tiles/ground3.png'))
        self.tiles.add(Tiles(600, 570, 'assets/tiles/ground3.png'))
        self.tiles.add(Tiles(675, 570, 'assets/tiles/ground3.png'))
        self.tiles.add(Tiles(750, 570, 'assets/tiles/ground3.png'))
        self.tiles.add(Tiles(825, 570, 'assets/tiles/ground3.png'))
        self.tiles.add(Tiles(900, 570, 'assets/tiles/ground3.png'))
        self.tiles.add(Tiles(975, 570, 'assets/tiles/ground3.png'))
        self.tiles.add(Tiles(1050, 570, 'assets/tiles/ground3.png'))
        self.tiles.add(Tiles(1125, 570, 'assets/tiles/ground3.png'))
        self.tiles.add(Tiles(1200, 570, 'assets/tiles/ground3.png'))
        self.tiles.add(Tiles(1275, 570, 'assets/tiles/ground3.png'))
        self.tiles.add(Tiles(1325, 570, 'assets/tiles/ground3.png'))
        self.tiles.add(Tiles(1400, 570, 'assets/tiles/ground3.png'))
        self.decor = pygame.sprite.Group()
        self.decor.add(Decoration(75, 570, 'assets/decoration/lampa.png'))
        self.decor.add(Decoration(150, 570, 'assets/decoration/fence1.png'))
        self.buildings = pygame.sprite.Group()
        self.buildings.add(Building(525, 570))
        self.enemies = pygame.sprite.Group()
        self.enemies.add(Enemy())
        self.object = pygame.sprite.Group()
        self.object.add(self.tiles, self.decor, self.buildings, self.enemies)


    def draw(self, screen):
        for i in self.bg:
            screen.blit(i, (0, 0))
        self.object.draw(screen)
        # self.enemies.update(screen, self)
        # self.tiles.draw(screen)
        # self.decor.draw(screen)
        # self.buildings.draw(screen)

    def move(self, delta_x):
        if delta_x > 0:
            if self.get_last().rect.right >= self.width:
                for obj in self.object:
                    obj.rect.x -= delta_x
        elif delta_x < 0:
            if self.object.sprites()[0].rect.left <= delta_x:
                for obj in self.object:
                    obj.rect.x -= delta_x

    def get_last(self):
        return max(self.object.sprites(), key=lambda obj: obj.rect.right)
