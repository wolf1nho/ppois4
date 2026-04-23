import math
import os

import pygame

from .constants import MAX_HP, UI_CONFIG, WEAPONS


class GameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("consolas", 24)
        self.big_font = pygame.font.SysFont("consolas", 52)
        self.menu_font = pygame.font.SysFont("consolas", 36)
        self.small_font = pygame.font.SysFont("consolas", 18)
        self.weapon_slot_font = pygame.font.SysFont("consolas", 16)
        self.weapon_images = self.load_weapon_images()

    def load_weapon_images(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        image_paths = {
            "Автомат": "assets/automatic.png",
            "Дробовик": "assets/shortgun.png",
            "Снайперка": "assets/awp.png",
        }
        loaded = {}
        for weapon_name, relative_path in image_paths.items():
            try:
                loaded[weapon_name] = pygame.image.load(os.path.join(base_dir, relative_path)).convert_alpha()
            except Exception:
                loaded[weapon_name] = None
        return loaded

    def draw_background(self):
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        self.screen.fill((14, 10, 16))
        for y in range(0, sh, 34):
            pygame.draw.line(self.screen, (34, 26, 42), (0, y), (sw, y), 1)
        for x in range(0, sw, 34):
            pygame.draw.line(self.screen, (34, 26, 42), (x, 0), (x, sh), 1)

    def draw_laser_bullet(self, bullet):
        speed = math.hypot(bullet.vx, bullet.vy)
        if speed == 0:
            return

        dx = bullet.vx / speed
        dy = bullet.vy / speed
        px = -dy
        py = dx

        length = max(12, bullet.radius * 5)
        half_width = max(2, bullet.radius // 2)
        half_len = length / 2

        x = bullet.x
        y = bullet.y

        p1 = (x - dx * half_len - px * half_width, y - dy * half_len - py * half_width)
        p2 = (x + dx * half_len - px * half_width, y + dy * half_len - py * half_width)
        p3 = (x + dx * half_len + px * half_width, y + dy * half_len + py * half_width)
        p4 = (x - dx * half_len + px * half_width, y - dy * half_len + py * half_width)

        pygame.draw.polygon(self.screen, bullet.color, (p1, p2, p3, p4))

        core_half_width = max(1, half_width - 1)
        c1 = (x - dx * half_len - px * core_half_width, y - dy * half_len - py * core_half_width)
        c2 = (x + dx * half_len - px * core_half_width, y + dy * half_len - py * core_half_width)
        c3 = (x + dx * half_len + px * core_half_width, y + dy * half_len + py * core_half_width)
        c4 = (x - dx * half_len + px * core_half_width, y - dy * half_len + py * core_half_width)
        pygame.draw.polygon(self.screen, (255, 255, 255), (c1, c2, c3, c4))

    def draw_health_pickup(self, pickup):
        cx = int(pickup.x)
        cy = int(pickup.y)
        radius = pickup.radius
        bar_w = max(26, radius * 3)
        bar_h = 5
        bar_x = cx - bar_w // 2
        bar_y = cy - radius - 14
        lifetime_ratio = max(0.0, min(1.0, pickup.lifetime / max(0.01, pickup.max_lifetime)))

        pygame.draw.rect(self.screen, (18, 30, 20), (bar_x, bar_y, bar_w, bar_h), border_radius=3)
        pygame.draw.rect(self.screen, (80, 235, 130), (bar_x, bar_y, int(bar_w * lifetime_ratio), bar_h), border_radius=3)
        pygame.draw.rect(self.screen, (200, 255, 220), (bar_x, bar_y, bar_w, bar_h), 1, border_radius=3)

        pygame.draw.circle(self.screen, (28, 95, 52), (cx, cy), radius + 2)
        pygame.draw.circle(self.screen, (68, 220, 120), (cx, cy), radius)
        pygame.draw.circle(self.screen, (180, 255, 210), (cx, cy), max(2, radius // 2), 2)

        cross_len = max(4, radius - 6)
        cross_thickness = max(2, radius // 3)
        pygame.draw.line(self.screen, (245, 255, 245), (cx - cross_len, cy), (cx + cross_len, cy), cross_thickness)
        pygame.draw.line(self.screen, (245, 255, 245), (cx, cy - cross_len), (cx, cy + cross_len), cross_thickness)

    def draw_hp_bar(self, player_hp):
        bar_x, bar_y = UI_CONFIG.hp_bar_pos
        bar_w, bar_h = UI_CONFIG.hp_bar_size
        ratio = max(0.0, min(1.0, player_hp / MAX_HP))
        hp_surface = pygame.Surface((bar_w, bar_h), pygame.SRCALPHA)
        pygame.draw.rect(hp_surface, (45, 25, 30, 140), (0, 0, bar_w, bar_h), border_radius=6)
        fill_color = (70, 210, 110) if ratio > 0.6 else ((255, 185, 70) if ratio > 0.3 else (230, 70, 70))
        pygame.draw.rect(hp_surface, (*fill_color, 190), (0, 0, int(bar_w * ratio), bar_h), border_radius=6)
        pygame.draw.rect(hp_surface, (235, 235, 235, 210), (0, 0, bar_w, bar_h), 2, border_radius=6)
        self.screen.blit(hp_surface, (bar_x, bar_y))

        hp_text = self.small_font.render(f"HP {int(player_hp)}/{MAX_HP}", True, (245, 245, 245))
        self.screen.blit(hp_text, (bar_x + 8, bar_y + 1))

    def draw_crosshair(self, player):
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

        aim_end_x = player.x + math.cos(player.aim_angle) * UI_CONFIG.crosshair_aim_distance
        aim_end_y = player.y + math.sin(player.aim_angle) * UI_CONFIG.crosshair_aim_distance
        pygame.draw.line(
            self.screen,
            (90, 220, 150),
            (int(player.x), int(player.y)),
            (int(aim_end_x), int(aim_end_y)),
            2,
        )

    def draw_weapon_slot(self, x, y, width, height, weapon_name, footer_label, active=False):
        base_color = (26, 30, 38) if not active else (62, 44, 18)
        border_color = (110, 130, 160) if not active else (255, 215, 110)
        text_color = (205, 215, 230) if not active else (255, 235, 170)

        slot_surface = pygame.Surface((width, height), pygame.SRCALPHA)
        slot_surface.fill((0, 0, 0, 0))
        pygame.draw.rect(slot_surface, (*base_color, 150), (0, 0, width, height), border_radius=10)
        pygame.draw.rect(slot_surface, (*border_color, 185), (0, 0, width, height), 2, border_radius=10)

        image = self.weapon_images.get(weapon_name)
        image_box = pygame.Rect(8, 8, width - 16, max(24, height - 48))
        if image is not None:
            iw, ih = image.get_size()
            scale = min(image_box.width / iw, image_box.height / ih)
            scaled_size = (max(1, int(iw * scale)), max(1, int(ih * scale)))
            scaled = pygame.transform.smoothscale(image, scaled_size)
            image_pos = (
                image_box.x + (image_box.width - scaled_size[0]) // 2,
                image_box.y + (image_box.height - scaled_size[1]) // 2,
            )
            slot_surface.blit(scaled, image_pos)
        else:
            pygame.draw.rect(slot_surface, (48, 56, 68), image_box, border_radius=8)
            fallback = self.small_font.render(weapon_name, True, (230, 230, 230))
            slot_surface.blit(
                fallback,
                (image_box.centerx - fallback.get_width() // 2, image_box.centery - fallback.get_height() // 2),
            )

        footer_text = self.weapon_slot_font.render(footer_label, True, text_color)
        name_text = self.weapon_slot_font.render(weapon_name, True, text_color)
        slot_surface.blit(footer_text, (width // 2 - footer_text.get_width() // 2, height - 38))
        slot_surface.blit(name_text, (width // 2 - name_text.get_width() // 2, height - 20))

        self.screen.blit(slot_surface, (x, y))

    def draw_weapon_hud(self, player):
        weapon_types = list(WEAPONS.keys())
        current_index = weapon_types.index(player.current_weapon)
        left_weapon = WEAPONS[weapon_types[(current_index - 1) % len(weapon_types)]].name
        current_weapon = WEAPONS[player.current_weapon].name
        right_weapon = WEAPONS[weapon_types[(current_index + 1) % len(weapon_types)]].name

        sw = self.screen.get_width()
        panel_w = 318
        panel_h = 122
        panel_x = sw - panel_w - 18
        panel_y = 12

        panel_surface = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel_surface, (16, 18, 24, 110), (0, 0, panel_w, panel_h), border_radius=16)
        pygame.draw.rect(panel_surface, (75, 90, 110, 170), (0, 0, panel_w, panel_h), 2, border_radius=16)
        self.screen.blit(panel_surface, (panel_x, panel_y))

        title = self.small_font.render("ОРУЖИЕ", True, (220, 230, 240))
        self.screen.blit(title, (panel_x + 16, panel_y + 12))

        side_w = 72
        main_w = 126
        slot_h = 72
        slot_y = panel_y + 34

        self.draw_weapon_slot(panel_x + 12, slot_y, side_w, slot_h, left_weapon, "Q")
        self.draw_weapon_slot(panel_x + 12 + side_w + 12, slot_y, main_w, slot_h, current_weapon, "СЕЙЧАС", active=True)
        self.draw_weapon_slot(panel_x + 12 + side_w + 12 + main_w + 12, slot_y, side_w, slot_h, right_weapon, "E")

    def draw_hud(self, game):
        self.draw_hp_bar(game.player.hp)
        self.draw_weapon_hud(game.player)

        score_text = self.font.render(f"Счёт: {game.score}", True, (230, 230, 230))
        time_text = self.font.render(f"Время: {game.time_survived:05.1f}", True, (230, 230, 230))
        total_waves = game.wave_manager.config.total_waves
        wave_text = self.font.render(f"Волна: {min(game.wave_manager.current_wave, total_waves)}/{total_waves}", True, (245, 220, 140))
        switch_text = self.small_font.render("Q/E или 1-3 - смена", True, (200, 200, 200))
        pending = game.wave_manager.pending_count(len(game.enemies))
        left_text = self.small_font.render(f"Осталось на волне: {pending}", True, (200, 220, 255))
        boss_text = self.small_font.render("Волна босса", True, (255, 205, 120)) if game.wave_manager.is_boss_wave() else None

        left = UI_CONFIG.hud_left
        top = UI_CONFIG.hud_top
        step = 24
        info_lines = [score_text, time_text, wave_text, switch_text, left_text]
        if boss_text is not None:
            info_lines.append(boss_text)

        info_height = 20 + step * len(info_lines)
        max_width = max(line.get_width() for line in info_lines) + 24
        info_surface = pygame.Surface((max_width, info_height), pygame.SRCALPHA)
        pygame.draw.rect(info_surface, (12, 14, 18, 88), (0, 0, max_width, info_height), border_radius=12)
        pygame.draw.rect(info_surface, (70, 82, 98, 135), (0, 0, max_width, info_height), 1, border_radius=12)
        self.screen.blit(info_surface, (left - 8, top - 6))

        self.screen.blit(score_text, (left, top))
        self.screen.blit(time_text, (left, top + step))
        self.screen.blit(wave_text, (left, top + step * 2))
        self.screen.blit(switch_text, (left, top + step * 3))
        self.screen.blit(left_text, (left, top + step * 4))
        if boss_text is not None:
            self.screen.blit(boss_text, (left, top + step * 5))

        if game.wave_manager.wave_banner_timer > 0 and not game.game_over:
            alpha = max(0.0, min(1.0, game.wave_manager.wave_banner_timer / game.wave_manager.config.banner_duration))
            bw, bh = UI_CONFIG.wave_banner_size
            banner_surface = pygame.Surface((bw, bh), pygame.SRCALPHA)
            banner_surface.fill((20, 20, 20, int(170 * alpha)))
            self.screen.blit(banner_surface, (self.screen.get_width() // 2 - bw // 2, UI_CONFIG.wave_banner_top))
            banner_color = (255, 220, 120) if game.wave_manager.current_wave % game.wave_manager.config.boss_every == 0 else (220, 220, 220)
            banner_text = self.menu_font.render(f"ВОЛНА {game.wave_manager.current_wave}", True, banner_color)
            self.screen.blit(banner_text, (self.screen.get_width() // 2 - banner_text.get_width() // 2, UI_CONFIG.wave_banner_top + 10))

    def draw_playing(self, game):
        self.draw_background()

        for bullet in game.bullets:
            self.draw_laser_bullet(bullet)

        for bullet in game.enemy_bullets:
            self.draw_laser_bullet(bullet)

        for pickup in game.health_pickups:
            self.draw_health_pickup(pickup)

        for enemy in game.enemies:
            pygame.draw.circle(self.screen, enemy.color_fill, (int(enemy.x), int(enemy.y)), enemy.radius)
            pygame.draw.circle(self.screen, enemy.color_outline, (int(enemy.x), int(enemy.y)), enemy.radius, 2)
            if enemy.hp < enemy.max_hp:
                hp_w = max(14, enemy.radius * 2)
                hp_ratio = max(0.0, enemy.hp / enemy.max_hp)
                ex = int(enemy.x - hp_w / 2)
                ey = int(enemy.y - enemy.radius - 10)
                pygame.draw.rect(self.screen, (20, 20, 20), (ex, ey, hp_w, 4))
                pygame.draw.rect(self.screen, (90, 220, 90), (ex, ey, int(hp_w * hp_ratio), 4))

        if not game.game_over:
            pygame.draw.circle(self.screen, (70, 170, 255), (int(game.player.x), int(game.player.y)), game.player.radius)
            pygame.draw.circle(self.screen, (205, 235, 255), (int(game.player.x), int(game.player.y)), game.player.radius, 3)

        for p in game.death_particles:
            alpha_ratio = max(0.0, p["life"] / p["max_life"])
            radius = max(1, int(p["size"] * alpha_ratio))
            pygame.draw.circle(self.screen, p["color"], (int(p["x"]), int(p["y"])), radius)

        self.draw_crosshair(game.player)
        self.draw_hud(game)

    def draw_game_over_overlay(self, score):
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 165))
        self.screen.blit(overlay, (0, 0))

        title = self.big_font.render("КРИМЗОЛЕНД", True, (255, 80, 80))
        lose = self.font.render("Ты проиграл", True, (245, 245, 245))
        final_score = self.font.render(f"Финальный счёт: {score}", True, (245, 245, 245))
        hint = self.small_font.render("ESC - меню", True, (220, 220, 220))

        sw = self.screen.get_width()
        sh = self.screen.get_height()
        self.screen.blit(title, (sw // 2 - title.get_width() // 2, sh // 2 - 90))
        self.screen.blit(lose, (sw // 2 - lose.get_width() // 2, sh // 2 - 20))
        self.screen.blit(final_score, (sw // 2 - final_score.get_width() // 2, sh // 2 + 18))
        self.screen.blit(hint, (sw // 2 - hint.get_width() // 2, sh // 2 + 58))

    def draw_name_entry(self, game):
        self.draw_playing(game)
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 180))
        self.screen.blit(overlay, (0, 0))

        sw = self.screen.get_width()
        sh = self.screen.get_height()

        if game.victory:
            title = self.menu_font.render("ПОБЕДА!", True, (255, 220, 120))
            prompt_text = "Введи имя и нажми Enter:"
        else:
            title = self.menu_font.render("Новый рекорд", True, (255, 220, 120))
            prompt_text = "Введи имя и нажми Enter:"
        score_line = self.font.render(f"Очки: {game.pending_record}", True, (235, 235, 235))
        prompt = self.font.render(prompt_text, True, (235, 235, 235))
        name_value = self.font.render(game.name_input + "_", True, (120, 255, 170))
        hint = self.small_font.render("Backspace - удалить | ESC - пропустить", True, (200, 200, 200))

        self.screen.blit(title, (sw // 2 - title.get_width() // 2, sh // 2 - 120))
        self.screen.blit(score_line, (sw // 2 - score_line.get_width() // 2, sh // 2 - 70))
        self.screen.blit(prompt, (sw // 2 - prompt.get_width() // 2, sh // 2 - 20))
        self.screen.blit(name_value, (sw // 2 - name_value.get_width() // 2, sh // 2 + 22))
        self.screen.blit(hint, (sw // 2 - hint.get_width() // 2, sh // 2 + 65))

    def draw_menu(self, menu_selected):
        self.screen.fill((0, 0, 0))
        title = self.big_font.render("КРИМЗОЛЕНД", True, (255, 80, 80))
        options = ["Начать игру", "Рекорды", "Выход"]
        colors = [(255, 255, 255) if i != menu_selected else (255, 255, 0) for i in range(3)]

        self.screen.blit(title, (self.screen.get_width() // 2 - title.get_width() // 2, 100))
        for i, opt in enumerate(options):
            text = self.menu_font.render(f"{i + 1}. {opt}", True, colors[i])
            self.screen.blit(text, (self.screen.get_width() // 2 - text.get_width() // 2, 250 + i * 50))

    def draw_highscores(self, highscores):
        self.screen.fill((0, 0, 0))
        title = self.big_font.render("ТАБЛИЦА РЕКОРДОВ", True, (255, 80, 80))
        back = self.small_font.render("ESC - назад", True, (200, 200, 200))

        sw = self.screen.get_width()
        self.screen.blit(title, (sw // 2 - title.get_width() // 2, 60))
        self.screen.blit(back, (40, 40))

        header = self.small_font.render("МЕСТО   ИГРОК             ОЧКИ     ДАТА         ВРЕМЯ", True, (150, 210, 255))
        self.screen.blit(header, (sw // 2 - header.get_width() // 2, 165))

        if not highscores:
            empty = self.font.render("Рекордов пока нет", True, (230, 230, 230))
            self.screen.blit(empty, (sw // 2 - empty.get_width() // 2, 250))
            return

        for i, rec in enumerate(highscores[:10]):
            color = (255, 220, 120) if i == 0 else (235, 235, 235)
            line = self.small_font.render(
                f"{i + 1:>2}      {rec['name']:<20} {rec['score']:>6}   {rec['date']:<10}   {rec['time']}",
                True,
                color,
            )
            self.screen.blit(line, (sw // 2 - line.get_width() // 2, 200 + i * 28))

    def draw_pause(self, game, pause_selected):
        self.draw_playing(game)
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((0, 0, 0, 150))
        self.screen.blit(overlay, (0, 0))

        title = self.big_font.render("ПАУЗА", True, (255, 80, 80))
        options = ["Продолжить", "Выйти в меню"]
        colors = [(255, 255, 255) if i != pause_selected else (255, 255, 0) for i in range(2)]

        sw = self.screen.get_width()
        sh = self.screen.get_height()
        self.screen.blit(title, (sw // 2 - title.get_width() // 2, sh // 2 - 100))
        for i, opt in enumerate(options):
            text = self.menu_font.render(opt, True, colors[i])
            self.screen.blit(text, (sw // 2 - text.get_width() // 2, sh // 2 - 20 + i * 50))
