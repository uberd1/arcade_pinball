import arcade
import math
from .constants import *
from .vector_utils import get_rectangle_corners


class VectorBall(arcade.Sprite):
    """Стильный стальной шарик с бликом."""

    def __init__(self, x, y):
        super().__init__(scale=1.0)
        self.center_x = x
        self.center_y = y

    def draw_custom(self):
        # Основное тело шара (Циан/Неон)
        arcade.draw_circle_filled(self.center_x, self.center_y, BALL_RADIUS, COLOR_BALL)

        # Блик для объема (белое пятно сверху-слева)
        arcade.draw_circle_filled(
            self.center_x - BALL_RADIUS * 0.3,
            self.center_y + BALL_RADIUS * 0.3,
            BALL_RADIUS * 0.35,
            (255, 255, 255, 180)
        )


class VectorWall(arcade.Sprite):
    """Стена с эффектом неоновой трубки."""

    def __init__(self, x, y, width, height, angle=0):
        super().__init__(scale=1.0)
        self.center_x = x
        self.center_y = y
        self.width = width
        self.height = height
        self.angle = angle

    def draw_custom(self):
        points = get_rectangle_corners(self.center_x, self.center_y, self.width, self.height, self.angle)

        # 1. Внешнее размытое свечение (Neon Glow)
        arcade.draw_polygon_outline(points, (COLOR_WALL[0], COLOR_WALL[1], COLOR_WALL[2], 60), line_width=8)
        # 2. Темная основа стены
        arcade.draw_polygon_filled(points, COLOR_BACKGROUND)
        # 3. Яркий внутренний контур
        arcade.draw_polygon_outline(points, COLOR_WALL_OUTLINE, line_width=2)


class VectorFlipper(arcade.Sprite):
    """Флиппер, который рисуется от точки вращения (а не из центра)."""

    def __init__(self, x, y, side="left"):
        super().__init__(scale=1.0)
        self.center_x = x
        self.center_y = y
        self.side = side
        # Используем уменьшенные размеры для большего пространства
        self.f_width = 70  # Компактный размер
        self.f_height = 12

    def draw_custom(self):
        # Угол берется из физики Pymunk
        angle_rad = math.radians(self.angle)
        direction = 1 if self.side == "left" else -1

        # Вычисляем конец лапки от точки вращения
        end_x = self.center_x + math.cos(angle_rad) * self.f_width * direction
        end_y = self.center_y + math.sin(angle_rad) * self.f_width * direction

        # Рисуем сустав (болт, на котором держится флиппер)
        arcade.draw_circle_filled(self.center_x, self.center_y, self.f_height / 1.5, COLOR_FLIPPER)

        # Рисуем тело лапки (скругленная линия)
        arcade.draw_line(self.center_x, self.center_y, end_x, end_y, COLOR_FLIPPER, line_width=self.f_height)

        # Рисуем закругленный кончик
        arcade.draw_circle_filled(end_x, end_y, self.f_height / 2, COLOR_FLIPPER)


class VectorBumper(arcade.Sprite):
    """Классический круглый бампер с анимацией вспышки."""

    def __init__(self, x, y):
        super().__init__(scale=1.0)
        self.center_x = x
        self.center_y = y
        self.hit_timer = 0
        self.radius = 14  # Уменьшенный радиус для свободного поля

    def hit(self):
        self.hit_timer = 15

    def update_animation(self):
        if self.hit_timer > 0:
            self.hit_timer -= 1

    def draw_custom(self):
        # Цвет меняется на белый при ударе
        current_color = arcade.color.WHITE if self.hit_timer > 5 else COLOR_BUMPER

        # Внешнее свечение при ударе
        if self.hit_timer > 0:
            arcade.draw_circle_outline(self.center_x, self.center_y, self.radius + 6,
                                       (255, 255, 255, self.hit_timer * 10), border_width=2)

        # Основное тело бампера
        arcade.draw_circle_filled(self.center_x, self.center_y, self.radius, current_color)

        # Декоративные кольца внутри (как в настоящих автоматах)
        arcade.draw_circle_outline(self.center_x, self.center_y, self.radius * 0.7, arcade.color.BLACK, border_width=2)
        arcade.draw_circle_filled(self.center_x, self.center_y, self.radius * 0.2, arcade.color.BLACK)