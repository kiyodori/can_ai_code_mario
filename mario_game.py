import pygame
from pygame.locals import *

pygame.init()

# 画面の設定
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Simple Mario Game")

# マリオの設定
mario_pos = [WIDTH // 2, HEIGHT - 150]
mario_speed = 5
jumping = False
jump_count = 10

game_over = False

# 敵キャラクターのクラス
class Enemy:
    def __init__(self, x, y, speed):
        self.x = x
        self.y = y
        self.speed = speed

    def move(self):
        self.x -= self.speed
        if self.x < -50:
            self.x = WIDTH

    def draw(self):
        draw_detailed_goomba(self.x, self.y)

    def get_rect(self):
        return pygame.Rect(self.x, self.y, 50, 70)

enemy = Enemy(WIDTH, HEIGHT - 150, 4)

def draw_detailed_mario(x, y):
    # Body
    pygame.draw.rect(screen, (255, 0, 0), (x+15, y+40, 20, 20))
    pygame.draw.rect(screen, (0, 0, 255), (x+5, y+60, 40, 15))

    # Head
    pygame.draw.ellipse(screen, (255, 223, 196), (x+10, y+10, 30, 30))

    # Hat
    pygame.draw.polygon(screen, (255, 0, 0), [(x+10, y+10), (x+25, y), (x+40, y+10)])

    # Eyes
    pygame.draw.ellipse(screen, (255, 255, 255), (x+20, y+15, 8, 8))
    pygame.draw.ellipse(screen, (255, 255, 255), (x+28, y+15, 8, 8))
    pygame.draw.ellipse(screen, (0, 0, 0), (x+23, y+18, 4, 4))
    pygame.draw.ellipse(screen, (0, 0, 0), (x+31, y+18, 4, 4))

    # Nose
    pygame.draw.ellipse(screen, (255, 223, 196), (x+25, y+25, 6, 8))

    # Mouth
    pygame.draw.arc(screen, (0, 0, 0), (x+20, y+30, 15, 10), 0, 3.14)

    # Legs
    pygame.draw.rect(screen, (0, 0, 255), (x+10, y+75, 10, 10))
    pygame.draw.rect(screen, (0, 0, 255), (x+30, y+75, 10, 10))

    # Shoes
    pygame.draw.ellipse(screen, (255, 0, 0), (x+5, y+85, 15, 5))
    pygame.draw.ellipse(screen, (255, 0, 0), (x+30, y+85, 15, 5))

    # Arms
    pygame.draw.rect(screen, (255, 0, 0), (x, y+45, 10, 15))
    pygame.draw.rect(screen, (255, 0, 0), (x+40, y+45, 10, 15))

def draw_detailed_goomba(x, y):
    # Body
    pygame.draw.ellipse(screen, (139, 69, 19), (x+10, y+30, 30, 20))

    # Head
    pygame.draw.ellipse(screen, (139, 69, 19), (x+5, y+10, 40, 25))

    # Eyes
    pygame.draw.ellipse(screen, (255, 255, 255), (x+15, y+15, 10, 10))
    pygame.draw.ellipse(screen, (255, 255, 255), (x+25, y+15, 10, 10))
    pygame.draw.ellipse(screen, (0, 0, 0), (x+18, y+18, 5, 5))
    pygame.draw.ellipse(screen, (0, 0, 0), (x+28, y+18, 5, 5))

    # Feet
    pygame.draw.ellipse(screen, (0, 0, 0), (x+10, y+45, 15, 5))
    pygame.draw.ellipse(screen, (0, 0, 0), (x+25, y+45, 15, 5))

def draw_background():
    # Sky, Ground, Clouds, Hills... (as previously defined)
    screen.fill((135, 206, 235))
    pygame.draw.rect(screen, (0, 128, 0), (0, HEIGHT-50, WIDTH, 50))

def check_collision(player_rect, enemy_rect):
    return player_rect.colliderect(enemy_rect)

def display_game_over_screen():
    screen.fill((0, 0, 0))
    font = pygame.font.Font(None, 74)
    game_over_text = font.render('GAME OVER', True, (255, 0, 0))
    screen.blit(game_over_text, (WIDTH // 2 - game_over_text.get_width() // 2, HEIGHT // 2 - game_over_text.get_height() // 2))
    font = pygame.font.Font(None, 36)
    restart_text = font.render('Press SPACE to restart', True, (255, 255, 255))
    screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 50))
    pygame.display.flip()

running = True
while running:
    for event in pygame.event.get():
        if event.type == QUIT:
            running = False

    # ゲームループ内でのキー入力の処理部分
    keys = pygame.key.get_pressed()
    if keys[K_LEFT] and mario_pos[0] > 0:
        mario_pos[0] -= mario_speed
    if keys[K_RIGHT] and mario_pos[0] < WIDTH - 50:  # 50はマリオの幅
        mario_pos[0] += mario_speed
    if not jumping and keys[K_SPACE]:
        jumping = True

    # ジャンプの処理
    if jumping:
        if jump_count >= -10:
            neg = 1
            if jump_count < 0:
                neg = -1
            mario_pos[1] -= (jump_count ** 2) * 0.5 * neg
            jump_count -= 1
        else:
            jumping = False
            jump_count = 10

    # Drawing
    if not game_over:
        draw_background()
        draw_detailed_mario(*mario_pos)
        enemy.move()
        enemy.draw()

        mario_rect = pygame.Rect(mario_pos[0], mario_pos[1], 50, 80)
        if check_collision(mario_rect, enemy.get_rect()):
            game_over = True
            display_game_over_screen()
    else:
        keys = pygame.key.get_pressed()
        if keys[K_SPACE]:
            game_over = False
            mario_pos = [WIDTH // 2, HEIGHT - 150]  # Y座標を正確に設定
            jumping = False  # 追加: ジャンプ状態をリセット
            jump_count = 10  # 追加: ジャンプカウントをリセット
            enemy.x = WIDTH

    pygame.display.flip()
    pygame.time.Clock().tick(60)

pygame.quit()
