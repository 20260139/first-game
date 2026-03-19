import pygame
import sys
import random

pygame.init()
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("My First Pygame")

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 30)

x = 400
y = 300
speed = 5
radius = 50

color = (0, 200, 255)

running = True

while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # 방향키 누를 때 색 변경
        if event.type == pygame.KEYDOWN:
            if event.key in (pygame.K_LEFT, pygame.K_RIGHT, pygame.K_UP, pygame.K_DOWN):
                color = (
                    random.randint(0,255),
                    random.randint(0,255),
                    random.randint(0,255)
                )

    # 🔥 이동 벡터 생성
    move = pygame.math.Vector2(0, 0)
    keys = pygame.key.get_pressed()

    if keys[pygame.K_LEFT]:
        move.x -= 1
    if keys[pygame.K_RIGHT]:
        move.x += 1
    if keys[pygame.K_UP]:
        move.y -= 1
    if keys[pygame.K_DOWN]:
        move.y += 1

    # 🔥 normalize 적용 (속도 균일화)
    if move.length() != 0:
        move = move.normalize() * speed

    x += move.x
    y += move.y

    # 화면 밖 제한
    x = max(radius, min(x, 800 - radius))
    y = max(radius, min(y, 600 - radius))

    screen.fill(BLACK)
    pygame.draw.circle(screen, color, (int(x), int(y)), radius)

    # FPS 표시
    fps = int(clock.get_fps())
    fps_text = font.render(f"FPS: {fps}", True, WHITE)
    screen.blit(fps_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()