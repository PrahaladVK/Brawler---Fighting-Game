import pygame
import sys
from pygame import mixer
from fighter import Fighter

mixer.init()
pygame.init()

# Create game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Brawler")

# Set framerate
clock = pygame.time.Clock()
FPS = 60

# Define colours
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
WHITE = (255, 255, 255)

# Define game variables
score = [0, 0]  # Player scores. [P1, P2]
round_over = False
ROUND_OVER_COOLDOWN = 2000

# Define fighter variables
WARRIOR_SIZE = 162
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [72, 56]
WARRIOR_DATA = [WARRIOR_SIZE, WARRIOR_SCALE, WARRIOR_OFFSET]
WIZARD_SIZE = 250
WIZARD_SCALE = 3
WIZARD_OFFSET = [112, 107]
WIZARD_DATA = [WIZARD_SIZE, WIZARD_SCALE, WIZARD_OFFSET]

# Load music and sounds
pygame.mixer.music.load("assets/audio/music.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1, 0.0, 5000)
sword_fx = pygame.mixer.Sound("assets/audio/sword.wav")
sword_fx.set_volume(0.5)
magic_fx = pygame.mixer.Sound("assets/audio/magic.wav")
magic_fx.set_volume(0.75)

# Load background image
bg_image = pygame.image.load("assets/images/background/background.jpg").convert_alpha()

# Load spritesheets
warrior_sheet = pygame.image.load("assets/images/warrior/Sprites/warrior.png").convert_alpha()
wizard_sheet = pygame.image.load("assets/images/wizard/Sprites/wizard.png").convert_alpha()

# Load victory image
victory_img = pygame.image.load("assets/images/icons/victory.png").convert_alpha()

# Define number of steps in each animation
WARRIOR_ANIMATION_STEPS = [10, 8, 1, 7, 7, 3, 7]
WIZARD_ANIMATION_STEPS = [8, 8, 1, 8, 8, 3, 7]

# Define font
count_font = pygame.font.Font("assets/fonts/turok.ttf", 80)
score_font = pygame.font.Font("assets/fonts/turok.ttf", 30)

# Global variables for fighters
fighter_1 = None
fighter_2 = None

def create_fighters():
    global fighter_1, fighter_2
    fighter_1 = Fighter(1, 200, 310, False, WARRIOR_DATA, warrior_sheet, WARRIOR_ANIMATION_STEPS, sword_fx)
    fighter_2 = Fighter(2, 700, 310, True, WIZARD_DATA, wizard_sheet, WIZARD_ANIMATION_STEPS, magic_fx)

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg():
    scaled_bg = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

def draw_health_bar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400, 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

def game_loop():
    global round_over
    intro_count = 3
    last_count_update = pygame.time.get_ticks()
    create_fighters()
    run = True

    while run:
        clock.tick(FPS)

        draw_bg()
        draw_health_bar(fighter_1.health, 20, 20)
        draw_health_bar(fighter_2.health, 580, 20)
        draw_text("P1: " + str(score[0]), score_font, RED, 20, 60)
        draw_text("P2: " + str(score[1]), score_font, RED, 580, 60)

        if intro_count <= 0:
            fighter_1.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_2, round_over)
            fighter_2.move(SCREEN_WIDTH, SCREEN_HEIGHT, screen, fighter_1, round_over)
        else:
            draw_text(str(intro_count), count_font, RED, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 3)
            if (pygame.time.get_ticks() - last_count_update) >= 1000:
                intro_count -= 1
                last_count_update = pygame.time.get_ticks()

        fighter_1.update()
        fighter_2.update()
        fighter_1.draw(screen)
        fighter_2.draw(screen)

        if round_over:
            screen.blit(victory_img, (SCREEN_WIDTH // 2 - victory_img.get_width() // 2, SCREEN_HEIGHT // 3))  # Display victory image

            pygame.display.update()
            pygame.time.wait(2000)  # wait for 2 seconds
            round_over = False  # reset round_over flag
            create_fighters()  # create new fighters for the next round

        if round_over == False:
            if fighter_1.alive == False:
                score[1] += 1
                round_over = True
            elif fighter_2.alive == False:
                score[0] += 1
                round_over = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False

        pygame.display.update()

    round_over = False

def draw_menu():
    screen.fill((0, 0, 0))  # Fill the screen with black
    draw_text("Main Menu", count_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 4)
    draw_text("1. New Game", score_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
    draw_text("2. Exit", score_font, WHITE, SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 50)
    pygame.display.update()

def main_menu():
    while True:
        draw_menu()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_1:
                    game_loop()
                elif event.key == pygame.K_2:
                    pygame.quit()
                    sys.exit()

if __name__ == "__main__":
    main_menu()
    pygame.quit()