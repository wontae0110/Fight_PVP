import pygame as pg
from .Entity import Entity
from .Character import Character

class Mine_entity(Entity):
    def __init__(self, position: pg.Vector2, size: int, user: Character):
        #image = pg.image.load("./assets/mine.png").convert_alpha()
        # 단순한 도형(붉은 원)으로 지뢰 이미지 대체
        image = pg.Surface((size, size), pg.SRCALPHA)
        pg.draw.circle(image, (200, 30, 30), (size // 2, size // 2), size // 2)
        pg.draw.circle(image, (0, 0, 0), (size // 2, size // 2), size // 2, 2)  # 테두리
        super().__init__(image, position, size)
        self.damage = 10  # 지뢰의 데미지 설정
        self.user = user  # 지뢰를 설치한 플레이어
            
    def isCollide(self, move: pg.Vector2): # 충돌 여부 확인
        # 충돌 여부를 확인하기 위해 임시로 rect를 복사
        temp_rect = self.rect.copy()
        temp_rect.x += int(move.x)
        temp_rect.y += int(move.y)

        from map.init_setting import screen_width, screen_height, screen
        from map.CreateMap import players, grounds, bullets
        #if temp_rect.left < 0 or temp_rect.right > screen_width or temp_rect.top < 0 or temp_rect.bottom > screen_height: # 화면 밖으로 나가는지 확인
        #    return True
        old_rect = temp_rect.copy()
        temp_rect.clamp_ip(screen.get_rect())

        if temp_rect.topleft != old_rect.topleft:
            return True

        
        for p in players: # 플레이어와 충돌 체크
            if p != self.user and temp_rect.colliderect(p.rect):
                p.damage(self.damage)  # 플레이어에게 피해 주기
                self.kill()  # 지뢰 제거
                return True
        for g in grounds:
            if temp_rect.colliderect(g.rect):
                return True
            
        return False