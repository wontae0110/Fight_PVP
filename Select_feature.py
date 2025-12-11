import pygame as pg
import os
import sys
from Tool import draw_text_with_outline

player1_gun = None
player2_gun = None
player1_skill = None
player2_skill = None

def select_item(title, menu):
    from map.init_setting import screen, screen_height, screen_width
    # 색상
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # 폰트
    font_current = pg.font.SysFont(None, 50)   # 현재 선택지
    font_other = pg.font.SysFont(None, 35)     # 이전/다음 선택지

    current_index = 0
    running = True
    while running:
        background_image = pg.image.load("./assets/setting_background.png").convert()
        screen.blit(background_image, (0, 0)) # 배경화면 그리기

        #제목 표시
        draw_text_with_outline(title, font_current, RED, WHITE, (screen_width // 2, screen_height // 4), screen, 2)
        
        # 표시할 맵 이름
        prev_menu = menu[current_index - 1] if current_index > 0 else ""
        next_manu = menu[current_index + 1] if current_index < len(menu) - 1 else ""
        current_manu = menu[current_index]

        # 이전 맵
        if prev_menu:
            draw_text_with_outline(prev_menu, font_other, BLACK, WHITE, (screen_width // 2, screen_height // 2 - 40), screen, 2)
        
        # 현재 맵
        draw_text_with_outline(current_manu, font_current, RED, WHITE, (screen_width // 2, screen_height // 2), screen, 2)
        
        # 다음 맵
        if next_manu:
            draw_text_with_outline(next_manu, font_other, BLACK, WHITE, (screen_width // 2, screen_height // 2 + 40), screen, 2)

        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
                pg.quit()
                sys.exit()
            elif event.type == pg.KEYDOWN:
                if event.key in [pg.K_w, pg.K_UP]:
                    if current_index > 0:
                        current_index -= 1
                elif event.key in [pg.K_s, pg.K_DOWN]:
                    if current_index < len(menu) - 1:
                        current_index += 1
                elif event.key in [pg.K_SPACE, pg.K_RETURN]:
                    running = False

        pg.display.flip()
    return current_manu

def select_feature():
    from map.init_setting import screen, screen_height, screen_width
    global player1_gun, player2_gun, player1_skill, player2_skill

    # 메뉴 항목
    guns = [
        "pistol",
        "shotgun",
        "sniper"
    ]

    # 메뉴 항목
    skills = [
        "mine",
        "heal"
    ]

    player1_gun = select_item("Player1 Gun", guns)
    player1_skill = select_item("Player1 Skill", skills)
    player2_gun = select_item("Player2 Gun", guns)
    player2_skill = select_item("Player2 Skill", skills)