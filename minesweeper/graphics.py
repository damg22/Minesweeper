"""All drawing: tiles, numbers, mines, flags, LED digits, smiley. No game logic here."""

import pygame

from . import settings as S


# --------------------------------------------------------------------------- bevels
def bevel(surf, rect, width, raised=True):
    """Draw a classic 3D border *inside* rect."""
    rect = pygame.Rect(rect)
    tl = S.LIGHT if raised else S.SHADOW
    br = S.SHADOW if raised else S.LIGHT
    for i in range(width):
        l, t, r, b = rect.left + i, rect.top + i, rect.right - 1 - i, rect.bottom - 1 - i
        pygame.draw.line(surf, tl, (l, t), (r, t))
        pygame.draw.line(surf, tl, (l, t), (l, b))
        pygame.draw.line(surf, br, (l + 1, b), (r, b))
        pygame.draw.line(surf, br, (r, t + 1), (r, b))


def frame(surf, content_rect, width, raised=False):
    """Draw a 3D border *around* content_rect (outside it)."""
    bevel(surf, pygame.Rect(content_rect).inflate(2 * width, 2 * width), width, raised)


# --------------------------------------------------------------------------- tiles
def _raised(T):
    s = pygame.Surface((T, T))
    s.fill(S.BG)
    bevel(s, s.get_rect(), S.TILE_BEVEL, raised=True)
    return s


def _sunken(T, color=S.BG):
    s = pygame.Surface((T, T))
    s.fill(color)
    pygame.draw.line(s, S.SHADOW, (0, 0), (T - 1, 0))
    pygame.draw.line(s, S.SHADOW, (0, 0), (0, T - 1))
    return s


