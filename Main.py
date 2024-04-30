import pygame
from pygame.locals import *
import sys
import math
from gun import *
from Enemies import *
import Serializer


pygame.init()
pygame.font.init()
pygame.mixer.init()
font = pygame.font.Font(None, 36)

WIDTH, HEIGHT = 1400, 1000
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Edvins Spel")
Clock = pygame.time.Clock()

import Graphics
from Tiles import *

shooting_sound = pygame.mixer.Sound("Sounds/revo.mp3")
coin1sound = pygame.mixer.Sound("Sounds/coin.wav")
coin2sound = pygame.mixer.Sound("Sounds/coin2.wav")
coin3sound = pygame.mixer.Sound("Sounds/coin3.wav")
metal1sound = pygame.mixer.Sound("Sounds/metal-small1.wav")
metal2sound = pygame.mixer.Sound("Sounds/metal-small2.wav")
ouch_sound = pygame.mixer.Sound("Sounds/ouch.mp3")
snail_hit_sound = pygame.mixer.Sound("Sounds/snail_hit.wav")

# Load player images for different states (idle and jump)
heart_surf = pygame.image.load("Graphics/items/heart.png").convert_alpha()

hp = 100
max_hp = 100
hpbar_surface = pygame.Surface((max_hp, 8))
hpbar_rect = hpbar_surface.get_rect
hpbar_surface.fill((255,0,0))
hpbarborder_surface = pygame.Surface((max_hp, 9))
hpbarborder_rect = hpbarborder_surface.get_rect()
hpbarborder_surface.fill((0,0,0))
last_health_decrease_time = 0
grace_period = 500
gunny_surf = pygame.image.load("Graphics/items/gunny.png").convert_alpha()
gunny_rect = gunny_surf.get_rect()
coinanimlist = [pygame.image.load(f"Graphics/items/coin{i:02d}.png").convert_alpha() for i in range(18)]
coin_surf = coinanimlist[0]
snailanimlist = [pygame.image.load(f"Graphics/foes/snail{i:02d}.png").convert_alpha() for i in range(2)]
snail_surf = snailanimlist[0]
coinsoundlist = [coin1sound, coin2sound, coin3sound]
metalsoundlist = [metal1sound, metal2sound]
playeridlelist = Graphics.loadList(["playeridle00", "playeridle01", "playeridle02"])
playerwalkleftlist = Graphics.loadList(["playerwalkleft0", "playerwalkleft1", "playerwalkleft2", "playerwalkleft3"])
player_idle_surf = playeridlelist[0]
player_surf = playeridlelist[0]
player_rect = player_surf.get_rect(center=(800, 800))
player_speed = 3  # Adjust the player's movement speed

nomad_surf = Graphics.load("nomad")
nomad_rect = nomad_surf.get_rect(center=(900,400))
tent_surf = Graphics.load("tent1")
tent_rect = tent_surf.get_rect(center=(910,380))
palm_surf = Graphics.load("palm")
palm_rect = palm_surf.get_rect()
main_menu_surf = Graphics.load("main_menu2")
main_menu_rect = main_menu_surf.get_rect()
plank_surf = Graphics.load("plank")
scorch_surf = Graphics.load("scorch")
platform_surf = pygame.image.load("Graphics/platform.png")
platform_rect = platform_surf.get_rect(center=(700, 250))


# Initialize flags to track key presses
moving_left = False
moving_right = False
moving_up = False
moving_down = False
on_platform = False
playing_backgroundmusic = False
bullet_upgrade = False
bullet_upgrade2 = False
coin_inv = 0
gunny_offset = (20, 50)
# Animation variables
walk_frame = 0
walk_animation_speed = 5
idle_index = 0
animation_speed = 0.15
left_index = 0
right_index = 0
up_index = 0
down_index = 0
coin_index = 0
coinsound_index = 0
metalsound_index = 0
snail_index = 0
gun = Gun(screen)
start_time = pygame.time.get_ticks()

frame = screen.get_rect()
camera = frame.copy()

snails = []
coins = []


data = Serializer.load('data.pickle')
# Load saved data
if '.' in data: # change to 'coins' to enable
    coin_inv = data['coins']
    
