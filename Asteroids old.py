import pygame as py
import math

# Pygame setup
py.init()
py.display.set_caption("Asteroids")
clock = py.time.Clock()

pxl = 64
w, h = 800, 800

screen = py.display.set_mode((w, h))

x, y = 400, 400
x_speed, y_speed = 0, 0

arrow = py.image.load("Arrow.png").convert_alpha()
glow = py.image.load("Glow.png").convert_alpha()
arrow_angle = 0
vel = 5

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

    keys = py.key.get_pressed()

    if keys[py.K_a]:
        arrow_angle += 2
    elif keys[py.K_d]:
        arrow_angle -= 2

    if keys[py.K_w]:
        angle_in_radians = math.radians(arrow_angle)
        x_speed = -vel * math.sin(angle_in_radians)
        y_speed = -vel * math.cos(angle_in_radians)
    elif keys[py.K_s]:
        angle_in_radians = math.radians(arrow_angle)
        x_speed = vel * math.sin(angle_in_radians)
        y_speed = vel * math.cos(angle_in_radians)
    else:
        x_speed *= deceleration
        y_speed *= deceleration

    if x < -64:
        x = w + 64
    if x > w + 64:
        x = -64
    if y < -64:
        y = h + 64
    if y > h + 64:
        y = -64
        
    x += x_speed 
    y += y_speed
    
    rotated_arrow = py.transform.rotozoom(arrow, arrow_angle, 1)
    rotated_glow = py.transform.rotozoom(glow, arrow_angle, 1)
    
    rotated_arrow_rect = rotated_arrow.get_rect(center = (x, y))
    rotated_glow_rect = rotated_glow.get_rect(center = (x, y))

    screen.blit(rotated_arrow, rotated_arrow_rect)
    screen.blit(rotated_glow, rotated_glow_rect)

    py.display.update()
    clock.tick(100)

py.quit()
