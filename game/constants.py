import arcade

# --- Настройки Экрана ---
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 800
SCREEN_TITLE = "Neon Vector Pinball [Pro Edition]"

# --- Настройки Физики (Pymunk) ---
# Гравитация направлена вниз (по оси Y отрицательная)
GRAVITY_X = 0
GRAVITY_Y = -1200
# Damping (сопротивление воздуха): 1.0 - нет сопротивления, 0.9 - сильное
PHYSICS_DAMPING = 0.96

# --- Параметры Объектов ---
BALL_RADIUS = 10
BALL_MASS = 1.0
BALL_FRICTION = 0.5
BALL_ELASTICITY = 0.85  # Прыгучесть шарика

# Параметры стен
WALL_FRICTION = 0.5
WALL_ELASTICITY = 0.7

# Параметры бамперов (отбивалок)
BUMPER_RADIUS = 14
BUMPER_ELASTICITY = 1.5  # Сильный отскок
BUMPER_FRICTION = 0.6

# Параметры флипперов (лапок)
FLIPPER_WIDTH = 70   # Было 90
FLIPPER_HEIGHT = 12  # Было 15
FLIPPER_MAX_ANGLE = 30
FLIPPER_MIN_ANGLE = -30
FLIPPER_SPEED = 20

# --- Цветовая Палитра (Neon Style) ---
# Используем RGBA для прозрачности, если нужно
COLOR_BACKGROUND = (10, 10, 20)      # Почти черный
COLOR_BALL = (0, 255, 255)           # Cyan
COLOR_WALL = (50, 50, 200)           # Dark Blue
COLOR_WALL_OUTLINE = (100, 100, 255) # Light Blue
COLOR_BUMPER = (255, 0, 128)         # Neon Pink
COLOR_FLIPPER = (255, 200, 0)        # Gold/Yellow
COLOR_TEXT_MAIN = (255, 255, 255)
COLOR_TEXT_SHADOW = (100, 100, 100)
COLOR_PARTICLE_START = (255, 255, 0)
COLOR_PARTICLE_END = (255, 0, 0)

# --- Битовые маски коллизий (Bitmasks) ---
# Pymunk использует категории для фильтрации столкновений
CATEGORY_WALL = 0b0001
CATEGORY_BALL = 0b0010
CATEGORY_FLIPPER = 0b0100
CATEGORY_BUMPER = 0b1000

# --- Пути к файлам ---
FILE_HIGHSCORE = "data/highscore.txt"

# --- Тексты UI ---
TEXT_TITLE = "NEON PINBALL"
TEXT_START = "START GAME"
TEXT_EXIT = "EXIT"
TEXT_GAME_OVER = "GAME OVER"
TEXT_SCORE = "Score: "
TEXT_RESTART = "Press CLICK to Restart"