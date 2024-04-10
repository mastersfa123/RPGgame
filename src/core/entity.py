import pygame


class Animation:
    def __init__(self, frames, speed, resize=False):
        self.speed = speed
        self.clock = pygame.time.Clock()
        self.current_frame = 0
        if resize:
            self.frames = [
                self.scale_img(i)
                for i in frames
            ]
        else:
            self.frames = frames
        self.rect = self.frames[self.current_frame].get_rect()

    def update(self, x, y):
        self.clock.tick(self.speed)
        self.rect.x = x
        self.rect.y = y
        self.current_frame = (self.current_frame + 1) % len(self.frames)

    def draw(self, screen, direction_right):
        if direction_right:
            screen.blit(self.frames[self.current_frame], self.rect)
        else:
            screen.blit(pygame.transform.flip(self.frames[self.current_frame], True, False), self.rect)

    def scale_img(self, img):
        return pygame.transform.scale(
            img,
            (img.get_width() * 2, img.get_height() * 2)
        )


class Entity(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super().__init__()
        self.name = name
        self.health = 100
        self.base_damage = 10
        self.speed = 10
        self.level = 1
        self.intelligence = 1
        self.stamina = 10
        self.position_x = x
        self.position_y = y

    def get_damage(self, damage):
        self.health -= damage

    def level_up(self):
        self.level += 1


class Enemy(Entity):
    def __init__(self, name='axe_warrior', x=300, y=300, *args, **kwargs):
        super().__init__(name, x, y)
        self.animation_walk = Animation([
            pygame.image.load(f'assets/enemies/axe_warrior/walk/walk{i}.png') for i in range(1, 7)
        ], 20)
        self.animation_fall = Animation([
            pygame.image.load(f'assets/enemies/axe_warrior/walk/walk{i}.png') for i in range(1, 7)
        ], 20)
        self.animation_jump = Animation([
            pygame.image.load(f'assets/enemies/axe_warrior/walk/walk{i}.png') for i in range(1, 7)
        ], 20)
        self.animation = self.animation_walk
        self.direction_right = True
        self.on_ground = False
        self.gravity = 15
        self.is_jumping = False
        self.jump_force = 8
        self.jump_count = self.jump_force
        self.rect = self.animation.rect

    def check_collision(self, tiles):
        self.on_ground = False
        collided_tiles = pygame.sprite.spritecollide(self.animation, tiles, False)
        for tile in collided_tiles:
            if self.animation.rect.colliderect(tile.rect):
                if tile.rect.top < self.animation.rect.bottom < tile.rect.bottom:
                    self.on_ground = True

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.animation = self.animation_jump
        else:
            if self.jump_count > 0:

                self.position_y -= (self.jump_count ** 2) / 2

                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = self.jump_force
            self.animation = self.animation_jump

    def fall(self):
        self.position_y += self.gravity
        self.animation = self.animation_fall

    def update(self, screen, location):
        self.animation.update(self.position_x, self.position_y)
        self.animation.draw(screen, self.direction_right)
        self.check_collision(location.tiles)

        if not self.on_ground:
            if not self.is_jumping:
                self.fall()
            else:
                self.jump()


class Player(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.direction_right = True
        self.position_x = 300
        self.position_y = 300
        self.speed = 10
        self.is_jumping = False
        self.jump_force = 8
        self.jump_count = self.jump_force
        self.on_ground = False
        self.gravity = 15

        self.animation_idle = Animation([
            pygame.image.load(f'assets/player/idle/idle{i}.png') for i in range(1, 7)
        ], 20, resize=True)
        self.animation_run = Animation([
            pygame.image.load(f'assets/player/run/run{i}.png') for i in range(1, 9)
        ], 20, resize=True)
        self.animation_attack = Animation([
            pygame.image.load(f'assets/player/attack/attack{i}.png') for i in range(1, 9)
        ], 20, resize=True)
        self.animation_jump = Animation([
            pygame.image.load(f'assets/player/jump/jump{i}.png') for i in range(1, 9)
        ], 20, resize=True)
        self.animation_dead = Animation([
            pygame.image.load(f'assets/player/dead/dead{i}.png') for i in range(1, 13)
        ], 20, resize=True)
        self.animation_fall = Animation([
            pygame.image.load(f'assets/player/fall/jump{i}.png') for i in range(9, 17)
        ], 20, resize=True)
        self.animation = self.animation_idle

    def move_left(self, location):
        location.move(- self.speed)
        self.direction_right = False
        if self.position_x - self.speed > 200:
            self.position_x -= self.speed
        if self.is_jumping:
            self.animation = self.jump
        else:
            self.animation = self.animation_run

    def move_right(self, location):
        location.move(self.speed)
        self.direction_right = True
        if self.position_x + self.speed < 600:
            self.position_x += self.speed
        self.animation = self.animation_run

    def idle(self):
        self.animation = self.animation_idle

    def attack(self):
        self.animation = self.animation_attack

    def jump(self):
        if not self.is_jumping:
            self.is_jumping = True
            self.animation = self.animation_jump
        else:
            if self.jump_count > 0:

                self.position_y -= (self.jump_count ** 2) / 2

                self.jump_count -= 1
            else:
                self.is_jumping = False
                self.jump_count = self.jump_force
            self.animation = self.animation_jump

    def update(self, keys, screen, event_list, location):
        self.animation.update(self.position_x, self.position_y)
        self.animation.draw(screen, self.direction_right)
        self.check_collision(location.tiles)

        if keys[pygame.K_d]:
            self.move_right(location)
        elif keys[pygame.K_a]:
            self.move_left(location)
        else:
            self.idle()
        if not self.on_ground:
            if not self.is_jumping:
                self.fall()
            else:
                self.jump()
        else:
            if keys[pygame.K_SPACE]:
                self.jump()

        for event in event_list:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    self.attack()

    def check_collision(self, tiles):
        self.on_ground = False
        collided_tiles = pygame.sprite.spritecollide(self.animation, tiles, False)
        for tile in collided_tiles:
            if self.animation.rect.colliderect(tile.rect):
                if tile.rect.top < self.animation.rect.bottom < tile.rect.bottom:
                    self.on_ground = True

    def fall(self):
        self.position_y += self.gravity
        self.animation = self.animation_fall
