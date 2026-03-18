import pygame
import random
import math

pygame.init()

WIDTH, HEIGHT = 900, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Fancy Particle Playground")

clock = pygame.time.Clock()

particles = []

class Particle:
    def __init__(self, x, y):

        self.x = x
        self.y = y

        angle = random.uniform(0, math.pi * 2)
        speed = random.uniform(2, 7)

        self.vx = math.cos(angle) * speed
        self.vy = math.sin(angle) * speed

        self.life = random.randint(60, 100)
        self.size = random.randint(3, 6)

        self.hue = random.randint(0, 360)

    def update(self):

        self.x += self.vx
        self.y += self.vy

        self.vy += 0.05
        self.life -= 1

        self.hue += 3

    def get_color(self):

        r = int((math.sin(self.hue * 0.02) + 1) * 127)
        g = int((math.sin(self.hue * 0.02 + 2) + 1) * 127)
        b = int((math.sin(self.hue * 0.02 + 4) + 1) * 127)

        return (r, g, b)

    def draw(self, surf):

        color = self.get_color()

        # glow
        pygame.draw.circle(surf, color, (int(self.x), int(self.y)), self.size + 6)
        pygame.draw.circle(surf, color, (int(self.x), int(self.y)), self.size + 3)

        # main particle
        pygame.draw.circle(surf, (255,255,255), (int(self.x), int(self.y)), self.size)

    def alive(self):
        return self.life > 0


def draw_background(surface, t):

    for y in range(HEIGHT):
        c = int(50 + 30 * math.sin(y * 0.02 + t))
        color = (10, c, 80)
        pygame.draw.line(surface, color, (0, y), (WIDTH, y))


running = True
time = 0

while running:

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        # 큰 폭발
        if event.type == pygame.MOUSEBUTTONDOWN:
            for _ in range(120):
                particles.append(Particle(event.pos[0], event.pos[1]))

    mouse = pygame.mouse.get_pos()
    buttons = pygame.mouse.get_pressed()

    # 마우스 드래그 파티클
    if buttons[0]:
        for _ in range(10):
            particles.append(Particle(mouse[0], mouse[1]))

    time += 0.03

    draw_background(screen, time)

    for p in particles:
        p.update()
        p.draw(screen)

    particles = [p for p in particles if p.alive()]

    pygame.display.flip()
    clock.tick(60)

pygame.quit()