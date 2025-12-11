import pygame as pg
from .Gun import Gun
from entity.Bullet import Bullet
from Tool import secondToTick

class Sniper(Gun):
    def __init__(self, image, position: pg.Vector2):
        super().__init__(image, position, size=(90, 90), bullet_speed=60)
        self.init_attack_cooltime = secondToTick(1) #총 발사 쿨타임

    def shoot(self, shooter):
        image = pg.image.load("./assets/bullet.png").convert_alpha()
        image = pg.transform.rotate(image, -self.angle)

        from map.CreateMap import bullets
        bullets.add(Bullet(image, self.position, (20, 20), pg.Vector2(0, self.bullet_speed).rotate(self.angle), shooter, 1, 3))