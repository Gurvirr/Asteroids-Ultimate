import pygame as py
import math

# Pygame setup
py.init()
py.display.set_caption("Asteroids")
clock = py.time.Clock()
font = py.freetype.Font("assets/FiraMono-Medium.ttf", 20)

# Screen setup
w, h = 1200, 800
screen = py.display.set_mode((w, h))

# Colours
white = (255,255,255)
black = (17,17,17)

# Text renderer
def render_text(text, x, y): 
    font.render_to(screen, (x, y), text, white)

# Player info
x, y = 600, 400
x_speed, y_speed = 0, 0
sprite_w, sprite_h = 48, 64
vel = 0
acceleration = 0.005
angle = 0
deceleration = 0.98
bullet_positions = []

# Image handler
arrow_img = py.image.load("assets/Arrow.png").convert_alpha()
glow_img = py.image.load("assets/Glow.png").convert_alpha()
bullet_img = py.image.load("assets/Bullet.png").convert_alpha()

active = True

# Game loop
while active:
    screen.fill((17, 17, 17))

    # Event listener
    for event in py.event.get():
        if event.type == py.QUIT:
            active = False
        if event.type == py.KEYDOWN:
            if event.key == py.K_ESCAPE:
                active = False
            if event.key == py.K_SPACE or event.key == py.K_q:
                bullet_angle = angle
                bullet_x, bullet_y = rotated_arrow_rect.center
                bullet_positions.append([bullet_x, bullet_y, bullet_angle])

    keys = py.key.get_pressed()

    # Player rotation
    if keys[py.K_a]:    
        angle += 3
    elif keys[py.K_d]:
        angle -= 3

    # Player movement
    if keys[py.K_w]:
        if x_speed > -9 or y_speed > -9:
            x_speed += -vel
            y_speed += -vel
            # Acceleration
            vel += acceleration

    elif keys[py.K_s]:
        if x_speed < 9 or y_speed < 9:
            x_speed += vel
            y_speed += vel
            # Acceleration
            vel += acceleration

    # Deceleration
    else:
        vel = 0
        x_speed *= deceleration
        y_speed *= deceleration
        if -0.3 < x_speed < 0.3 or -0.3 < y_speed < 0.3:
            x_speed = 0
            y_speed = 0

    # Boundary teleportation
    if x < -sprite_w:
        x = w + sprite_w
    if x > w + sprite_w:
        x = -sprite_w
    if y < -sprite_h:
        y = h + sprite_h
    if y > h + sprite_h:
        y = -sprite_h
    
    # Position handler
    angle_in_radians = math.radians(angle)
    x += x_speed * math.sin(angle_in_radians)
    y += y_speed * math.cos(angle_in_radians)
    
    # Bullet handler
    for bullet in bullet_positions:
        bullet[0] -= 9.5 * math.sin(math.radians(bullet[2]))
        bullet[1] -= 9.5 * math.cos(math.radians(bullet[2]))
        rotated_bullet = py.transform.rotozoom(bullet_img, bullet[2], 1)
        rotated_bullet_rect = rotated_bullet.get_rect(center = (bullet[0], bullet[1]))
        screen.blit(rotated_bullet, rotated_bullet_rect)
    
    # Rotation handler
    rotated_arrow = py.transform.rotozoom(arrow_img, angle, 1)
    rotated_glow = py.transform.rotozoom(glow_img, angle, 1)
    rotated_arrow_rect = rotated_arrow.get_rect(center = (x, y))
    rotated_glow_rect = rotated_glow.get_rect(center = (x, y))
    
    # Display handler
    screen.blit(rotated_arrow, rotated_arrow_rect)
    screen.blit(rotated_glow, rotated_glow_rect)
    render_text(str(rotated_arrow_rect.center), 10, 10)
    render_text(str(angle), 10, 40)
    
    py.display.update()
    clock.tick(100)

py.quit()
