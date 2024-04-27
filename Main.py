import pygame
from pygame.locals import *
import sys
import math
from gun import *
from Enemies import *
import Graphics
import Serializer

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
heart_surf = pygame.image.load("Graphics/items/heart.png").convert_alpha()
bullet_upgrade_surf = Graphics.load("bullet_upgrade1")
bullet_upgrade_surf2 = Graphics.load("bullet_upgrade2")
bullet_upgrade_rect2 = bullet_upgrade_surf2.get_rect(center = (150, 1250))
maxhpup_surf = Graphics.load("maxhpup")
maxhpup_rect = maxhpup_surf.get_rect(center = (1525, 1250))
bullet_upgrade_rect = bullet_upgrade_surf.get_rect(center = (150, 250))
poweruplist = [bullet_upgrade_rect, maxhpup_rect]
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
playeridlelist = Graphics.loadList(["playeridle00", "playeridle01", "playeridle02"])
playerwalkleftlist = Graphics.loadList(["playerwalkleft0", "playerwalkleft1", "playerwalkleft2"])
playerwalkrightlist = Graphics.loadList(["playerwalkright00", "playerwalkright01", "playerwalkright02"])
player_idle_surf = playeridlelist[0]
player_surf = playeridlelist[0]
player_rect = player_surf.get_rect(center=(800, 800))
player_speed = 10  # Adjust the player's movement speed

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
    
def check_col(rect, speed_x, speed_y):
    next_rect = rect.move(speed_x, speed_y)
    for tile in tiles:
        tile_rect = tile.rect.move(camera.topleft)
        if tile.collision and pygame.Rect.colliderect(tile.rect, rect):
            return True
    return False
def display_shop():
    shop_running = True
    global bullet_upgrade
    global bullet_upgrade2
    global max_hp
    global hp
    while shop_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_rect.colliderect(bullet_upgrade_rect) and coin_inv >= 50:
                    bullet_upgrade = True
                    shop_running = False
                if mouse_rect.colliderect(bullet_upgrade_rect2) and coin_inv >=100 and bullet_upgrade == True:
                    bullet_upgrade2 = True
                    shop_running = False
                if mouse_rect.colliderect(maxhpup_rect) and coin_inv >=25:
                    max_hp += 10
                    hp += 10
                    shop_running = False
        mouse_x, mouse_y = pygame.mouse.get_pos()
        screen.fill((0, 0, 0))
        title_surface = font.render("Upgrading time!", True, (255, 255, 255))
        title_rect = title_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 150))
        up1_surface = font.render("1 more bullet", True, (255, 255, 255))
        up1_rect = up1_surface.get_rect(center=(300, 280))
        up2_surface = font.render("1 more bullet", True, (255, 255, 255))
        up2_rect = up2_surface.get_rect(center=(300,380))
        up3_surface = font.render("10 more max hp", True, (255, 255, 255))
        up3_rect = up3_surface.get_rect(center=(300,480))
        c1_surface = font.render(":50", True, (255, 255, 255))
        c1_rect = c1_surface.get_rect(center=(65, 290))
        c2_surface = font.render(":100", True, (255, 255, 255))
        c2_rect = c2_surface.get_rect(center=(65, 390))
        c3_surface = font.render(":25", True, (255, 255, 255))
        c3_rect = c3_surface.get_rect(center=(65, 490))
        bullet_upgrade_rect = (100, 250, 64, 64)
        bullet_upgrade_rect2 = (100, 350, 64, 64)
        maxhpup_rect = (100, 450, 64 ,64)
        coin_rect = (20,280)
        coin_rect1 = (20, 380)
        coin_rect2 = (20, 480)

        mouse_rect = pygame.Rect(mouse_x, mouse_y, 1, 1)

        if bullet_upgrade == False:
            screen.blit(bullet_upgrade_surf, bullet_upgrade_rect)
            screen.blit(up1_surface, up1_rect)
            screen.blit(c1_surface, c1_rect)
            screen.blit(coinanimlist[0], coin_rect)
        if bullet_upgrade == True and bullet_upgrade2 == False:
            screen.blit(bullet_upgrade_surf2, bullet_upgrade_rect2)
            screen.blit(up2_surface, up2_rect)
            screen.blit(c2_surface, c2_rect)
            screen.blit(coinanimlist[0], coin_rect1)
        screen.blit(maxhpup_surf, maxhpup_rect)
        screen.blit(up3_surface, up3_rect)
        screen.blit(coinanimlist[0], coin_rect2)
        screen.blit(c3_surface, c3_rect)
        screen.blit(title_surface, title_rect)
        pygame.display.flip()

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
        title_surface = font.render("Snails", False, (255, 255, 255))
        start_surface = font.render("Press SPACE to start", False, (255, 255, 255))
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
        if not check_col(next_player_rect, -player_speed, 0):
            player_rect.x -= player_speed
    if moving_right:
        next_player_rect = player_render_rect.move(+player_speed, 0)
        if not check_col(next_player_rect, +player_speed, 0):
            player_rect.x += player_speed
    if moving_up:
        next_player_rect = player_render_rect.move(0, -player_speed)
        if not check_col(next_player_rect, -player_speed, 0):
            player_rect.y -= player_speed
    if moving_down:
        next_player_rect = player_render_rect.move(0, +player_speed)
        if not check_col(next_player_rect, +player_speed, 0):
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
        pygame.mixer.music.load("Sounds/backgroundmusic.ogg")
        pygame.mixer.music.play(loops=-1)
        playing_backgroundmusic = True
###CAMERA####

    camera.center = player_rect.center



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



    mouse_pos = pygame.mouse.get_pos()
    dx = mouse_pos[0] - (player_render_rect.x + player_rect.width + gunny_offset[0])
    dy = mouse_pos[1] - (player_render_rect.y + gunny_offset[1])
    angle = math.degrees(math.atan2(-dy, dx))
    if mouse_pos[0] > player_render_rect.centerx:
        player_surf = pygame.transform.flip(player_surf, True, False)
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
    filled_width = int(hp_percentage * 100)
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
        coin_inv = 0
        hp = 70
        start_time = pygame.time.get_ticks()
        for snail in snails[:]:
            snails.remove(snail)
        for coin in coins[:]:
            coins.remove(coin)

    if seconds == 30 and coin_inv >= 25:
        display_shop()


    current_hp_surf = font.render(str(hp) + ("/") + str(max_hp), False, (255, 255, 255))
    current_time_surf = font.render(str(minutes) + (":") + str(seconds).zfill(2), False, (255, 255, 255))
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
    screen.blit(current_hp_surf, (55, 540))
    gun.update()
    gun.remove_bullets_off_screen()

    pygame.display.update()

pygame.quit()
sys.exit()
