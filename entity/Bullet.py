import pygame as pg
from .Entity import Entity

class Bullet(Entity):
    def __init__(self, image, position: pg.Vector2, size: tuple, vec: pg.Vector2, shooter, damage: int, damage_increase: int = 0):
        super().__init__(image, position, size)

        self.rect = self.image.get_rect()  # 히트박스(직사각형)
        self.rect.topleft = (self.position.x, self.position.y)  # 직사각형 위치 설정

        self.inclination = vec # 기울기
        self.shooter = shooter

        self.damage_amount = damage # 데미지 양
        self.damage_increase = damage_increase # 데미지 증가량

    def isCollide(self, move: pg.Vector2): # 충돌 여부 확인
        # 충돌 여부를 확인하기 위해 임시로 rect를 복사
        temp_rect = self.rect.copy()
        temp_rect.x += int(move.x)
        temp_rect.y += int(move.y)

        from map.init_setting import screen_width, screen_height
        from map.CreateMap import players, grounds, bullets
        if temp_rect.left < 0 or temp_rect.right > screen_width or temp_rect.top < 0 or temp_rect.bottom > screen_height: # 화면 밖으로 나가는지 확인
            self.kill()
            return True
        
        for p in players: # 플레이어와 충돌 체크
            if p == self.shooter:
                continue
            #한 플레이어 여러번 맞기 방지 제작!!!
            if p.rect.colliderect(temp_rect):
                p.damage(self.damage_amount)  # 플레이어에게 피해 주기
                self.kill()
                return True
        
        for g in grounds:
            if temp_rect.colliderect(g.rect):
                self.kill()
                return True
        for b in bullets:
            if b != self and b.shooter != self.shooter and temp_rect.colliderect(b.rect):
                self.kill()
                b.kill()
                return True
            
        return False
        
    def update(self):
        self.move(self.inclination)  # 총알 이동
        if (self.damage_amount + self.damage_increase >= 0):
            self.damage_amount += self.damage_increase  # 데미지 증가