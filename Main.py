import pygame
from pygame.locals import *
import sys
import math
from gun import *
from Tiles import *
from Enemies import *

pygame.init()
pygame.font.init()
pygame.mixer.init()
font = pygame.font.Font(None, 36)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Edvins Spel")
Clock = pygame.time.Clock()


# Load player images for different states (idle and jump)
player_idle1_surf = pygame.image.load("Graphics/player/playeridle1.png").convert_alpha()
player_idle2_surf = pygame.image.load("Graphics/player/playeridle2.png").convert_alpha()
player_idle3_surf = pygame.image.load("Graphics/player/playeridle3.png").convert_alpha()
player_walkup_surf = pygame.image.load("Graphics/player/playerwalkup.png").convert_alpha()
player_walkup1_surf = pygame.image.load("Graphics/player/playerwalkup1.png").convert_alpha()
player_walkup2_surf = pygame.image.load("Graphics/player/playerwalkup2.png").convert_alpha()
player_walkdown_surf = pygame.image.load("Graphics/player/playerwalkdown.png").convert_alpha()
player_walkdown1_surf = pygame.image.load("Graphics/player/playerwalkdown1.png").convert_alpha()
player_walkdown2_surf = pygame.image.load("Graphics/player/playerwalkdown2.png").convert_alpha()
player_walkdown3_surf = pygame.image.load("Graphics/player/playerwalkdow3.png").convert_alpha()


player_walkleft1_surf = pygame.image.load("Graphics/player/playerwalkleft1.png").convert_alpha()
player_walkleft2_surf = pygame.image.load("Graphics/player/playerwalkleft2.png").convert_alpha()
player_walkleft3_surf = pygame.image.load("Graphics/player/playerwalkleft3.png").convert_alpha()
player_walkright1_surf = pygame.image.load("Graphics/player/playerwalkright1.png").convert_alpha()
player_walkright2_surf = pygame.image.load("Graphics/player/playerwalkright2.png").convert_alpha()
player_walkright3_surf = pygame.image.load("Graphics/player/playerwalkright3.png").convert_alpha()


# Set player_rect and initial player_surf to idle surface
playerwalkdownlist = [player_walkdown_surf, player_walkdown1_surf, player_walkdown2_surf, player_walkdown3_surf]
playerwalkuplist = [player_walkup_surf, player_walkup1_surf, player_walkup2_surf]
playeridlelist = [player_idle1_surf, player_idle2_surf, player_idle3_surf]
playerwalkleftlist = [player_walkleft1_surf, player_walkleft2_surf, player_walkleft3_surf]
playerwalkrightlist = [player_walkright1_surf, player_walkright2_surf, player_walkright3_surf]
player_surf = playeridlelist[0]
player_rect = player_surf.get_rect(center=(WIDTH//2, HEIGHT//2))
player_speed = 10  # Adjust the player's movement speed


# Initialize flags to track key presses
moving_left = False
moving_right = False
moving_up = False
moving_down = False
on_platform = False
# Animation variables
walk_frame = 0
walk_animation_speed = 7
idle_index = 0
animation_speed = 0.15
left_index = 0
right_index = 0
up_index = 0
down_index = 0
gun = Gun(screen)

frame = screen.get_rect()
camera = frame.copy()

snail_surf = pygame.image.load("Graphics/foes/snail1.png")



snails = []







def display_menu():
    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    menu_running = False

        screen.fill((0, 0, 0))
        title_surface = font.render("Snails", True, (255, 255, 255))
        start_surface = font.render("Press SPACE to start", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
        start_rect = start_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 150))
        screen.blit(title_surface, title_rect)
        screen.blit(start_surface, start_rect)
        pygame.display.flip()

display_menu()

running = True
while running:
    Clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Set flags when keys are pressed or released
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_a:
                moving_left = True
            if event.key == pygame.K_d:
                moving_right = True
            if event.key == pygame.K_w:
                moving_up = True
            if event.key == pygame.K_s:
                moving_down = True

            if event.key == pygame.K_e:
                # Get mouse position
                mouse_x, mouse_y = pygame.mouse.get_pos()
                # Shoot a bullet towards the mouse position
                bullet_speed_x, bullet_speed_y = gun.shoot(player_render_rect, mouse_x, mouse_y)

                # Inside the loop where you handle bullet movement
                for bullet, speed in gun.bullets:
                    bullet.x += speed[0]  # Move bullet horizontally
                    bullet.y += speed[1]  # Move bullet vertically
                    pygame.draw.rect(screen, gun.bullet_color, bullet)

        elif event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False

    # Move the player horizontally based on the state of the flags
    if moving_left:
        player_rect.x -= player_speed
    if moving_right:
        player_rect.x += player_speed
    if moving_up:
        player_rect.y -= player_speed
    if moving_down:
        player_rect.y += player_speed



    mouse_x, mouse_y = pygame.mouse.get_pos()

    if moving_left:
        player_surf = playerwalkleftlist[int(left_index)]
        left_index += animation_speed
        if left_index >= len(playerwalkleftlist):
            left_index = 0
    elif moving_right:
        player_surf = playerwalkrightlist[int(right_index)]
        right_index += animation_speed
        if right_index >= len(playerwalkrightlist):
             right_index = 0
    elif moving_up:
        player_surf = playerwalkuplist[int(up_index)]
        up_index += animation_speed
        if up_index >= len(playerwalkuplist):
            up_index = 0
    elif moving_down:
        player_surf = playerwalkdownlist[int(down_index)]
        down_index += animation_speed
        if down_index >= len(playerwalkdownlist):
            down_index = 0
    else:
        player_surf = playeridlelist[int(idle_index)]
        idle_index += animation_speed
        if idle_index >= len(playeridlelist):
            idle_index = 0

###CAMERA####

    camera.center = player_rect.center


    for tile in tiles:
        if tile.image == water_image:
            # Adjust tile position relative to the camera
            tile_rect = tile.rect.move(camera.topleft)
            if player_rect.colliderect(tile_rect):
                # Perform collision handling
                if moving_left and player_rect.left < tile_rect.right:
                    moving_left = False
                    player_rect.x += 40
                if moving_right and player_rect.right > tile_rect.left:
                    moving_right = False
                    player_rect.x -= 40
                if moving_up and player_rect.top < tile_rect.bottom:
                    moving_up = False
                    player_rect.y += 40
                if moving_down and player_rect.bottom > tile_rect.top:
                    moving_down = False
                    player_rect.y -= 40

    player_render_rect = player_rect.move(-camera.x, -camera.y)



    
    #player_render_rect = player_rect.move(-camera.x, -camera.y)



        
    screen.fill((70, 192, 236))
    for tile in tiles:
        tile.pos(WIDTH//2 + camera.x,HEIGHT//2 + camera.y)
    tiles.draw(screen)
    for snail in snails:
        snail.move_towards_target()
        snail_render_rect = snail.rect.move(-camera.x, -camera.y)
        screen.blit(snail_surf, snail_render_rect)
        #screen.blit(snail_surf, snail)

    if len(snails) <= 2:
        for _ in range(10):
            snail_rect = snail_surf.get_rect()
            snail_rect.x = random.randint(0, 2000)
            snail_rect.y = random.randint(0, 2000)
            snail = Enemy(snail_rect, player_rect)
            snail.rect = snail_rect
            snails.append(snail)

    gun.check_collisions(snails, camera)

    screen.blit(player_surf, player_render_rect)
    #screen.blit(player_surf, player_rect)
    gun.update()
    # Remove bullets that have gone off the screen
    gun.remove_bullets_off_screen()


    pygame.display.update()

pygame.quit()
sys.exit()
