import pygame as pg
from entity import Entity
from item.Pistol import Pistol
from Tool import secondToTick

class Character(Entity):
    def __init__(self, type:int, image, position: pg.Vector2, size: tuple, move_keys: list):
        super().__init__(image, position, size)
        self.type = type # 캐릭터 타입 (1: 플레이어1, 2: 플레이어2)
        self.move_keys = move_keys # [left, right, jump, shoot]
        self.health = 20 # 체력
        self.gun = None
        self.didAttack = False  # 공격 여부
        self.gun_turn_angle = 0 # 총 회전 각도
        self.jump_first_power = (20) # 점프 초기 힘
        self.jump_power = 0 # 점프 힘
        self.jump_speed = (15) # 점프 속도
        self._prev_jump_key = False # 이전 프레임 점프 키 상태
        self.skill = None # 스킬
        self.original_image = self.image.copy()  # 원본 이미지 저장
        self.damage_effect_time = 0  # 데미지 효과 지속 시간
        self.DAMAGE_EFFECT_DURATION = secondToTick(0.5)  # 데미지 효과 지속 시간 (틱)

    def getSkill(self, skillType: str):
        if skillType == "mine":
            from skill.MineSkill import MineSkill
            self.skill = MineSkill()
        elif skillType == "heal":
            from skill.Heal import Heal
            self.skill = Heal()

    def getGun(self, gunType: str): #image, size: int, bullet_speed: int
        if self.type == 1:
            self.gun_turn_angle = 2
        elif self.type == 2:
            self.gun_turn_angle = -2

        if gunType == "pistol":
            image = None
            if (self.type == 1):
                image = pg.image.load("./assets/right_gun.png").convert_alpha()
                image = pg.transform.rotate(image, -90)
            elif (self.type == 2):
                image = pg.image.load("./assets/left_gun.png").convert_alpha()
                image = pg.transform.rotate(image, 90)
            self.gun = Pistol(image, pg.Vector2((self.rect.left + self.rect.right) / 2, (self.rect.top + self.rect.bottom) / 2)) # 총 생성
        elif gunType == "shotgun":
            image = pg.image.load("./assets/shotgun.png").convert_alpha()
            image = pg.transform.rotate(image, -90)
            if (self.type == 2):
                image = pg.transform.flip(image, True, False)

            from item.Shotgun import Shotgun
            self.gun = Shotgun(image, pg.Vector2((self.rect.left + self.rect.right) / 2, (self.rect.top + self.rect.bottom) / 2)) # 총 생성
        elif gunType == "sniper":
            image = pg.image.load("./assets/sniper.png").convert_alpha()
            image = pg.transform.rotate(image, -90)
            if (self.type == 2):
                image = pg.transform.flip(image, True, False)

            from item.Sniper import Sniper
            self.gun = Sniper(image, pg.Vector2((self.rect.left + self.rect.right) / 2, (self.rect.top + self.rect.bottom) / 2)) # 총 생성

    def setLocation(self, position: pg.Vector2): # 위치 설정
        self.position = position
        self.rect.topleft = (self.position.x, self.position.y)

    def control(self): # 플레이어 조작
        keys = pg.key.get_pressed() # 현재 키 상태 가져오기
        move_dest = pg.Vector2(0, 0) # 이동할 거리 초기화

        if keys[self.move_keys[0]]: # 왼쪽 방향키
            move_dest.x = -self.speed
        if keys[self.move_keys[1]]: # 오른쪽 방향키
            move_dest.x = self.speed
        if keys[self.move_keys[2]] and not self.dropping:
            self.jump_power = self.jump_first_power
            self.dropping = True  # 점프 시 낙하 중으로 설정

        if keys[self.move_keys[3]]: # 공격
            if self.gun and not self.didAttack:
                self.gun.shoot(self)
                self.gun_turn_angle *= -1
                self.didAttack = True
        else:
            self.didAttack = False

        if keys[self.move_keys[4]]: # 스킬 사용
            if self.skill:
                self.skill.use(self)

        return move_dest
    
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
            if p != self and temp_rect.colliderect(p.rect):
                return True
        for g in grounds:
            if temp_rect.colliderect(g.rect):
                return True
            
        return False

    def jump(self): # 점프 error : 더블점프 문제 고치기
        if self.jump_power > 0:
            self.jump_power -= 1
            return pg.Vector2(0, -self.jump_speed)
        return pg.Vector2(0, 0)
    
    def damage(self, damage): # 피해 받기
        self.health -= int(damage)
        # 데미지 효과 시작
        self.damage_effect_time = self.DAMAGE_EFFECT_DURATION
        # 이미지를 빨간색으로 변경
        red_image = self.original_image.copy()
        red_image.fill((255, 0, 0, 128), special_flags=pg.BLEND_RGBA_MULT)
        self.image = red_image
        
        if self.health <= 0:
            self.kill()  # 캐릭터 제거
    
    def heal(self, amount): # 회복
        self.health = min(self.health + int(amount), 20)
    
    def update(self):
        # 이동
        move_dest = pg.Vector2(0, 0)
        self.gravity()
        move_dest += self.control()  # 플레이어 조작
        move_dest += self.jump()  # 점프 조작
        move = self.move(move_dest)
        
        if move.y == 0:  # 천장에 닿았을 때
            self.jump_power = 0

        # 데미지 효과 업데이트
        if self.damage_effect_time > 0:
            self.damage_effect_time -= 1
            if self.damage_effect_time <= 0:
                # 효과 시간이 끝나면 원래 이미지로 복구
                self.image = self.original_image.copy()

        # 총 위치 업데이트
        self.gun.setLocation(pg.Vector2((self.rect.left + self.rect.right) / 2, (self.rect.top + self.rect.bottom) / 2))
        self.gun.turn(self.gun_turn_angle)  # 총 회전
        self.gun.update()  # 총 업데이트
        self.skill.update()  # 스킬 업데이트