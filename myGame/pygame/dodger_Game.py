import pygame
import random
import sys
import base64
import io

# ⭐ 너 base64 넣는 곳
SHEET_B64 = "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"

# =========================
# 🎧 AUDIO (추가된 부분)
# =========================
pygame.mixer.init()

LASER_SOUND_PATH = "./laser.wav"   # ⭐ 여기에 상대경로 (예: "./laser.wav")
BGM_PATH = "./background.mp3"           # ⭐ 여기에 상대경로 (예: "./bgm.mp3")

laser_sfx = None
bgm = None

try:
    if LASER_SOUND_PATH:
        laser_sfx = pygame.mixer.Sound(LASER_SOUND_PATH)

    if BGM_PATH:
        pygame.mixer.music.load(BGM_PATH)
        pygame.mixer.music.play(-1)  # 무한 반복
except:
    pass
# =========================

def load_base64_image(b64_string):
    image_data = base64.b64decode(b64_string)
    image_file = io.BytesIO(image_data)
    return pygame.image.load(image_file).convert_alpha()

pygame.init()

WIDTH, HEIGHT = 800, 600
FPS = 60

WHITE  = (255, 255, 255)
RED    = (220, 50, 50)
GREEN  = (50, 200, 100)
GRAY   = (40, 40, 40)
YELLOW = (240, 200, 0)
BLUE   = (50, 120, 220)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 36)
font_big = pygame.font.SysFont(None, 72)

PLAYER_W, PLAYER_H = 50, 30
ENEMY_W, ENEMY_H = 30, 30
ITEM_SIZE = 25

LEVELS = [
    {"min_speed": 3, "max_speed": 5,  "spawn": 40, "label": "Lv.1"},
    {"min_speed": 5, "max_speed": 8,  "spawn": 25, "label": "Lv.2"},
    {"min_speed": 7, "max_speed": 12, "spawn": 15, "label": "Lv.3"},
]

def spawn_enemy(level):
    x = random.randint(0, WIDTH - ENEMY_W)
    speed = random.randint(level["min_speed"], level["max_speed"])
    return pygame.Rect(x, -ENEMY_H, ENEMY_W, ENEMY_H), speed

def spawn_item():
    x = random.randint(0, WIDTH - ITEM_SIZE)
    speed = random.randint(3, 6)
    return pygame.Rect(x, -ITEM_SIZE, ITEM_SIZE, ITEM_SIZE), speed

def draw_hud(score, level_cfg, lives):
    screen.blit(font.render(f"Score: {score}", True, WHITE), (10, 10))
    screen.blit(font.render(f"{level_cfg['label']}", True, YELLOW), (10, 40))
    screen.blit(font.render(f"Lives: {'♥ ' * lives}", True, RED), (WIDTH - 180, 10))

def game_over(score):
    screen.fill(GRAY)
    screen.blit(font_big.render("GAME OVER", True, RED), (220, 220))
    screen.blit(font.render(f"Score: {score}", True, WHITE), (320, 320))
    screen.blit(font.render("R: Restart  Q: Quit", True, WHITE), (260, 380))
    pygame.display.flip()

    while True:
        for e in pygame.event.get():
            if e.type == pygame.QUIT:
                pygame.quit(); sys.exit()
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_r:
                    return True
                if e.key == pygame.K_q:
                    pygame.quit(); sys.exit()

def main():
    player = pygame.Rect(WIDTH//2, HEIGHT-60, PLAYER_W, PLAYER_H)
    enemies = []
    items = []
    lasers = []

    score = 0
    lives = 3
    spawn_timer = 0
    item_timer = 0

    level_idx = 0
    level = LEVELS[level_idx]

    sheet = load_base64_image(SHEET_B64)
    player_frames = []
    for i in range(3):
        frame = pygame.Surface((32, 32), pygame.SRCALPHA)
        frame.blit(sheet, (0, 0), (i * 32, 0, 32, 32))
        player_frames.append(frame)

    frame_index = 0
    frame_timer = 0
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

        frame_timer += 1
        if frame_timer >= 10:
            frame_timer = 0
            frame_index = (frame_index + 1) % len(player_frames)

        spawn_timer += 1
        if spawn_timer >= level["spawn"]:
            spawn_timer = 0
            enemies.append(list(spawn_enemy(level)))

        item_timer += 1
        if item_timer >= 120:
            item_timer = 0
            if random.random() < 0.3:
                items.append(list(spawn_item()))

        # ⭐ 레이저 생성 (SFX 추가됨)
        if random.random() < 0.03:
            delay = random.randint(30, 60)
            duration = 18
            lasers.append([player.centerx, 0, delay, duration, False, 0])

        new_enemies = []
        for rect, speed in enemies:
            rect.y += speed
            if rect.top < HEIGHT:
                new_enemies.append([rect, speed])
            else:
                score += 1
        enemies = new_enemies

        new_items = []
        for rect, speed in items:
            rect.y += speed
            if rect.top < HEIGHT:
                new_items.append([rect, speed])
        items = new_items

        new_lasers = []
        for x, timer, delay, duration, locked, state in lasers:
            timer += 1

            if state == 0:
                if delay - timer <= 12:
                    locked = True
                if not locked:
                    x = player.centerx
                if timer >= delay:
                    state = 1
                    timer = 0

            elif state == 1:
                if timer >= 3:
                    state = 2
                    timer = 0
                    
                    if laser_sfx:
                        laser_sfx.play()

            elif state == 2:
                duration -= 1
                beam_rect = pygame.Rect(x - 12, 0, 24, HEIGHT)

                if invincible == 0 and player.colliderect(beam_rect):
                    lives -= 1
                    invincible = 90

                    if lives <= 0:
                        if game_over(score):
                            main()
                        return

                if duration <= 0:
                    continue

            new_lasers.append([x, timer, delay, duration, locked, state])

        lasers = new_lasers

        if invincible > 0:
            invincible -= 1
        else:
            for rect, _ in enemies:
                if player.colliderect(rect):
                    lives -= 1
                    invincible = 90
                    enemies.clear()

                    if lives <= 0:
                        if game_over(score):
                            main()
                        return
                    break

        new_items = []
        for rect, speed in items:
            if player.colliderect(rect):
                lives = min(lives + 1, 5)
            else:
                new_items.append([rect, speed])
        items = new_items

        level_idx = min(score // 20, len(LEVELS) - 1)
        level = LEVELS[level_idx]

        screen.fill(GRAY)

        if invincible == 0 or (invincible // 10) % 2 == 0:
            img = pygame.transform.scale(player_frames[frame_index], (PLAYER_W, PLAYER_H))
            screen.blit(img, player)

        for rect, _ in enemies:
            pygame.draw.rect(screen, RED, rect)

        for rect, _ in items:
            pygame.draw.rect(screen, GREEN, rect)

        for x, timer, delay, duration, locked, state in lasers:

            if state == 0:
                progress = timer / delay
                blink_speed = max(2, int(10 - progress * 8))

                if (timer // blink_speed) % 2 == 0:
                    pygame.draw.line(screen, (255, 100, 100), (x, 0), (x, HEIGHT), 5)

            elif state == 2:
                alpha = int(128 + 127 * abs(pygame.math.Vector2(1, 0).rotate(timer * 20).x))
                beam = pygame.Surface((50, HEIGHT), pygame.SRCALPHA)
                beam.fill((255, 255, 255, alpha))
                screen.blit(beam, (x - 25, 0))

        draw_hud(score, level, lives)

        pygame.display.flip()

main()
