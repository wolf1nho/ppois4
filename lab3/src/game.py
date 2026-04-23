import math
import os
import random
import sys

import pygame

from .collision_system import CollisionSystem
from .constants import (
    DEATH_EFFECTS,
    ENEMY_BASE_SPEED,
    ENEMY_SPAWN_SPEED_JITTER_MAX,
    ENEMY_SPAWN_SPEED_JITTER_MIN,
    ENEMY_TYPES,
    FPS,
    GameState,
    HEALTH_PICKUP_CONFIG,
    HIGHSCORE_FILE,
    MAX_HP,
    TIME_SCALE,
    enemy_radius_for,
)
from .enemy import Enemy
from .input_handler import InputHandler
from .pickup import HealthPickup
from .player import Player
from .renderer import GameRenderer
from .score_service import ScoreService
from .wave_manager import WaveManager


class Game:
    def __init__(self):
        pygame.init()
        try:
            pygame.mixer.init()
        except Exception:
            pass

        pygame.display.set_caption("Кримзоленд")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()

        self.running = True
        self.state = GameState.MENU
        self.menu_selected = 0
        self.pause_selected = 0
        self.name_input = ""
        self.pending_record = None
        self.last_death_cause = "contact"
        self.last_wave_sound = 0

        self.score_service = ScoreService(HIGHSCORE_FILE)
        self.highscores = self.score_service.load()
        self.renderer = GameRenderer(self.screen)
        self.input_handler = InputHandler()
        self.wave_manager = WaveManager()

        self.sounds = {
            "automatic": self.load_sound("assets/automatic.mp3"),
            "shotgun": self.load_sound("assets/shortgun.mp3"),
            "sniper": self.load_sound("assets/awp.mp3"),
            "player_damage": self.load_sound("assets/playerdamagesound.mp3"),
            "new_wave": self.load_sound("assets/nextwave.mp3"),
            "boss_wave": self.load_sound("assets/boss_wave.mp3"),
            "victory": self.load_sound("assets/game_completed.mp3"),
            "death": self.load_sound("assets/game_over.mp3"),
            "pickup": self.load_sound("assets/pickup.mp3"),
            "ui_move": self.load_sound("assets/ui_move.mp3"),
            "ui_accept": self.load_sound("assets/ui_accept.mp3"),
            "ui_esc": self.load_sound("assets/ui_esc.mp3"),
            # "enemy_death": self.load_sound("assets/enemydeath.mp3")
        }

        self.reset()

    def load_sound(self, relative_path):
        try:
            base_dir = os.path.dirname(os.path.dirname(__file__))
            sound_path = os.path.join(base_dir, relative_path)
            return pygame.mixer.Sound(sound_path)
        except Exception:
            return None

    def save_record(self, name, score):
        self.highscores = self.score_service.add_record(self.highscores, name, score)
        self.score_service.save(self.highscores)

    def play_sound(self, sound_key):
        sound = self.sounds.get(sound_key)
        if sound:
            sound.play()

    def displayed_wave(self):
        if self.last_wave_sound <= 0:
            return 1
        return min(self.last_wave_sound, self.wave_manager.config.total_waves)

    def reset(self):
        self.last_wave_sound = 0
        self.player = Player(self.screen, sounds=self.sounds)
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.health_pickups = []
        self.death_particles = []

        self.score = 0
        self.time_survived = 0.0
        self.game_over = False
        self.victory = False

        self.wave_manager.reset()

    def try_spawn_health_pickup(self, x, y, enemy_type):
        chance = HEALTH_PICKUP_CONFIG.boss_drop_chance if enemy_type == "boss" else HEALTH_PICKUP_CONFIG.drop_chance
        if random.random() > chance:
            return
        self.health_pickups.append(
            HealthPickup(
                x=x,
                y=y,
                heal_amount=HEALTH_PICKUP_CONFIG.heal_amount,
                radius=HEALTH_PICKUP_CONFIG.radius,
                lifetime=HEALTH_PICKUP_CONFIG.lifetime,
            )
        )

    def update_health_pickups(self, dt):
        for pickup in self.health_pickups:
            pickup.update(dt)
            if not pickup.alive:
                continue

            dist = math.hypot(self.player.x - pickup.x, self.player.y - pickup.y)
            if dist <= self.player.radius + pickup.radius:
                self.player.hp = min(MAX_HP, self.player.hp + pickup.heal_amount)
                pickup.alive = False
                if self.sounds.get("pickup"):
                    self.sounds["pickup"].play()

        self.health_pickups = [p for p in self.health_pickups if p.alive]

    def spawn_enemy(self, enemy_type=None):
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        if enemy_type is None:
            enemy_type = self.wave_manager.choose_enemy_type(self.wave_manager.current_wave)
        stats = ENEMY_TYPES[enemy_type]
        radius = enemy_radius_for(stats)

        side = random.randint(0, 3)
        if side == 0:
            x, y = random.randint(0, sw), -radius
        elif side == 1:
            x, y = sw + radius, random.randint(0, sh)
        elif side == 2:
            x, y = random.randint(0, sw), sh + radius
        else:
            x, y = -radius, random.randint(0, sh)

        speed = (
            ENEMY_BASE_SPEED
            * stats.speed_mult
            * random.uniform(ENEMY_SPAWN_SPEED_JITTER_MIN, ENEMY_SPAWN_SPEED_JITTER_MAX)
            * self.wave_manager.difficulty
        )
        self.enemies.append(Enemy(x, y, speed, enemy_type=enemy_type))

    def damage_player(self, damage, cause):
        if self.game_over:
            return

        self.player.hp -= int(damage)
        if self.player.hp <= 0:
            self.player.hp = 0
            self.last_death_cause = cause
            self.trigger_player_death()
        elif self.sounds.get("player_damage"):
            self.sounds["player_damage"].play()

    def trigger_player_death(self):
        if self.game_over:
            return
        self.game_over = True
        self.play_sound("death")
        self.spawn_death_effect(self.last_death_cause)
        self.trigger_name_entry()

    def trigger_name_entry(self):
        self.state = GameState.NAME_ENTRY
        self.name_input = ""
        self.pending_record = self.score

    def spawn_death_effect(self, cause):
        if "projectile" in cause:
            profile = DEATH_EFFECTS["projectile"]
        elif "tank" in cause:
            profile = DEATH_EFFECTS["tank"]
        else:
            profile = DEATH_EFFECTS["default"]

        for _ in range(profile.particle_count):
            angle = random.uniform(0.0, math.tau)
            speed = random.uniform(profile.speed_min, profile.speed_max)
            life = random.uniform(profile.life_min, profile.life_max)
            self.death_particles.append(
                {
                    "x": self.player.x,
                    "y": self.player.y,
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "life": life,
                    "max_life": life,
                    "size": random.randint(2, 6),
                    "color": random.choice(profile.palette),
                    "drag": profile.drag,
                }
            )

    def update_death_particles(self, dt):
        alive = []
        for p in self.death_particles:
            p["life"] -= dt
            if p["life"] <= 0:
                continue
            p["x"] += p["vx"] * dt
            p["y"] += p["vy"] * dt
            p["vx"] *= p["drag"]
            p["vy"] *= p["drag"]
            alive.append(p)
        self.death_particles = alive

    def update(self, dt):
        dt *= TIME_SCALE

        if self.game_over:
            self.update_death_particles(dt)
            return

        pygame.event.pump()
        keys = pygame.key.get_pressed()
        self.player.move(dt, keys)
        self.player.update_aim()

        mouse_pressed = pygame.mouse.get_pressed(num_buttons=3)
        if mouse_pressed[0]:
            self.bullets.extend(self.player.shoot())

        for bullet in self.bullets:
            bullet.update(dt)
        for bullet in self.enemy_bullets:
            bullet.update(dt)

        for enemy in self.enemies:
            enemy.update(dt, self.player)
            enemy_bullet = enemy.try_shoot(dt, self.player, self.screen)
            if enemy_bullet is not None:
                self.enemy_bullets.append(enemy_bullet)

        score_delta, killed_enemies = CollisionSystem.handle(
            self.player,
            self.enemies,
            self.bullets,
            self.enemy_bullets,
            self.damage_player,
        )
        self.score += score_delta
        for x, y, enemy_type in killed_enemies:
            self.try_spawn_health_pickup(x, y, enemy_type)

        self.bullets = [b for b in self.bullets if b.alive]
        self.enemy_bullets = [b for b in self.enemy_bullets if b.alive]
        self.enemies = [e for e in self.enemies if e.alive]

        self.update_health_pickups(dt)
        self.time_survived += dt

        result = self.wave_manager.update(dt, len(self.enemies), len(self.enemy_bullets))
        if result.wave_started:
            wave_sound = "boss_wave" if self.wave_manager.is_boss_wave() else "new_wave"
            self.play_sound(wave_sound)
            self.last_wave_sound = self.wave_manager.current_wave
        for enemy_type in result.spawn_types:
            self.spawn_enemy(enemy_type)

        if result.victory:
            self.victory = True
            self.play_sound("victory")
            self.trigger_name_entry()

        self.update_death_particles(dt)

    def handle_keydown(self, event):
        self.input_handler.handle_keydown(self, event)

    def draw(self):
        self.renderer.draw_playing(self)
        if self.game_over and self.state == GameState.PLAYING:
            self.renderer.draw_game_over_overlay(self.score)

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)

            if self.state == GameState.PLAYING:
                self.update(dt)

            if self.state == GameState.MENU:
                self.renderer.draw_menu(self.menu_selected)
            elif self.state == GameState.PLAYING:
                self.draw()
            elif self.state == GameState.PAUSED:
                self.renderer.draw_pause(self, self.pause_selected)
            elif self.state == GameState.HIGHSCORES:
                self.renderer.draw_highscores(self.highscores)
            elif self.state == GameState.NAME_ENTRY:
                self.update_death_particles(dt)
                self.renderer.draw_name_entry(self)

            pygame.display.flip()

        pygame.quit()
        sys.exit()
