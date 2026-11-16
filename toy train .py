import pygame
import sys
import random

pygame.init()

# SCREEN
WIDTH, HEIGHT = 1100, 700
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Indian Railway Train Simulator - Game")
clock = pygame.time.Clock()

# COLORS
BLACK = (15, 15, 20)
WHITE = (245, 245, 245)
GREY = (100, 105, 110)
DARK = (45, 45, 50)
CONCRETE = (170, 165, 155)
BLUE = (20, 75, 155)
LIGHT_BLUE = (40, 130, 210)
RED = (190, 30, 30)
YELLOW = (255, 210, 30)
GREEN = (20, 130, 70)
BROWN = (105, 65, 35)
ORANGE = (230, 130, 30)

font = pygame.font.SysFont("Arial", 18, bold=True)
small = pygame.font.SysFont("Arial", 13, bold=True)
big = pygame.font.SysFont("Arial", 30, bold=True)
huge = pygame.font.SysFont("Arial", 54, bold=True)

# GAME SETTINGS
LANES = [345, 505]              # upper and lower railway tracks
PLAYER_X = 100
PLAYER_SPEED = 4
TARGET_SCORE = 500
player_lane = 0
score = 0
level = 1
game_over = False
won = False
paused = False

# The player's train
player_train = ["S1", "S2", "S3"]
player_width = len(player_train) * 85 + 130
player_y = LANES[player_lane]

# Traffic and obstacles
traffic = []
spawn_timer = 0
traffic_speed = 5
font_message = pygame.font.SysFont("Arial", 22, bold=True)


def draw_text(text, font_type, color, x, y):
    image = font_type.render(str(text), True, color)
    screen.blit(image, (x, y))


def draw_station():
    screen.fill((195, 210, 220))

    # Station building
    pygame.draw.rect(screen, (185, 180, 165), (0, 0, WIDTH, 255))
    pygame.draw.rect(screen, DARK, (0, 0, WIDTH, 22))

    # Windows
    for x in range(20, WIDTH, 150):
        pygame.draw.rect(screen, BLUE, (x, 35, 110, 75))
        pygame.draw.rect(screen, WHITE, (x + 48, 35, 4, 75))

    # Station name
    pygame.draw.rect(screen, GREEN, (300, 115, 500, 50))
    pygame.draw.rect(screen, WHITE, (300, 115, 500, 50), 3)
    draw_text("INDIAN RAILWAYS", big, WHITE, 430, 123)

    # Information board
    pygame.draw.rect(screen, BLACK, (340, 25, 440, 75))
    pygame.draw.rect(screen, YELLOW, (340, 25, 440, 75), 3)
    draw_text("TRAIN INFORMATION", font, YELLOW, 455, 30)
    draw_text("12631  CHENNAI EXPRESS", small, WHITE, 355, 55)
    draw_text("ARR: 10:30   DEP: 10:45", small, GREEN, 355, 77)

    # Shops
    shops = [
        (30, "TEA & COFFEE", BROWN),
        (240, "FOOD STALL", RED),
        (450, "BOOK SHOP", BLUE),
        (660, "SNACKS", GREEN),
    ]
    for x, name, color in shops:
        pygame.draw.rect(screen, color, (x, 185, 170, 65))
        pygame.draw.rect(screen, WHITE, (x, 185, 170, 65), 3)
        pygame.draw.rect(screen, YELLOW, (x, 165, 170, 22))
        draw_text(name, small, BLACK, x + 18, 190)
        pygame.draw.rect(screen, BROWN, (x + 10, 220, 150, 30))

    # Platform
    pygame.draw.rect(screen, CONCRETE, (0, 250, WIDTH, 85))
    pygame.draw.rect(screen, YELLOW, (0, 320, WIDTH, 5))

    for x in range(20, WIDTH, 260):
        pygame.draw.rect(screen, GREY, (x, 110, 12, 145))

    for x in [80, 480, 850]:
        pygame.draw.rect(screen, BROWN, (x, 290, 100, 10))
        pygame.draw.rect(screen, BROWN, (x + 10, 300, 8, 25))
        pygame.draw.rect(screen, BROWN, (x + 80, 300, 8, 25))

    for x in [170, 550, 950]:
        pygame.draw.line(screen, DARK, (x, 110), (x, 160), 5)
        pygame.draw.circle(screen, YELLOW, (x, 165), 12)

    # Passengers
    for x in [200, 390, 720, 1000]:
        pygame.draw.circle(screen, (210, 160, 120), (x, 265), 9)
        pygame.draw.rect(screen, BLUE, (x - 9, 275, 18, 32))
        pygame.draw.line(screen, BLACK, (x - 5, 305), (x - 8, 320), 4)
        pygame.draw.line(screen, BLACK, (x + 5, 305), (x + 8, 320), 4)


def draw_tracks():
    for y in [420, 580]:
        pygame.draw.rect(screen, (90, 90, 90), (0, y - 25, WIDTH, 65))
        for x in range(0, WIDTH, 35):
            pygame.draw.rect(screen, BROWN, (x, y - 20, 18, 55))
        pygame.draw.rect(screen, WHITE, (0, y - 10, WIDTH, 7))
        pygame.draw.rect(screen, WHITE, (0, y + 18, WIDTH, 7))


