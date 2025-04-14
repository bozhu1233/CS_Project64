import stddraw
import random
import sys
import math

# Set up the game window
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 400
stddraw.setCanvasSize(WINDOW_WIDTH, WINDOW_HEIGHT)
stddraw.setXscale(0, WINDOW_WIDTH)
stddraw.setYscale(0, WINDOW_HEIGHT)

# Colors
WHITE = stddraw.WHITE
RED = stddraw.RED
BLUE = stddraw.BLUE
BLACK = stddraw.BLACK
GREEN = stddraw.GREEN

# Player stuff
player_x = WINDOW_WIDTH // 2
PLAYER_SIZE = 15
PLAYER_SPEED = 5
PLAYER_Y = 20
TURRET_LENGTH = 20
turret_angle = math.radians(90)  # Start pointing up
TURRET_ROTATE_SPEED = math.radians(1)  # Slower: ~60°/sec
turret_direction = 1  # 1 for right-to-left, -1 for left-to-right

# Missile stuff
MISSILE_SIZE = 5
MISSILE_SPEED = 8
missiles = []
RECHARGE_TIME = 30  # ~0.5s at 60 FPS
recharge_timer = 0
can_shoot = True  # No longer restricts shooting

# Enemy stuff
ENEMY_SIZE = 15
ENEMY_SPEED = 1
enemies = []
ENEMY_ROWS = 2
ENEMY_COLS = 4
ENEMY_SPACING = 80

# Game stuff
score = 0
game_over = False
enemy_direction = 1

def show_start_screen():
    stddraw.clear(BLACK)
    stddraw.setPenColor(WHITE)
    stddraw.setFontSize(50)
    stddraw.text(WINDOW_WIDTH // 2, 350, "COSMIC CONQUISTADORS")
    stddraw.setFontSize(30)
    stddraw.text(WINDOW_WIDTH // 2, 250, "Instructions:")
    stddraw.setFontSize(20)
    stddraw.text(WINDOW_WIDTH // 2, 200, "[A] move left, [D] move right")
    stddraw.text(WINDOW_WIDTH // 2, 170, "[Space] to shoot")
    stddraw.text(WINDOW_WIDTH // 2, 140, "Turret rotates automatically")
    stddraw.text(WINDOW_WIDTH // 2, 110, "[X] to quit")
    stddraw.text(WINDOW_WIDTH // 2, 80, "[R] to restart after game over")
    stddraw.setFontSize(30)
    stddraw.text(WINDOW_WIDTH // 2, 50, "Press any key to start")
    stddraw.show(0)
    while True:
        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            if key == 'x':
                sys.exit()
            break
        stddraw.show(100)

def start_game():
    global player_x, missiles, enemies, game_over, score, enemy_direction, turret_angle, recharge_timer, can_shoot, turret_direction
    player_x = WINDOW_WIDTH // 2
    missiles = []
    enemies = []
    score = 0
    game_over = False
    enemy_direction = 1
    turret_angle = math.radians(90)
    recharge_timer = 0
    can_shoot = True
    turret_direction = 1
    for row in range(ENEMY_ROWS):
        for col in range(ENEMY_COLS):
            enemy_x = 100 + col * ENEMY_SPACING
            enemy_y = WINDOW_HEIGHT - 50 - row * ENEMY_SPACING
            enemies.append([enemy_x, enemy_y])

def draw_stuff():
    stddraw.clear(BLACK)
    stddraw.setPenColor(WHITE)
    stddraw.setFontSize(20)
    stddraw.text(50, WINDOW_HEIGHT - 20, f"Score: {score}")
    stddraw.setPenColor(BLUE)
    stddraw.filledCircle(player_x, PLAYER_Y, PLAYER_SIZE)
    stddraw.setPenColor(WHITE)
    turret_end_x = player_x + TURRET_LENGTH * math.cos(turret_angle)
    turret_end_y = PLAYER_Y + TURRET_LENGTH * math.sin(turret_angle)
    stddraw.line(player_x, PLAYER_Y, turret_end_x, turret_end_y)
    stddraw.setPenColor(WHITE)
    for missile in missiles:
        stddraw.filledCircle(missile[0], missile[1], MISSILE_SIZE)
    stddraw.setPenColor(RED)
    for enemy in enemies:
        stddraw.filledCircle(enemy[0], enemy[1], ENEMY_SIZE)
    stddraw.show(20)

def check_hits():
    global score, game_over
    for missile in missiles[:]:
        for enemy in enemies[:]:
            if ((missile[0] - enemy[0]) ** 2 + (missile[1] - enemy[1]) ** 2) ** 0.5 < (MISSILE_SIZE + ENEMY_SIZE):
                missiles.remove(missile)
                enemies.remove(enemy)
                score += 10
                break
        if (missile[1] > WINDOW_HEIGHT or missile[0] < 0 or 
            missile[0] > WINDOW_WIDTH or missile[1] < 0):
            missiles.remove(missile)
    for enemy in enemies:
        dist = ((player_x - enemy[0]) ** 2 + (PLAYER_Y - enemy[1]) ** 2) ** 0.5

def play_game():
    global player_x, enemy_direction, game_over, turret_angle, recharge_timer, can_shoot, turret_direction
    start_game()
    while not game_over:
        # Removed recharge timer logic to allow continuous shooting
        turret_angle += TURRET_ROTATE_SPEED * turret_direction
        if turret_angle > math.radians(180):
            turret_angle = math.radians(180)
            turret_direction = -1
        elif turret_angle < math.radians(0):
            turret_angle = math.radians(0)
            turret_direction = 1
        while stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            if key == 'a' and player_x > PLAYER_SIZE:
                player_x -= PLAYER_SPEED
            elif key == 'd' and player_x < WINDOW_WIDTH - PLAYER_SIZE:
                player_x += PLAYER_SPEED
            elif key == ' ':  # Removed can_shoot condition
                missile_x = player_x + TURRET_LENGTH * math.cos(turret_angle)
                missile_y = PLAYER_Y + TURRET_LENGTH * math.sin(turret_angle)
                missiles.append([missile_x, missile_y,
                               MISSILE_SPEED * math.cos(turret_angle),
                               MISSILE_SPEED * math.sin(turret_angle)])
                turret_direction *= -1  # Flip direction after shot
            elif key == 'x':
                sys.exit()
        for missile in missiles:
            missile[0] += missile[2]
            missile[1] += missile[3]
        move_down = False
        for enemy in enemies:
            enemy[0] += ENEMY_SPEED * enemy_direction
            if enemy[0] < ENEMY_SIZE or enemy[0] > WINDOW_WIDTH - ENEMY_SIZE:
                move_down = True
        if move_down:
            enemy_direction *= -1
            for enemy in enemies:
                enemy[1] -= 20
        check_hits()
        if not enemies:
            game_over = True
        draw_stuff()
    stddraw.clear(BLACK)
    stddraw.setFontSize(40)
    if enemies:
        stddraw.setPenColor(RED)
        stddraw.text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, "Game Over!")
    else:
        stddraw.setPenColor(GREEN)
        stddraw.text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2, "You Win!")
    stddraw.setFontSize(20)
    stddraw.text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 30, f"Score: {score}")
    stddraw.text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 60, "Press 'r' to restart")
    stddraw.text(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 90, "Press 'x' to quit")
    stddraw.show(0)
    while True:
        if stddraw.hasNextKeyTyped():
            key = stddraw.nextKeyTyped()
            if key == 'r':
                break
            if key == 'x':
                sys.exit()
        stddraw.show(100)

print("Starting my cool space game!")
while True:
    show_start_screen()
    play_game()
