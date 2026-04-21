import math

WIDTH, HEIGHT = 960, 640
FPS = 60
TIME_SCALE = 0.78

PLAYER_SPEED = 280
PLAYER_RADIUS = 26
BULLET_SPEED = 560
BULLET_RADIUS = 6
ENEMY_BASE_SPEED = 120
ENEMY_RADIUS = 18
SPAWN_INTERVAL_START = 1.5
TOTAL_WAVES = 25

MAX_HP = 100
HIGHSCORE_FILE = "highscore.json"

# Enemy balance
ENEMY_SHOOT_DISTANCE = 500
ENEMY_BULLET_SPEED = 280
ENEMY_BULLET_RADIUS = 7

ENEMY_TYPES = {
    "grunt": {
        "name": "Обычный",
        "hp": 20,
        "radius": 22,
        "speed_mult": 0.78,
        "score": 12,
        "contact_damage": 14,
        "can_shoot": False,
        "shoot_interval": 0.0,
        "bullet_damage": 0,
        "color_fill": (205, 52, 52),
        "color_outline": (255, 110, 110),
    },
    "tank": {
        "name": "Танк",
        "hp": 70,
        "radius": 30,
        "speed_mult": 0.5,
        "score": 36,
        "contact_damage": 28,
        "can_shoot": False,
        "shoot_interval": 0.0,
        "bullet_damage": 0,
        "color_fill": (132, 42, 24),
        "color_outline": (215, 98, 60),
    },
    "swift": {
        "name": "Быстрый",
        "hp": 12,
        "radius": 18,
        "speed_mult": 1.25,
        "score": 16,
        "contact_damage": 10,
        "can_shoot": False,
        "shoot_interval": 0.0,
        "bullet_damage": 0,
        "color_fill": (124, 52, 205),
        "color_outline": (188, 146, 255),
    },
    "shooter": {
        "name": "Стрелок",
        "hp": 24,
        "radius": 24,
        "speed_mult": 0.68,
        "score": 28,
        "contact_damage": 12,
        "can_shoot": True,
        "shoot_interval": 1.8,
        "bullet_damage": 12,
        "color_fill": (42, 104, 192),
        "color_outline": (122, 186, 255),
    },
    "boss": {
        "name": "Босс",
        "hp": 420,
        "radius": 48,
        "speed_mult": 0.46,
        "score": 300,
        "contact_damage": 45,
        "can_shoot": True,
        "shoot_interval": 1.2,
        "bullet_damage": 20,
        "color_fill": (86, 20, 20),
        "color_outline": (255, 205, 70),
    },
}

# Weapon types
WEAPON_PISTOL = 0
WEAPON_SHOTGUN = 1
WEAPON_SNIPER = 2
WEAPON_AUTOMATIC = 3

# Weapon stats
WEAPONS = {
    WEAPON_PISTOL: {'name': 'Пистолет', 'reload_time': 0.12, 'damage': 10},
    WEAPON_SHOTGUN: {'name': 'Дробовик', 'reload_time': 0.5, 'damage': 5, 'pellets': 5, 'spread': 0.3},
    WEAPON_SNIPER: {'name': 'Снайперка', 'reload_time': 1.0, 'damage': 50, 'speed': 1000, 'radius': 6},
    WEAPON_AUTOMATIC: {'name': 'Автомат', 'reload_time': 0.05, 'damage': 7},
}
