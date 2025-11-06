import pygame as pg
import sys
from InGame import startGame
from map import createMap
from Tool import draw_text_with_outline

def start_lobby():
    from map.init_setting import screen_width, screen_height, screen

    # 색상 정의
    WHITE = (255, 255, 255)
    GREEN = (0, 255, 0)
    GRAY = (128, 128, 128)
    RED = (255, 0, 0)
    BLACK = (0, 0, 0)

    # 글꼴 설정
    title_font = pg.font.SysFont(None, 50)
    menu_font = pg.font.SysFont(None, 40)

    # 메뉴 항목
    menu_items = [
        {"text": "play", "color": GREEN, "rect": None},
        {"text": "setting", "color": GRAY, "rect": None},
        {"text": "exit", "color": RED, "rect": None}
    ]

    selected_index = 0  # 현재 선택된 메뉴

    # 메인 루프 
    running = True
    while running:
        image = pg.image.load("./assets/lobby_background.png").convert() # 배경 이미지 불러오기
        screen.blit(image, (0, 0)) # 배경화면 그리기

        title_image = pg.image.load("./assets/title.png").convert_alpha()
        title_image = pg.transform.scale(title_image, (800, 600))
        title_rect = title_image.get_rect(center=(screen_width//2, screen_height//4))
        screen.blit(title_image, title_rect)  # 타이틀 그리기

        # 메뉴 그리기
        start_y = screen_height//2
        gap = 50
        for i, item in enumerate(menu_items):
            # 렌더링용 rect는 미리 계산해서 저장
            text_surface_for_rect = menu_font.render(item["text"], True, item["color"])
            text_rect = text_surface_for_rect.get_rect(center=(screen_width//2, start_y + i*gap))
            item["rect"] = text_rect

            # 실제 그리기는 Tool의 함수로 (테두리 색: BLACK)
            draw_text_with_outline(item["text"], menu_font, item["color"], BLACK, text_rect.center, screen, 2)

            # 선택된 메뉴 옆에 삼각형 표시
            if i == selected_index:
                triangle_points = [
                    (text_rect.left - 30, text_rect.centery - 10),
                    (text_rect.left - 30, text_rect.centery + 10),
                    (text_rect.left - 10, text_rect.centery)
                ]
                pg.draw.polygon(screen, WHITE, triangle_points)


        pg.display.flip()

        # 이벤트 처리
        for event in pg.event.get():
            if event.type == pg.QUIT:
                running = False
            elif event.type == pg.KEYDOWN:
                if event.key == pg.K_DOWN or event.key == pg.K_s:
                    selected_index = (selected_index + 1) % len(menu_items)
                elif event.key == pg.K_UP or event.key == pg.K_w:
                    selected_index = (selected_index - 1) % len(menu_items)
                elif event.key == pg.K_SPACE:
                    if menu_items[selected_index]["text"] == "play":
                        play()
                    elif menu_items[selected_index]["text"] == "setting":
                        from Setting import setting
                        setting()
                    elif menu_items[selected_index]["text"] == "exit":
                        running = False
                    #print(menu_items[selected_index]["text"])
            elif event.type == pg.MOUSEBUTTONDOWN:
                mouse_pos = event.pos
                for item in menu_items:
                    if item["rect"] and item["rect"].collidepoint(mouse_pos):
                        if item["text"] == "play":
                            play()
                        if item["text"] == "setting":
                            from Setting import setting
                            setting()
                        #print(f"{item['text']} clicked!")  # 클릭된 메뉴 출력
                        if item["text"] == "exit":
                            running = False
    pg.quit()
    sys.exit()

def play():
    game_running = True
    while game_running:
        result = startGame()  # 게임 시작
        if result == "lobby":
            print("로비로 돌아가기")
            game_running = False  # 종료
        elif result == "replay":
            print("게임 다시 시작")
            continue  # 게임 다시 시작
        else:
            game_running = False  # 종료
            break