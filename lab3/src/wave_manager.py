import random
from dataclasses import dataclass

from .constants import ENEMY_TYPES
from .waves_config import WAVE_CONFIG


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
        self.wave_pause_timer = self.config.wave_pause
        self.wave_queue = []
        self.wave_banner_timer = 0.0
        self.spawn_timer = 0.0
        self.spawn_interval = self.config.get_wave(self.current_wave).spawn_interval
        self.difficulty = self.config.get_wave(self.current_wave).difficulty

    def choose_enemy_type(self, wave):
        wave_config = self.config.get_wave(wave)
        enemy_pool = [
            enemy_type
            for enemy_type, count in wave_config.enemy_counts.items()
            for _ in range(count)
            if enemy_type != "boss"
        ]
        return random.choice(enemy_pool) if enemy_pool else "grunt"

    def build_wave_queue(self, wave):
        wave_config = self.config.get_wave(wave)
        queue = []
        for enemy_type, count in wave_config.enemy_counts.items():
            if enemy_type not in ENEMY_TYPES:
                raise ValueError(f"Unknown enemy type in wave config: {enemy_type}")
            queue.extend([enemy_type] * count)

        if wave_config.shuffle:
            random.shuffle(queue)
        return queue

    def start_wave(self, wave):
        wave_config = self.config.get_wave(wave)
        self.wave_queue = self.build_wave_queue(wave)
        self.wave_active = True
        self.wave_pause_timer = 0.0
        self.wave_banner_timer = self.config.banner_duration
        self.spawn_timer = 0.0
        self.difficulty = wave_config.difficulty
        self.spawn_interval = wave_config.spawn_interval

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
        return self.config.is_boss_wave(self.current_wave)

    def is_boss_wave_number(self, wave_number):
        return self.config.is_boss_wave(wave_number)

    def pending_count(self, alive_enemies):
        return len(self.wave_queue) + alive_enemies
