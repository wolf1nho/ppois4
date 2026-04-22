import math
from abc import ABC, abstractmethod

from .bullet import Bullet
from .constants import WeaponType


class Weapon(ABC):
    def __init__(self, stats):
        self.stats = stats

    @abstractmethod
    def fire(self, x, y, aim_angle, screen):
        raise NotImplementedError


class PistolWeapon(Weapon):
    def fire(self, x, y, aim_angle, screen):
        vx = math.cos(aim_angle) * self.stats.bullet_speed
        vy = math.sin(aim_angle) * self.stats.bullet_speed
        return [Bullet(x, y, vx, vy, screen, self.stats.damage, self.stats.bullet_radius)]


class AutomaticWeapon(Weapon):
    def fire(self, x, y, aim_angle, screen):
        vx = math.cos(aim_angle) * self.stats.bullet_speed
        vy = math.sin(aim_angle) * self.stats.bullet_speed
        return [Bullet(x, y, vx, vy, screen, self.stats.damage, self.stats.bullet_radius)]


class SniperWeapon(Weapon):
    def fire(self, x, y, aim_angle, screen):
        vx = math.cos(aim_angle) * self.stats.bullet_speed
        vy = math.sin(aim_angle) * self.stats.bullet_speed
        return [Bullet(x, y, vx, vy, screen, self.stats.damage, self.stats.bullet_radius)]


class ShotgunWeapon(Weapon):
    def fire(self, x, y, aim_angle, screen):
        bullets = []
        pellets = self.stats.pellets
        spread = self.stats.spread
        for i in range(pellets):
            angle = aim_angle + (i - pellets // 2) * spread / pellets
            vx = math.cos(angle) * self.stats.bullet_speed
            vy = math.sin(angle) * self.stats.bullet_speed
            bullets.append(Bullet(x, y, vx, vy, screen, self.stats.damage, self.stats.bullet_radius))
        return bullets


def create_weapon(weapon_type, stats):
    if weapon_type == WeaponType.SHOTGUN:
        return ShotgunWeapon(stats)
    if weapon_type == WeaponType.SNIPER:
        return SniperWeapon(stats)
    if weapon_type == WeaponType.AUTOMATIC:
        return AutomaticWeapon(stats)
    return PistolWeapon(stats)
