import pygame as pg
import sys

def draw_text_with_outline(text, font, text_color, outline_color, pos, surface):
    x, y = pos
    # 테두리 그리기
    for dx in [-2, -1, 0, 1, 2]:
        for dy in [-2, -1, 0, 1, 2]:
            if dx != 0 or dy != 0:
                outline_surface = font.render(text, True, outline_color)
                rect = outline_surface.get_rect(center=(x + dx, y + dy))
                surface.blit(outline_surface, rect)
    # 글자 본체 그리기
    text_surface = font.render(text, True, text_color)
    rect = text_surface.get_rect(center=pos)
    surface.blit(text_surface, rect)

def setting():
    from map.init_setting import screen, screen_height, screen_width

    # 색상
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)

    # 폰트
    font_current = pg.font.SysFont(None, 50)
    font_other = pg.font.SysFont(None, 35)

    setting_option = ["select map", "control", "go to lobby"]
    current_index = 0
    running = True

    while running:
        #screen.blit("./assets/setting_background.png") # 배경화면 그리기
        screen.fill((0, 0, 0))

        prev_map = setting_option[current_index - 1] if current_index > 0 else ""
        next_map = setting_option[current_index + 1] if current_index < len(setting_option) - 1 else ""
        current_map = setting_option[current_index]

        # 이전 옵션
        if prev_map:
            draw_text_with_outline(prev_map, font_other, BLACK, WHITE, (screen_width // 2, screen_height // 2 - 40), screen)
        # 현재 옵션
        draw_text_with_outline(current_map, font_current, RED, WHITE, (screen_width // 2, screen_height // 2), screen)
        # 다음 옵션
        if next_map:
            draw_text_with_outline(next_map, font_other, BLACK, WHITE, (screen_width // 2, screen_height // 2 + 40), screen)

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
                    if current_index < len(setting_option) - 1:
                        current_index += 1
                elif event.key in [pg.K_SPACE, pg.K_RETURN]:
                    if current_map == "select map":
                        from Select_map import select_map
                        select_map()
                    elif current_map == "control":
                        pass
                    elif current_map == "go to lobby":
                        running = False
                        break

        pg.display.flip()
