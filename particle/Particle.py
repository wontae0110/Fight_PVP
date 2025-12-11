import pygame as pg
from abc import ABCMeta, abstractmethod

class Particle(metaclass=ABCMeta):
    def __init__(self, position: pg.Vector2):
        self.position = position
        self.init_duration = 0
        self.duration = 0
        

    @abstractmethod
    def draw(self):
        pass

    def update(self) -> bool: #파티클의 존재여부 반환
        self.duration -= 1

        if self.duration <= 0:
            return False
        
        return True