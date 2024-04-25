import pygame
from pygame.locals import *
import sys
import math
from gun import *
from Enemies import *
import Graphics

pygame.init()
pygame.font.init()
pygame.mixer.init()
font = pygame.font.Font(None, 36)

WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Edvins Spel")
Clock = pygame.time.Clock()

from Tiles import *

shooting_sound = pygame.mixer.Sound("Sounds/flaunch.wav")
coin1sound = pygame.mixer.Sound("Sounds/coin.wav")
coin2sound = pygame.mixer.Sound("Sounds/coin2.wav")
coin3sound = pygame.mixer.Sound("Sounds/coin3.wav")
ouch_sound = pygame.mixer.Sound("Sounds/ouch.mp3")

# Load player images for different states (idle and jump)
player_idle1_surf = Graphics.load("playeridle1")
player_idle2_surf = pygame.image.load("Graphics/player/playeridle2.png").convert_alpha()
player_idle3_surf = pygame.image.load("Graphics/player/playeridle3.png").convert_alpha()
player_walkup_surf = pygame.image.load("Graphics/player/playerwalkup.png").convert_alpha()
player_walkup1_surf = pygame.image.load("Graphics/player/playerwalkup1.png").convert_alpha()
player_walkup2_surf = pygame.image.load("Graphics/player/playerwalkup2.png").convert_alpha()
player_walkdown_surf = pygame.image.load("Graphics/player/playerwalkdown.png").convert_alpha()
player_walkdown1_surf = pygame.image.load("Graphics/player/playerwalkdown1.png").convert_alpha()
player_walkdown2_surf = pygame.image.load("Graphics/player/playerwalkdown2.png").convert_alpha()
player_walkdown3_surf = pygame.image.load("Graphics/player/playerwalkdow3.png").convert_alpha()

player_walkright1_surf = pygame.image.load("Graphics/player/playerwalkright1.png").convert_alpha()
player_walkright2_surf = pygame.image.load("Graphics/player/playerwalkright2.png").convert_alpha()
player_walkright3_surf = pygame.image.load("Graphics/player/playerwalkright3.png").convert_alpha()
heart_surf = pygame.image.load("Graphics/items/heart.png").convert_alpha()
pierce_surf = pygame.image.load("Graphics/items/pierce.png").convert_alpha()
pierce_rect = pierce_surf.get_rect()

hpbar_surface = pygame.Surface((70, 8))
hpbar_rect = hpbar_surface.get_rect
hpbar_surface.fill((255,0,0))
hpbarborder_surface = pygame.Surface((70, 9))
hpbarborder_rect = hpbarborder_surface.get_rect()
hpbarborder_surface.fill((0,0,0))
hp = 70
max_hp = 70
last_health_decrease_time = 0
grace_period = 1500
gunny_surf = pygame.image.load("Graphics/items/gunny.png").convert_alpha()
gunny_rect = gunny_surf.get_rect()
coinanimlist = [pygame.image.load(f"Graphics/items/coin{i:02d}.png").convert_alpha() for i in range(18)]
coin_surf = coinanimlist[0]
snailanimlist = [pygame.image.load(f"Graphics/foes/snail{i:02d}.png").convert_alpha() for i in range(2)]
snail_surf = snailanimlist[0]
coinsoundlist = [coin1sound, coin2sound, coin3sound]
playerwalkdownlist = [player_walkdown_surf, player_walkdown1_surf, player_walkdown2_surf, player_walkdown3_surf]
playerwalkuplist = [player_walkup_surf, player_walkup1_surf, player_walkup2_surf]
playeridlelist = [player_idle1_surf, player_idle2_surf, player_idle3_surf]
playerwalkleftlist = Graphics.loadList(["playerwalkleft1", "playerwalkleft2", "playerwalkleft3"])
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
playing_backgroundmusic = False
coin_inv = 0
gunny_offset = (20, 50)
# Animation variables
walk_frame = 0
walk_animation_speed = 7
idle_index = 0
animation_speed = 0.15
left_index = 0
right_index = 0
up_index = 0
down_index = 0
coin_index = 0
coinsound_index = 0
snail_index = 0
gun = Gun(screen)

frame = screen.get_rect()
camera = frame.copy()

