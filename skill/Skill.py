from abc import ABCMeta, abstractmethod

class Skill(metaclass=ABCMeta):
    def __init__(self):
        self.cooltime = 0  # 스킬 쿨타임(tick 단위)
        self.init_cooltime = 0  # 초기 쿨타임 설정(tick 단위)

    @abstractmethod
    def use(self, user): #스킬 사용
        pass

    def update(self):
        if self.cooltime > 0: #쿨타임 감소
            self.cooltime -= 1