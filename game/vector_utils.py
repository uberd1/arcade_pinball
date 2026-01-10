import math

class Vector2D:
    """
    Класс, представляющий двумерный вектор (x, y).
    Используется для расчетов физики и отрисовки векторной графики.
    """
    def __init__(self, x: float, y: float):
        self.x = x
        self.y = y

    def __repr__(self):
        return f"Vector2D({self.x}, {self.y})"

    def add(self, other):
        """Сложение векторов."""
        return Vector2D(self.x + other.x, self.y + other.y)

    def sub(self, other):
        """Вычитание векторов."""
        return Vector2D(self.x - other.x, self.y - other.y)

    def mul(self, scalar: float):
        """Умножение вектора на скаляр (число)."""
        return Vector2D(self.x * scalar, self.y * scalar)

    def length(self) -> float:
        """Возвращает длину (модуль) вектора."""
        return math.sqrt(self.x**2 + self.y**2)

    def normalize(self):
        """Возвращает нормализованный вектор (длиной 1)."""
        l = self.length()
        if l != 0:
            return Vector2D(self.x / l, self.y / l)
        return Vector2D(0, 0)

    def rotate(self, angle_degrees: float, origin=None):
        """
        Вращает вектор вокруг заданной точки (origin).
        Если origin не задан, вращает вокруг (0,0).
        """
        if origin is None:
            origin = Vector2D(0, 0)

        # Перевод в радианы
        radians = math.radians(angle_degrees)
        cos_a = math.cos(radians)
        sin_a = math.sin(radians)

        # Сдвиг к началу координат
        shifted_x = self.x - origin.x
        shifted_y = self.y - origin.y

        # Формула поворота
        new_x = shifted_x * cos_a - shifted_y * sin_a
        new_y = shifted_x * sin_a + shifted_y * cos_a

        # Обратный сдвиг
        return Vector2D(new_x + origin.x, new_y + origin.y)

    @staticmethod
    def get_distance(v1, v2) -> float:
        """Статический метод для вычисления расстояния между двумя векторами."""
        dx = v1.x - v2.x
        dy = v1.y - v2.y
        return math.sqrt(dx**2 + dy**2)

    @staticmethod
    def from_tuple(t: tuple):
        """Создает вектор из кортежа (x, y)."""
        return Vector2D(t[0], t[1])

    def to_tuple(self) -> tuple:
        """Преобразует вектор в кортеж."""
        return (self.x, self.y)

def get_rectangle_corners(center_x, center_y, width, height, angle=0):
    """
    Вспомогательная функция для получения координат углов прямоугольника
    с учетом его вращения. Используется для отрисовки стен и флипперов.
    """
    center = Vector2D(center_x, center_y)
    half_w = width / 2
    half_h = height / 2

    # Создаем 4 угла относительно центра
    corners = [
        Vector2D(center_x - half_w, center_y + half_h), # Top Left
        Vector2D(center_x + half_w, center_y + half_h), # Top Right
        Vector2D(center_x + half_w, center_y - half_h), # Bottom Right
        Vector2D(center_x - half_w, center_y - half_h)  # Bottom Left
    ]

    # Вращаем каждый угол, если есть угол поворота
    if angle != 0:
        rotated_corners = [v.rotate(angle, center).to_tuple() for v in corners]
        return rotated_corners
    
    return [v.to_tuple() for v in corners]