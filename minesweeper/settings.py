"""Visual constants and difficulty presets. Tweak freely."""

# --- Sizes (pixels) ---------------------------------------------------------
TILE = 30          # size of one cell
BORDER = 10        # gap between the window edge and the panels
BEVEL = 3          # thickness of the 3D panel borders
TILE_BEVEL = 3     # thickness of the raised-tile border
MENU_H = 26        # height of the difficulty menu bar
HEADER_H = 50      # height of the counter / smiley / timer panel
SMILEY = 38        # smiley button size
FPS = 60

# --- Difficulty presets: (rows, cols, mines) --------------------------------
DIFFICULTIES = {
    "beginner": (9, 9, 10),
    "intermediate": (16, 16, 40),
    "expert": (16, 30, 99),
}
DIFFICULTY_KEYS = {"1": "beginner", "2": "intermediate", "3": "expert"}

# Custom board limits (same as the classic game)
MIN_ROWS, MAX_ROWS = 9, 24
MIN_COLS, MAX_COLS = 9, 30

# --- Colours ----------------------------------------------------------------
BG = (192, 192, 192)
LIGHT = (255, 255, 255)
SHADOW = (128, 128, 128)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
MENU_BG = (225, 225, 225)
MENU_TEXT = (30, 30, 30)
MENU_ACTIVE = (0, 0, 160)

LED_ON = (255, 0, 0)
LED_OFF = (70, 0, 0)
LED_BG = (0, 0, 0)

# Classic number colours, 1 through 8
NUMBER_COLORS = {
    1: (0, 0, 255),
    2: (0, 128, 0),
    3: (255, 0, 0),
    4: (0, 0, 128),
    5: (128, 0, 0),
    6: (0, 128, 128),
    7: (0, 0, 0),
    8: (128, 128, 128),
}
