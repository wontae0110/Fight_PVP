import pygame as pg
from .Gun import Gun
from entity.Bullet import Bullet
from Tool import secondToTick

class Pistol(Gun):
    def __init__(self, image, position: pg.Vector2):
        super().__init__(image, position, size=(80, 80), bullet_speed=20)
        self.init_attack_cooltime = secondToTick(0.2) # 권총의 공격 속도 설정 (발사 간격)

    def shoot(self, shooter):
        if self.cur_attack_cooltime > 0:
            return  # 아직 쿨타임이 남아있으면 발사하지 않음
        self.cur_attack_cooltime = self.init_attack_cooltime  # 쿨타임 초기화

        image = pg.image.load("./assets/bullet.png").convert_alpha()
        image = pg.transform.rotate(image, -self.angle)
        # 총알 생성
        from map.CreateMap import bullets
        bullets.add(Bullet(image, self.position, (20, 20), pg.Vector2(0, self.bullet_speed).rotate(self.angle), shooter, 2)) # 총알 생성