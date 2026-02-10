import arcade
from .constants import *


class UIElement:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.visible = True

    def draw(self):
        raise NotImplementedError


class Button(UIElement):
    def __init__(self, x, y, width, height, text, action_func=None):
        super().__init__(x, y)
        self.width = width
        self.height = height
        self.text_str = text
        self.action = action_func
        self.is_hovered = False

        self.text_obj = arcade.Text(
            text,
            x,
            y,
            arcade.color.WHITE,
            20,
            anchor_x="center",
            anchor_y="center"
        )

    def check_mouse(self, mouse_x, mouse_y):
        left = self.x - self.width / 2
        right = self.x + self.width / 2
        bottom = self.y - self.height / 2
        top = self.y + self.height / 2

        self.is_hovered = (left < mouse_x < right and bottom < mouse_y < top)
        return self.is_hovered

    def on_click(self):
        if self.action:
            self.action()

    def draw(self):
        if not self.visible:
            return

        bg_color = arcade.color.CYAN if self.is_hovered else arcade.color.MIDNIGHT_BLUE
        text_color = arcade.color.BLACK if self.is_hovered else arcade.color.WHITE

        # Обновляем цвет текста
        self.text_obj.color = text_color

        arcade.draw_rect_filled(
            arcade.rect.XYWH(self.x, self.y, self.width, self.height),
            bg_color
        )
        arcade.draw_rect_outline(
            arcade.rect.XYWH(self.x, self.y, self.width, self.height),
            arcade.color.WHITE,
            2
        )

        self.text_obj.draw()


class TextLabel(UIElement):
    def __init__(self, x, y, text, font_size=30, color=arcade.color.WHITE):
        super().__init__(x, y)
        # Создаем объекты текста для оптимизации
        self.shadow_obj = arcade.Text(
            text, x + 2, y - 2, COLOR_TEXT_SHADOW, font_size, anchor_x="center"
        )
        self.main_obj = arcade.Text(
            text, x, y, color, font_size, anchor_x="center"
        )

    def draw(self):
        self.shadow_obj.draw()
        self.main_obj.draw()
