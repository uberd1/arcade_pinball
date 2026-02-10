import arcade
from game.views import MainMenuView
from game.constants import SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE


def main():
    # Создание экземпляра окна
    window = arcade.Window(SCREEN_WIDTH, SCREEN_HEIGHT, SCREEN_TITLE)

    # Центрирование окна на экране пользователя
    window.center_window()

    # Инициализация стартового меню
    start_view = MainMenuView()

    # Переключение на стартовое меню
    window.show_view(start_view)

    # Запуск главного цикла Arcade
    arcade.run()


if __name__ == "__main__":
    main()
