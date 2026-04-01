import pygame
import random
import sys

pygame.init()

def get_korean_font(size):
    candidates = ["malgungothic", "applegothic", "nanumgothic", "notosanscjk"]
    for name in candidates:
        font = pygame.font.SysFont(name, size)
        if font.get_ascent() > 0:
            return font
    return pygame.font.SysFont(None, size)

WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE  = (255, 255, 255)
BLUE   = (50, 120, 220)
RED    = (220, 50, 50)
YELLOW = (240, 200, 0)
GRAY   = (40, 40, 40)
GREEN  = (50, 200, 100)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Dodger")
clock = pygame.time.Clock()
font = get_korean_font(36)
font_big = get_korean_font(72)

LEVELS = [
    {"min_speed": 3, "max_speed": 5,  "spawn": 40, "label": "Lv.1"},
    {"min_speed": 5, "max_speed": 8,  "spawn": 25, "label": "Lv.2"},
    {"min_speed": 7, "max_speed": 12, "spawn": 15, "label": "Lv.3"},
]

PLAYER_W, PLAYER_H = 50, 30
ENEMY_W, ENEMY_H = 30, 30
ITEM_SIZE = 25

def spawn_enemy(level_cfg):
    x = random.randint(0, WIDTH - ENEMY_W)
    speed = random.randint(level_cfg["min_speed"], level_cfg["max_speed"])
    return pygame.Rect(x, -ENEMY_H, ENEMY_W, ENEMY_H), speed

def spawn_item():
    x = random.randint(0, WIDTH - ITEM_SIZE)
    speed = random.randint(3, 6)
    return pygame.Rect(x, -ITEM_SIZE, ITEM_SIZE, ITEM_SIZE), speed

def draw_hud(score, level_cfg, lives):
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"{level_cfg['label']}", True, YELLOW), (10, 40))
    screen.blit(font.render(f"Lives: {'♥ ' * lives}", True, RED), (WIDTH - 180, 10))

def game_over_screen(score):
    screen.fill(GRAY)
    screen.blit(font_big.render("GAME OVER", True, RED), (220, 220))
    screen.blit(font.render(f"Score: {score}", True, WHITE), (350, 310))
    screen.blit(font.render("R: Restart   Q: Quit", True, WHITE), (270, 360))
    pygame.display.flip()
    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r: return True
                if e.key == pygame.K_q: pygame.quit(); sys.exit()

def main():
    player = pygame.Rect(WIDTH // 2 - PLAYER_W // 2, HEIGHT - 60, PLAYER_W, PLAYER_H)
    enemies = []
    items = []
    lasers = []

    score = 0
    lives = 3
    spawn_timer = 0
    item_timer = 0
    level_idx = 0
    level_cfg = LEVELS[level_idx]
    invincible = 0

    while True:
        clock.tick(FPS)

        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT] and player.left > 0:
            player.x -= 5
        if keys[pygame.K_RIGHT] and player.right < WIDTH:
            player.x += 5

        # 적 생성
        spawn_timer += 1
        if spawn_timer >= level_cfg["spawn"]:
            spawn_timer = 0
            rect, speed = spawn_enemy(level_cfg)
            enemies.append([rect, speed])

        # 아이템 생성
        item_timer += 1
        if item_timer >= 120:
            item_timer = 0
            if random.random() < 0.3:
                rect, speed = spawn_item()
                items.append([rect, speed])

        # ⭐ 레이저 생성
        laser_chance = min(0.01 + score * 0.0002, 0.05)
        if random.random() < laser_chance:
            delay = random.randint(30, 60)
            duration = 18
            lasers.append([player.centerx, 0, delay, duration, False, 0])
            # [x, timer, delay, duration, locked, state]

        # 적 이동
        survived = []
        for rect, speed in enemies:
            rect.y += speed
            if rect.top < HEIGHT:
                survived.append([rect, speed])
            else:
                score += 1
        enemies = survived

        # 아이템 이동
        survived_items = []
        for rect, speed in items:
            rect.y += speed
            if rect.top < HEIGHT:
                survived_items.append([rect, speed])
        items = survived_items

        # ⭐ 레이저 업데이트
        new_lasers = []
        for x, timer, delay, duration, locked, state in lasers:
            timer += 1

            # 0: 경고
            if state == 0:
                if delay - timer <= 12:
                    locked = True
                if not locked:
                    x = player.centerx
                if timer >= delay:
                    state = 1
                    timer = 0

            # 1: 대기 (0.05초 ≈ 3프레임)
            elif state == 1:
                if timer >= 3:
                    state = 2
                    timer = 0

            # 2: 빔
            elif state == 2:
                duration -= 1
                beam_rect = pygame.Rect(x - 12, 0, 24, HEIGHT)

                if invincible == 0 and player.colliderect(beam_rect):
                    lives -= 1
                    invincible = 90
                    if lives <= 0:
                        if game_over_screen(score):
                            main()
                        return

                if duration <= 0:
                    continue

            new_lasers.append([x, timer, delay, duration, locked, state])

        lasers = new_lasers

        # 충돌 처리
        if invincible > 0:
            invincible -= 1
        else:
            for rect, _ in enemies:
                if player.colliderect(rect):
                    lives -= 1
                    invincible = 90
                    enemies.clear()
                    if lives <= 0:
                        if game_over_screen(score):
                            main()
                        return
                    break

        # 아이템 충돌
        new_items = []
        for rect, speed in items:
            if player.colliderect(rect):
                lives = min(lives + 1, 5)
            else:
                new_items.append([rect, speed])
        items = new_items

        level_idx = min(score // 20, len(LEVELS) - 1)
        level_cfg = LEVELS[level_idx]

        screen.fill(GRAY)

        if (invincible // 10) % 2 == 0:
            pygame.draw.rect(screen, BLUE, player)

        for rect, _ in enemies:
            pygame.draw.rect(screen, RED, rect)

        for rect, _ in items:
            pygame.draw.rect(screen, GREEN, rect)

        # ⭐ 레이저 그리기
        for x, timer, delay, duration, locked, state in lasers:

            # 경고
            if state == 0:
                progress = timer / delay
                blink_speed = int(10 - progress * 8)
                if blink_speed < 2:
                    blink_speed = 2

                if (timer // blink_speed) % 2 == 0:
                    pygame.draw.line(screen, (255, 100, 100), (x, 0), (x, HEIGHT), 5)

            # 빔
            elif state == 2:
                alpha = int(128 + 127 * abs(pygame.math.Vector2(1, 0).rotate(timer * 20).x))
                beam = pygame.Surface((50, HEIGHT), pygame.SRCALPHA)
                beam.fill((255, 255, 255, alpha))
                screen.blit(beam, (x - 25, 0))

        draw_hud(score, level_cfg, lives)
        pygame.display.flip()

main()

