import pygame


class Enemy:
    def __init__(self, rect, target):
        self.rect = rect
        self.target = target
        self.speed = 1

    def move_towards_target(self, camera, tiles):
        if self.rect.x < self.target.x and not self.check_col(
            camera, tiles, self.speed, 0
        ):
            self.rect.x += self.speed
        elif self.rect.x > self.target.x and not self.check_col(
            camera, tiles, -self.speed, 0
        ):
            self.rect.x -= self.speed

        if self.rect.y < self.target.y and not self.check_col(
            camera, tiles, 0, self.speed
        ):
            self.rect.y += self.speed
        elif self.rect.y > self.target.y and not self.check_col(
            camera, tiles, 0, -self.speed
        ):
            self.rect.y -= self.speed

    def check_col(self, camera, tiles, x, y):
        copy = pygame.Rect.copy(self.rect)
        copy = copy.move(x - camera.x, y - camera.y)

        for tile in tiles:
            if tile.collision and pygame.Rect.colliderect(tile.rect, copy):
                return True

        return False
