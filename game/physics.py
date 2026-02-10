import pymunk
import arcade
import math


class PymunkPhysics:
    STATIC = pymunk.Body.STATIC
    DYNAMIC = pymunk.Body.DYNAMIC

    def __init__(self, gravity=(0, -2000), damping=0.95):
        self.space = pymunk.Space()
        self.space.gravity = gravity
        self.space.damping = damping
        self.sprites = []
        # Словарь для хранения моторов флипперов: {body: motor}
        self.flipper_motors = {}

    def add_sprite(self, sprite, body_type=DYNAMIC, friction=0.0, elasticity=1.0, mass=1.0, collision_type=0):
        # --- 1. СТАТИЧНЫЕ ОБЪЕКТЫ ---
        if collision_type in [0, 2]:
            body = self.space.static_body
            cx, cy = sprite.center_x, sprite.center_y

            if collision_type == 2:
                # --- БАМПЕРЫ ---
                shape = pymunk.Circle(body, 14, offset=(cx, cy))
                shape.elasticity = elasticity

            else:
                # --- СТЕНЫ ---
                width = sprite.width
                height = sprite.height

                # Переводим угол из градусов (Arcade) в радианы (Pymunk)
                angle_rad = math.radians(sprite.angle)

                # Вычисляем параметры для Матрицы Трансформации
                # Поворот + Смещение
                cos_a = math.cos(angle_rad)
                sin_a = math.sin(angle_rad)

                # Создаем трансформацию:
                # a, b, c, d - отвечают за поворот и масштаб
                # tx, ty - отвечают за позицию (смещение)
                # Формула: x' = ax + cy + tx; y' = bx + dy + ty
                transform = pymunk.Transform(
                    a=cos_a,
                    b=sin_a,
                    c=-sin_a,
                    d=cos_a,
                    tx=sprite.center_x,
                    ty=sprite.center_y
                )

                # Если это маленький угловой блок
                if width < 100 and height < 100 and sprite.angle == 0:
                    # Если блок повернут, считаем его просто наклонной стеной
                    points = [
                        (-width / 2, -height / 2),
                        (width / 2, 0),
                        (-width / 2, height / 2)
                    ]
                    # Зеркалим для правой стороны (если нужно)
                    if sprite.center_x > 300:
                        points = [
                            (width / 2, -height / 2),
                            (-width / 2, 0),
                            (width / 2, height / 2)
                        ]
                    poly = pymunk.Poly(None, points)
                    vertices = poly.get_vertices()
                else:
                    # ОБЫЧНЫЕ И НАКЛОННЫЕ СТЕНЫ
                    # Создаём прямоугольник вокруг (0,0)
                    # Важно: используем исходные размеры спрайта без учета поворота!
                    local_points = [
                        (-width / 2, -height / 2),
                        (width / 2, -height / 2),
                        (width / 2, height / 2),
                        (-width / 2, height / 2)
                    ]
                    vertices = local_points

                shape = pymunk.Poly(body, vertices=vertices, transform=transform)
                shape.elasticity = elasticity

            # Общие настройки для статики
            shape.friction = friction
            shape.collision_type = collision_type
            self.space.add(shape)
            self.sprites.append((sprite, None))
            return None

        # --- 2. ШАРИК ---
        radius = 10
        moment = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, moment, body_type=body_type)
        body.position = (sprite.center_x, sprite.center_y)

        # Ограничитель скорости
        def limit_velocity(body, gravity, damping, dt):
            max_velocity = 1500
            pymunk.Body.update_velocity(body, gravity, damping, dt)
            if body.velocity.length > max_velocity:
                body.velocity = body.velocity * (max_velocity / body.velocity.length)

        body.velocity_func = limit_velocity

        shape = pymunk.Circle(body, radius)
        shape.friction = 0.0
        shape.elasticity = elasticity
        shape.collision_type = collision_type

        self.space.add(body, shape)
        self.sprites.append((sprite, body))
        return body

    def add_flipper(self, sprite, side="left"):
        mass = 50.0
        width, height = 75, 14

        # Момент инерции для вращения вокруг конца (примерно)
        moment = pymunk.moment_for_box(mass, (width, height))

        body = pymunk.Body(mass, moment)
        body.position = (sprite.center_x, sprite.center_y)

        dir = 1 if side == "left" else -1
        # Форма флиппера
        points = [(0, -height / 2), (width * dir, -height / 4), (width * dir, height / 4), (0, height / 2)]

        shape = pymunk.Poly(body, points)
        shape.friction = 0.5
        shape.elasticity = 0.2
        shape.collision_type = 3

        # Шарнир (гвоздь)
        pivot = pymunk.PivotJoint(self.space.static_body, body, (sprite.center_x, sprite.center_y))

        # Ограничитель угла
        min_angle = math.radians(-30)
        max_angle = math.radians(30)
        limit = pymunk.RotaryLimitJoint(self.space.static_body, body, min_angle, max_angle)

        motor = pymunk.SimpleMotor(self.space.static_body, body, 0)
        motor.max_force = 10_000_000  # Достаточно силы, чтобы ударить мяч

        # Сохраняем мотор, чтобы управлять им в power_flipper
        self.flipper_motors[body] = motor

        self.space.add(body, shape, pivot, limit, motor)
        self.sprites.append((sprite, body))
        return body

    def step(self, delta_time=1 / 60):
        steps = 20

        dt = delta_time / steps
        for _ in range(steps):
            self.space.step(dt)

        # Синхронизация спрайтов
        for sprite, body in self.sprites:
            if body:
                sprite.center_x, sprite.center_y = body.position
                sprite.angle = math.degrees(body.angle)

    def power_flipper(self, body, is_pressed, side="left"):
        if body in self.flipper_motors:
            motor = self.flipper_motors[body]

            # Скорость вращения (радианы в секунду)
            # Если нажат - бьем вверх, иначе - возвращаем вниз
            speed = 15 if is_pressed else -10

            if side == "right":
                speed = -speed  # Инверсия для правой стороны

            motor.rate = speed

    def add_sprite_list(self, sprite_list, **kwargs):
        # Передача не одного спрайта а списка, например стены
        for sprite in sprite_list:
            self.add_sprite(sprite, **kwargs)
