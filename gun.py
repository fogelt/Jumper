import math
import pygame
import random




class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.bullet_width = 6
        self.bullet_height = 6
        self.bullet_color = (0, 0, 0)
        self.bullet_speed = 20
        self.bullets = []  # Each bullet will be a tuple (rect, speed)

    def shoot1(self, gunny_rect, mouse_x, mouse_y):
        new_bullet = pygame.Rect(gunny_rect.left, gunny_rect.centery - 30 - self.bullet_height // 2, self.bullet_width,
                                 self.bullet_height)

        # Calculate angle between player and mouse
        angle = math.atan2(mouse_y - gunny_rect.centery + 30, mouse_x - gunny_rect.left)

        # Set bullet speed based on angle
        bullet_speed_x = self.bullet_speed * math.cos(angle)
        bullet_speed_y = self.bullet_speed * math.sin(angle)

        self.bullets.append((new_bullet, (bullet_speed_x, bullet_speed_y)))
        return bullet_speed_x, bullet_speed_y

    def shoot(self, gunny_rect, mouse_x, mouse_y, bullet_upgrade2):
            angle = math.atan2(mouse_y - gunny_rect.centery + 30, mouse_x - gunny_rect.left)
            num_bullets = 2 if not bullet_upgrade2 else 3
            angle_range = math.radians(30)
            angle_increment = angle_range / (num_bullets - 1)
            bullet_speeds = []
            for i in range(num_bullets):
                adjusted_angle = angle - (angle_range / 2) + (i * angle_increment)

                bullet_speed_x = self.bullet_speed * math.cos(adjusted_angle)
                bullet_speed_y = self.bullet_speed * math.sin(adjusted_angle)

                bullet_speeds.append((bullet_speed_x, bullet_speed_y))

                new_bullet = pygame.Rect(gunny_rect.left, gunny_rect.centery - 30 - self.bullet_height // 2,
                                         self.bullet_width, self.bullet_height)
                self.bullets.append((new_bullet, (bullet_speed_x, bullet_speed_y)))

            return bullet_speeds

    def update(self):
        for bullet, speed in self.bullets:
            bullet.x += speed[0]  # Move bullet horizontally
            bullet.y += speed[1]  # Move bullet vertically
            pygame.draw.rect(self.screen, self.bullet_color, bullet)

    def remove_bullets_off_screen(self):
        self.bullets = [(bullet, speed) for bullet, speed in self.bullets if
                        bullet.x < 800]

    def check_collisions(self, snails, camera, coins, coin_rect):
        for bullet, _ in self.bullets[:]:
            adjusted_snail_rects = [snail.rect.move(-camera.x, -camera.y) for snail in snails]
            index = bullet.collidelist(adjusted_snail_rects)
            if index != -1:  # If collision detected
                removed_snail = snails.pop(index)
                coin_rect.x = removed_snail.rect.x
                coin_rect.y = removed_snail.rect.y
                coins.append(coin_rect)
                self.bullets.remove((bullet, _))

                break