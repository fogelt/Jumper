import sys

import pygame.transform

import Serializer
from Enemies import *
from gun import *

import scripts.initializer as initializer
import scripts.music_controller as music_controller
import scripts.sound_controller as sound_controller
import scripts.graphics_controller as graphics_controller
import scripts.map_controller as map_controller
import scripts.shop_controller as shop_controller

import scripts.sound_enum as sound_enum
import scripts.graphics_enum as graphics_enum

font = initializer.get_font()
screen = initializer.get_screen()
clock = initializer.get_clock()
HEIGHT = initializer.HEIGHT
WIDTH = initializer.WIDTH

# Load player images for different states (idle and jump)
heart_surf = pygame.image.load("Graphics/items/heart.png").convert_alpha()

hp = 100
max_hp = 100
hpbar_surface = pygame.Surface((max_hp, 8))
hpbar_rect = hpbar_surface.get_rect
hpbar_surface.fill((255, 0, 0))
hpbarborder_surface = pygame.Surface((max_hp, 9))
hpbarborder_rect = hpbarborder_surface.get_rect()
hpbarborder_surface.fill((0, 0, 0))
last_health_decrease_time = 0
grace_period = 1000
gunny_surf = pygame.image.load("Graphics/items/gunny.png").convert_alpha()
gunny_rect = gunny_surf.get_rect()
coinanimlist = [pygame.image.load(f"Graphics/items/coin{i:02d}.png").convert_alpha() for i in range(18)]
coin_surf = coinanimlist[0]
snailanimlist = [pygame.image.load(f"Graphics/foes/snail{i:02d}.png").convert_alpha() for i in range(2)]
snail_surf = snailanimlist[0]
skeleanimlist = graphics_controller.load_list(graphics_enum.Type.SKELETON)
skele_surf = skeleanimlist[0]

playeridlelist = graphics_controller.load_list(graphics_enum.Type.PLAYER_IDLE)
playerwalkleftlist = graphics_controller.load_list(graphics_enum.Type.PLAYER_WALK_LEFT)
player_idle_surf = playeridlelist[0]
player_surf = playeridlelist[0]
player_rect = player_surf.get_rect(center=(800, 800))
player_speed = 3  # Adjust the player's movement speed

nomad_surf = graphics_controller.load(graphics_enum.Type.NOMAD)
nomad_rect = nomad_surf.get_rect(center=(900, 400))
tent_surf = graphics_controller.load(graphics_enum.Type.TENT)
tent_rect = tent_surf.get_rect(center=(910, 380))
palm_surf = graphics_controller.load(graphics_enum.Type.PALM)
palm_rect = palm_surf.get_rect()
main_menu_surf = graphics_controller.load(graphics_enum.Type.MAIN_MENU)
main_menu_surf = pygame.transform.scale(main_menu_surf, (1280, 720))
main_menu_rect = main_menu_surf.get_rect()
scorch_surf = pygame.image.load("Graphics/scorch.png")
platform_surf = pygame.image.load("Graphics/platform.png")
platform_rect = platform_surf.get_rect(center=(700, 250))
pygame.display.set_icon(snail_surf)

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

snail_index = 0
skele_index = 0
gun = Gun(screen)
start_time = pygame.time.get_ticks()

frame = screen.get_rect()
camera = frame.copy()

snails = []
skeles = []
coins = []


def check_col(rect, speed_x, speed_y):
    rect.move(speed_x, speed_y)

    for tile_ in map_controller.tile_list:
        tile_.rect.move(camera.topleft)


data = Serializer.load('data.pickle')
# Load saved data
if '.' in data:  # change to 'coins' to enable
    coin_inv = data['coins']

WAVE_INTERVAL = 2000
time_since_last_wave = 0
last_wave_time = pygame.time.get_ticks()


def spawn_snail_wave(num_snails):
    for _ in range(num_snails):
        snail_rect = snail_surf.get_rect()
        snail_rect.x = random.randint(0, 1300)
        snail_rect.y = random.randint(0, 1100)
        _snail = Enemy(snail_rect, player_rect)
        _snail.rect = snail_rect
        snails.append(_snail)

    global last_wave_time
    last_wave_time = pygame.time.get_ticks()


def spawn_skele_wave(num_skeles):
    for _ in range(num_skeles):
        skele_rect = skele_surf.get_rect()
        skele_rect.x = random.randint(0, 1300)
        skele_rect.y = random.randint(0, 1100)
        _skele = Enemy(skele_rect, player_rect)
        _skele.rect = skele_rect
        skeles.append(_skele)

    global last_wave_time
    last_wave_time = pygame.time.get_ticks()


def check_col(rect):
    for tile_ in map_controller.tile_list:
        if tile_.collision and pygame.Rect.colliderect(tile_.rect, rect):
            return True

    return False


