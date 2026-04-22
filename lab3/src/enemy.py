import math

from .bullet import Bullet
from .constants import (
    ENEMY_BASE_SPEED,
    ENEMY_BULLET_RADIUS,
    ENEMY_BULLET_SPEED,
    ENEMY_SHOOT_DISTANCE,
    ENEMY_TYPES,
    enemy_bullet_damage_for,
    enemy_contact_damage_for,
    enemy_hp_for,
    enemy_radius_for,
    enemy_score_for,
    enemy_shoot_interval_for,
)


class Enemy:
    def __init__(self, x, y, speed, enemy_type="grunt"):
        data = ENEMY_TYPES[enemy_type]
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.name = data.name
        self.max_hp = enemy_hp_for(data)
        self.hp = float(self.max_hp)
        self.radius = enemy_radius_for(data)
        self.speed = speed if speed is not None else ENEMY_BASE_SPEED * data.speed_mult
        self.score_value = enemy_score_for(data)
        self.contact_damage = enemy_contact_damage_for(data)
        self.can_shoot = data.can_shoot
        self.shoot_interval = enemy_shoot_interval_for(data)
        self.bullet_damage = enemy_bullet_damage_for(data)
        self.color_fill = data.color_fill
        self.color_outline = data.color_outline
        self.shoot_timer = self.shoot_interval
        self.alive = True

    def update(self, dt, player):
        dx = player.x - self.x
        dy = player.y - self.y
        length = math.hypot(dx, dy)
        if length == 0:
            return
        dx /= length
        dy /= length
        self.x += dx * self.speed * dt
        self.y += dy * self.speed * dt

    def take_damage(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False
            return True
        return False

    def try_shoot(self, dt, player, screen):
        if not self.can_shoot or not self.alive:
            return None

        self.shoot_timer -= dt
        if self.shoot_timer > 0:
            return None

        dx = player.x - self.x
        dy = player.y - self.y
        dist = math.hypot(dx, dy)
        if dist == 0 or dist > ENEMY_SHOOT_DISTANCE:
            return None

        self.shoot_timer = self.shoot_interval
        vx = dx / dist * ENEMY_BULLET_SPEED
        vy = dy / dist * ENEMY_BULLET_SPEED
        return Bullet(
            self.x,
            self.y,
            vx,
            vy,
            screen,
            damage=self.bullet_damage,
            radius=ENEMY_BULLET_RADIUS,
            is_enemy=True,
            color=(255, 122, 122),
        )
