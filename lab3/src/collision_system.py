import math

from .constants import PLAYER_RADIUS


class CollisionSystem:
    @staticmethod
    def handle(player, enemies, bullets, enemy_bullets, damage_player):
        score_delta = 0
        killed_enemies = []

        for enemy in enemies:
            if not enemy.alive:
                continue

            dist_to_player = math.hypot(enemy.x - player.x, enemy.y - player.y)
            if dist_to_player <= enemy.radius + PLAYER_RADIUS:
                enemy.alive = False
                damage_player(enemy.contact_damage, f"contact_{enemy.enemy_type}")
                continue

            for bullet in bullets:
                if not bullet.alive:
                    continue
                dist = math.hypot(enemy.x - bullet.x, enemy.y - bullet.y)
                if dist <= enemy.radius + bullet.radius:
                    bullet.alive = False
                    killed = enemy.take_damage(bullet.damage)
                    if killed:
                        score_delta += enemy.score_value
                        killed_enemies.append((enemy.x, enemy.y, enemy.enemy_type))
                    break

        for bullet in enemy_bullets:
            if not bullet.alive:
                continue
            dist = math.hypot(player.x - bullet.x, player.y - bullet.y)
            if dist <= PLAYER_RADIUS + bullet.radius:
                bullet.alive = False
                damage_player(bullet.damage, "projectile")

        return score_delta, killed_enemies