def display_shop():
    global bullet_upgrade
    global bullet_upgrade2
    global max_hp
    global hp
    global coin_inv
    global player_speed

    while shop_controller.display_shop(font, screen, WIDTH, HEIGHT, bullet_upgrade, bullet_upgrade2, max_hp, hp,
                                       coin_inv, player_speed, sound_controller, sound_enum, coinanimlist, player_surf,
                                       player_render_rect):
        pass

def display_pause_menu():
    pause_running = True

    while pause_running:
        _mouse_x, _mouse_y = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(_mouse_x, _mouse_y, 1, 1)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_rect.colliderect(quit_border):
                    pause_running = False
                    display_menu()

            if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                pause_running = False

        pygame.draw.rect(screen, (0, 0, 0), (WIDTH // 2.6, HEIGHT // 1.13, 300, 35), 0, 5)
        quit_border = pygame.draw.rect(screen, (233, 104, 28), (WIDTH // 2.6, HEIGHT // 1.13, 300, 35), 4, 5)
        quit_text = font.render("Back to main menu", True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.1))
        screen.blit(player_surf, player_render_rect)
        screen.blit(quit_text, quit_text_rect)

        pygame.display.flip()
def display_menu():
    menu_running = True

    while menu_running:
        _mouse_x, _mouse_y = pygame.mouse.get_pos()
        mouse_rect = pygame.Rect(_mouse_x, _mouse_y, 1, 1)
        screen.blit(main_menu_surf, main_menu_rect)
        screen.blit(scorch_surf, (400, 30))

        pygame.draw.rect(screen, (0, 0, 0), (WIDTH // 2.27, HEIGHT // 2.65, 250, 35), 0, 5)
        start_border = pygame.draw.rect(screen, (233, 104, 28), (WIDTH // 2.27, HEIGHT // 2.65, 250, 35), 4, 5)
        start_text = font.render("Start game", True, (255, 255, 255))
        start_text_rect = start_text.get_rect(center=(WIDTH // 2, HEIGHT // 2.5))

        pygame.draw.rect(screen, (0, 0, 0), (WIDTH // 2.27, HEIGHT // 2.23, 250, 35), 0, 5)
        settings_border = pygame.draw.rect(screen, (233, 104, 28), (WIDTH // 2.27, HEIGHT // 2.23, 250, 35), 4, 5)
        settings_text = font.render("Settings", True, (255, 255, 255))
        settings_text_rect = settings_text.get_rect(center=(WIDTH // 2.03, HEIGHT // 2.1))

        pygame.draw.rect(screen, (0, 0, 0), (WIDTH // 2.27, HEIGHT // 1.89, 250, 35), 0, 5)
        quit_border = pygame.draw.rect(screen, (233, 104, 28), (WIDTH // 2.27, HEIGHT // 1.89, 250, 35), 4, 5)
        quit_text = font.render("Quit game", True, (255, 255, 255))
        quit_text_rect = quit_text.get_rect(center=(WIDTH // 2, HEIGHT // 1.8))

        for _event in pygame.event.get():
            if _event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            if _event.type == pygame.MOUSEBUTTONDOWN:
                if mouse_rect.colliderect(start_border):
                    menu_running = False

                if mouse_rect.colliderect(settings_border):
                    pass

                if mouse_rect.colliderect(quit_border):
                    sys.exit()

        screen.blit(start_text, start_text_rect)
        screen.blit(settings_text, settings_text_rect)
        screen.blit(quit_text, quit_text_rect)

        pygame.display.flip()

display_menu()

running = True
nomad_render_rect = pygame.Rect(0, 0, 0, 0)
player_render_rect = pygame.Rect(0, 0, 0, 0)
while running:
    clock.tick(60)

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
            if event.key == pygame.K_ESCAPE:
                display_pause_menu()

        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()

            if bullet_upgrade:
                bullet_speeds = gun.shoot(gunny_rect, mouse_x, mouse_y, bullet_upgrade2)
                sound_controller.play_sound(sound_enum.Type.GUN)

                for bullet_speed_x, bullet_speed_y in bullet_speeds:
                    new_bullet = pygame.Rect(gunny_rect.left, gunny_rect.centery - 30 - gun.bullet_height // 2,
                                             gun.bullet_width, gun.bullet_height)
                    gun.bullets.append((new_bullet, (bullet_speed_x, bullet_speed_y)))
            else:
                bullet_speed_x, bullet_speed_y = gun.shoot1(gunny_rect, mouse_x, mouse_y)
                sound_controller.play_sound(sound_enum.Type.GUN)

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

    skele_surf = skeleanimlist[int(skele_index)]
    skele_index += animation_speed

    if skele_index >= len(skeleanimlist):
        skele_index = 0

    if not playing_backgroundmusic:
        music_controller.play()
        playing_backgroundmusic = True

    # CAMERA
    camera.center = player_rect.center

    nomad_render_rect = nomad_rect.move(-camera.x, -camera.y)
    player_render_rect = player_rect.move(-camera.x, -camera.y)
    tent_render_rect = tent_rect.move(-camera.x, -camera.y)
    palm_render_rect = palm_rect.move(-camera.x, -camera.y)
    platform_render_rect = platform_rect.move(-camera.x, -camera.y)

    shop_text_surf = font.render("Press [E] to shop", True, (255, 255, 255))
    shop_text_rect = shop_text_surf.get_rect(center=(730, 552))

    screen.fill((70, 192, 236))

    for tile in map_controller.tile_list:
        tile.pos(WIDTH // 2 + camera.x, HEIGHT // 2 + camera.y)

    map_controller.tile_list.draw(screen)

    for snail in snails:
        snail.move_towards_target(camera, map_controller.tile_list)
        snail_render_rect = snail.rect.move(-camera.x, -camera.y)
        if snail_render_rect.centerx < player_render_rect.centerx:
            snail_surf = pygame.transform.flip(snail_surf, True, False)

        screen.blit(snail_surf, snail_render_rect)

    for skele in skeles:
        skele.move_towards_target(camera, map_controller.tile_list)
        skele_render_rect = skele.rect.move(-camera.x, -camera.y)
        if skele_render_rect.centerx < player_render_rect.centerx:
            skele_surf = pygame.transform.flip(skele_surf, True, False)

        screen.blit(skele_surf, skele_render_rect)

    screen.blit(tent_surf, (tent_render_rect.x + 100, tent_render_rect.y + 0))
    screen.blit(nomad_surf, nomad_render_rect)

    if current_time - last_wave_time >= WAVE_INTERVAL:
        spawn_snail_wave(1)
        spawn_skele_wave(1)
        time_since_last_wave = current_time

    coin_rect = coin_surf.get_rect()
    adjusted_coin_rects = [coin.move(-camera.x, -camera.y) for coin in coins]
    index = player_render_rect.collidelist(adjusted_coin_rects)

    if index != -1:
        coins.pop(index)
        sound_controller.play_random_sound(sound_enum.Type.METAL)
        coin_inv += 1

    coin_inv_text_surf = font.render(": " + str(coin_inv), False, (255, 255, 255))

    mouse_pos = pygame.mouse.get_pos()
    dx = mouse_pos[0] - (player_render_rect.x + player_rect.width)
    dy = mouse_pos[1] - player_render_rect.y
    angle = math.degrees(math.atan2(-dy, dx))

    if mouse_pos[0] < player_render_rect.centerx:
        rotated_gunny_image = pygame.transform.flip(gunny_surf, False, True)
        player_surf = pygame.transform.flip(player_surf, True, False)
        gunny_offset = (-10, 15)
        if 100 <= angle <= 150:
            gunny_offset = (0, -15)

        if -90 >= angle >= -125:
            gunny_offset = (0, 15)

    else:
        rotated_gunny_image = gunny_surf
        gunny_offset = (30, 15)
        if angle >= 25:
            gunny_offset = (20, -15)

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
    adjusted_skele_rects = [skele.rect.move(-camera.x, -camera.y) for skele in skeles]
    index2 = player_render_rect.collidelist(adjusted_skele_rects)

    if index1 != -1 and current_time - last_health_decrease_time >= grace_period:
        hp -= 5
        last_health_decrease_time = current_time
        sound_controller.play_sound(sound_enum.Type.OUCH)
        sound_controller.play_sound(sound_enum.Type.SNAIL_HIT)
        if hp < 0:
            hp = 0

    if index2 != -1 and current_time - last_health_decrease_time >= grace_period:
        hp -= 10
        last_health_decrease_time = current_time
        sound_controller.play_sound(sound_enum.Type.OUCH)
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

    current_hp_surf = font.render(str(hp) + "/" + str(max_hp), False, (255, 255, 255))
    current_time_surf = font.render(str(minutes) + ":" + str(seconds).zfill(2), False, (255, 255, 255))
    gun.check_collisions(snails, skeles, camera, coins, coin_rect)

    for coin in coins:
        screen.blit(coin_surf, (coin.x - camera.x, coin.y - camera.y))

    gunny_rect = player_render_rect.move(gunny_offset)
    screen.blit(platform_surf, platform_render_rect)
    screen.blit(rotated_gunny_image, gunny_rect)

    doodad_above_player_list = pygame.sprite.Group()
    doodad_behind_player_list = pygame.sprite.Group()

    for doodad in map_controller.doodad_list:
        doodad.pos(WIDTH // 2 + camera.x, HEIGHT // 2 + camera.y)
        if doodad.render_order() == 0:
            doodad_above_player_list.add(doodad)
        else:
            doodad_behind_player_list.add(doodad)

    doodad_behind_player_list.draw(screen)
    screen.blit(player_surf, player_render_rect)
    doodad_above_player_list.draw(screen)

    screen.blit(palm_surf, (palm_render_rect.x + 300, palm_render_rect.y + 150))
    screen.blit(coinanimlist[0], (15, 570))
    screen.blit(coin_inv_text_surf, (40, 570))
    screen.blit(heart_surf, (15, 540))
    screen.blit(current_time_surf, (WIDTH // 2, 50))
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