def draw_train(x, y, coaches, coach_width, engine_color):
    for i, name in enumerate(coaches):
        cx = x + i * coach_width
        pygame.draw.rect(screen, (220, 220, 220), (cx, y, coach_width, 60))
        pygame.draw.rect(screen, BLUE, (cx, y + 23, coach_width, 12))
        for wx in [8, 40]:
            pygame.draw.rect(screen, BLACK, (cx + wx, y + 7, 25, 17))
        pygame.draw.rect(screen, BLUE, (cx + 62, y + 32, 15, 28))
        draw_text(name, small, BLACK, cx + 28, y + 39)
        pygame.draw.circle(screen, BLACK, (cx + 20, y + 65), 9)
        pygame.draw.circle(screen, BLACK, (cx + coach_width - 20, y + 65), 9)

    engine_x = x + len(coaches) * coach_width
    pygame.draw.rect(screen, engine_color, (engine_x, y, 110, 60))
    pygame.draw.polygon(screen, engine_color, [
        (engine_x + 110, y), (engine_x + 130, y + 30),
        (engine_x + 110, y + 60)
    ])
    pygame.draw.rect(screen, BLACK, (engine_x + 15, y + 8, 35, 22))
    draw_text("INDIAN", small, WHITE, engine_x + 50, y + 38)
    pygame.draw.circle(screen, BLACK, (engine_x + 25, y + 65), 9)
    pygame.draw.circle(screen, BLACK, (engine_x + 80, y + 65), 9)


def draw_obstacle(item):
    # A red railway signal/barrier on the track
    x, lane = item["x"], item["lane"]
    y = LANES[lane] + 5
    pygame.draw.rect(screen, RED, (x, y, 45, 35), border_radius=5)
    pygame.draw.rect(screen, WHITE, (x + 7, y + 7, 31, 7))
    pygame.draw.rect(screen, YELLOW, (x + 7, y + 21, 31, 7))
    pygame.draw.circle(screen, BLACK, (x + 22, y + 42), 7)


def reset_game():
    global player_lane, player_y, score, level, game_over, won
    global traffic, spawn_timer, traffic_speed, paused
    player_lane = 0
    player_y = LANES[player_lane]
    score = 0
    level = 1
    traffic = []
    spawn_timer = 0
    traffic_speed = 5
    game_over = False
    won = False
    paused = False


def draw_hud():
    pygame.draw.rect(screen, BLACK, (10, 10, 260, 88), border_radius=8)
    draw_text(f"SCORE: {score}", font, YELLOW, 25, 20)
    draw_text(f"LEVEL: {level}", font, WHITE, 25, 48)
    draw_text(f"TARGET: {TARGET_SCORE}", font, GREEN, 130, 48)
    draw_text("UP/DOWN: CHANGE TRACK", small, WHITE, 25, 73)


def draw_end_screen():
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 175))
    screen.blit(overlay, (0, 0))
    if won:
        heading = "YOU WIN!"
        color = GREEN
        message = "You reached the target score!"
    else:
        heading = "GAME OVER"
        color = RED
        message = "Your train hit an obstacle!"
    title = huge.render(heading, True, color)
    screen.blit(title, title.get_rect(center=(WIDTH // 2, 270)))
    msg = font_message.render(message, True, WHITE)
    screen.blit(msg, msg.get_rect(center=(WIDTH // 2, 335)))
    msg2 = font_message.render(f"Final Score: {score}    Press R to Restart", True, YELLOW)
    screen.blit(msg2, msg2.get_rect(center=(WIDTH // 2, 390)))


# MAIN GAME LOOP
running = True
while running:
    dt = clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_ESCAPE:
                running = False

            if event.key == pygame.K_r and (game_over or won):
                reset_game()

            if not game_over and not won:
                if event.key == pygame.K_UP:
                    player_lane = 0
                elif event.key == pygame.K_DOWN:
                    player_lane = 1
                elif event.key == pygame.K_p:
                    paused = not paused

    if not game_over and not won and not paused:
        # Smoothly move the player's train between tracks
        player_y += (LANES[player_lane] - player_y) * 0.22

        # Spawn obstacles on either track
        spawn_timer += dt
        if spawn_timer >= max(650, 1450 - level * 90):
            spawn_timer = 0
            traffic.append({
                "x": WIDTH + 30,
                "lane": random.randint(0, 1),
                "passed": False
            })

        # Move obstacles towards the player's train
        current_speed = traffic_speed + (level - 1) * 0.8
        for item in traffic:
            item["x"] -= current_speed

            # Collision check
            obstacle_rect = pygame.Rect(item["x"], LANES[item["lane"]] + 5, 45, 35)
            player_rect = pygame.Rect(PLAYER_X, int(player_y), player_width - 10, 60)
            if item["lane"] == player_lane and player_rect.colliderect(obstacle_rect):
                game_over = True

            # Award points when an obstacle safely passes the player
            if not item["passed"] and item["x"] + 45 < PLAYER_X:
                item["passed"] = True
                score += 25

        traffic = [item for item in traffic if item["x"] > -60]

        # Level progression
        new_level = 1 + score // 125
        if new_level > level:
            level = new_level

        if score >= TARGET_SCORE:
            won = True

    # DRAW
    draw_station()
    draw_tracks()

    # Player train
    draw_train(PLAYER_X, int(player_y), player_train, 85, BLUE)

    # Draw obstacles
    for item in traffic:
        draw_obstacle(item)

    draw_hud()

    draw_text("WELCOME TO INDIAN RAILWAYS", font, WHITE, 390, 660)
    draw_text("P: PAUSE    ESC: QUIT", small, WHITE, 900, 15)

    if paused and not game_over and not won:
        draw_text("PAUSED - PRESS P TO CONTINUE", big, YELLOW, 330, 370)

    if game_over or won:
        draw_end_screen()

    pygame.display.flip()

pygame.quit()
sys.exit()
