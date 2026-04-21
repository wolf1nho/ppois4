from .constants import BULLET_RADIUS


class Bullet:
    def __init__(
        self,
        x,
        y,
        vx,
        vy,
        screen,
        damage=10,
        radius=BULLET_RADIUS,
        is_enemy=False,
        color=None,
    ):
        self.screen = screen
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy
        self.alive = True
        self.damage = damage
        self.radius = radius
        self.is_enemy = is_enemy
        self.color = color if color is not None else ((255, 120, 120) if is_enemy else (255, 240, 170))

    def update(self, dt):
        self.x += self.vx * dt
        self.y += self.vy * dt
        sw = self.screen.get_width()
        sh = self.screen.get_height()
        if self.x < -self.radius or self.x > sw + self.radius:
            self.alive = False
        if self.y < -self.radius or self.y > sh + self.radius:
            self.alive = False
