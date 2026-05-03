from dataclasses import dataclass
from enum import Enum, IntEnum

WIDTH, HEIGHT = 960, 640
FPS = 60
TIME_SCALE = 0.78

PLAYER_SPEED = 290
PLAYER_RADIUS = 35
BULLET_SPEED = 700
BULLET_RADIUS = 6

MAX_HP = 100
HIGHSCORE_FILE = "highscore.json"

ENEMY_BASE_SPEED = 180
ENEMY_SHOOT_DISTANCE = 500
ENEMY_BULLET_SPEED = 550
ENEMY_BULLET_RADIUS = 7
ENEMY_BASE_HP = 20
ENEMY_BASE_RADIUS = 25
ENEMY_BASE_SCORE = 20
ENEMY_BASE_CONTACT_DAMAGE = 10
ENEMY_BASE_BULLET_DAMAGE = 10
ENEMY_BASE_SHOOT_INTERVAL = 1.0
ENEMY_SPAWN_SPEED_JITTER_MIN = 0.88
ENEMY_SPAWN_SPEED_JITTER_MAX = 1.12


class GameState(str, Enum):
    MENU = "menu"
    PLAYING = "playing"
    PAUSED = "paused"
    HIGHSCORES = "highscores"
    NAME_ENTRY = "name_entry"


class WeaponType(IntEnum):
    PISTOL = 0
    SHOTGUN = 1
    SNIPER = 2
    AUTOMATIC = 3

WEAPON_PISTOL = WeaponType.PISTOL
WEAPON_SHOTGUN = WeaponType.SHOTGUN
WEAPON_SNIPER = WeaponType.SNIPER
WEAPON_AUTOMATIC = WeaponType.AUTOMATIC


@dataclass(frozen=True)
class EnemyStats:
    name: str
    hp_mult: float
    radius_mult: float
    speed_mult: float
    score_mult: float
    contact_damage_mult: float
    can_shoot: bool
    shoot_interval_mult: float
    bullet_damage_mult: float
    color_fill: tuple[int, int, int]
    color_outline: tuple[int, int, int]
    image_path: str | None = None


@dataclass(frozen=True)
class WeaponStats:
    name: str
    reload_time: float
    damage: int
    bullet_speed: int = BULLET_SPEED
    bullet_radius: int = BULLET_RADIUS
    pellets: int = 1
    spread: float = 0.0
    sound_key: str = "pistol"


@dataclass(frozen=True)
class DeathEffectProfile:
    palette: tuple[tuple[int, int, int], ...]
    particle_count: int
    speed_min: float
    speed_max: float
    life_min: float
    life_max: float
    drag: float


@dataclass(frozen=True)
class UiConfig:
    hp_bar_pos: tuple[int, int] = (16, 12)
    hp_bar_size: tuple[int, int] = (280, 22)
    hud_left: int = 16
    hud_top: int = 42
    hud_line_gap: int = 28
    crosshair_aim_distance: int = 50
    wave_banner_size: tuple[int, int] = (430, 54)
    wave_banner_top: int = 20


@dataclass(frozen=True)
class HealthPickupConfig:
    drop_chance: float = 0.2
    boss_drop_chance: float = 0.85
    heal_amount: int = 20
    radius: int = 14
    lifetime: float = 12.0


UI_CONFIG = UiConfig()
HEALTH_PICKUP_CONFIG = HealthPickupConfig()


def enemy_hp_for(stats: EnemyStats) -> int:
    return max(1, int(round(ENEMY_BASE_HP * stats.hp_mult)))


def enemy_radius_for(stats: EnemyStats) -> int:
    return max(8, int(round(ENEMY_BASE_RADIUS * stats.radius_mult)))


def enemy_score_for(stats: EnemyStats) -> int:
    return max(1, int(round(ENEMY_BASE_SCORE * stats.score_mult)))


def enemy_contact_damage_for(stats: EnemyStats) -> int:
    return max(1, int(round(ENEMY_BASE_CONTACT_DAMAGE * stats.contact_damage_mult)))


def enemy_bullet_damage_for(stats: EnemyStats) -> int:
    if not stats.can_shoot:
        return 0
    return max(1, int(round(ENEMY_BASE_BULLET_DAMAGE * stats.bullet_damage_mult)))


