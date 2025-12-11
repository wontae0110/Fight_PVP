import pygame as pg
import time
from .Particle import Particle
from Tool import secondToTick


class HealParticle(Particle):
    def __init__(self, position: pg.Vector2):
        super().__init__(position)
        self.init_duration = secondToTick(2)  # 2초 후 사라짐
        self.duration = self.init_duration

        self.alpha = 255

        # 십자 모양 Surface 생성
        self.surface = pg.Surface((20, 20), pg.SRCALPHA)

    def draw(self):
        from map.init_setting import screen
        self.surface.fill((0, 0, 0, 0))  # 이전 프레임 지우기

        # 점점 사라지는 알파 값 (2초 동안 255 → 0)
        self.alpha = max(0, int(255 * (self.duration / self.init_duration)))

        # 십자 그리기 (두 직선을 겹쳐 십자 모양)
        pg.draw.line(self.surface, (0, 140, 40, self.alpha),
                    (10, 0), (10, 20), 3)
        pg.draw.line(self.surface, (0, 140, 40, self.alpha),
                    (0, 10), (20, 10), 3)

        screen.blit(self.surface, (self.position.x - 10, self.position.y - 10))