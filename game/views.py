import arcade
import os
import random
import math
from .constants import *
from .objects import VectorBall, VectorFlipper
from .ui import Button, TextLabel
from .levels import create_level_1, create_level_2

# Импортируем физический движок
from .physics import PymunkPhysics


class MainMenuView(arcade.View):
    def __init__(self):
        super().__init__()
        self.ui_elements = []

        self.ui_elements.append(TextLabel(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 100, TEXT_TITLE, 40, COLOR_BALL))

        self.ui_elements.append(Button(
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
            200, 50, TEXT_START, self.start_game
        ))

        self.ui_elements.append(Button(
            SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 70,
            200, 50, TEXT_EXIT, arcade.exit
        ))

    def on_show_view(self):
        arcade.set_background_color(COLOR_BACKGROUND)

    def start_game(self):
        game_view = GameView()
        game_view.setup()
        self.window.show_view(game_view)

    def on_draw(self):
        self.clear()
        for element in self.ui_elements:
            element.draw()

    def on_mouse_motion(self, x, y, dx, dy):
        for element in self.ui_elements:
            if isinstance(element, Button):
                element.check_mouse(x, y)

    def on_mouse_press(self, x, y, button, modifiers):
        if button == arcade.MOUSE_BUTTON_LEFT:
            for element in self.ui_elements:
                if isinstance(element, Button):
                    if element.check_mouse(x, y):
                        element.on_click()


