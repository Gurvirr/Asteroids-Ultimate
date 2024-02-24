import pygame as py
import math
import random

# Pygame setup
py.init()
py.display.set_caption("Asteroids")
clock = py.time.Clock()
font = py.freetype.Font("assets/FiraMono-Medium.ttf", 20)

# Screen setup
w, h = 1920, 1080
screen = py.display.set_mode((w, h))

# Colours
white = (255, 255, 255)
black = (17, 17, 17)

# Text renderer
def render_text(text, x, y):
    font.render_to(screen, (x, y), text, white)

# Player info
x, y = w / 2, h / 2
x_speed, y_speed = 0, 0
sprite_w, sprite_h = 48, 64
vel = 0
acceleration = 0.005
angle = 0
deceleration = 0.98
bullet_positions = []
shot_time = 0
bullet_delay = 80
angle_offsets = [offset for offset in range(-180, 181, 15)]
guide_x, guide_y = 0, 0
beam_x, beam_y = 0, 0
show_guide_lines = False
tractor_beam = False
click_count = 0

shake_intensity = 7
shake_duration = 2500
shake_start_time = -shake_duration  # Initialize with a negative value
shake_offset = (0, 0)

def calculate_screen_shake():
    global shake_start_time, shake_offset

    current_time = py.time.get_ticks()
    elapsed_time = current_time - shake_start_time

    if elapsed_time < shake_duration:
        shake_offset = (random.uniform(-shake_intensity, shake_intensity),
                        random.uniform(-shake_intensity, shake_intensity))
    else:
        shake_offset = (0, 0)

tractor_beam_duration = 2500
tractor_beam_start_time = 0

# Image handler
arrow_img = py.image.load("assets/Arrow.png").convert_alpha()
arrow_glow_img = py.image.load("assets/Arrow Glow.png").convert_alpha()
bullet_img = py.image.load("assets/Bullet.png").convert_alpha()
bullet_glow_img = py.image.load("assets/Bullet Glow.png").convert_alpha()
guide_lines_img = py.image.load("assets/Guide Line.png").convert_alpha()
tractor_beam_glow_img = py.image.load("assets/Tractor Beam Glow.png").convert_alpha()
tractor_beam_img = py.image.load("assets/Tractor Beam.png").convert_alpha()

