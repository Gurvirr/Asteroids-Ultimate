import pygame as py
import math

# Pygame setup
py.init()
py.display.set_caption("Asteroids")
clock = py.time.Clock()

pxl = 64
w, h = 1200, 800
counter = 0
screen = py.display.set_mode((w, h))

x, y = 400, 400
x_speed, y_speed = 0, 0
 # Initial acceleration rate
vel = 0
max_vel = 5  # Maximum velocity
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
        angle_in_radians = math.radians(arrow_angle)
        if x_speed > -9 or y_speed > -9:
            x_speed += -vel
            y_speed += -vel
            vel += acceleration

    elif keys[py.K_s]:
        angle_in_radians = math.radians(arrow_angle)
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
    
    rotated_arrow = py.transform.rotozoom(arrow, arrow_angle, 1)
    rotated_glow = py.transform.rotozoom(glow, arrow_angle, 1)
    
    rotated_arrow_rect = rotated_arrow.get_rect(center = (x, y))
    rotated_glow_rect = rotated_glow.get_rect(center = (x, y))

    screen.blit(rotated_arrow, rotated_arrow_rect)
    screen.blit(rotated_glow, rotated_glow_rect)

    py.display.update()
    clock.tick(100)

py.quit()
