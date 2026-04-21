import math
import pygame
from .constants import PLAYER_SPEED, PLAYER_RADIUS, BULLET_SPEED, WIDTH, HEIGHT, MAX_HP, WEAPON_PISTOL, WEAPON_SHOTGUN, WEAPON_SNIPER, WEAPON_AUTOMATIC, WEAPONS
from .bullet import Bullet


class Player:
    def __init__(self, screen):
        self.screen = screen
        self.x = self.screen.get_width() // 2
        self.y = self.screen.get_height() // 2
        self.hp = MAX_HP
        self.current_weapon = WEAPON_PISTOL
        self.reload_timer = 0.0
        self.aim_angle = 0.0  # Угол прицела (в радианах)

    def move(self, dt, keys):
        dx = 0
        dy = 0
        if keys[pygame.K_a] or keys[1092]:  # 'ф' = 1092
            dx -= 1
        if keys[pygame.K_d] or keys[1074]:  # 'в' = 1074
            dx += 1
        if keys[pygame.K_w] or keys[1094]:  # 'ц' = 1094
            dy -= 1
        if keys[pygame.K_s] or keys[1099]:  # 'ы' = 1099
            dy += 1

        if dx != 0 or dy != 0:
            if dx != 0 and dy != 0:
                # Diagonal movement, normalize to maintain speed
                length = math.hypot(dx, dy)
                dx /= length
                dy /= length
            self.x += dx * PLAYER_SPEED * dt
            self.y += dy * PLAYER_SPEED * dt

        self.x = max(PLAYER_RADIUS, min(self.screen.get_width() - PLAYER_RADIUS, self.x))
        self.y = max(PLAYER_RADIUS, min(self.screen.get_height() - PLAYER_RADIUS, self.y))

        if self.reload_timer > 0:
            self.reload_timer -= dt

    def update_aim(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        self.aim_angle = math.atan2(mouse_y - self.y, mouse_x - self.x)

    def shoot(self):
        weapon = WEAPONS[self.current_weapon]
        if self.reload_timer > 0:
            return []

        dx = math.cos(self.aim_angle)
        dy = math.sin(self.aim_angle)
        self.reload_timer = weapon['reload_time']

        bullets = []
        if self.current_weapon == WEAPON_SHOTGUN:
            # Shotgun: multiple pellets with spread
            pellets = weapon['pellets']
            spread = weapon['spread']
            for i in range(pellets):
                angle = self.aim_angle + (i - pellets // 2) * spread / pellets
                vx = math.cos(angle) * BULLET_SPEED
                vy = math.sin(angle) * BULLET_SPEED
                bullets.append(Bullet(self.x, self.y, vx, vy, self.screen, weapon['damage']))
        elif self.current_weapon == WEAPON_SNIPER:
            # Sniper: single high-damage bullet
            vx = dx * weapon['speed']
            vy = dy * weapon['speed']
            bullets.append(Bullet(self.x, self.y, vx, vy, self.screen, weapon['damage'], weapon['radius']))
        elif self.current_weapon == WEAPON_AUTOMATIC:
            # Automatic: fast fire
            vx = dx * BULLET_SPEED
            vy = dy * BULLET_SPEED
            bullets.append(Bullet(self.x, self.y, vx, vy, self.screen, weapon['damage']))
        else:  # Pistol
            vx = dx * BULLET_SPEED
            vy = dy * BULLET_SPEED
            bullets.append(Bullet(self.x, self.y, vx, vy, self.screen, weapon['damage']))

        return bullets

    def switch_weapon(self, direction):
        self.current_weapon = (self.current_weapon + direction) % len(WEAPONS)

    def select_weapon(self, weapon_id):
        if 0 <= weapon_id < len(WEAPONS):
            self.current_weapon = weapon_id