# Audio handler
bullet_sfx = py.mixer.Sound("assets/Bullet SFX.wav")
tractor_beam_sfx = py.mixer.Sound("assets/Tractor Beam SFX.wav")

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

            # Bullet - Regular
            if event.key == py.K_SPACE or event.key == py.K_q:
                bullet_angle = angle
                bullet_x, bullet_y = rotated_arrow_rect.center
                bullet_x -= 30 * math.sin(math.radians(bullet_angle))
                bullet_y -= 30 * math.cos(math.radians(bullet_angle))
                bullet_positions.append([bullet_x, bullet_y, bullet_angle])
                bullet_sfx.play()

            # Bullet - Pulse
            if event.key == py.K_e:
                shots = 0
                while shots < len(angle_offsets):
                    bullet_angle = angle + angle_offsets[shots]
                    bullet_x, bullet_y = rotated_arrow_rect.center
                    bullet_positions.append([bullet_x, bullet_y, bullet_angle])
                    shots += 1
                bullet_sfx.play()

            # Bullet - Tractor Beam
            if event.key == py.K_f and not tractor_beam:
                click_count += 1
                show_guide_lines = not show_guide_lines

                if click_count == 2:
                    tractor_beam_sfx.play()
                    tractor_beam = not tractor_beam
                    click_count = 0
                    tractor_beam_start_time = py.time.get_ticks()
                    shake_start_time = py.time.get_ticks()

    keys = py.key.get_pressed()

    # Player rotation
    if keys[py.K_a] and not tractor_beam:
        if not show_guide_lines:
            angle += 3
        else:
            angle += 1
    elif keys[py.K_d] and not tractor_beam:
        if not show_guide_lines:
            angle -= 3
        else:
            angle -= 1

    # Player movement
    if keys[py.K_w] and not tractor_beam:
        if x_speed > -9 or y_speed > -9:
            x_speed += -vel
            y_speed += -vel
            # Acceleration
            vel += acceleration

    elif keys[py.K_s] and not tractor_beam:
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

    # TEST CODE
    colour = (97, 212, 97)

    # Bullet handler
    for bullet in bullet_positions:
        bullet[0] -= 9.5 * math.sin(math.radians(bullet[2]))
        bullet[1] -= 9.5 * math.cos(math.radians(bullet[2]))

        rotated_bullet = py.transform.rotozoom(bullet_img, bullet[2], 1)
        rotated_bullet_glow = py.transform.rotozoom(bullet_glow_img, bullet[2], 1)

        rotated_bullet_rect = rotated_bullet.get_rect(center = (bullet[0] + shake_offset[0], bullet[1] + shake_offset[1]))
        rotated_bullet_glow_rect = rotated_bullet_glow.get_rect(center = (bullet[0] + shake_offset[0], bullet[1] + shake_offset[1]))

        screen.blit(rotated_bullet_glow, rotated_bullet_glow_rect)
        screen.blit(rotated_bullet, rotated_bullet_rect)

        # Bullet culling
        if bullet[0] < 0 or bullet[0] > w or bullet[1] < 0 or bullet[1] > h:
            bullet_positions.remove(bullet)

        # Bullet collision handler
        if rotated_bullet_rect.colliderect(asteroid):
            colour = (255, 0, 0)

    if show_guide_lines:
        guide_x, guide_y = x, y
        guide_x -= 1010 * math.sin(math.radians(angle))
        guide_y -= 1010 * math.cos(math.radians(angle))
        rotated_guide_lines = py.transform.rotozoom(guide_lines_img, angle, 1)
        rotated_guide_lines_rect = rotated_guide_lines.get_rect(center = (guide_x, guide_y))
        screen.blit(rotated_guide_lines, rotated_guide_lines_rect)

    if tractor_beam:
        beam_x, beam_y = x, y
        beam_x -= 995 * math.sin(math.radians(angle))
        beam_y -= 995 * math.cos(math.radians(angle))

        rotated_tractor_beam_glow = py.transform.rotozoom(tractor_beam_glow_img, angle, 1)
        rotated_tractor_beam = py.transform.rotozoom(tractor_beam_img, angle, 1)

        rotated_tractor_beam_glow_rect = rotated_tractor_beam_glow.get_rect(center = (beam_x, beam_y))
        rotated_tractor_beam_rect = rotated_tractor_beam.get_rect(center = (beam_x, beam_y))

        # Apply screen shake to the tractor beam
        screen.blit(rotated_tractor_beam_glow, (rotated_tractor_beam_glow_rect.x + shake_offset[0], rotated_tractor_beam_glow_rect.y + shake_offset[1]))
        screen.blit(rotated_tractor_beam, (rotated_tractor_beam_rect.x + shake_offset[0], rotated_tractor_beam_rect.y + shake_offset[1]))
        
        if rotated_tractor_beam_rect.colliderect(asteroid):
            colour = (255, 0, 0)
            
        if py.time.get_ticks() - tractor_beam_start_time >= tractor_beam_duration:
            tractor_beam = False

    # TEST CODE
    asteroid = py.Rect(300, 300, 60, 60)
    py.draw.rect(screen, colour, asteroid)

    # Rotation handler
    rotated_arrow = py.transform.rotozoom(arrow_img, angle, 1)
    rotated_arrow_glow = py.transform.rotozoom(arrow_glow_img, angle, 1)

    rotated_arrow_rect = rotated_arrow.get_rect(center = (x + shake_offset[0], y + shake_offset[1]))
    rotated_arrow_glow_rect = rotated_arrow_glow.get_rect(center = (x + shake_offset[0], y + shake_offset[1]))

    # Display handler
    screen.blit(rotated_arrow, rotated_arrow_rect)
    screen.blit(rotated_arrow_glow, rotated_arrow_glow_rect)

    render_text(str(rotated_arrow_rect.center), 10, 10)
    render_text(str(angle), 10, 40)

    py.display.update()
    clock.tick(100)
    calculate_screen_shake()

py.quit()