def _blit_center(dst, src, offset=(0, 0)):
    r = src.get_rect(center=(dst.get_width() // 2 + offset[0], dst.get_height() // 2 + offset[1]))
    dst.blit(src, r)


def _draw_mine(s, T):
    cx, cy = T // 2, T // 2
    r = int(T * 0.27)
    spike = int(T * 0.40)
    d = int(spike * 0.72)
    w = max(2, T // 14)
    pygame.draw.line(s, S.BLACK, (cx - spike, cy), (cx + spike, cy), w)
    pygame.draw.line(s, S.BLACK, (cx, cy - spike), (cx, cy + spike), w)
    pygame.draw.line(s, S.BLACK, (cx - d, cy - d), (cx + d, cy + d), w)
    pygame.draw.line(s, S.BLACK, (cx - d, cy + d), (cx + d, cy - d), w)
    pygame.draw.circle(s, S.BLACK, (cx, cy), r)
    hl = max(2, T // 9)
    pygame.draw.rect(s, S.WHITE, (cx - r // 2 - hl // 2, cy - r // 2 - hl // 2, hl, hl))


def _draw_flag(s, T):
    pole_x = T // 2 + T // 15
    pw = max(2, T // 14)
    top = int(T * 0.18)
    cloth_h = int(T * 0.30)
    # base
    pygame.draw.rect(s, S.BLACK, (int(T * 0.24), int(T * 0.72), int(T * 0.54), max(2, T // 12)))
    pygame.draw.rect(s, S.BLACK, (int(T * 0.36), int(T * 0.66), int(T * 0.30), max(2, T // 12)))
    # pole
    pygame.draw.rect(s, S.BLACK, (pole_x, top, pw, int(T * 0.52)))
    # cloth (points left)
    pygame.draw.polygon(s, S.RED, [(pole_x, top), (pole_x, top + cloth_h), (int(T * 0.20), top + cloth_h // 2)])


def build_tiles(T=S.TILE):
    """Pre-render every tile type once. Returns {name: Surface}."""
    font = pygame.font.Font(None, int(T * 1.05))
    tiles = {}

    tiles["hidden"] = _raised(T)

    for n in range(9):
        s = _sunken(T)
        if n:
            _blit_center(s, font.render(str(n), True, S.NUMBER_COLORS[n]), (1, 1))
        tiles[f"num_{n}"] = s
    tiles["pressed"] = tiles["num_0"]

    s = _raised(T)
    _draw_flag(s, T)
    tiles["flag"] = s

    q = font.render("?", True, S.BLACK)
    s = _raised(T)
    _blit_center(s, q, (0, 1))
    tiles["question"] = s
    s = _sunken(T)
    _blit_center(s, q, (1, 2))
    tiles["question_pressed"] = s

    s = _sunken(T)
    _draw_mine(s, T)
    tiles["mine"] = s

    s = _sunken(T, S.RED)
    _draw_mine(s, T)
    tiles["mine_exploded"] = s

    s = _sunken(T)
    _draw_mine(s, T)
    m, w = int(T * 0.18), max(2, T // 12)
    pygame.draw.line(s, S.RED, (m, m), (T - m, T - m), w)
    pygame.draw.line(s, S.RED, (m, T - m), (T - m, m), w)
    tiles["flag_wrong"] = s

    return tiles


# --------------------------------------------------------------------------- LED counter
_SEGMENTS = {
    "0": "abcdef", "1": "bc", "2": "abdeg", "3": "abcdg", "4": "bcfg",
    "5": "acdfg", "6": "acdefg", "7": "abc", "8": "abcdefg", "9": "abcdfg",
    "-": "g", " ": "",
}


def _segment_polys(x, y, w, h, t):
    g = 1
    my = y + h / 2
    return {
        "a": [(x + g, y), (x + w - g, y), (x + w - g - t, y + t), (x + g + t, y + t)],
        "d": [(x + g + t, y + h - t), (x + w - g - t, y + h - t), (x + w - g, y + h), (x + g, y + h)],
        "g": [(x + g, my), (x + g + t, my - t / 2), (x + w - g - t, my - t / 2),
              (x + w - g, my), (x + w - g - t, my + t / 2), (x + g + t, my + t / 2)],
        "f": [(x, y + g), (x + t, y + t + g), (x + t, my - t / 2 - g), (x, my - g)],
        "b": [(x + w, y + g), (x + w, my - g), (x + w - t, my - t / 2 - g), (x + w - t, y + t + g)],
        "e": [(x, my + g), (x + t, my + t / 2 + g), (x + t, y + h - t - g), (x, y + h - g)],
        "c": [(x + w, my + g), (x + w, y + h - g), (x + w - t, y + h - t - g), (x + w - t, my + t / 2 + g)],
    }


def led_size(digits=3, h=34):
    dw = int(h * 0.52)
    pad = 4
    return (digits * dw + (digits - 1) * 3 + 2 * pad, h + 2 * pad)


def draw_led(surf, topleft, value, digits=3, h=34):
    """Seven-segment red counter. Clamps to the displayable range."""
    value = max(-(10 ** (digits - 1) - 1), min(10 ** digits - 1, int(value)))
    text = f"-{abs(value):0{digits - 1}d}" if value < 0 else f"{value:0{digits}d}"
    size = led_size(digits, h)
    rect = pygame.Rect(topleft, size)
    pygame.draw.rect(surf, S.LED_BG, rect)
    frame(surf, rect, 1, raised=False)
    dw, pad, t = int(h * 0.52), 4, max(3, h // 9)
    for i, ch in enumerate(text):
        x = rect.left + pad + i * (dw + 3)
        on = _SEGMENTS.get(ch, "")
        for name, poly in _segment_polys(x, rect.top + pad, dw, h, t).items():
            pygame.draw.polygon(surf, S.LED_ON if name in on else S.LED_OFF, poly)
    return rect


# --------------------------------------------------------------------------- smiley
HAPPY, SURPRISED, DEAD, COOL = "happy", "surprised", "dead", "cool"


def draw_smiley(surf, rect, face=HAPPY, pressed=False):
    rect = pygame.Rect(rect)
    pygame.draw.rect(surf, S.BG, rect)
    pygame.draw.rect(surf, S.SHADOW, rect, 1)
    inner = rect.inflate(-2, -2)
    if pressed:
        pygame.draw.line(surf, S.SHADOW, inner.topleft, inner.topright, 2)
        pygame.draw.line(surf, S.SHADOW, inner.topleft, inner.bottomleft, 2)
    else:
        bevel(surf, inner, 3, raised=True)

    off = 1 if pressed else 0
    cx, cy = rect.centerx + off, rect.centery + off
    R = int(rect.width * 0.36)
    pygame.draw.circle(surf, S.YELLOW, (cx, cy), R)
    pygame.draw.circle(surf, S.BLACK, (cx, cy), R, 2)

    ex, ey = int(R * 0.38), int(R * 0.28)
    er = max(2, R // 7)
    lw = max(2, R // 8)

    if face == DEAD:
        k = er + 1
        for sx in (-ex, ex):
            x, y = cx + sx, cy - ey
            pygame.draw.line(surf, S.BLACK, (x - k, y - k), (x + k, y + k), 2)
            pygame.draw.line(surf, S.BLACK, (x - k, y + k), (x + k, y - k), 2)
    elif face == COOL:
        gw, gh = int(R * 0.55), int(R * 0.34)
        for sx in (-1, 1):
            x0 = cx + (2 if sx > 0 else -2 - gw)
            pygame.draw.polygon(surf, S.BLACK, [(x0, cy - ey - gh // 2), (x0 + gw, cy - ey - gh // 2),
                                                (x0 + gw - (gw // 4 if sx < 0 else 0), cy - ey + gh // 2),
                                                (x0 + (gw // 4 if sx > 0 else 0), cy - ey + gh // 2)])
        pygame.draw.line(surf, S.BLACK, (cx - R + 2, cy - ey - gh // 2 + 1), (cx + R - 2, cy - ey - gh // 2 + 1), 2)
    else:
        for sx in (-ex, ex):
            pygame.draw.circle(surf, S.BLACK, (cx + sx, cy - ey), er)

    if face == SURPRISED:
        pygame.draw.circle(surf, S.BLACK, (cx, cy + int(R * 0.42)), max(3, R // 4), 2)
    elif face == DEAD:
        _mouth(surf, cx, cy + R * 0.58, R * 0.42, -R * 0.20, lw)
    else:
        _mouth(surf, cx, cy + R * 0.28, R * 0.50, R * 0.25, lw)


def _mouth(surf, cx, base_y, half_w, depth, width):
    """Smooth parabolic mouth: depth > 0 smiles, depth < 0 frowns."""
    pts = []
    for i in range(13):
        t = i / 12 * 2 - 1
        pts.append((cx + t * half_w, base_y + depth * (1 - t * t)))
    pygame.draw.lines(surf, S.BLACK, False, pts, width)
