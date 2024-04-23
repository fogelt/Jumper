import math
import pygame
import random


class Gun:
    def __init__(self, screen):
        self.screen = screen
        self.bullet_width = 10
        self.bullet_height = 10
        self.bullet_color = (0, 0, 0)
        self.bullet_speed = 10
        self.bullets = []  # Each bullet will be a tuple (rect, speed)

    def shoot(self, player_render_rect, mouse_x, mouse_y):
        new_bullet = pygame.Rect(player_render_rect.right, player_render_rect.centery - self.bullet_height // 2, self.bullet_width,
                                 self.bullet_height)

        # Calculate angle between player and mouse
        angle = math.atan2(mouse_y - player_render_rect.centery, mouse_x - player_render_rect.right)

        # Set bullet speed based on angle
        bullet_speed_x = self.bullet_speed * math.cos(angle)
        bullet_speed_y = self.bullet_speed * math.sin(angle)

        self.bullets.append((new_bullet, (bullet_speed_x, bullet_speed_y)))
        return bullet_speed_x, bullet_speed_y

    def update(self):
        for bullet, speed in self.bullets:
            bullet.x += speed[0]  # Move bullet horizontally
            bullet.y += speed[1]  # Move bullet vertically
            pygame.draw.rect(self.screen, self.bullet_color, bullet)

    def remove_bullets_off_screen(self):
        self.bullets = [(bullet, speed) for bullet, speed in self.bullets if
                        bullet.x < 800]  # Adjust 800 according to your screen width

    def check_collisions(self, snails, camera):
        for bullet, _ in self.bullets[:]:
            adjusted_snail_rects = [snail.rect.move(-camera.x, -camera.y) for snail in snails]
            index = bullet.collidelist(adjusted_snail_rects)
            if index != -1:  # If collision detected
                self.bullets.remove((bullet, _))
                snails.pop(index)



                break