def enemy_shoot_interval_for(stats: EnemyStats) -> float:
    if not stats.can_shoot:
        return 0.0
    return max(0.05, ENEMY_BASE_SHOOT_INTERVAL * stats.shoot_interval_mult)

ENEMY_TYPES = {
    "grunt": EnemyStats(
        name="Обычный",
        hp_mult=1.0,
        radius_mult=1.1,
        speed_mult=0.85,
        score_mult=0.6,
        contact_damage_mult=1.4,
        can_shoot=False,
        shoot_interval_mult=0.0,
        bullet_damage_mult=0.0,
        color_fill=(205, 52, 52),
        color_outline=(255, 110, 110),
        image_path="assets/grunt.jpeg",
    ),
    "tank": EnemyStats(
        name="Танк",
        hp_mult=3.5,
        radius_mult=1.5,
        speed_mult=0.55,
        score_mult=1.8,
        contact_damage_mult=2.8,
        can_shoot=False,
        shoot_interval_mult=0.0,
        bullet_damage_mult=0.0,
        color_fill=(132, 42, 24),
        color_outline=(215, 98, 60),
        image_path="assets/tank.jpeg",
    ),
    "swift": EnemyStats(
        name="Быстрый",
        hp_mult=0.6,
        radius_mult=0.9,
        speed_mult=1.05,
        score_mult=0.8,
        contact_damage_mult=1.0,
        can_shoot=False,
        shoot_interval_mult=0.0,
        bullet_damage_mult=0.0,
        color_fill=(124, 52, 205),
        color_outline=(188, 146, 255),
        image_path="assets/swift.jpeg",
    ),
    "shooter": EnemyStats(
        name="Стрелок",
        hp_mult=1.2,
        radius_mult=1.2,
        speed_mult=0.78,
        score_mult=1.4,
        contact_damage_mult=1.2,
        can_shoot=True,
        shoot_interval_mult=1.2,
        bullet_damage_mult=1.2,
        color_fill=(42, 104, 192),
        color_outline=(122, 186, 255),
        image_path="assets/shooter.jpeg",
    ),
    "boss": EnemyStats(
        name="Босс",
        hp_mult=21.0,
        radius_mult=3.0,
        speed_mult=0.4,
        score_mult=25.0,
        contact_damage_mult=4.5,
        can_shoot=True,
        shoot_interval_mult=0.7,
        bullet_damage_mult=2.0,
        color_fill=(86, 20, 20),
        color_outline=(255, 205, 70),
        image_path="assets/boss.jpeg",
    ),
}

WEAPONS = {
    WeaponType.SHOTGUN: WeaponStats(
        name="Дробовик",
        reload_time=0.7,
        damage=5,
        pellets=5,
        spread=0.3,
        sound_key="shotgun",
    ),
    WeaponType.SNIPER: WeaponStats(
        name="Снайперка",
        reload_time=1.0,
        damage=50,
        bullet_speed=1000,
        bullet_radius=6,
        sound_key="sniper",
    ),
    WeaponType.AUTOMATIC: WeaponStats(name="Автомат", reload_time=0.1, damage=7, sound_key="automatic"),
}

KEY_ALIASES = {
    "left_ru": 1092,
    "right_ru": 1074,
    "up_ru": 1094,
    "down_ru": 1099,
    "q_ru": 1081,
    "e_ru": 1091,
    "r_ru": 1082,
    "1_ascii": 49,
    "2_ascii": 50,
    "3_ascii": 51,
    "4_ascii": 52,
}

DEATH_EFFECTS = {
    "projectile": DeathEffectProfile(
        palette=((255, 180, 140), (255, 90, 90), (255, 220, 120)),
        particle_count=60,
        speed_min=300,
        speed_max=400,
        life_min=0.4,
        life_max=1.0,
        drag=0.96,
    ),
    "tank": DeathEffectProfile(
        palette=((255, 255, 255), (180, 220, 255), (105, 170, 255)),
        particle_count=45,
        speed_min=200,
        speed_max=260,
        life_min=0.35,
        life_max=0.85,
        drag=0.96,
    ),
    "default": DeathEffectProfile(
        palette=((255, 120, 120), (255, 180, 180), (255, 230, 230)),
        particle_count=50,
        speed_min=250,
        speed_max=340,
        life_min=0.35,
        life_max=0.95,
        drag=0.96,
    ),
}
