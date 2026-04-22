class HealthPickup:
    def __init__(self, x, y, heal_amount, radius, lifetime):
        self.x = x
        self.y = y
        self.heal_amount = int(heal_amount)
        self.radius = int(radius)
        self.lifetime = float(lifetime)
        self.alive = True

    def update(self, dt):
        if not self.alive:
            return
        self.lifetime -= dt
        if self.lifetime <= 0:
            self.alive = False
