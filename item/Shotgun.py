from .Gun import Gun
import pygame as pg
from entity.Bullet import Bullet
from Tool import secondToTick

class Shotgun(Gun):
    def __init__(self, image, position: pg.Vector2):
        super().__init__(image, position, size=(100, 100), bullet_speed=15)
        self.init_attack_cooltime = secondToTick(1) # 샷건의 공격 속도 설정 (발사 간격)

    def shoot(self, shooter):
        if self.cur_attack_cooltime > 0:
            return  # 아직 쿨타임이 남아있으면 발사하지 않음
        self.cur_attack_cooltime = self.init_attack_cooltime  # 쿨타임 초기화

        from map.CreateMap import bullets
        for angle_offset in [-10, 5, 0, 5, 10]:  # 다섯 발의 총알을 약간씩 다른 각도로 발사
            image = pg.image.load("./assets/bullet.png").convert_alpha()
            image = pg.transform.rotate(image, -(self.angle + angle_offset))
            # 총알 생성
            bullets.add(Bullet(image, self.position, (20, 20), pg.Vector2(0, self.bullet_speed).rotate(self.angle + angle_offset), shooter, 5, -0.1)) # 총알 생성