import pygame
import math

pygame.init()

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
clock = pygame.time.Clock()

font = pygame.font.SysFont(None, 36)

# 색상
BLUE = (0, 0, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLACK = (0, 0, 0)
GRAY = (160, 160, 160)

# ---------------- PLAYER ----------------
player = pygame.Rect(100, 100, 100, 100)
player_surf = pygame.Surface((100, 100))
player_surf.fill(GRAY)

# ---------------- OBB (FIXED) ----------------
fixed = pygame.Rect(WIDTH//2 - 50, HEIGHT//2 - 50, 100, 100)
fixed_base = pygame.Surface((100, 100), pygame.SRCALPHA)
fixed_base.fill(GRAY)

fixed_angle = 0
rotation_speed = 1
speed = 5

# ---------------- OBB ----------------
def get_rotated_rect(rect, angle):
    cx, cy = rect.center
    w, h = rect.width / 2, rect.height / 2

    corners = [(-w, -h), (w, -h), (w, h), (-w, h)]
    rotated = []

    rad = math.radians(angle)

    for x, y in corners:
        rx = x * math.cos(rad) - y * math.sin(rad)
        ry = x * math.sin(rad) + y * math.cos(rad)
        rotated.append((cx + rx, cy + ry))

    return rotated

def dot(a, b):
    return a[0]*b[0] + a[1]*b[1]

def get_axes(points):
    axes = []
    for i in range(len(points)):
        p1 = points[i]
        p2 = points[(i+1) % len(points)]
        edge = (p2[0] - p1[0], p2[1] - p1[1])
        normal = (-edge[1], edge[0])
        length = math.hypot(normal[0], normal[1])
        axes.append((normal[0]/length, normal[1]/length))
    return axes

def project(points, axis):
    min_p = float('inf')
    max_p = float('-inf')
    for p in points:
        proj = dot(p, axis)
        min_p = min(min_p, proj)
        max_p = max(max_p, proj)
    return min_p, max_p

def obb_collision(p1, p2):
    axes = get_axes(p1) + get_axes(p2)
    for axis in axes:
        min1, max1 = project(p1, axis)
        min2, max2 = project(p2, axis)
        if max1 < min2 or max2 < min1:
            return False
    return True

# ---------------- LOOP ----------------
running = True
while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    keys = pygame.key.get_pressed()

    # 이동
    if keys[pygame.K_LEFT]:
        player.x -= speed
    if keys[pygame.K_RIGHT]:
        player.x += speed
    if keys[pygame.K_UP]:
        player.y -= speed
    if keys[pygame.K_DOWN]:
        player.y += speed

    player.clamp_ip(screen.get_rect())

    # 회전
    fixed_angle += rotation_speed

    # ---------------- 충돌 ----------------
    pc = player.center
    fc = fixed.center

    pr = player.width // 2
    fr = fixed.width // 2

    dx = pc[0] - fc[0]
    dy = pc[1] - fc[1]
    dist = math.sqrt(dx*dx + dy*dy)

    circle_hit = dist <= (pr + fr)
    aabb_hit = player.colliderect(fixed)

    player_pts = get_rotated_rect(player, 0)
    fixed_pts = get_rotated_rect(fixed, fixed_angle)

    obb_hit = obb_collision(player_pts, fixed_pts)

    # ---------------- RENDER ----------------
    screen.fill(BLACK)

    # 🔷 AABB 스프라이트
    screen.blit(player_surf, player.topleft)

    # 🔷 OBB 스프라이트 (수정된 부분)
    rotated = pygame.transform.rotate(fixed_base, -fixed_angle)
    rect = rotated.get_rect(center=fixed.center)
    screen.blit(rotated, rect.topleft)

    # 🔷 윤곽선
    pygame.draw.rect(screen, RED, player, 2)
    pygame.draw.polygon(screen, GREEN, fixed_pts, 2)

    # 🔵 원
    pygame.draw.circle(screen, BLUE, pc, pr, 2)
    pygame.draw.circle(screen, BLUE, fc, fr, 2)

    # ---------------- TEXT ----------------
    screen.blit(font.render("Circle: " + ("HIT" if circle_hit else "SAFE"), True, BLUE), (10, 10))
    screen.blit(font.render("AABB: " + ("HIT" if aabb_hit else "SAFE"), True, RED), (10, 50))
    screen.blit(font.render("OBB: " + ("HIT" if obb_hit else "SAFE"), True, GREEN), (10, 90))

    pygame.display.flip()

pygame.quit()