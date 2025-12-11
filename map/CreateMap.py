import pygame as pg
from entity import Character
import os
import random
from block import Ground
import csv
from item.Pistol import Pistol

player1 = None
player2 = None
players = None
grounds = None
guns = None
bullets = None
mines = None
WHITE = (255, 255, 255)  # 흰색 배경
background_image = None
particles = None

def createMap():
    from Select_feature import player1_gun, player2_gun, player1_skill, player2_skill
    from .init_setting import tile_size, screen, screen_width, screen_height
    from Select_map import selected_map
    global player1, player2, players, guns, grounds, bullets, WHITE, background_image, mines, particles


    screen.fill(WHITE) # 배경화면 그리기 (나중에는 이미지 삽입으로 변경)

    #캐릭터 & 오브젝트
    RED = (255, 0, 0) #임시 플레이어 색상 (추후 삭제)
    BLUE = (0, 0, 225) #임시 플레이어 색상 (추후 삭제)
    players = pg.sprite.Group() # 플레이어 그룹
    grounds = pg.sprite.Group() # 바닥 그룹

    selected_file = None
    folder_path = os.path.join(os.path.dirname(__file__)+"/map_list")
    if selected_map == "RANDOM":
        selected_file = os.listdir(folder_path) # 폴더 내 모든 파일 목록 가져오기
        selected_file = [f for f in selected_file if os.path.isdir(os.path.join(folder_path, f))] # 숨김 파일, 폴더 등 제외하고 파일만 필터링
    else:
        selected_file = [os.path.join(folder_path, selected_map)] # 선택된 맵 파일만 리스트에 추가

    # 파일이 있을 때만 랜덤 선택
    if selected_file:
        selected_file = random.choice(selected_file) # 랜덤으로 파일 선택
        map_path = os.path.join(folder_path, selected_file) # 선택된 맵 파일 경로
        data = [] # 맵 데이터 초기화

        with open(map_path+"/map.csv", newline='', encoding='utf-8') as f:
            reader = csv.reader(f)
            for row in reader:
                data.append(row)  # 각 행을 리스트로 추가

        background_image = pg.image.load(map_path+"/background.png").convert() # 배경 이미지 불러오기
        screen.blit(background_image, (0, 0)) # 배경화면 그리기 (나중에는 이미지 삽입으로 변경)

        # 맵 생성
        for y in range(len(data)):
            for x in range(len(data[y])):
                if data[y][x] == 'P1':
                    image = pg.image.load("./assets/player1.png").convert_alpha()
                    
                    player1 = Character(1, image, pg.Vector2(x*tile_size, y*tile_size), (50, 50), [pg.K_a, pg.K_d, pg.K_w, pg.K_s, pg.K_q])
                elif data[y][x] == 'P2':
                    image = pg.image.load("./assets/player2.png").convert_alpha()

                    player2 = Character(2, image, pg.Vector2(x*tile_size, y*tile_size), (50, 50), [pg.K_j, pg.K_l, pg.K_i, pg.K_k, pg.K_o])
                elif data[y][x] == 'Gm':
                    # 임시로 바닥 이미지 생성 (추후에 삭제)
                    image = pg.image.load("./assets/mid_ground.png").convert_alpha()
                    
                    ground = Ground(image, pg.Vector2(x * tile_size, y * tile_size), tile_size)
                    grounds.add(ground)
                elif data[y][x] == 'Gl':
                    image = pg.image.load("./assets/left_ground.png").convert_alpha()
                    
                    ground = Ground(image, pg.Vector2(x * tile_size, y * tile_size), tile_size)
                    grounds.add(ground)
                elif data[y][x] == 'Gr':
                    image = pg.image.load("./assets/right_ground.png").convert_alpha()
                    
                    ground = Ground(image, pg.Vector2(x * tile_size, y * tile_size), tile_size)
                    grounds.add(ground)

        # 플레이어 총 생성
        player1.getGun(player1_gun)  # 플레이어 총 생성
        player2.getGun(player2_gun)  # 플레이어 총 생성
        player1.getSkill(player1_skill)  # 플레이어 스킬 생성
        player2.getSkill(player2_skill)  # 플레이어 스킬 생성
        players.add(player1, player2)

        guns = pg.sprite.Group()  # 총 그룹 생성
        guns.add(player1.gun, player2.gun)  # 총을 그룹에 추가
        
        bullets = pg.sprite.Group()  # 총알 그룹 생성
        mines = pg.sprite.Group()  # 지뢰 그룹 생성

        particles = []  # 효과 리스트 초기화
    else:
        print("폴더에 맵이 없습니다")
