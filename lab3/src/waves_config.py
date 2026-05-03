from dataclasses import dataclass


@dataclass(frozen=True)
class WaveDefinition:
    enemy_counts: dict[str, int]
    difficulty: float
    spawn_interval: float
    boss_wave: bool = False
    shuffle: bool = True


@dataclass(frozen=True)
class WavesConfig:
    waves: tuple[WaveDefinition, ...]
    wave_pause: float = 2.4
    banner_duration: float = 2.2

    @property
    def total_waves(self) -> int:
        return len(self.waves)

    def get_wave(self, wave_number: int) -> WaveDefinition:
        return self.waves[wave_number - 1]

    def is_boss_wave(self, wave_number: int) -> bool:
        return 1 <= wave_number <= self.total_waves and self.get_wave(wave_number).boss_wave


WAVE_CONFIG = WavesConfig(
    waves=(
        WaveDefinition(enemy_counts={"grunt": 10, "swift": 2}, difficulty=1.25, spawn_interval=1.00),
        WaveDefinition(enemy_counts={"grunt": 14, "swift": 3}, difficulty=1.31, spawn_interval=0.97),
        WaveDefinition(enemy_counts={"grunt": 17, "swift": 5}, difficulty=1.37, spawn_interval=0.94),
        WaveDefinition(enemy_counts={"grunt": 21, "swift": 6}, difficulty=1.43, spawn_interval=0.91),
        WaveDefinition(
            enemy_counts={"grunt": 4, "swift": 3, "tank": 2, "shooter": 1, "boss": 1},
            difficulty=1.49,
            spawn_interval=0.88,
            boss_wave=True,
        ),
        WaveDefinition(
            enemy_counts={"grunt": 17, "swift": 10, "tank": 7, "shooter": 3},
            difficulty=1.55,
            spawn_interval=0.85,
        ),
        WaveDefinition(
            enemy_counts={"grunt": 19, "swift": 11, "tank": 8, "shooter": 4},
            difficulty=1.61,
            spawn_interval=0.82,
        ),
        WaveDefinition(
            enemy_counts={"grunt": 21, "swift": 13, "tank": 8, "shooter": 5},
            difficulty=1.67,
            spawn_interval=0.79,
        ),
        WaveDefinition(
            enemy_counts={"grunt": 23, "swift": 14, "tank": 10, "shooter": 5},
            difficulty=1.73,
            spawn_interval=0.76,
        ),
        WaveDefinition(
            enemy_counts={"grunt": 5, "swift": 3, "tank": 4, "shooter": 3, "boss": 1},
            difficulty=1.79,
            spawn_interval=0.73,
            boss_wave=True,
        ),
        WaveDefinition(
            enemy_counts={"grunt": 20, "swift": 14, "tank": 14, "shooter": 14},
            difficulty=1.85,
            spawn_interval=0.70,
        ),
        WaveDefinition(
            enemy_counts={"grunt": 21, "swift": 15, "tank": 15, "shooter": 16},
            difficulty=1.91,
            spawn_interval=0.67,
        ),
        WaveDefinition(
            enemy_counts={"grunt": 23, "swift": 16, "tank": 17, "shooter": 16},
            difficulty=1.97,
            spawn_interval=0.64,
        ),
        WaveDefinition(
            enemy_counts={"grunt": 25, "swift": 17, "tank": 18, "shooter": 17},
            difficulty=2.03,
            spawn_interval=0.61,
        ),
        WaveDefinition(
            enemy_counts={"grunt": 6, "swift": 4, "tank": 5, "shooter": 5, "boss": 1},
            difficulty=2.09,
            spawn_interval=0.58,
            boss_wave=True,
        ),
    )
)
