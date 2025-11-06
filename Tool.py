from map.init_setting import TICK_PER_SECOND

def secondToTick(seconds: float) -> int: # 초를 틱으로 변환
    return int(seconds * TICK_PER_SECOND)

def draw_text_with_outline(text, font, text_color, outline_color, pos, surface, border_thickness: int): # 텍스트와 테두리 그리기
    x, y = pos
    # 테두리 Surface는 한 번만 렌더링
    outline_surface = font.render(text, True, outline_color)
    # 테두리 그리기 (두께에 따라 범위 조정)
    for dx in range(-border_thickness, border_thickness + 1):
        for dy in range(-border_thickness, border_thickness + 1):
            if dx == 0 and dy == 0:
                continue
            rect = outline_surface.get_rect(center=(x + dx, y + dy))
            surface.blit(outline_surface, rect)
    # 글자 본체 그리기
    text_surface = font.render(text, True, text_color)
    rect = text_surface.get_rect(center=pos)
    surface.blit(text_surface, rect)