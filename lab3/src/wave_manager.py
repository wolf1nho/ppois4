import random
from dataclasses import dataclass

from .constants import WAVE_CONFIG


@dataclass
class WaveTickResult:
    spawn_types: list[str]
    wave_started: bool
    wave_completed: bool
    victory: bool


class WaveManager:
    def __init__(self, config=WAVE_CONFIG):
        self.config = config
        self.reset()

    def reset(self):
        self.current_wave = 1
        self.wave_active = False
        self.wave_pause_timer = 0.0
        self.wave_queue = []
        self.wave_banner_timer = self.config.banner_duration
        self.spawn_timer = 0.0
        self.spawn_interval = self.config.spawn_interval_start
        self.difficulty = self.config.difficulty_base
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
        if wave % self.config.boss_every == 0:
            minions_count = self.config.boss_minions_base + wave
            queue = [self.choose_enemy_type(wave) for _ in range(minions_count)]
            queue.append("boss")
            random.shuffle(queue)
            return queue

        enemy_count = self.config.base_enemy_count + wave * self.config.enemy_per_wave_increment
        return [self.choose_enemy_type(wave) for _ in range(enemy_count)]

    def start_wave(self, wave):
        self.wave_queue = self.build_wave_queue(wave)
        self.wave_active = True
        self.wave_pause_timer = 0.0
        self.spawn_timer = 0.0
        self.difficulty = self.config.difficulty_base + (wave - 1) * self.config.difficulty_step
        self.spawn_interval = max(
            self.config.min_spawn_interval,
            self.config.spawn_interval_start - (wave - 1) * self.config.spawn_interval_wave_step,
        )

    def update(self, dt, alive_enemies, alive_enemy_bullets):
        spawn_types = []
        wave_started = False
        wave_completed = False
        victory = False

        if self.wave_active:
            self.spawn_timer += dt
            while self.wave_queue and self.spawn_timer >= self.spawn_interval:
                spawn_types.append(self.wave_queue.pop(0))
                self.spawn_timer -= self.spawn_interval

            if not self.wave_queue and alive_enemies == 0 and alive_enemy_bullets == 0:
                self.wave_active = False
                self.current_wave += 1
                wave_completed = True
                if self.current_wave > self.config.total_waves:
                    victory = True
                else:
                    self.wave_pause_timer = self.config.wave_pause
                    self.wave_banner_timer = self.config.banner_duration
        else:
            if self.wave_pause_timer > 0:
                self.wave_pause_timer -= dt
                if self.wave_pause_timer <= 0:
                    self.start_wave(self.current_wave)
                    wave_started = True

        if self.wave_banner_timer > 0:
            self.wave_banner_timer -= dt

        return WaveTickResult(
            spawn_types=spawn_types,
            wave_started=wave_started,
            wave_completed=wave_completed,
            victory=victory,
        )

    def is_boss_wave(self):
        return self.current_wave <= self.config.total_waves and self.current_wave % self.config.boss_every == 0

    def pending_count(self, alive_enemies):
        return len(self.wave_queue) + alive_enemies
