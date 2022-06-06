import pygame
from sys import exit
from random import randint, choice


class Dino(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        dino_standing = pygame.image.load(
            'graphics/Dino/dino-stationary.png').convert_alpha()
        dino_run_1 = pygame.image.load(
            'graphics/Dino/dino-run-0.png').convert_alpha()
        dino_run_2 = pygame.image.load(
            'graphics/Dino/dino-run-1.png').convert_alpha()
        self.dino_run = [dino_run_1, dino_run_2, dino_standing]
        self.dino_index = 2

        self.image = self.dino_run[self.dino_index]
        self.rect = self.image.get_rect(midbottom=(80, 300))
        self.gravity = 0

        self.jump_sound = pygame.mixer.Sound('audio/jump.mp3')
        self.jump_sound.set_volume(0.25)

    def dino_input(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE] and self.rect.bottom >= 300:
            self.gravity = -18
            self.jump_sound.play()

    def apply_gravity(self):
        self.gravity += 1
        self.rect.y += self.gravity
        if self.rect.bottom >= 300:
            self.rect.bottom = 300

    def animation_state(self):
        self.dino_index += 0.1
        if self.dino_index >= len(self.dino_run):
            self.dino_index = 0
        self.image = self.dino_run[int(self.dino_index)]

    def update(self):
        self.dino_input()
        self.apply_gravity()
        self.animation_state()


class Obstacle(pygame.sprite.Sprite):
    def __init__(self, choice):
        super().__init__()

        self.choice = choice
        if choice == 'cactus1':
            cactus = pygame.image.load(
                'graphics/Cactus/Cactus-1.png').convert_alpha()
            cactus = pygame.transform.rotozoom(cactus, 0, 0.75)
            self.image = cactus
            self.rect = self.image.get_rect(
                midbottom=(randint(900, 1100), 300))
        elif choice == 'cactus2':
            cactus = pygame.image.load(
                'graphics/Cactus/Cactus-2.png').convert_alpha()
            cactus = pygame.transform.rotozoom(cactus, 0, 0.65)
            self.image = cactus
            self.rect = self.image.get_rect(
                midbottom=(randint(900, 1100), 300))
        else:
            bird_fly1 = pygame.image.load('graphics/Bird/T_.png')
            bird_fly2 = pygame.image.load('graphics/Bird/T_2.png')
            bird_fly1 = pygame.transform.rotozoom(bird_fly1, 0, 0.375)
            bird_fly2 = pygame.transform.rotozoom(bird_fly2, 0, 0.375)
            self.bird_fly = [bird_fly1, bird_fly2]
            self.bird_fly_index = 0
            self.image = self.bird_fly[self.bird_fly_index]
            self.rect = self.image.get_rect(
                midbottom=(randint(900, 1100), 180))

    def update(self):
        global obstacle_speed
        self.rect.x -= obstacle_speed
        if self.choice == 'bird':
            self.animation_state()
        self.destroy()

    def destroy(self):
        if self.rect.x <= -100:
            self.kill()

    def animation_state(self):
        self.bird_fly_index += 0.1
        if self.bird_fly_index >= len(self.bird_fly):
            self.bird_fly_index = 0
        self.image = self.bird_fly[int(self.bird_fly_index)]


def display_score():
    current_time = int(pygame.time.get_ticks() / 1000) - start_time
    score_surf = test_font.render(
        f'Score: {current_time}', False, (64, 64, 64))
    score_rect = score_surf.get_rect(center=(400, 50))
    screen.blit(score_surf, score_rect)
    return current_time


def collision_sprite():
    if pygame.sprite.spritecollide(dino.sprite, obstacle_group, False):
        obstacle_group.empty()
        return False
    else:
        return True


pygame.init()
screen = pygame.display.set_mode((800, 400))
pygame.display.set_caption('Dinosaur Game')
clock = pygame.time.Clock()
test_font = pygame.font.Font('font/Pixeltype.ttf', 50)
game_active = False
start_time = 0
score = 0
bg_music = pygame.mixer.Sound('audio/music.wav')
bg_music.play(loops=-1).set_volume(0.25)

# Groups
dino = pygame.sprite.GroupSingle()
dino.add(Dino())

obstacle_group = pygame.sprite.Group()

obstacle_speed = 6

# sky_surface = pygame.image.load('graphics/Sky.png').convert()
ground_surface = pygame.image.load('graphics/groundline.png').convert()

# Intro screen
dino_stand = pygame.image.load(
    'graphics/Dino/dino-stationary.png').convert_alpha()
dino_stand = pygame.transform.rotozoom(dino_stand, 0, 2)
dino_stand_rect = dino_stand.get_rect(center=(400, 200))

game_name = test_font.render('Dino Sprinter', False, (111, 196, 169))
game_name_rect = game_name.get_rect(center=(400, 80))

game_message = test_font.render('Press space to start', False, (111, 196, 169))
game_message_rect = game_message.get_rect(center=(400, 330))

# Timer
obstacle_timer = pygame.USEREVENT + 1
obstacle_timer_speed = 1500
pygame.time.set_timer(obstacle_timer, obstacle_timer_speed)

while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()

        if game_active:
            if event.type == obstacle_timer:
                obstacle_group.add(
                    Obstacle(choice(['bird', 'cactus2', 'cactus1', 'cactus1'])))
                if obstacle_timer_speed >= 1000:
                    obstacle_timer_speed -= 25
                    pygame.time.set_timer(obstacle_timer, obstacle_timer_speed)

                if obstacle_speed <= 50:
                    obstacle_speed += 0.4

        else:
            if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                game_active = True
                start_time = int(pygame.time.get_ticks() / 1000)
                obstacle_timer_speed = 1500
                obstacle_speed = 6

    if game_active:
        # screen.blit(sky_surface, (0, 0))
        screen.fill((255, 255, 255))
        screen.blit(ground_surface, (0, 280))
        score = display_score()

        dino.draw(screen)
        dino.update()

        obstacle_group.draw(screen)
        obstacle_group.update()

        game_active = collision_sprite()

    else:
        screen.fill((94, 129, 162))
        screen.blit(dino_stand, dino_stand_rect)

        score_message = test_font.render(
            f'Your score: {score}', False, (111, 196, 169))
        score_message_rect = score_message.get_rect(center=(400, 330))
        screen.blit(game_name, game_name_rect)

        if score == 0:
            screen.blit(game_message, game_message_rect)
        else:
            screen.blit(score_message, score_message_rect)

    pygame.display.update()
    clock.tick(60)
