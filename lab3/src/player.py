import math

import pygame

from .constants import KEY_ALIASES, MAX_HP, PLAYER_RADIUS, PLAYER_SPEED, WEAPONS, WeaponType
from .weapon import create_weapon


class Player:
    def __init__(self, screen, sounds=None):
        self.screen = screen
        self.sounds = sounds or {}
        self.x = self.screen.get_width() // 2
        self.y = self.screen.get_height() // 2
        self.hp = MAX_HP
        self.radius = PLAYER_RADIUS
        self.current_weapon = WeaponType.AUTOMATIC
        self.reload_timer = 0.0
        self.aim_angle = 0.0
        self.arsenal = {weapon_type: create_weapon(weapon_type, stats) for weapon_type, stats in WEAPONS.items()}

    def move(self, dt, keys):
        dx = 0
        dy = 0

        if keys[pygame.K_a] or keys[KEY_ALIASES["left_ru"]]:
            dx -= 1
        if keys[pygame.K_d] or keys[KEY_ALIASES["right_ru"]]:
            dx += 1
        if keys[pygame.K_w] or keys[KEY_ALIASES["up_ru"]]:
            dy -= 1
        if keys[pygame.K_s] or keys[KEY_ALIASES["down_ru"]]:
            dy += 1

        if dx != 0 or dy != 0:
            if dx != 0 and dy != 0:
                length = math.hypot(dx, dy)
                dx /= length
                dy /= length
            self.x += dx * PLAYER_SPEED * dt
            self.y += dy * PLAYER_SPEED * dt

        self.x = max(self.radius, min(self.screen.get_width() - self.radius, self.x))
        self.y = max(self.radius, min(self.screen.get_height() - self.radius, self.y))

        if self.reload_timer > 0:
            self.reload_timer -= dt

    def update_aim(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.aim_angle = math.atan2(mouse_y - self.y, mouse_x - self.x)

    def shoot(self):
        stats = WEAPONS[self.current_weapon]
        if self.reload_timer > 0:
            return []

        self.reload_timer = stats.reload_time
        bullets = self.arsenal[self.current_weapon].fire(self.x, self.y, self.aim_angle, self.screen)
        sound = self.sounds.get(stats.sound_key)
        if sound:
            sound.play()
        return bullets

    def switch_weapon(self, direction):
        weapon_types = list(WEAPONS.keys())
        current_index = weapon_types.index(self.current_weapon)
        new_index = (current_index + direction) % len(weapon_types)
        self.current_weapon = weapon_types[new_index]

    def select_weapon(self, weapon_index):
        weapon_types = list(WEAPONS.keys())
        if 0 <= weapon_index < len(weapon_types):
            self.current_weapon = weapon_types[weapon_index]
