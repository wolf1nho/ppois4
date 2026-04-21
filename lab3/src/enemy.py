import math
from .constants import ENEMY_BASE_SPEED, ENEMY_BULLET_RADIUS, ENEMY_BULLET_SPEED, ENEMY_SHOOT_DISTANCE, ENEMY_TYPES
from .bullet import Bullet


class Enemy:
    def __init__(self, x, y, speed, enemy_type="grunt"):
        data = ENEMY_TYPES[enemy_type]
        self.x = x
        self.y = y
        self.enemy_type = enemy_type
        self.name = data["name"]
        self.max_hp = data["hp"]
        self.hp = float(self.max_hp)
        self.radius = data["radius"]
        self.speed = speed if speed is not None else ENEMY_BASE_SPEED * data["speed_mult"]
        self.score_value = data["score"]
        self.contact_damage = data["contact_damage"]
        self.can_shoot = data["can_shoot"]
        self.shoot_interval = data["shoot_interval"]
        self.bullet_damage = data["bullet_damage"]
        self.color_fill = data["color_fill"]
        self.color_outline = data["color_outline"]
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
