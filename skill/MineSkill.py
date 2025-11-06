from .Skill import Skill
from entity import Character
import pygame as pg
from entity.Mine_entity import Mine_entity
from Tool import secondToTick

class MineSkill(Skill):
    def __init__(self):
        super().__init__()
        self.init_cooltime = secondToTick(3)
        self.cooltime = 0

    def use(self, user: Character):
        if self.cooltime > 0:
            return  # 쿨타임이 남아있으면 스킬 사용 불가
        self.cooltime = self.init_cooltime  # 쿨타임 초기화

        from map.CreateMap import mines
        mines.add(Mine_entity(user.position, size=10, user=user))  # 지뢰 생성 및 추가