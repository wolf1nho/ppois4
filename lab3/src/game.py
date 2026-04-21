import datetime
import json
import math
import random
import sys

import pygame

from .constants import (
    ENEMY_BASE_SPEED,
    ENEMY_TYPES,
    FPS,
    HIGHSCORE_FILE,
    MAX_HP,
    PLAYER_RADIUS,
    SPAWN_INTERVAL_START,
    TIME_SCALE,
    TOTAL_WAVES,
    WEAPONS,
)
from .enemy import Enemy
from .player import Player


class Game:
    def __init__(self):
        pygame.init()
        pygame.display.set_caption("Кримзоленд")
        self.screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
        pygame.mouse.set_visible(False)
        self.clock = pygame.time.Clock()

        self.font = pygame.font.SysFont("consolas", 24)
        self.big_font = pygame.font.SysFont("consolas", 52)
        self.menu_font = pygame.font.SysFont("consolas", 36)
        self.small_font = pygame.font.SysFont("consolas", 18)

        self.running = True
        self.state = "menu"
        self.highscores = self.load_highscores()
        self.menu_selected = 0
        self.pause_selected = 0
        self.name_input = ""
        self.pending_record = None
        self.last_death_cause = "contact"

        self.reset()

    def load_highscores(self):
        try:
            with open(HIGHSCORE_FILE, "r", encoding="utf-8") as f:
                raw = f.read().strip()
            if not raw:
                return []

            # Backward compatibility with old plain integer score format
            if raw.isdigit():
                legacy_score = int(raw)
                if legacy_score <= 0:
                    return []
                now = datetime.datetime.now()
                return [
                    {
                        "name": "Legacy",
                        "score": legacy_score,
                        "date": now.strftime("%Y-%m-%d"),
                        "time": now.strftime("%H:%M:%S"),
                    }
                ]

            data = json.loads(raw)
            if not isinstance(data, list):
                return []

            clean = []
            for entry in data:
                if not isinstance(entry, dict):
                    continue
                name = str(entry.get("name", "Player"))[:20].strip() or "Player"
                score = int(entry.get("score", 0))
                date = str(entry.get("date", "---- -- --"))
                tm = str(entry.get("time", "--:--:--"))
                clean.append({"name": name, "score": score, "date": date, "time": tm})

            clean.sort(key=lambda x: x["score"], reverse=True)
            return clean[:10]
        except Exception:
            return []

    def save_highscores(self):
        with open(HIGHSCORE_FILE, "w", encoding="utf-8") as f:
            json.dump(self.highscores[:10], f, ensure_ascii=False, indent=2)

    def save_record(self, name, score):
        now = datetime.datetime.now()
        record = {
            "name": (name.strip() or "Player")[:20],
            "score": int(score),
            "date": now.strftime("%Y-%m-%d"),
            "time": now.strftime("%H:%M:%S"),
        }
        self.highscores.append(record)
        self.highscores.sort(key=lambda x: x["score"], reverse=True)
        self.highscores = self.highscores[:10]
        self.save_highscores()

    def reset(self):
        self.player = Player(self.screen)
        self.bullets = []
        self.enemy_bullets = []
        self.enemies = []
        self.death_particles = []

        self.score = 0
        self.time_survived = 0.0
        self.spawn_timer = 0.0
        self.spawn_interval = SPAWN_INTERVAL_START
        self.difficulty = 1.0
        self.game_over = False
        self.victory = False

        self.current_wave = 1
        self.wave_active = False
        self.wave_pause_timer = 0.0
        self.wave_queue = []
        self.wave_banner_timer = 2.2
        self.start_wave(self.current_wave)

    def choose_enemy_type(self, wave):
        roll = random.random()
        if wave <= 4:
            return "grunt" if roll < 0.8 else "swift"
        if wave <= 9:
            if roll < 0.45:
                return "grunt"
            if roll < 0.72:
                return "swift"
            if roll < 0.9:
                return "tank"
            return "shooter"

        if roll < 0.32:
            return "grunt"
        if roll < 0.54:
            return "swift"
        if roll < 0.77:
            return "tank"
        return "shooter"

    def build_wave_queue(self, wave):
        if wave % 5 == 0:
            minions_count = 5 + wave
            queue = [self.choose_enemy_type(wave) for _ in range(minions_count)]
            queue.append("boss")
            random.shuffle(queue)
            return queue

        enemy_count = 7 + wave * 2
        return [self.choose_enemy_type(wave) for _ in range(enemy_count)]

    def start_wave(self, wave):
        self.wave_queue = self.build_wave_queue(wave)
        self.wave_active = True
        self.wave_pause_timer = 0.0
        self.spawn_timer = 0.0
        self.wave_banner_timer = 2.2
        self.difficulty = 1.0 + (wave - 1) * 0.2
        self.spawn_interval = max(0.4, SPAWN_INTERVAL_START - (wave - 1) * 0.03)

    def spawn_enemy(self, enemy_type=None):
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        if enemy_type is None:
            enemy_type = self.choose_enemy_type(self.current_wave)
        radius = ENEMY_TYPES[enemy_type]["radius"]

        side = random.randint(0, 3)
        if side == 0:
            x, y = random.randint(0, sw), -radius
        elif side == 1:
            x, y = sw + radius, random.randint(0, sh)
        elif side == 2:
            x, y = random.randint(0, sw), sh + radius
        else:
            x, y = -radius, random.randint(0, sh)

        speed = ENEMY_BASE_SPEED * ENEMY_TYPES[enemy_type]["speed_mult"] * random.uniform(0.88, 1.24) * self.difficulty
        self.enemies.append(Enemy(x, y, speed, enemy_type=enemy_type))

    def complete_wave(self):
        self.wave_active = False
        self.current_wave += 1
        if self.current_wave > TOTAL_WAVES:
            self.victory = True
            self.trigger_name_entry()
            return

        self.wave_pause_timer = 2.4
        self.wave_banner_timer = 2.2

    def damage_player(self, damage, cause):
        if self.game_over:
            return

        self.player.hp -= int(damage)
        if self.player.hp <= 0:
            self.player.hp = 0
            self.last_death_cause = cause
            self.trigger_player_death()

    def trigger_player_death(self):
        if self.game_over:
            return
        self.game_over = True
        self.spawn_death_effect(self.last_death_cause)
        self.trigger_name_entry()

    def trigger_name_entry(self):
        self.state = "name_entry"
        self.name_input = ""
        self.pending_record = self.score

    def spawn_death_effect(self, cause):
        if "projectile" in cause:
            palette = [(255, 180, 140), (255, 90, 90), (255, 220, 120)]
            particle_count = 60
            speed_min, speed_max = 90, 420
            life_min, life_max = 0.4, 1.0
        elif "tank" in cause:
            palette = [(255, 255, 255), (180, 220, 255), (105, 170, 255)]
            particle_count = 45
            speed_min, speed_max = 70, 260
            life_min, life_max = 0.35, 0.85
        else:
            palette = [(255, 120, 120), (255, 180, 180), (255, 230, 230)]
            particle_count = 50
            speed_min, speed_max = 80, 340
            life_min, life_max = 0.35, 0.95

        for _ in range(particle_count):
            angle = random.uniform(0.0, math.tau)
            speed = random.uniform(speed_min, speed_max)
            self.death_particles.append(
                {
                    "x": self.player.x,
                    "y": self.player.y,
                    "vx": math.cos(angle) * speed,
                    "vy": math.sin(angle) * speed,
                    "life": random.uniform(life_min, life_max),
                    "max_life": random.uniform(life_min, life_max),
                    "size": random.randint(2, 6),
                    "color": random.choice(palette),
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
            p["vx"] *= 0.96
            p["vy"] *= 0.96
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
            bullets = self.player.shoot()
            self.bullets.extend(bullets)

        for bullet in self.bullets:
            bullet.update(dt)

        for bullet in self.enemy_bullets:
            bullet.update(dt)

        for enemy in self.enemies:
            enemy.update(dt, self.player)
            enemy_bullet = enemy.try_shoot(dt, self.player, self.screen)
            if enemy_bullet is not None:
                self.enemy_bullets.append(enemy_bullet)

        self.handle_collisions()

        self.bullets = [b for b in self.bullets if b.alive]
        self.enemy_bullets = [b for b in self.enemy_bullets if b.alive]
        self.enemies = [e for e in self.enemies if e.alive]

        self.time_survived += dt

        if self.wave_active:
            self.spawn_timer += dt
            while self.wave_queue and self.spawn_timer >= self.spawn_interval:
                enemy_type = self.wave_queue.pop(0)
                self.spawn_enemy(enemy_type)
                self.spawn_timer -= self.spawn_interval

            if not self.wave_queue and not self.enemies and not self.enemy_bullets:
                self.complete_wave()
        else:
            if self.wave_pause_timer > 0:
                self.wave_pause_timer -= dt
                if self.wave_pause_timer <= 0 and not self.game_over:
                    self.start_wave(self.current_wave)

        if self.wave_banner_timer > 0:
            self.wave_banner_timer -= dt

        self.update_death_particles(dt)

    def handle_collisions(self):
        for enemy in self.enemies:
            if not enemy.alive:
                continue

            dist_to_player = math.hypot(enemy.x - self.player.x, enemy.y - self.player.y)
            if dist_to_player <= enemy.radius + PLAYER_RADIUS:
                enemy.alive = False
                self.damage_player(enemy.contact_damage, f"contact_{enemy.enemy_type}")
                continue

            for bullet in self.bullets:
                if not bullet.alive:
                    continue
                dist = math.hypot(enemy.x - bullet.x, enemy.y - bullet.y)
                if dist <= enemy.radius + bullet.radius:
                    bullet.alive = False
                    killed = enemy.take_damage(bullet.damage)
                    if killed:
                        self.score += enemy.score_value
                    break

        for bullet in self.enemy_bullets:
            if not bullet.alive:
                continue
            dist = math.hypot(self.player.x - bullet.x, self.player.y - bullet.y)
            if dist <= PLAYER_RADIUS + bullet.radius:
                bullet.alive = False
                self.damage_player(bullet.damage, "projectile")

    def draw_background(self):
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        self.screen.fill((14, 10, 16))
        for y in range(0, sh, 34):
            pygame.draw.line(self.screen, (34, 26, 42), (0, y), (sw, y), 1)
        for x in range(0, sw, 34):
            pygame.draw.line(self.screen, (34, 26, 42), (x, 0), (x, sh), 1)

    def draw_hp_bar(self):
        bar_x, bar_y, bar_w, bar_h = 16, 12, 280, 22
        ratio = max(0.0, min(1.0, self.player.hp / MAX_HP))

        pygame.draw.rect(self.screen, (45, 25, 30), (bar_x, bar_y, bar_w, bar_h), border_radius=6)
        fill_color = (70, 210, 110) if ratio > 0.6 else ((255, 185, 70) if ratio > 0.3 else (230, 70, 70))
        pygame.draw.rect(self.screen, fill_color, (bar_x, bar_y, int(bar_w * ratio), bar_h), border_radius=6)
        pygame.draw.rect(self.screen, (235, 235, 235), (bar_x, bar_y, bar_w, bar_h), 2, border_radius=6)

        hp_text = self.small_font.render(f"HP {self.player.hp}/{MAX_HP}", True, (245, 245, 245))
        self.screen.blit(hp_text, (bar_x + 8, bar_y + 1))

    def draw(self):
        self.draw_background()

        for bullet in self.bullets:
            pygame.draw.circle(self.screen, bullet.color, (int(bullet.x), int(bullet.y)), bullet.radius)

        for bullet in self.enemy_bullets:
            pygame.draw.circle(self.screen, bullet.color, (int(bullet.x), int(bullet.y)), bullet.radius)

        for enemy in self.enemies:
            pygame.draw.circle(self.screen, enemy.color_fill, (int(enemy.x), int(enemy.y)), enemy.radius)
            pygame.draw.circle(self.screen, enemy.color_outline, (int(enemy.x), int(enemy.y)), enemy.radius, 2)
            if enemy.hp < enemy.max_hp:
                hp_w = max(14, enemy.radius * 2)
                hp_ratio = max(0.0, enemy.hp / enemy.max_hp)
                ex = int(enemy.x - hp_w / 2)
                ey = int(enemy.y - enemy.radius - 10)
                pygame.draw.rect(self.screen, (20, 20, 20), (ex, ey, hp_w, 4))
                pygame.draw.rect(self.screen, (90, 220, 90), (ex, ey, int(hp_w * hp_ratio), 4))

        if not self.game_over:
            pygame.draw.circle(self.screen, (70, 170, 255), (int(self.player.x), int(self.player.y)), PLAYER_RADIUS)
            pygame.draw.circle(self.screen, (205, 235, 255), (int(self.player.x), int(self.player.y)), PLAYER_RADIUS, 3)

        for p in self.death_particles:
            alpha_ratio = max(0.0, p["life"] / p["max_life"])
            radius = max(1, int(p["size"] * alpha_ratio))
            pygame.draw.circle(self.screen, p["color"], (int(p["x"]), int(p["y"])), radius)

        self.draw_crosshair()
        self.draw_hud()

        if self.game_over and self.state == "playing":
            self.draw_game_over()

    def draw_hud(self):
        self.draw_hp_bar()

        score_text = self.font.render(f"Счёт: {self.score}", True, (230, 230, 230))
        time_text = self.font.render(f"Время: {self.time_survived:05.1f}", True, (230, 230, 230))
        wave_text = self.font.render(f"Волна: {min(self.current_wave, TOTAL_WAVES)}/{TOTAL_WAVES}", True, (245, 220, 140))
        pause_text = self.small_font.render("P - пауза", True, (200, 200, 200))
        weapon_text = self.small_font.render(f"Оружие: {WEAPONS[self.player.current_weapon]['name']}", True, (220, 220, 220))
        switch_text = self.small_font.render("Q/E или 1-4 - смена", True, (200, 200, 200))
        aim_text = self.small_font.render("Мышь - прицел / ЛКМ - огонь", True, (200, 200, 200))
        pending = len(self.wave_queue) + len(self.enemies)
        left_text = self.small_font.render(f"Осталось на волне: {pending}", True, (200, 220, 255))
        if self.current_wave <= TOTAL_WAVES and self.current_wave % 5 == 0:
            boss_text = self.small_font.render("Волна босса", True, (255, 205, 120))
        else:
            boss_text = None

        self.screen.blit(score_text, (16, 42))
        self.screen.blit(time_text, (16, 70))
        self.screen.blit(wave_text, (16, 98))
        self.screen.blit(pause_text, (16, 128))
        self.screen.blit(weapon_text, (16, 151))
        self.screen.blit(switch_text, (16, 174))
        self.screen.blit(aim_text, (16, 197))
        self.screen.blit(left_text, (16, 220))
        if boss_text is not None:
            self.screen.blit(boss_text, (16, 243))

        if self.wave_banner_timer > 0 and not self.game_over:
            alpha = max(0.0, min(1.0, self.wave_banner_timer / 2.2))
            banner_surface = pygame.Surface((430, 54), pygame.SRCALPHA)
            banner_surface.fill((20, 20, 20, int(170 * alpha)))
            self.screen.blit(banner_surface, (self.screen.get_width() // 2 - 215, 20))
            banner_color = (255, 220, 120) if self.current_wave % 5 == 0 else (220, 220, 220)
            banner_text = self.menu_font.render(f"ВОЛНА {self.current_wave}", True, banner_color)
            self.screen.blit(banner_text, (self.screen.get_width() // 2 - banner_text.get_width() // 2, 30))

    def draw_crosshair(self):
        mouse_x, mouse_y = pygame.mouse.get_pos()
        pulse = 2 + int((math.sin(pygame.time.get_ticks() * 0.01) + 1.0) * 1.5)
        outer = 18 + pulse
        inner = 8

        pygame.draw.circle(self.screen, (20, 20, 20), (mouse_x, mouse_y), 11, 1)
        pygame.draw.circle(self.screen, (120, 255, 150), (mouse_x, mouse_y), 4)
        pygame.draw.circle(self.screen, (230, 255, 240), (mouse_x, mouse_y), 2)

        pygame.draw.line(self.screen, (80, 255, 120), (mouse_x - outer, mouse_y), (mouse_x - inner, mouse_y), 2)
        pygame.draw.line(self.screen, (80, 255, 120), (mouse_x + inner, mouse_y), (mouse_x + outer, mouse_y), 2)
        pygame.draw.line(self.screen, (80, 255, 120), (mouse_x, mouse_y - outer), (mouse_x, mouse_y - inner), 2)
        pygame.draw.line(self.screen, (80, 255, 120), (mouse_x, mouse_y + inner), (mouse_x, mouse_y + outer), 2)

        aim_distance = 50
        aim_end_x = self.player.x + math.cos(self.player.aim_angle) * aim_distance
        aim_end_y = self.player.y + math.sin(self.player.aim_angle) * aim_distance
        pygame.draw.line(
            self.screen,
            (90, 220, 150),
            (int(self.player.x), int(self.player.y)),
            (int(aim_end_x), int(aim_end_y)),
            2,
        )

    def draw_game_over(self):
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 165))
        self.screen.blit(overlay, (0, 0))

        title = self.big_font.render("КРИМЗОЛЕНД", True, (255, 80, 80))
        lose = self.font.render("Ты проиграл", True, (245, 245, 245))
        final_score = self.font.render(f"Финальный счёт: {self.score}", True, (245, 245, 245))
        hint = self.small_font.render("R - заново | ESC - меню", True, (220, 220, 220))

        sw = self.screen.get_width()
        sh = self.screen.get_height()
        self.screen.blit(title, (sw // 2 - title.get_width() // 2, sh // 2 - 90))
        self.screen.blit(lose, (sw // 2 - lose.get_width() // 2, sh // 2 - 20))
        self.screen.blit(final_score, (sw // 2 - final_score.get_width() // 2, sh // 2 + 18))
        self.screen.blit(hint, (sw // 2 - hint.get_width() // 2, sh // 2 + 58))

    def draw_name_entry(self):
        self.draw()
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        sw = self.screen.get_width()
        sh = self.screen.get_height()

        if self.victory:
            title = self.menu_font.render("ПОБЕДА! 25 волн пройдены", True, (255, 220, 120))
            prompt_text = "Введи имя для таблицы рекордов:"
        else:
            title = self.menu_font.render("Новый рекорд", True, (255, 220, 120))
            prompt_text = "Введи имя и нажми Enter:"
        score_line = self.font.render(f"Очки: {self.pending_record}", True, (235, 235, 235))
        prompt = self.font.render(prompt_text, True, (235, 235, 235))
        name_value = self.font.render(self.name_input + "_", True, (120, 255, 170))
        hint = self.small_font.render("Backspace - удалить | ESC - пропустить", True, (200, 200, 200))

        self.screen.blit(title, (sw // 2 - title.get_width() // 2, sh // 2 - 120))
        self.screen.blit(score_line, (sw // 2 - score_line.get_width() // 2, sh // 2 - 70))
        self.screen.blit(prompt, (sw // 2 - prompt.get_width() // 2, sh // 2 - 20))
        self.screen.blit(name_value, (sw // 2 - name_value.get_width() // 2, sh // 2 + 22))
        self.screen.blit(hint, (sw // 2 - hint.get_width() // 2, sh // 2 + 65))

    def draw_menu(self):
        self.screen.fill((0, 0, 0))
        title = self.big_font.render("КРИМЗОЛЕНД", True, (255, 80, 80))
        options = ["Начать игру", "Рекорды", "Выход"]
        colors = [(255, 255, 255) if i != self.menu_selected else (255, 255, 0) for i in range(3)]

        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 100))
        for i, opt in enumerate(options):
            text = self.menu_font.render(f"{i + 1}. {opt}", True, colors[i])
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 250 + i * 50))

    def draw_highscores(self):
        self.screen.fill((0, 0, 0))
        title = self.big_font.render("РЕКОРДЫ", True, (255, 80, 80))
        back = self.small_font.render("ESC - назад", True, (200, 200, 200))

        sw = self.screen.get_width()
        self.screen.blit(title, (sw // 2 - title.get_width() // 2, 60))
        self.screen.blit(back, (sw // 2 - back.get_width() // 2, 95))

        header = self.small_font.render("МЕСТО   ИМЯ                 ОЧКИ     ДАТА         ВРЕМЯ", True, (150, 210, 255))
        self.screen.blit(header, (sw // 2 - header.get_width() // 2, 165))

        if not self.highscores:
            empty = self.font.render("Рекордов пока нет", True, (230, 230, 230))
            self.screen.blit(empty, (sw // 2 - empty.get_width() // 2, 250))
            return

        for i, rec in enumerate(self.highscores[:10]):
            color = (255, 220, 120) if i == 0 else (235, 235, 235)
            line = self.small_font.render(
                f"{i + 1:>2}      {rec['name']:<20} {rec['score']:>6}   {rec['date']:<10}   {rec['time']}",
                True,
                color,
            )
            self.screen.blit(line, (sw // 2 - line.get_width() // 2, 200 + i * 28))

    def draw_pause(self):
        self.draw()
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        title = self.big_font.render("ПАУЗА", True, (255, 80, 80))
        options = ["Продолжить", "Выйти в меню"]
        colors = [(255, 255, 255) if i != self.pause_selected else (255, 255, 0) for i in range(2)]

        sw = self.screen.get_width()
        sh = self.screen.get_height()
        self.screen.blit(title, (sw // 2 - title.get_width() // 2, sh // 2 - 100))
        for i, opt in enumerate(options):
            text = self.menu_font.render(opt, True, colors[i])
            self.screen.blit(text, (sw // 2 - text.get_width() // 2, sh // 2 - 20 + i * 50))

    def handle_keydown(self, event):
        if self.state == "name_entry":
            if event.key == pygame.K_RETURN:
                self.save_record(self.name_input, self.pending_record)
                self.pending_record = None
                self.state = "highscores"
            elif event.key == pygame.K_BACKSPACE:
                self.name_input = self.name_input[:-1]
            elif event.key == pygame.K_ESCAPE:
                self.pending_record = None
                self.state = "menu"
                self.reset()
            elif event.unicode and event.unicode.isprintable() and len(self.name_input) < 20:
                self.name_input += event.unicode
            return

        if event.key == pygame.K_ESCAPE:
            if self.state == "playing" and self.game_over:
                self.state = "menu"
                self.reset()
            elif self.state == "highscores":
                self.state = "menu"
            elif self.state == "paused":
                self.state = "playing"
            elif self.state == "playing" and not self.game_over:
                self.state = "paused"
            else:
                self.running = False

        if self.state == "playing" and not self.game_over and event.key in (pygame.K_p, pygame.K_SPACE):
            self.state = "paused"

        if self.state == "playing" and event.key in (pygame.K_q, 1081):
            self.player.switch_weapon(-1)
        if self.state == "playing" and event.key in (pygame.K_e, 1091):
            self.player.switch_weapon(1)
        if self.state == "playing" and event.key in (pygame.K_1, 49):
            self.player.select_weapon(0)
        if self.state == "playing" and event.key in (pygame.K_2, 50):
            self.player.select_weapon(1)
        if self.state == "playing" and event.key in (pygame.K_3, 51):
            self.player.select_weapon(2)
        if self.state == "playing" and event.key in (pygame.K_4, 52):
            self.player.select_weapon(3)

        if self.state == "menu":
            if event.key in (pygame.K_DOWN, 1099):
                self.menu_selected = (self.menu_selected + 1) % 3
            elif event.key in (pygame.K_UP, 1094):
                self.menu_selected = (self.menu_selected - 1) % 3
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.menu_selected == 0:
                    self.reset()
                    self.state = "playing"
                elif self.menu_selected == 1:
                    self.state = "highscores"
                elif self.menu_selected == 2:
                    self.running = False

        if self.state == "paused":
            if event.key in (pygame.K_DOWN, 1099):
                self.pause_selected = (self.pause_selected + 1) % 2
            elif event.key in (pygame.K_UP, 1094):
                self.pause_selected = (self.pause_selected - 1) % 2
            elif event.key in (pygame.K_RETURN, pygame.K_SPACE):
                if self.pause_selected == 0:
                    self.state = "playing"
                elif self.pause_selected == 1:
                    self.state = "menu"
                    self.reset()

        if self.state == "playing" and self.game_over and event.key in (pygame.K_r, 1082):
            self.reset()
            self.state = "playing"

    def run(self):
        while self.running:
            dt = self.clock.tick(FPS) / 1000.0

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.running = False
                elif event.type == pygame.KEYDOWN:
                    self.handle_keydown(event)

            if self.state == "playing":
                self.update(dt)

            if self.state == "menu":
                self.draw_menu()
            elif self.state == "playing":
                self.draw()
            elif self.state == "paused":
                self.draw_pause()
            elif self.state == "highscores":
                self.draw_highscores()
            elif self.state == "name_entry":
                self.update_death_particles(dt)
                self.draw_name_entry()

            pygame.display.flip()

        pygame.quit()
        sys.exit()
