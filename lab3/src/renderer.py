import math
import os

import pygame

from .constants import ENEMY_TYPES, MAX_HP, UI_CONFIG, WEAPONS


class GameRenderer:
    def __init__(self, screen):
        self.screen = screen
        self.font = pygame.font.SysFont("consolas", 24)
        self.big_font = pygame.font.SysFont("consolas", 52)
        self.menu_font = pygame.font.SysFont("consolas", 36)
        self.small_font = pygame.font.SysFont("consolas", 18)
        self.weapon_slot_font = pygame.font.SysFont("consolas", 16)
        self.weapon_images = self.load_weapon_images()
        self.enemy_images = self.load_enemy_images()
        self.enemy_sprite_cache = {}
        self.surface_cache = {}

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

    def load_enemy_images(self):
        base_dir = os.path.dirname(os.path.dirname(__file__))
        loaded = {}
        for enemy_type, stats in ENEMY_TYPES.items():
            if not stats.image_path:
                loaded[enemy_type] = None
                continue
            try:
                loaded[enemy_type] = pygame.image.load(os.path.join(base_dir, stats.image_path)).convert_alpha()
            except Exception:
                loaded[enemy_type] = None
        return loaded

    def draw_enemy(self, enemy):
        enemy_image = self.enemy_images.get(enemy.enemy_type)
        cx = int(enemy.x)
        cy = int(enemy.y)

        if enemy_image is not None:
            cache_key = (enemy.enemy_type, enemy.radius)
            sprite_surface = self.enemy_sprite_cache.get(cache_key)
            if sprite_surface is None:
                diameter = max(2, enemy.radius * 2)
                scaled = pygame.transform.smoothscale(enemy_image, (diameter, diameter))
                sprite_surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
                sprite_surface.blit(scaled, (0, 0))

                mask_surface = pygame.Surface((diameter, diameter), pygame.SRCALPHA)
                pygame.draw.circle(mask_surface, (255, 255, 255, 255), (enemy.radius, enemy.radius), enemy.radius)
                sprite_surface.blit(mask_surface, (0, 0), special_flags=pygame.BLEND_RGBA_MULT)
                self.enemy_sprite_cache[cache_key] = sprite_surface
            self.screen.blit(sprite_surface, (cx - enemy.radius, cy - enemy.radius))
            pygame.draw.circle(self.screen, enemy.color_outline, (cx, cy), enemy.radius, 2)
            return

        pygame.draw.circle(self.screen, enemy.color_fill, (cx, cy), enemy.radius)
        pygame.draw.circle(self.screen, enemy.color_outline, (cx, cy), enemy.radius, 2)

    def draw_background(self):
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        self.screen.fill((14, 10, 16))
        for y in range(0, sh, 34):
            pygame.draw.line(self.screen, (34, 26, 42), (0, y), (sw, y), 1)
        for x in range(0, sw, 34):
            pygame.draw.line(self.screen, (34, 26, 42), (x, 0), (x, sh), 1)

    def _get_cached_surface(self, key, width, height, draw_fn):
        cached = self.surface_cache.get(key)
        if cached is not None:
            return cached
        surface = pygame.Surface((width, height), pygame.SRCALPHA)
        draw_fn(surface)
        self.surface_cache[key] = surface
        return surface

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
        current_display_wave = game.displayed_wave()
        wave_text = self.font.render(f"Волна: {current_display_wave}/{total_waves}", True, (245, 220, 140))
        switch_text = self.small_font.render("Q/E или 1-3 - смена", True, (200, 200, 200))
        pending = game.wave_manager.pending_count(len(game.enemies))
        left_text = self.small_font.render(f"Осталось на волне: {pending}", True, (200, 220, 255))
        is_boss_display_wave = game.wave_manager.config.is_boss_wave(current_display_wave)
        boss_text = self.small_font.render("Волна босса", True, (255, 205, 120)) if is_boss_display_wave else None

        left = UI_CONFIG.hud_left
        top = UI_CONFIG.hud_top
        step = 24
        info_lines = [score_text, time_text, wave_text, switch_text, left_text]
        if boss_text is not None:
            info_lines.append(boss_text)

        info_height = 20 + step * len(info_lines)
        max_width = max(line.get_width() for line in info_lines) + 24
        info_surface = self._get_cached_surface(
            ("hud_info_bg", max_width, info_height),
            max_width,
            info_height,
            lambda s: (
                pygame.draw.rect(s, (12, 14, 18, 88), (0, 0, max_width, info_height), border_radius=12),
                pygame.draw.rect(s, (70, 82, 98, 135), (0, 0, max_width, info_height), 1, border_radius=12),
            ),
        )
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
            banner_surface = self._get_cached_surface(
                ("wave_banner_bg", bw, bh, int(170 * alpha)),
                bw,
                bh,
                lambda s: s.fill((20, 20, 20, int(170 * alpha))),
            )
            self.screen.blit(banner_surface, (self.screen.get_width() // 2 - bw // 2, UI_CONFIG.wave_banner_top))
            banner_color = (255, 220, 120) if game.wave_manager.is_boss_wave() else (220, 220, 220)
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
            self.draw_enemy(enemy)
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

    def draw_name_entry(self, game):
        self.draw_playing(game)
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        overlay = pygame.Surface((sw, sh), pygame.SRCALPHA)
        overlay.fill((8, 12, 18, 190))
        self.screen.blit(overlay, (0, 0))

        if game.victory:
            title_text = "ПОБЕДА"
            title_color = (255, 220, 120)
            border_color = (230, 196, 110)
            accent_bg = (60, 76, 44, 220)
        else:
            title_text = "ПОРАЖЕНИЕ"
            title_color = (255, 130, 105)
            border_color = (185, 118, 104)
            accent_bg = (72, 44, 44, 220)

        panel_w = min(680, max(430, int(sw * 0.52)))
        panel_h = 340
        panel_x = sw // 2 - panel_w // 2
        panel_y = sh // 2 - panel_h // 2

        panel = self._get_cached_surface(
            ("name_entry_panel", panel_w, panel_h, border_color),
            panel_w,
            panel_h,
            lambda s: (
                pygame.draw.rect(s, (24, 34, 46, 230), (0, 0, panel_w, panel_h), border_radius=16),
                pygame.draw.rect(s, (*border_color, 235), (0, 0, panel_w, panel_h), 3, border_radius=16),
            ),
        )
        self.screen.blit(panel, (panel_x, panel_y))

        title = self.big_font.render(title_text, True, title_color)
        self.screen.blit(title, (sw // 2 - title.get_width() // 2, panel_y + 24))

        score_box_w = panel_w - 120
        score_box_h = 66
        score_box_x = sw // 2 - score_box_w // 2
        score_box_y = panel_y + 120
        score_box = self._get_cached_surface(
            ("name_entry_score_box", score_box_w, score_box_h, accent_bg, border_color),
            score_box_w,
            score_box_h,
            lambda s: (
                pygame.draw.rect(s, accent_bg, (0, 0, score_box_w, score_box_h), border_radius=12),
                pygame.draw.rect(s, (*border_color, 235), (0, 0, score_box_w, score_box_h), 2, border_radius=12),
            ),
        )
        self.screen.blit(score_box, (score_box_x, score_box_y))

        score_label = self.small_font.render("ТВОЙ СЧЕТ", True, (214, 232, 255))
        score_value = self.menu_font.render(str(game.pending_record), True, (245, 245, 245))
        self.screen.blit(score_label, (sw // 2 - score_label.get_width() // 2, score_box_y + 8))
        self.screen.blit(score_value, (sw // 2 - score_value.get_width() // 2, score_box_y + 26))

        prompt = self.small_font.render("Введите имя", True, (214, 232, 255))
        self.screen.blit(prompt, (sw // 2 - prompt.get_width() // 2, panel_y + 202))

        input_box_w = panel_w - 120
        input_box_h = 54
        input_box_x = sw // 2 - input_box_w // 2
        input_box_y = panel_y + 226
        input_box = self._get_cached_surface(
            ("name_entry_input_box", input_box_w, input_box_h),
            input_box_w,
            input_box_h,
            lambda s: (
                pygame.draw.rect(s, (44, 64, 88, 220), (0, 0, input_box_w, input_box_h), border_radius=10),
                pygame.draw.rect(s, (120, 150, 185, 235), (0, 0, input_box_w, input_box_h), 2, border_radius=10),
            ),
        )
        self.screen.blit(input_box, (input_box_x, input_box_y))

        typed_name = (game.name_input if game.name_input else "Игрок") + "_"
        name_value = self.font.render(typed_name, True, (180, 255, 210))
        self.screen.blit(name_value, (input_box_x + 18, input_box_y + 15))

    def draw_menu(self, menu_selected):
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        # Layered background so menu looks like a dedicated screen.
        self.screen.fill((10, 14, 20))
        for y in range(0, sh, 40):
            alpha = 25 + (y % 80)
            band = pygame.Surface((sw, 28), pygame.SRCALPHA)
            band.fill((24, 34, 48, alpha))
            self.screen.blit(band, (0, y))

        title = self.big_font.render("КРИМЗОЛЕНД", True, (255, 120, 95))
        self.screen.blit(title, (sw // 2 - title.get_width() // 2, sh // 2 - 220))

        options = self.get_menu_options()
        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(self.get_menu_button_rects()):
            hovered = rect.collidepoint(mouse_pos)
            active = i == menu_selected

            base_color = (24, 34, 46)
            fill_color = (54, 76, 102) if hovered else base_color
            if active:
                fill_color = (86, 112, 142)

            border_color = (230, 196, 110) if active else ((120, 150, 185) if hovered else (86, 108, 132))
            text_color = (255, 240, 190) if active else ((240, 246, 255) if hovered else (214, 226, 240))

            card = self._get_cached_surface(
                ("menu_card", rect.width, rect.height, fill_color, border_color),
                rect.width,
                rect.height,
                lambda s: (
                    pygame.draw.rect(s, (*fill_color, 220), (0, 0, rect.width, rect.height), border_radius=14),
                    pygame.draw.rect(s, (*border_color, 235), (0, 0, rect.width, rect.height), 3, border_radius=14),
                ),
            )
            self.screen.blit(card, rect.topleft)

            text = self.menu_font.render(options[i], True, text_color)
            self.screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))

    def get_menu_options(self):
        return ["Начать игру", "Рекорды", "Выход"]

    def get_menu_button_rects(self):
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        button_w = min(520, max(340, int(sw * 0.42)))
        button_h = 74
        gap = 20
        count = len(self.get_menu_options())
        total_h = count * button_h + (count - 1) * gap
        start_y = sh // 2 - total_h // 2 - 8
        start_x = sw // 2 - button_w // 2
        return [pygame.Rect(start_x, start_y + i * (button_h + gap), button_w, button_h) for i in range(count)]

    def draw_highscores(self, highscores):
        sw = self.screen.get_width()
        sh = self.screen.get_height()

        self.screen.fill((10, 14, 20))
        for y in range(0, sh, 40):
            alpha = 25 + (y % 80)
            band = pygame.Surface((sw, 28), pygame.SRCALPHA)
            band.fill((24, 34, 48, alpha))
            self.screen.blit(band, (0, y))

        title = self.big_font.render("ТАБЛИЦА РЕКОРДОВ", True, (255, 120, 95))
        subtitle = self.small_font.render("Лучшие результаты", True, (190, 205, 225))
        self.screen.blit(title, (sw // 2 - title.get_width() // 2, 52))
        self.screen.blit(subtitle, (sw // 2 - subtitle.get_width() // 2, 105))

        panel_w = min(900, max(700, int(sw * 0.72)))
        panel_h = min(470, max(350, int(sh * 0.62)))
        panel_x = sw // 2 - panel_w // 2
        panel_y = sh // 2 - panel_h // 2 + 40

        panel = self._get_cached_surface(
            ("highscores_panel", panel_w, panel_h),
            panel_w,
            panel_h,
            lambda s: (
                pygame.draw.rect(s, (24, 34, 46, 220), (0, 0, panel_w, panel_h), border_radius=16),
                pygame.draw.rect(s, (102, 130, 162, 235), (0, 0, panel_w, panel_h), 3, border_radius=16),
            ),
        )
        self.screen.blit(panel, (panel_x, panel_y))

        inner_x = panel_x + 24
        header_y = panel_y + 20
        row_w = panel_w - 48
        col_place = inner_x + 12
        col_name = inner_x + 92
        right_pad = 14
        col_time_right = inner_x + row_w - right_pad
        col_date_right = col_time_right - 110
        col_score_right = col_date_right - 125

        header_bg = self._get_cached_surface(
            ("highscores_header_bg", row_w),
            row_w,
            40,
            lambda s: (
                pygame.draw.rect(s, (44, 64, 88, 210), (0, 0, row_w, 40), border_radius=10),
                pygame.draw.rect(s, (120, 150, 185, 235), (0, 0, row_w, 40), 2, border_radius=10),
            ),
        )
        self.screen.blit(header_bg, (inner_x, header_y))

        header_color = (214, 232, 255)
        self.screen.blit(self.small_font.render("МЕСТО", True, header_color), (col_place, header_y + 10))
        self.screen.blit(self.small_font.render("ИГРОК", True, header_color), (col_name, header_y + 10))
        score_header = self.small_font.render("ОЧКИ", True, header_color)
        date_header = self.small_font.render("ДАТА", True, header_color)
        time_header = self.small_font.render("ВРЕМЯ", True, header_color)
        self.screen.blit(score_header, (col_score_right - score_header.get_width(), header_y + 10))
        self.screen.blit(date_header, (col_date_right - date_header.get_width(), header_y + 10))
        self.screen.blit(time_header, (col_time_right - time_header.get_width(), header_y + 10))

        if not highscores:
            empty = self.font.render("Рекордов пока нет", True, (230, 238, 248))
            self.screen.blit(empty, (sw // 2 - empty.get_width() // 2, panel_y + panel_h // 2 - 12))
            return

        for i, rec in enumerate(highscores[:10]):
            y = header_y + 52 + i * 36
            row_fill = (35, 50, 68, 170) if i % 2 == 0 else (30, 44, 60, 150)
            row = self._get_cached_surface(
                ("highscores_row_bg", row_w, row_fill, i == 0),
                row_w,
                30,
                lambda s: (
                    pygame.draw.rect(s, row_fill, (0, 0, row_w, 30), border_radius=8),
                    pygame.draw.rect(s, (230, 196, 110, 235), (0, 0, row_w, 30), 2, border_radius=8) if i == 0 else None,
                ),
            )
            self.screen.blit(row, (inner_x, y))

            color = (255, 236, 185) if i == 0 else (228, 236, 248)
            place_text = self.small_font.render(str(i + 1), True, color)
            raw_name = str(rec["name"])
            max_name_width = max(40, (col_score_right - 14) - col_name)
            fitted_name = raw_name
            while fitted_name and self.small_font.size(fitted_name)[0] > max_name_width:
                fitted_name = fitted_name[:-1]
            if fitted_name != raw_name and len(fitted_name) > 2:
                fitted_name = fitted_name[:-2] + ".."
            name_text = self.small_font.render(fitted_name, True, color)
            score_text = self.small_font.render(str(rec["score"]), True, color)
            date_text = self.small_font.render(str(rec["date"]), True, color)
            time_text = self.small_font.render(str(rec["time"]), True, color)

            self.screen.blit(place_text, (col_place, y + 7))
            self.screen.blit(name_text, (col_name, y + 7))
            self.screen.blit(score_text, (col_score_right - score_text.get_width(), y + 7))
            self.screen.blit(date_text, (col_date_right - date_text.get_width(), y + 7))
            self.screen.blit(time_text, (col_time_right - time_text.get_width(), y + 7))

    def get_pause_options(self):
        return ["Продолжить", "Выйти в меню"]

    def get_pause_button_rects(self):
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        button_w = min(500, max(320, int(sw * 0.4)))
        button_h = 70
        gap = 18
        count = len(self.get_pause_options())
        total_h = count * button_h + (count - 1) * gap
        start_y = sh // 2 - total_h // 2 + 8
        start_x = sw // 2 - button_w // 2
        return [pygame.Rect(start_x, start_y + i * (button_h + gap), button_w, button_h) for i in range(count)]

    def draw_pause(self, game, pause_selected):
        self.draw_playing(game)
        overlay = pygame.Surface((self.screen.get_width(), self.screen.get_height()), pygame.SRCALPHA)
        overlay.fill((8, 12, 18, 175))
        self.screen.blit(overlay, (0, 0))

        sw = self.screen.get_width()
        sh = self.screen.get_height()
        title = self.big_font.render("ПАУЗА", True, (255, 140, 105))
        self.screen.blit(title, (sw // 2 - title.get_width() // 2, sh // 2 - 170))

        options = self.get_pause_options()
        mouse_pos = pygame.mouse.get_pos()
        for i, rect in enumerate(self.get_pause_button_rects()):
            hovered = rect.collidepoint(mouse_pos)
            active = i == pause_selected

            base_color = (24, 34, 46)
            fill_color = (54, 76, 102) if hovered else base_color
            if active:
                fill_color = (86, 112, 142)

            border_color = (230, 196, 110) if active else ((120, 150, 185) if hovered else (86, 108, 132))
            text_color = (255, 240, 190) if active else ((240, 246, 255) if hovered else (214, 226, 240))

            card = self._get_cached_surface(
                ("pause_card", rect.width, rect.height, fill_color, border_color),
                rect.width,
                rect.height,
                lambda s: (
                    pygame.draw.rect(s, (*fill_color, 225), (0, 0, rect.width, rect.height), border_radius=14),
                    pygame.draw.rect(s, (*border_color, 235), (0, 0, rect.width, rect.height), 3, border_radius=14),
                ),
            )
            self.screen.blit(card, rect.topleft)

            text = self.menu_font.render(options[i], True, text_color)
            self.screen.blit(text, (rect.centerx - text.get_width() // 2, rect.centery - text.get_height() // 2))