snails = []
coins = []

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
                mouse_x, mouse_y = pygame.mouse.get_pos()
                bullet_speed_x, bullet_speed_y = gun.shoot(gunny_rect, mouse_x, mouse_y)
                shooting_sound.play()
                for bullet, speed in gun.bullets:
                    bullet.x += speed[0]
                    bullet.y += speed[1]
                    pygame.draw.rect(screen, gun.bullet_color, bullet)

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_a:
                moving_left = False
            if event.key == pygame.K_d:
                moving_right = False
            if event.key == pygame.K_w:
                moving_up = False
            if event.key == pygame.K_s:
                moving_down = False

    current_time = pygame.time.get_ticks()
    minutes = current_time // 60000
    seconds = (current_time // 1000) % 60

    if moving_left:
        player_rect.x -= player_speed
    if moving_right:
        player_rect.x += player_speed
    if moving_up:
        player_rect.y -= player_speed
    if moving_down:
        player_rect.y += player_speed

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
    coin_surf = coinanimlist[int(coin_index)]
    coin_index += animation_speed
    if coin_index >= len(coinanimlist):
        coin_index = 0
    snail_surf = snailanimlist[int(snail_index)]
    snail_index += animation_speed
    if snail_index >= len(snailanimlist):
        snail_index = 0


    if not playing_backgroundmusic:
        pygame.mixer.music.load("Sounds/backgroundmusic.ogg")
        pygame.mixer.music.play(loops=-1)
        playing_backgroundmusic = True
###CAMERA####

    camera.center = player_rect.center


    for tile in tiles:
        if tile.image == water_image:
            tile_rect = tile.rect.move(camera.topleft)
            if player_rect.colliderect(tile_rect):
                if moving_left and player_rect.left < tile_rect.right:
                    moving_left = False
                    player_rect.x += 50
                if moving_right and player_rect.right > tile_rect.left:
                    moving_right = False
                    player_rect.x -= 50
                if moving_up and player_rect.top < tile_rect.bottom:
                    moving_up = False
                    player_rect.y += 50
                if moving_down and player_rect.bottom > tile_rect.top:
                    moving_down = False
                    player_rect.y -= 50

    player_render_rect = player_rect.move(-camera.x, -camera.y)
        
    screen.fill((70, 192, 236))
    for tile in tiles:
        tile.pos(WIDTH//2 + camera.x,HEIGHT//2 + camera.y)
    tiles.draw(screen)
    for snail in snails:
        snail.move_towards_target()
        snail_render_rect = snail.rect.move(-camera.x, -camera.y)
        screen.blit(snail_surf, snail_render_rect)

    if len(snails) <= 2:
        for _ in range(10):
            snail_rect = snail_surf.get_rect()
            snail_rect.x = random.randint(0, 2000)
            snail_rect.y = random.randint(0, 2000)
            snail = Enemy(snail_rect, player_rect)
            snail.rect = snail_rect
            snails.append(snail)

    coin_rect = coin_surf.get_rect()

    adjusted_coin_rects = [coin.move(-camera.x, -camera.y) for coin in coins]
    index = player_render_rect.collidelist(adjusted_coin_rects)
    if index != -1:
        coins.pop(index)
        coinsoundlist[coinsound_index].play()
        coinsound_index = (coinsound_index + 1) % len(coinsoundlist)
        coin_inv += 1
    coin_inv_text_surf = font.render(": " + str(coin_inv), False, (255, 255, 255))
    current_time_surf = font.render(str(minutes)+(":")+str(seconds), False, (255, 255, 255))

    mouse_pos = pygame.mouse.get_pos()
    dx = mouse_pos[0] - (player_render_rect.x + player_rect.width + gunny_offset[0])
    dy = mouse_pos[1] - (player_render_rect.y + gunny_offset[1])
    angle = math.degrees(math.atan2(-dy, dx))
    if mouse_pos[0] < player_render_rect.centerx:
        rotated_gunny_image = pygame.transform.flip(gunny_surf, False, True)
        gunny_offset = (-20,35)
    else:
        rotated_gunny_image = gunny_surf
        gunny_offset = (20,35)
    rotated_gunny_image = pygame.transform.rotate(rotated_gunny_image, angle)
    gunny_rect = rotated_gunny_image.get_rect()
    gunny_rect.midright = (player_render_rect.x + gunny_offset[0], player_render_rect.y + gunny_offset[1])

    hpbar_rect = (50, 545)
    hpbarborder_rect = (50, 545)
    hp_percentage = hp / max_hp
    filled_width = int(hp_percentage * 70)
    hpbar_surface = pygame.transform.scale(hpbar_surface, (filled_width, 7))
    adjusted_snail_rects = [snail.rect.move(-camera.x, -camera.y) for snail in snails]
    index1 = player_render_rect.collidelist(adjusted_snail_rects)
    if index1 != -1 and current_time - last_health_decrease_time >= grace_period:
        hp -= 10
        last_health_decrease_time = current_time
        ouch_sound.play()
        if hp < 0:
            hp = 0
    if hp == 0:
        display_menu()
        hp = 70

    gun.check_collisions(snails, camera, coins, coin_rect)
    for coin in coins:
        screen.blit(coin_surf, (coin.x - camera.x, coin.y - camera.y))
    screen.blit(player_surf, player_render_rect)
    screen.blit(coinanimlist[0], (15,570))
    screen.blit(coin_inv_text_surf, (40, 570))
    screen.blit(heart_surf, (15, 540))
    screen.blit(current_time_surf, (400, 50))
    gunny_rect = player_render_rect.move(gunny_offset)
    screen.blit(rotated_gunny_image, gunny_rect)
    screen.blit(hpbarborder_surface, hpbarborder_rect)
    screen.blit(hpbar_surface, hpbar_rect)
    gun.update()
    gun.remove_bullets_off_screen()

    pygame.display.update()

pygame.quit()
sys.exit()
