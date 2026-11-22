"""
Window, layout, input handling and rendering.

The UI never decides game rules. It turns mouse/keyboard input into calls on
the Game (reveal / toggle_flag / chord) and draws whatever state the Game holds.

Controls
  Left click ...................... reveal
  Right click / Ctrl or Cmd+click . flag / question mark
  Left+Right, Middle, Shift+click . chord
  Smiley, F2, N ................... new game
  1 / 2 / 3 ....................... beginner / intermediate / expert
  Esc ............................. quit
"""

import asyncio
import random
import sys
import time

import pygame

from . import graphics as gfx
from . import settings as S
from .game import CellState, Game, GameStatus

IS_WEB = sys.platform == "emscripten"   # running in the browser via pygbag

LED_H = 30
MENU_ITEMS = [("Beginner", "beginner"), ("Intermediate", "intermediate"), ("Expert", "expert")]


class App:
    def __init__(self, difficulty="beginner", custom=None, game_factory=Game):
        if IS_WEB:
            # pygbag starts Python's random module from the same seed on every page
            # load, which would give every visitor the same boards.
            random.seed(time.time_ns())
        pygame.init()
        pygame.display.set_caption("Minesweeper")
        self.clock = pygame.time.Clock()
        self.menu_font = pygame.font.Font(None, 22)
        self.tiles = gfx.build_tiles(S.TILE)
        self.game_factory = game_factory

        self.difficulty = None if custom else difficulty
        self.dims = tuple(custom) if custom else S.DIFFICULTIES[difficulty]
        self.screen = None
        self.size = None
        self.new_game()

    # ------------------------------------------------------------------ setup
    def new_game(self):
        self.game = self.game_factory(*self.dims)
        self.start_time = None
        self.end_time = None
        self.left_down = self.right_down = self.middle_down = False
        self.chording = False
        self.after_chord = False      # swallow the second button release after a chord
        self.smiley_pressed = False
        self._layout()

    def set_difficulty(self, name):
        self.difficulty = name
        self.dims = S.DIFFICULTIES[name]
        self.new_game()

    def _layout(self):
        T, B, V = S.TILE, S.BORDER, S.BEVEL
        rows, cols = self.game.rows, self.game.cols
        board_w, board_h = cols * T, rows * T

        width = board_w + 2 * (B + V)
        self.menu_rect = pygame.Rect(0, 0, width, S.MENU_H)

        y = S.MENU_H + B + V
        self.header_rect = pygame.Rect(B + V, y, board_w, S.HEADER_H)
        y = self.header_rect.bottom + V + B + V
        self.board_rect = pygame.Rect(B + V, y, board_w, board_h)
        height = self.board_rect.bottom + V + B

        led_w, led_h = gfx.led_size(3, LED_H)
        hy = self.header_rect.centery - led_h // 2
        self.counter_pos = (self.header_rect.left + 6, hy)
        self.timer_pos = (self.header_rect.right - 6 - led_w, hy)
        self.smiley_rect = pygame.Rect(0, 0, S.SMILEY, S.SMILEY)
        self.smiley_rect.center = self.header_rect.center

        self.menu_hit = []
        x = 8
        for label, key in MENU_ITEMS:
            w = self.menu_font.size(label)[0]
            self.menu_hit.append((pygame.Rect(x - 4, 0, w + 8, S.MENU_H), label, key))
            x += w + 16

        if self.size != (width, height):
            self.size = (width, height)
            self.screen = pygame.display.set_mode(self.size)

    # ---------------------------------------------------------------- helpers
    def cell_at(self, pos):
        if not self.board_rect.collidepoint(pos):
            return None
        c = (pos[0] - self.board_rect.left) // S.TILE
        r = (pos[1] - self.board_rect.top) // S.TILE
        return (r, c)

    def _playable(self):
        return self.game.status in (GameStatus.READY, GameStatus.PLAYING)

    def _neighbours(self, r, c):
        for dr in (-1, 0, 1):
            for dc in (-1, 0, 1):
                rr, cc = r + dr, c + dc
                if 0 <= rr < self.game.rows and 0 <= cc < self.game.cols:
                    yield rr, cc

    def _sync_timer(self):
        status = self.game.status
        now = time.monotonic()
        if status == GameStatus.PLAYING and self.start_time is None:
            self.start_time = now
        if status in (GameStatus.WON, GameStatus.LOST) and self.end_time is None:
            if self.start_time is None:   # game ended on the very first click
                self.start_time = now
            self.end_time = now

    def elapsed(self):
        if self.start_time is None:
            return 0
        end = self.end_time if self.end_time is not None else time.monotonic()
        return min(999, int(end - self.start_time) + 1)

    def _act(self, method, cell):
        if cell is None or not self._playable():
            return
        getattr(self.game, method)(*cell)
        self._sync_timer()

    # ------------------------------------------------------------------ input
    def handle_event(self, e):
        if e.type == pygame.QUIT and not IS_WEB:
            return False
        if e.type == pygame.KEYDOWN:
            if e.key == pygame.K_ESCAPE and not IS_WEB:   # quitting a web page just leaves it blank
                return False
            if e.key in (pygame.K_F2, pygame.K_n):
                self.new_game()
            elif e.unicode in S.DIFFICULTY_KEYS:
                self.set_difficulty(S.DIFFICULTY_KEYS[e.unicode])
        elif e.type == pygame.MOUSEBUTTONDOWN:
            self._mouse_down(e.button, e.pos)
        elif e.type == pygame.MOUSEBUTTONUP:
            self._mouse_up(e.button, e.pos)
        return True

    def _mouse_down(self, button, pos):
        if button == 1:
            for rect, _, key in self.menu_hit:
                if rect.collidepoint(pos):
                    self.set_difficulty(key)
                    return
            if self.smiley_rect.collidepoint(pos):
                self.smiley_pressed = True
                return

        cell = self.cell_at(pos)
        if cell is None or not self._playable():
            return
        mods = pygame.key.get_mods()

        if button == 1:
            if mods & (pygame.KMOD_CTRL | pygame.KMOD_META):
                self._act("toggle_flag", cell)
                return
            self.left_down = True
            if self.right_down or mods & pygame.KMOD_SHIFT:
                self.chording = True
        elif button == 3:
            self.right_down = True
            if self.left_down:
                self.chording = True
            else:
                self._act("toggle_flag", cell)
        elif button == 2:
            self.middle_down = True
            self.chording = True

    def _mouse_up(self, button, pos):
        if button == 1 and self.smiley_pressed:
            self.smiley_pressed = False
            if self.smiley_rect.collidepoint(pos):
                self.new_game()
            return

        was_down = {1: self.left_down, 2: self.middle_down, 3: self.right_down}.get(button, False)
        if not was_down:
            return
        cell = self.cell_at(pos)

        if self.chording:
            self._act("chord", cell)
            self.chording = False
            self.after_chord = True
        elif button == 1 and not self.after_chord:
            self._act("reveal", cell)

        if button == 1:
            self.left_down = False
        elif button == 2:
            self.middle_down = False
        elif button == 3:
            self.right_down = False
        if not (self.left_down or self.right_down or self.middle_down):
            self.after_chord = False

    # ----------------------------------------------------------------- render
    def _pressed_cells(self):
        """Cells drawn pushed-in while a mouse button is held (purely visual)."""
        if not self._playable():
            return set()
        cell = self.cell_at(pygame.mouse.get_pos())
        if cell is None:
            return set()
        if self.chording:
            return set(self._neighbours(*cell))
        if self.left_down and not self.after_chord:
            return {cell}
        return set()

    def _tile_key(self, cell, pressed):
        status = self.game.status
        st = cell.state
        if st == CellState.REVEALED:
            if cell.is_mine:
                return "mine_exploded" if cell.exploded else "mine"
            return f"num_{cell.adjacent_mines}"
        if status == GameStatus.LOST:
            if cell.is_mine and st != CellState.FLAGGED:
                return "mine_exploded" if cell.exploded else "mine"
            if st == CellState.FLAGGED and not cell.is_mine:
                return "flag_wrong"
        if status == GameStatus.WON and cell.is_mine:
            return "flag"
        if st == CellState.FLAGGED:
            return "flag"
        if st == CellState.QUESTION:
            return "question_pressed" if pressed else "question"
        return "pressed" if pressed else "hidden"

    def _face(self):
        status = self.game.status
        if status == GameStatus.LOST:
            return gfx.DEAD
        if status == GameStatus.WON:
            return gfx.COOL
        if (self.left_down or self.chording) and self.cell_at(pygame.mouse.get_pos()):
            return gfx.SURPRISED
        return gfx.HAPPY

    def _draw_menu(self):
        pygame.draw.rect(self.screen, S.MENU_BG, self.menu_rect)
        pygame.draw.line(self.screen, S.SHADOW, (0, S.MENU_H - 1), (self.size[0], S.MENU_H - 1))
        mouse = pygame.mouse.get_pos()
        for rect, label, key in self.menu_hit:
            active = key == self.difficulty
            if rect.collidepoint(mouse):
                pygame.draw.rect(self.screen, S.BG, rect)
            text = self.menu_font.render(label, True, S.MENU_ACTIVE if active else S.MENU_TEXT)
            tr = text.get_rect(center=rect.center)
            self.screen.blit(text, tr)
            if active:
                pygame.draw.line(self.screen, S.MENU_ACTIVE, (tr.left, tr.bottom), (tr.right, tr.bottom))

    def render(self):
        scr = self.screen
        scr.fill(S.BG)
        self._draw_menu()

        # outer raised window frame
        outer = pygame.Rect(0, S.MENU_H, self.size[0], self.size[1] - S.MENU_H)
        gfx.bevel(scr, outer, S.BEVEL, raised=True)

        # header panel
        gfx.frame(scr, self.header_rect, S.BEVEL - 1, raised=False)
        gfx.draw_led(scr, self.counter_pos, self.game.flags_remaining(), h=LED_H)
        gfx.draw_led(scr, self.timer_pos, self.elapsed(), h=LED_H)
        gfx.draw_smiley(scr, self.smiley_rect, self._face(), self.smiley_pressed)

        # board
        gfx.frame(scr, self.board_rect, S.BEVEL, raised=False)
        pressed = self._pressed_cells()
        T, ox, oy = S.TILE, self.board_rect.left, self.board_rect.top
        for r in range(self.game.rows):
            for c in range(self.game.cols):
                key = self._tile_key(self.game.cell(r, c), (r, c) in pressed)
                scr.blit(self.tiles[key], (ox + c * T, oy + r * T))

        pygame.display.flip()

    # ------------------------------------------------------------------- loop
    async def run_async(self):
        """Main loop. Async so the browser build (pygbag) gets control back every
        frame; on desktop it runs exactly like a normal loop."""
        running = True
        while running:
            for e in pygame.event.get():
                if not self.handle_event(e):
                    running = False
                    break
            if running:
                self.render()
                self.clock.tick(S.FPS)
                await asyncio.sleep(0)
        pygame.quit()

    def run(self):
        asyncio.run(self.run_async())
