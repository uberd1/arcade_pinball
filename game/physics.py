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

    def add_sprite(self, sprite, body_type=DYNAMIC, friction=0.0, elasticity=1.0, mass=1.0, collision_type=0):
        # --- 1. СТАТИЧНЫЕ ОБЪЕКТЫ ---
        if collision_type in [0, 2]:
            body = self.space.static_body

            if collision_type == 2:
                # Бамперы
                shape = pymunk.Circle(body, 14, offset=(sprite.center_x, sprite.center_y))
                shape.elasticity = 1.4
            else:
                # СТЕНЫ: СКОШЕННЫЕ УГЛЫ
                width = sprite.width
                height = sprite.height

                # Если это маленький боковой блок - делаем его треугольным, чтобы шар летел ВБОК
                if width < 100 and height < 100:
                    points = [
                        (-width / 2, -height / 2),
                        (width / 2, 0),
                        (-width / 2, height / 2)
                    ]
                    # Зеркалим для правой стороны
                    if sprite.center_x > 300:
                        points = [
                            (width / 2, -height / 2),
                            (-width / 2, 0),
                            (width / 2, height / 2)
                        ]

                    poly = pymunk.Poly(None, points)
                    shape = pymunk.Poly(body, poly.get_vertices(),
                                        transform=pymunk.Transform(tx=sprite.center_x, ty=sprite.center_y))
                else:
                    # Обычные стены
                    shape = pymunk.Poly.create_box(body, (width, height))
                    shape.unsafe_set_vertices(
                        pymunk.Poly.create_box(None, (width, height)).get_vertices(),
                        pymunk.Transform(tx=sprite.center_x, ty=sprite.center_y)
                    )

                shape.elasticity = 0.8

            shape.friction = 0.0
            shape.collision_type = collision_type
            self.space.add(shape)
            self.sprites.append((sprite, None))
            return None

        # --- 2. ШАРИК ---
        radius = 7
        # Масса шара 1.0 - он очень легкий по сравнению с флиппером
        moment = pymunk.moment_for_circle(mass, 0, radius)
        body = pymunk.Body(mass, moment, body_type=body_type)
        body.position = (sprite.center_x, sprite.center_y)

        # Ограничитель скорости (чтобы не пролетал сквозь стены)
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

    def add_sprite_list(self, sprite_list, **kwargs):
        for sprite in sprite_list:
            self.add_sprite(sprite, **kwargs)

    def add_flipper(self, sprite, side="left"):
        # ИСПРАВЛЕНИЕ: Используем конечную массу, но большую.
        # Масса 100 против массы шара 1.0 — это как танк против футбольного мяча.
        # Шар не сможет продавить флиппер, но математика не сломается.
        mass = 100.0
        width, height = 75, 14

        # ИСПРАВЛЕНИЕ: Считаем честный момент инерции для коробочки
        moment = pymunk.moment_for_box(mass, (width, height))

        body = pymunk.Body(mass, moment)
        body.position = (sprite.center_x, sprite.center_y)

        dir = 1 if side == "left" else -1
        # Делаем флиппер клиновидным (сужается к концу) для лучшего отскока
        points = [(0, -height / 2), (width * dir, -height / 4), (width * dir, height / 4), (0, height / 2)]

        shape = pymunk.Poly(body, points)
        shape.friction = 0.1
        shape.elasticity = 0.5
        shape.collision_type = 3

        # Шарнир в центре спрайта
        pivot = pymunk.PivotJoint(self.space.static_body, body, (sprite.center_x, sprite.center_y))

        # Ограничитель вращения (-30 ... +30 градусов)
        # RotaryLimitJoint работает как жесткий поводок
        limit = pymunk.RotaryLimitJoint(self.space.static_body, body, math.radians(-30), math.radians(30))

        # Добавляем немного "вязкости" самому суставу, чтобы он не дрожал
        pivot.error_bias = 0.0

        self.space.add(body, shape, pivot, limit)
        self.sprites.append((sprite, body))
        return body

    def step(self, delta_time=1 / 60):
        steps = 30
        for _ in range(steps):
            self.space.step(delta_time / steps)

        for sprite, body in self.sprites:
            if body:
                sprite.center_x, sprite.center_y = body.position
                sprite.angle = math.degrees(body.angle)

    def power_flipper(self, body, is_pressed, side="left"):
        if body:
            if is_pressed:
                # Скорость 200 - очень резкий удар
                body.angular_velocity = 200 if side == "left" else -200
            else:
                # Скорость возврата
                body.angular_velocity = -80 if side == "left" else 80