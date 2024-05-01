import pygame
import sys

is_initialized = False


def open_shop(screen, width, height):
    background_surface = pygame.Surface((width, height), pygame.SRCALPHA)
    background_surface.fill((0, 0, 0, 128))
    background_surface.set_alpha(150)
    screen.blit(background_surface, (0, 0))


def display_shop(font, screen, width, height, bullet_upgrade, bullet_upgrade2, max_hp, hp, coin_inv, player_speed,
                 sound_controller, sound_enum, coinanimlist, player_surf, player_render_rect):
    global is_initialized
    _mouse_x, _mouse_y = pygame.mouse.get_pos()
    mouse_rect = pygame.Rect(_mouse_x, _mouse_y, 1, 1)

    if not is_initialized:
        is_initialized = True
        open_shop(screen, width, height)  # TODO: Flytta mer hit

    title_surface = font.render("Shop", True, (255, 255, 255))
    title_rect = title_surface.get_rect(center=(width // 2, height // 2 - 150))
    pygame.draw.rect(screen, (45, 45, 45), (width // 2 - 50, height // 2 - 162, 100, 25), 0, 50)

    pygame.draw.rect(screen, (45, 45, 45), (width // 2 - 140, height // 2 - 112, 210, 25), 0, 50)
    coin_inv_shop_text = font.render("You have " + str(coin_inv) + "x", True, (255, 255, 255))
    coin_inv_shop_text_rect = coin_inv_shop_text.get_rect(center=(width // 2 - 50, height // 2 - 100))
    screen.blit(coin_inv_shop_text, coin_inv_shop_text_rect)
    coin_rect_info = (740, 390)

    exit_border = pygame.draw.rect(screen, (205, 45, 45), (width // 2 + 100, height // 2 + 250, 150, 25), 0, 50)
    exit_text = font.render("Exit shop", True, (255, 255, 255))
    exit_text_rect = exit_text.get_rect(center=(width // 2 + 175, height // 2 + 263))
    screen.blit(exit_text, exit_text_rect)

    up1_border = pygame.draw.rect(screen, (45, 45, 45), (width // 2 - 210, height // 2 - 60, 200, 25), 0, 50)
    up1_surface = font.render("Broken shotgun", True, (255, 255, 255))
    up1_rect = up1_surface.get_rect(center=(592, 452))

    up2_border = pygame.draw.rect(screen, (45, 45, 45), (width // 2 - 210, height // 2 - 10, 200, 25), 0, 50)
    up2_surface = font.render("Repair shotgun", True, (255, 255, 255))
    up2_rect = up2_surface.get_rect(center=(592, 502))

    up3_border = pygame.draw.rect(screen, (45, 45, 45), (width // 2 - 210, height // 2 + 39, 180, 25), 0, 50)
    up3_surface = font.render("+10 Hitpoints", True, (255, 255, 255))
    up3_rect = up3_surface.get_rect(center=(572, 552))

    up4_border = pygame.draw.rect(screen, (45, 45, 45), (width // 2 - 210, height // 2 + 89, 180, 25), 0, 50)
    up4_surface = font.render("+1 Movement", True, (255, 255, 255))
    up4_rect = up4_surface.get_rect(center=(572, 602))

    pygame.draw.rect(screen, (45, 45, 45), (400, height // 2 - 60, 85, 25), 0, 50)
    c1_surface = font.render("50x", True, (255, 255, 255))
    c1_rect = c1_surface.get_rect(center=(430, 452))
    pygame.draw.rect(screen, (45, 45, 45), (400, height // 2 - 10, 85, 25), 0, 50)
    c2_surface = font.render("100x", True, (255, 255, 255))
    c2_rect = c2_surface.get_rect(center=(430, 502))

    pygame.draw.rect(screen, (45, 45, 45), (400, height // 2 + 39, 85, 25), 0, 50)
    c3_surface = font.render("25x", True, (255, 255, 255))
    c3_rect = c3_surface.get_rect(center=(430, 552))

    pygame.draw.rect(screen, (45, 45, 45), (400, height // 2 + 89, 85, 25), 0, 50)
    c4_surface = font.render("25x", True, (255, 255, 255))
    c4_rect = c4_surface.get_rect(center=(430, 602))
    coin_rect4 = (458, 592)

    _coin_rect = (458, 442)
    coin_rect1 = (458, 492)
    coin_rect2 = (458, 542)

    for _event in pygame.event.get():
        if _event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        if _event.type == pygame.MOUSEBUTTONDOWN:
            if mouse_rect.colliderect(up1_border) and bullet_upgrade is False and coin_inv >= 50:
                coin_inv -= 50
                sound_controller.play_random_sound(sound_enum.Type.COIN)
                bullet_upgrade = True

            if mouse_rect.colliderect(
                    up2_border) and bullet_upgrade and bullet_upgrade2 is False and coin_inv >= 100:
                coin_inv -= 100
                sound_controller.play_random_sound(sound_enum.Type.COIN)
                bullet_upgrade2 = True

            if mouse_rect.colliderect(up3_border) and max_hp <= 200 and coin_inv >= 25:
                coin_inv -= 25
                sound_controller.play_random_sound(sound_enum.Type.COIN)
                max_hp += 10
                hp += 10

            if mouse_rect.colliderect(up4_border) and player_speed <= 9 and coin_inv >= 25:
                coin_inv -= 25
                sound_controller.play_random_sound(sound_enum.Type.COIN)
                player_speed += 1

            if mouse_rect.colliderect(exit_border):
                is_initialized = False
                return False

    screen.blit(up1_surface, up1_rect)
    screen.blit(c1_surface, c1_rect)
    screen.blit(coinanimlist[0], _coin_rect)
    screen.blit(up2_surface, up2_rect)
    screen.blit(c2_surface, c2_rect)
    screen.blit(coinanimlist[0], coin_rect1)

    if bullet_upgrade:
        pygame.draw.rect(screen, (205, 45, 45), (width // 2 - 300, height // 2 - 50, 270, 7), 0, 50)

    if bullet_upgrade2:
        pygame.draw.rect(screen, (205, 45, 45), (width // 2 - 300, height // 2 - 0, 290, 7), 0, 50)

    if bullet_upgrade is False:
        pygame.draw.rect(screen, (205, 45, 45), (width // 2 - 300, height // 2 - 0, 290, 7), 0, 50)

    screen.blit(up3_surface, up3_rect)
    screen.blit(coinanimlist[0], coin_rect2)
    screen.blit(c3_surface, c3_rect)
    screen.blit(c4_surface, c4_rect)
    screen.blit(coinanimlist[0], coin_rect4)
    screen.blit(up4_surface, up4_rect)

    if max_hp >= 200:
        pygame.draw.rect(screen, (205, 45, 45), (width // 2 - 300, height // 2 + 50, 270, 7), 0, 50)

    if player_speed >= 9:
        pygame.draw.rect(screen, (205, 45, 45), (width // 2 - 300, height // 2 + 100, 270, 7), 0, 50)

    screen.blit(title_surface, title_rect)
    screen.blit(player_surf, player_render_rect)
    screen.blit(coinanimlist[0], coin_rect_info)
    pygame.display.flip()
    return True