WAVE_INTERVAL = 30000
time_since_last_wave = 0
last_wave_time = pygame.time.get_ticks()
def spawn_wave(num_snails):
    for _ in range(num_snails):
        snail_rect = snail_surf.get_rect()
        snail_rect.x = random.randint(0, 1300)
        snail_rect.y = random.randint(0, 1100)
        snail = Enemy(snail_rect, player_rect)
        snail.rect = snail_rect
        snails.append(snail)
    global last_wave_time
    last_wave_time = pygame.time.get_ticks()

def check_col(rect):
    for tile in tiles:
        if tile.collision and pygame.Rect.colliderect(tile.rect, rect):
            return True
    return False

def display_shop():
    shop_running = True
    global bullet_upgrade
    global bullet_upgrade2
    global max_hp
    global hp
    global coin_inv
    global coinsound_index
    global player_speed
    while shop_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_rect.colliderect(up1_border) and bullet_upgrade == False and coin_inv >= 50:
                    coin_inv -=50
                    coinsoundlist[coinsound_index].play()
                    coinsound_index = (coinsound_index + 1) % len(coinsoundlist)
                    bullet_upgrade = True

                if mouse_rect.colliderect(up2_border) and bullet_upgrade == True and bullet_upgrade2 == False and coin_inv >= 100:
                    coin_inv -= 100
                    coinsoundlist[coinsound_index].play()
                    coinsound_index = (coinsound_index + 1) % len(coinsoundlist)
                    bullet_upgrade2 = True

                if mouse_rect.colliderect(up3_border) and max_hp <=200 and coin_inv >=25:
                    coin_inv -=25
                    coinsoundlist[coinsound_index].play()
                    coinsound_index = (coinsound_index + 1) % len(coinsoundlist)
                    max_hp += 10
                    hp += 10
                if mouse_rect.colliderect(up4_border) and player_speed <= 9 and coin_inv >= 25:
                    coin_inv -= 25
                    coinsoundlist[coinsound_index].play()
                    coinsound_index = (coinsound_index + 1) % len(coinsoundlist)
                    player_speed += 1
                if mouse_rect.colliderect(exit_border):
                    shop_running = False

        mouse_x, mouse_y = pygame.mouse.get_pos()
        title_surface = font.render("Shop", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
        title_border = pygame.draw.rect(screen, (45,45,45), (WIDTH//2 - 50, HEIGHT//2 - 162, 100, 25), 0, 50)

        coin_inv_border = pygame.draw.rect(screen, (45, 45, 45), (WIDTH // 2 - 140, HEIGHT // 2 - 112, 210, 25), 0, 50)
        coin_inv_shop_text = font.render("You have "+str(coin_inv)+"x", True, (255, 255, 255))
        coin_inv_shop_text_rect = coin_inv_shop_text.get_rect(center=(WIDTH//2 - 50, HEIGHT//2 - 100))
        screen.blit(coin_inv_shop_text, coin_inv_shop_text_rect)
        coin_rect_info = (740, 390)

        exit_border = pygame.draw.rect(screen, (205, 45, 45), (WIDTH // 2 + 100, HEIGHT // 2 + 250, 150, 25), 0, 50)
        exit_text = font.render("Exit shop", True, (255, 255, 255))
        exit_text_rect = exit_text.get_rect(center=(WIDTH // 2 + 175, HEIGHT // 2 + 263))
        screen.blit(exit_text, exit_text_rect)

        up1_border = pygame.draw.rect(screen, (45, 45, 45), (WIDTH // 2 - 210, HEIGHT // 2 - 60, 180, 25), 0, 50)
        up1_surface = font.render("+1 Projectile", True, (255, 255, 255))
        up1_rect = up1_surface.get_rect(center=(572, 452))

        up2_border = pygame.draw.rect(screen, (45, 45, 45), (WIDTH // 2 - 210, HEIGHT // 2 - 10, 180, 25), 0, 50)
        up2_surface = font.render("+1 Projectile", True, (255, 255, 255))
        up2_rect = up2_surface.get_rect(center=(572,502))

        up3_border = pygame.draw.rect(screen, (45, 45, 45), (WIDTH // 2 - 210, HEIGHT // 2 + 39, 180, 25), 0, 50)
        up3_surface = font.render("+10 Hitpoints", True, (255, 255, 255))
        up3_rect = up3_surface.get_rect(center=(572,552))

        up4_border = pygame.draw.rect(screen, (45, 45, 45), (WIDTH // 2 - 210, HEIGHT // 2 + 89, 180, 25), 0, 50)
        up4_surface = font.render("+1 Movement", True, (255, 255, 255))
        up4_rect = up4_surface.get_rect(center=(572, 602))

        c1_border = pygame.draw.rect(screen, (45, 45, 45), (400, HEIGHT // 2 - 60, 85, 25), 0, 50)
        c1_surface = font.render("50x", True, (255, 255, 255))
        c1_rect = c1_surface.get_rect(center=(430, 452))
        c2_border = pygame.draw.rect(screen, (45, 45, 45), (400, HEIGHT // 2 - 10, 85, 25), 0, 50)
        c2_surface = font.render("100x", True, (255, 255, 255))
        c2_rect = c2_surface.get_rect(center=(430, 502))

        c3_border = pygame.draw.rect(screen, (45, 45, 45), (400, HEIGHT // 2 +39, 85, 25), 0, 50)
        c3_surface = font.render("25x", True, (255, 255, 255))
        c3_rect = c3_surface.get_rect(center=(430, 552))

        c4_border = pygame.draw.rect(screen, (45, 45, 45), (400, HEIGHT // 2 + 89, 85, 25), 0, 50)
        c4_surface = font.render("25x", True, (255, 255, 255))
        c4_rect = c4_surface.get_rect(center=(430, 602))
        coin_rect4 = (458, 592)



        coin_rect = (458, 442)
        coin_rect1 = (458, 492)
        coin_rect2 = (458, 542)

        mouse_rect = pygame.Rect(mouse_x, mouse_y, 1, 1)

        screen.blit(up1_surface, up1_rect)
        screen.blit(c1_surface, c1_rect)
        screen.blit(coinanimlist[0], coin_rect)
        screen.blit(up2_surface, up2_rect)
        screen.blit(c2_surface, c2_rect)
        screen.blit(coinanimlist[0], coin_rect1)
        if bullet_upgrade == True:
            pygame.draw.rect(screen, (205, 45, 45), (WIDTH // 2 - 300, HEIGHT // 2 - 50, 270, 7), 0, 50)
        if bullet_upgrade2 == True:
            pygame.draw.rect(screen, (205, 45, 45), (WIDTH // 2 - 300, HEIGHT // 2 - 0, 270, 7), 0, 50)
        screen.blit(up3_surface, up3_rect)
        screen.blit(coinanimlist[0], coin_rect2)
        screen.blit(c3_surface, c3_rect)
        screen.blit(c4_surface, c4_rect)
        screen.blit(coinanimlist[0], coin_rect4)
        screen.blit(up4_surface, up4_rect)
        if max_hp >= 200:
            pygame.draw.rect(screen, (205, 45, 45), (WIDTH // 2 - 300, HEIGHT // 2 + 50, 270, 7), 0, 50)
        if player_speed >= 9:
            pygame.draw.rect(screen, (205, 45, 45), (WIDTH // 2 - 300, HEIGHT // 2 + 100, 270, 7), 0, 50)
        screen.blit(title_surface, title_rect)
        screen.blit(player_surf, player_render_rect)
        screen.blit(coinanimlist[0], coin_rect_info)
        pygame.display.flip()

def display_menu():
    menu_running = True
    while menu_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_rect.colliderect(exit_border):
                    menu_running = False


        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(mouse_x, mouse_y, 1, 1)
        screen.blit(main_menu_surf, main_menu_rect)
        screen.blit(scorch_surf, (130, 140))
        screen.blit(plank_surf, (130,280))

        exit_border = pygame.draw.rect(screen, (205, 45, 45), (WIDTH // 2 + 100, HEIGHT // 2 + 250, 150, 25), 0, 50)
        exit_text = font.render("Start game", True, (255, 255, 255))
        exit_text_rect = exit_text.get_rect(center=(WIDTH // 2 + 175, HEIGHT // 2 + 263))
        screen.blit(exit_text, exit_text_rect)

        pygame.display.flip()

display_menu()

running = True
while running:
    Clock.tick(60)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
            # Data you want to save
            data = {'coins': coin_inv, 'otherData': 1, 'etc': 2}
            Serializer.save(data, 'data.pickle')
                
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
                if player_render_rect.colliderect(nomad_render_rect):
                    display_shop()
                    moving_left = False
                    moving_up = False
                    moving_down = False
                    moving_right = False


        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            if bullet_upgrade == True:
                bullet_speeds = gun.shoot(gunny_rect, mouse_x, mouse_y, bullet_upgrade2)
                shooting_sound.play()
                for bullet_speed_x, bullet_speed_y in bullet_speeds:
                    new_bullet = pygame.Rect(gunny_rect.left, gunny_rect.centery - 30 - gun.bullet_height // 2,
                                                 gun.bullet_width, gun.bullet_height)
                    gun.bullets.append((new_bullet, (bullet_speed_x, bullet_speed_y)))
            else:
                bullet_speed_x, bullet_speed_y = gun.shoot1(gunny_rect, mouse_x, mouse_y)
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
    elapsed_time = pygame.time.get_ticks() - start_time
    minutes = elapsed_time // 60000
    seconds = (elapsed_time // 1000) % 60



    if moving_left:
        next_player_rect = player_render_rect.move(-player_speed, 0)
        if not check_col(next_player_rect):
            player_rect.x -= player_speed
    if moving_right:
        next_player_rect = player_render_rect.move(+player_speed, 0)
        if not check_col(next_player_rect):
            player_rect.x += player_speed
    if moving_up:
        next_player_rect = player_render_rect.move(0, -player_speed)
        if not check_col(next_player_rect):
            player_rect.y -= player_speed
    if moving_down:
        next_player_rect = player_render_rect.move(0, +player_speed)
        if not check_col(next_player_rect):
            player_rect.y += player_speed

    if moving_left:
        player_surf = playerwalkleftlist[int(left_index)]
        left_index += animation_speed
        if left_index >= len(playerwalkleftlist):
            left_index = 0
    elif moving_right:
        player_surf = playerwalkleftlist[int(left_index)]
        left_index += animation_speed
        if left_index >= len(playerwalkleftlist):
            left_index = 0
    elif moving_up:
        player_surf = playerwalkleftlist[int(left_index)]
        left_index += animation_speed
        if left_index >= len(playerwalkleftlist):
            left_index = 0
    elif moving_down:
        player_surf = playerwalkleftlist[int(left_index)]
        left_index += animation_speed
        if left_index >= len(playerwalkleftlist):
            left_index = 0
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
        pygame.mixer.music.load("Sounds/caravan.ogg.ogg")
        pygame.mixer.music.set_volume(10)
        pygame.mixer.music.play(loops=-1)
        playing_backgroundmusic = True
###CAMERA####

    camera.center = player_rect.center


    nomad_render_rect = nomad_rect.move(-camera.x, -camera.y)
    player_render_rect = player_rect.move(-camera.x, -camera.y)
    tent_render_rect = tent_rect.move(-camera.x, -camera.y)
    palm_render_rect = palm_rect.move(-camera.x, -camera.y)
    platform_render_rect = platform_rect.move(-camera.x, -camera.y)


    shop_text_surf = font.render("Press [E] to shop", True, (255, 255, 255))
    shop_text_rect = shop_text_surf.get_rect(center=(730, 552))

    screen.fill((70, 192, 236))
    for tile in tiles:
        tile.pos(WIDTH//2 + camera.x,HEIGHT//2 + camera.y)
    tiles.draw(screen)
    
    for snail in snails:
        snail.move_towards_target(camera, tiles)
        snail_render_rect = snail.rect.move(-camera.x, -camera.y)
        if snail_render_rect.centerx < player_render_rect.centerx:
            snail_surf = pygame.transform.flip(snail_surf, True, False)
        screen.blit(snail_surf, snail_render_rect)
    screen.blit(tent_surf, (tent_render_rect.x + 100, tent_render_rect.y + 0))
    screen.blit(nomad_surf, nomad_render_rect)



    if current_time - last_wave_time >= WAVE_INTERVAL:
        spawn_wave(5)
        time_since_last_wave = current_time

    coin_rect = coin_surf.get_rect()
    adjusted_coin_rects = [coin.move(-camera.x, -camera.y) for coin in coins]
    index = player_render_rect.collidelist(adjusted_coin_rects)
    if index != -1:
        coins.pop(index)
        metalsoundlist[metalsound_index].play()
        metalsound_index = (metalsound_index + 1) % len(metalsoundlist)
        coin_inv += 1
    coin_inv_text_surf = font.render(": " + str(coin_inv), False, (255, 255, 255))



    mouse_pos = pygame.mouse.get_pos()
    dx = mouse_pos[0] - (player_render_rect.x + player_rect.width)
    dy = mouse_pos[1] - (player_render_rect.y)
    angle = math.degrees(math.atan2(-dy, dx))

    if mouse_pos[0] < player_render_rect.centerx:
        rotated_gunny_image = pygame.transform.flip(gunny_surf, False, True)
        player_surf = pygame.transform.flip(player_surf, True, False)
        gunny_offset = (-10,15)
        if 100 <= angle <= 150:
            gunny_offset =(0,-15)
        if -90 >= angle >= -125:
            gunny_offset = (0,15)
    else:
        rotated_gunny_image = gunny_surf
        gunny_offset = (30,15)
        if angle >= 25:
            gunny_offset = (20,-15)
    rotated_gunny_image = pygame.transform.rotate(rotated_gunny_image, angle)
    gunny_rect = rotated_gunny_image.get_rect()
    gunny_rect.midleft = (player_render_rect.left, player_render_rect.centery)

    hpbar_rect = (50, 545)
    hpbarborder_rect = (50, 545)
    hp_percentage = hp / max_hp
    filled_width = int(hp_percentage * 100)
    hpbar_surface = pygame.transform.scale(hpbar_surface, (filled_width, 7))
    adjusted_snail_rects = [snail.rect.move(-camera.x, -camera.y) for snail in snails]
    index1 = player_render_rect.collidelist(adjusted_snail_rects)
    if index1 != -1 and current_time - last_health_decrease_time >= grace_period:
        hp -= 10
        last_health_decrease_time = current_time
        ouch_sound.play()
        snail_hit_sound.play()
        if hp < 0:
            hp = 0
    if hp == 0:
        bullet_upgrade = False
        bullet_upgrade2 = False
        display_menu()
        coin_inv = 0
        hp = 100
        max_hp = 100
        start_time = pygame.time.get_ticks()
        for snail in snails[:]:
            snails.remove(snail)
        for coin in coins[:]:
            coins.remove(coin)


    current_hp_surf = font.render(str(hp) + ("/") + str(max_hp), False, (255, 255, 255))
    current_time_surf = font.render(str(minutes) + (":") + str(seconds).zfill(2), False, (255, 255, 255))
    gun.check_collisions(snails, camera, coins, coin_rect)

    for coin in coins:
        screen.blit(coin_surf, (coin.x - camera.x, coin.y - camera.y))
    gunny_rect = player_render_rect.move(gunny_offset)
    screen.blit(platform_surf, platform_render_rect)
    screen.blit(rotated_gunny_image, gunny_rect)
    screen.blit(player_surf, player_render_rect)
    screen.blit(palm_surf, (palm_render_rect.x + 300, palm_render_rect.y + 150))
    screen.blit(coinanimlist[0], (15,570))
    screen.blit(coin_inv_text_surf, (40, 570))
    screen.blit(heart_surf, (15, 540))
    screen.blit(current_time_surf, (WIDTH//2, 50))
    screen.blit(hpbarborder_surface, hpbarborder_rect)
    screen.blit(hpbar_surface, hpbar_rect)
    if player_render_rect.colliderect(nomad_render_rect):
        shop_text_border = pygame.draw.rect(screen, (45, 45, 45), (620, HEIGHT // 2 + 38, 220, 25), 0, 50)
        screen.blit(shop_text_surf, shop_text_rect)
    screen.blit(current_hp_surf, (55, 540))
    gun.update()
    gun.remove_bullets_off_screen()
    pygame.display.update()

pygame.quit()
sys.exit()