class GameView(arcade.View):
    def __init__(self):
        super().__init__()
        self.wall_list = arcade.SpriteList()
        self.bumper_list = arcade.SpriteList()
        self.flipper_list = arcade.SpriteList()
        self.ball_list = arcade.SpriteList()
        self.particles = []

        self.score = 0
        self.game_over = False

        self.score_text = arcade.Text("", 20, SCREEN_HEIGHT - 40, COLOR_TEXT_MAIN, 20)
        self.physics_engine = None

    def setup(self):
        self.wall_list = arcade.SpriteList()
        self.bumper_list = arcade.SpriteList()
        self.flipper_list = arcade.SpriteList()
        self.ball_list = arcade.SpriteList()

        # Загружаем уровень
        walls_data, bumpers_data = create_level_1()
        for w in walls_data: self.wall_list.append(w)
        for b in bumpers_data: self.bumper_list.append(b)

        # Создаем флипперы
        self.left_flipper = VectorFlipper(220, 80, "left")
        self.right_flipper = VectorFlipper(SCREEN_WIDTH - 220, 80, "right")
        self.flipper_list.extend([self.left_flipper, self.right_flipper])

        # Создаем шарик
        self.ball = VectorBall(SCREEN_WIDTH - 100, 600)
        self.ball_list.append(self.ball)

        # Инициализация физики
        self.physics_engine = PymunkPhysics(
            gravity=(GRAVITY_X, GRAVITY_Y),
            damping=PHYSICS_DAMPING
        )

        # 1. Добавляем стены
        self.physics_engine.add_sprite_list(
            self.wall_list,
            friction=WALL_FRICTION,
            elasticity=WALL_ELASTICITY,
            collision_type=0
        )

        # 2. Добавляем бамперы
        self.physics_engine.add_sprite_list(
            self.bumper_list,
            friction=BUMPER_FRICTION,
            elasticity=BUMPER_ELASTICITY,
            collision_type=2
        )

        # 3. Добавляем шарик
        self.ball_body = self.physics_engine.add_sprite(
            self.ball,
            mass=BALL_MASS,
            friction=BALL_FRICTION,
            elasticity=BALL_ELASTICITY,
            collision_type=1
        )

        # 4. Добавляем флипперы
        self.left_flipper_body = self.physics_engine.add_flipper(self.left_flipper, side="left")
        self.right_flipper_body = self.physics_engine.add_flipper(self.right_flipper, side="right")

    def on_draw(self):
        self.clear()

        # Рисуем все объекты
        for lst in [self.wall_list, self.bumper_list, self.flipper_list]:
            for item in lst:
                item.draw_custom()

        if not self.game_over:
            self.ball.draw_custom()

        self.draw_particles()

        self.score_text.text = f"{TEXT_SCORE}{self.score}"
        self.score_text.draw()

    def on_update(self, delta_time):
        if self.game_over: return

        self.physics_engine.step(delta_time)

        # --- ОБРАБОТКА БАМПЕРОВ ЧЕРЕЗ MATH.DIST ---
        for bumper in self.bumper_list:
            # Считаем расстояние между центрами
            dist = math.dist(
                (self.ball.center_x, self.ball.center_y),
                (bumper.center_x, bumper.center_y)
            )
            #Засчитываем удары от бампера
            if dist < 30 and bumper.hit_timer <= 0:
                bumper.hit()
                self.score += 100
                self.spawn_particles(self.ball.center_x, self.ball.center_y)

                # Физический пинок от бампера
                # Вычисляем вектор направления от бампера к шару
                normal_x = (self.ball.center_x - bumper.center_x) / dist
                normal_y = (self.ball.center_y - bumper.center_y) / dist
                force = 500
                self.ball_body.apply_impulse_at_local_point((normal_x * force, normal_y * force))

        for bumper in self.bumper_list:
            bumper.update_animation()

        self.update_particles()

        # Проверка падения шара
        if self.ball.center_y < -50:
            self.do_game_over()

    def do_game_over(self):
        self.game_over = True
        self.save_highscore()
        view = GameOverView(self.score)
        self.window.show_view(view)

    def on_key_press(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.physics_engine.power_flipper(self.left_flipper_body, True, "left")
        elif key == arcade.key.RIGHT:
            self.physics_engine.power_flipper(self.right_flipper_body, True, "right")

    def on_key_release(self, key, modifiers):
        if key == arcade.key.LEFT:
            self.physics_engine.power_flipper(self.left_flipper_body, False, "left")
        elif key == arcade.key.RIGHT:
            self.physics_engine.power_flipper(self.right_flipper_body, False, "right")

    def spawn_particles(self, x, y):
        for _ in range(15):
            angle = random.uniform(0, 360)
            speed = random.uniform(3, 7)
            dx = math.cos(math.radians(angle)) * speed
            dy = math.sin(math.radians(angle)) * speed
            life = random.uniform(0.5, 1.0)
            self.particles.append([x, y, dx, dy, life, life])

    def update_particles(self):
        for p in self.particles[:]:
            p[0] += p[2]
            p[1] += p[3]
            p[4] -= 0.05
            if p[4] <= 0:
                self.particles.remove(p)

    def draw_particles(self):
        for p in self.particles:
            alpha = int(255 * (p[4] / p[5]))
            color = (255, 255, 0, alpha)
            arcade.draw_point(p[0], p[1], color, 3)

    def save_highscore(self):
        if not os.path.exists("data"): os.makedirs("data")
        old_score = 0
        if os.path.exists(FILE_HIGHSCORE):
            try:
                with open(FILE_HIGHSCORE, "r") as f:
                    old_score = int(f.read())
            except:
                pass
        if self.score > old_score:
            with open(FILE_HIGHSCORE, "w") as f: f.write(str(self.score))


class GameOverView(arcade.View):
    #Экран Окончания игры
    def __init__(self, score):
        super().__init__()
        self.score = score
        self.title_text = arcade.Text(TEXT_GAME_OVER, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 + 50, arcade.color.RED, 50,
                                      anchor_x="center")
        self.score_text = arcade.Text(f"{TEXT_SCORE}{self.score}", SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2,
                                      arcade.color.WHITE, 30, anchor_x="center")
        self.info_text = arcade.Text(TEXT_RESTART, SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2 - 80, arcade.color.GRAY, 20,
                                     anchor_x="center")

    def on_show_view(self):
        arcade.set_background_color(arcade.color.BLACK)

    def on_draw(self):
        self.clear()
        self.title_text.draw()
        self.score_text.draw()
        self.info_text.draw()

    def on_key_press(self, symbol, modifiers):
        # Проверяем, что нажата именно клавиша Enter
        if symbol == arcade.key.ENTER:
            game_view = GameView()
            game_view.setup()
            self.window.show_view(game_view)
