import pygame as py
import math

# Pygame setup
py.init()
py.display.set_caption("Asteroids")
clock = py.time.Clock()

w, h = 1200, 800
screen = py.display.set_mode((w, h))    

x, y = 400, 400
x_speed, y_speed = 0, 0
vel = 0
acceleration = 0.005  # Rate of acceleration increase

arrow = py.image.load("Arrow.png").convert_alpha()
glow = py.image.load("Glow.png").convert_alpha()
arrow_angle = 0

deceleration = 0.98  # Adjust the deceleration rate as needed

run_program = True
while run_program:
    screen.fill((17, 17, 17))

    for event in py.event.get():
        if event.type == py.QUIT:
            run_program = False
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                run_program = False
            if event.key == py.K_SPACE:
                print("hello")

    keys = py.key.get_pressed()

    if keys[py.K_a]:
        arrow_angle += 3
    elif keys[py.K_d]:
        arrow_angle -= 3

    if keys[py.K_w]:
        if x_speed > -9 or y_speed > -9:
            x_speed += -vel
            y_speed += -vel
            vel += acceleration

    elif keys[py.K_s]:
        if x_speed < 9 or y_speed < 9:
            x_speed += vel
            y_speed += vel
            vel += acceleration
    
    else:
        # Reset acceleration when not pressing "W" or "S"
        vel = 0
        x_speed *= deceleration
        y_speed *= deceleration
        if -0.3 < x_speed < 0.3 or -0.3 < y_speed < 0.3:
            x_speed = 0
            y_speed = 0

    if x < -32:
        x = w + 32
    if x > w + 32:
        x = -32
    if y < -32:
        y = h + 32
    if y > h + 32:
        y = -32

    angle_in_radians = math.radians(arrow_angle)
    x += x_speed * math.sin(angle_in_radians)
    y += y_speed * math.cos(angle_in_radians)
    
    surface = py.Surface((50, 50))
    surface.fill((255,255,255))
    
    rotated_surface = py.transform.rotate(surface, arrow_angle)
    rotated_rect = rotated_surface.get_rect(center = (x, y))
    screen.blit(rotated_surface, (rotated_rect))
    
    py.display.update()
    clock.tick(100)

py.quit()
