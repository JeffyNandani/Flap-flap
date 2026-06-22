import pygame
from sys import exit
import random

# game variables
GAME_WIDTH = 360
GAME_HEIGHT = 640

# bird variables
bird_x = GAME_WIDTH / 8
bird_y = GAME_HEIGHT / 2
bird_width = 34
bird_height = 24


class Bird(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, bird_x, bird_y, bird_width, bird_height)
        self.img = img


# pipe variables
pipe_x = GAME_WIDTH
pipe_y = 0
pipe_width = 64
pipe_height = 512


class Pipe(pygame.Rect):
    def __init__(self, img):
        pygame.Rect.__init__(self, pipe_x, pipe_y, pipe_width, pipe_height)
        self.img = img
        self.passed = False


pygame.init()

# images
backgroundzz = pygame.image.load("Assets/flappybirdbg.png")
up = pygame.image.load("Assets/toppipe.png")
down = pygame.image.load("Assets/bottompipe.png")
bird_img = pygame.image.load("Assets/flappybird.png")

bird_img = pygame.transform.scale(bird_img, (bird_width, bird_height))
up = pygame.transform.scale(up, (pipe_width, pipe_height))
down = pygame.transform.scale(down, (pipe_width, pipe_height))

# game setup
screen = pygame.display.set_mode((GAME_WIDTH, GAME_HEIGHT))
pygame.display.set_caption("Flappy Bird")
clock = pygame.time.Clock()

# game logic
bird = Bird(bird_img)
pipes = []

velocity_x = -2
velocity_y = 0
gravity = 0.4
game_over = False


def draw():
    screen.blit(backgroundzz, (0, 0))
    screen.blit(bird.img, bird)

    for pipe in pipes:
        screen.blit(pipe.img, pipe)

    if game_over:
        font = pygame.font.SysFont("Arial", 40)
        text = font.render("Game Over", True, "white")
        screen.blit(text, (90, 250))


def move():
    global velocity_y, game_over

    # bird movement
    velocity_y += gravity
    bird.y += velocity_y

    # top limit
    if bird.y < 0:
        bird.y = 0

    # bottom collision
    if bird.y > GAME_HEIGHT:
        game_over = True

    # pipe movement
    for pipe in pipes:
        pipe.x += velocity_x

        # collision with bird
        if bird.colliderect(pipe):
            game_over = True

    # remove off-screen pipes
    while len(pipes) > 0 and pipes[0].x < -pipe_width:
        pipes.pop(0)


def create_pipe():
    random_pipe_y = pipe_y - pipe_height / 4 - random.random() * (pipe_height / 2)
    gap = GAME_HEIGHT / 4

    # top pipe
    top_pipe = Pipe(up)
    top_pipe.y = random_pipe_y
    pipes.append(top_pipe)

    # bottom pipe
    bottom_pipe = Pipe(down)
    bottom_pipe.y = top_pipe.y + pipe_height + gap
    pipes.append(bottom_pipe)


# pipe spawn timer
create_pipe_timer = pygame.USEREVENT + 1
pygame.time.set_timer(create_pipe_timer, 1500)

# game loop
running = True
while running:
    for even in pygame.event.get():
        if even.type == pygame.QUIT:
            pygame.quit()
            exit()

        if even.type == create_pipe_timer and not game_over:
            create_pipe()

        if even.type == pygame.KEYDOWN:
            if even.key == pygame.K_SPACE:

                if game_over:
                    # restart game
                    bird.y = bird_y
                    pipes.clear()
                    velocity_y = 0
                    game_over = False
                else:
                    # jump
                    velocity_y = -6

    if not game_over:
        move()

    draw()
    pygame.display.update()
    clock.tick(60)