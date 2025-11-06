import pygame as pg
from abc import ABCMeta, abstractmethod

class Gun(pg.sprite.Sprite, metaclass=ABCMeta):
    def __init__(self, image, position: pg.Vector2, size: int, bullet_speed: int):
        super().__init__()
        self.image = image # 이미지 설정
        self.image = pg.transform.scale(self.image, (size, size)) # 이미지 크기 조정
        self.position = position # 위치 설정
        self.rect = self.image.get_rect()  # 히트박스(직사각형)
        self.rect.center = position  # 직사각형 위치 설정
        self.isExist = True  # 오브젝트 존재 여부
        self.turnedImage = []
        self.bullet_speed = bullet_speed  # 총알 속도 설정

        self.init_attack_cooltime = 1  # 공격 속도 설정 (발사 간격) (tick 단위)
        self.cur_attack_cooltime = 0  # 현재 공격 쿨타임 (tick 단위)

        for i in range(0, 360):
            rotated_image = pg.transform.rotate(self.image, -i)
            self.turnedImage.append(rotated_image)

        self.angle = 0 # 총의 각도

    def turn(self, angle: int):
        self.angle += angle
        self.angle %= 360

        old_center = self.rect.center  # 회전 전 중심 저장
        self.image = self.turnedImage[self.angle]
        self.rect = self.image.get_rect(center=old_center)

    def setLocation(self, position: pg.Vector2): # 위치 설정
        self.position = position
        self.rect.center = position

    @abstractmethod
    def shoot(self, shooter):
        pass


    def update(self):
        if self.cur_attack_cooltime > 0:
            self.cur_attack_cooltime -= 1