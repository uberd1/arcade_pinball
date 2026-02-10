from .objects import VectorWall, VectorBumper
from .constants import SCREEN_WIDTH, SCREEN_HEIGHT


def create_level_1():
    walls = []
    bumpers = []

    # --- 1. Внешний периметр (Коробка) ---
    
    # Левая вертикальная стена (длинная)
    # x=10, y=400, width=20, height=800
    walls.append(VectorWall(10, 400, 20, 800))
    
    # Правая вертикальная стена
    walls.append(VectorWall(SCREEN_WIDTH - 10, 400, 20, 800))
    
    # Потолок (Верхняя крышка)
    walls.append(VectorWall(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 20))

    # --- 2. Срезанные углы ---
    
    # Левый верхний угол (наклон 45 градусов)
    # x=60, y=750, w=100, h=20, angle=45
    walls.append(VectorWall(60, 750, 100, 20, angle=45))
    
    # Правый верхний угол (наклон -45 градусов)
    walls.append(VectorWall(SCREEN_WIDTH - 60, 750, 100, 20, angle=-45))

    # --- 3. Нижняя воронка (Слив к флипперам) ---
    # Это самые важные стены, они направляют мяч к лапкам
    
    # Левый скат
    walls.append(VectorWall(120, 150, 220, 20, angle=-30))
    
    # Правый скат
    walls.append(VectorWall(SCREEN_WIDTH - 120, 150, 220, 20, angle=30))

    # --- 4. Препятствия в центре стола ---
    
    # Центральный треугольник (из 3 стен)
    cx, cy = SCREEN_WIDTH / 2, 500
    # Горизонтальная планка
    walls.append(VectorWall(cx, cy, 100, 20, angle=0))
    # Левая наклонная
    walls.append(VectorWall(cx - 40, cy + 40, 60, 20, angle=60))
    # Правая наклонная
    walls.append(VectorWall(cx + 40, cy + 40, 60, 20, angle=-60))

    # Боковые "уши" (отбойники у стен)
    walls.append(VectorWall(40, 400, 60, 20, angle=20))
    walls.append(VectorWall(SCREEN_WIDTH - 40, 400, 60, 20, angle=-20))

    # --- 5. Бамперы (Круглые цели) ---
    
    # Треугольник из бамперов наверху
    bumpers.append(VectorBumper(SCREEN_WIDTH / 2, 650))           # Верхний
    bumpers.append(VectorBumper(SCREEN_WIDTH / 2 - 80, 600))      # Левый
    bumpers.append(VectorBumper(SCREEN_WIDTH / 2 + 80, 600))      # Правый
    
    # Дополнительный бампер в сложной зоне
    bumpers.append(VectorBumper(SCREEN_WIDTH / 2, 350))

    return walls, bumpers


def create_level_2():
    walls = []
    bumpers = []
    
    # Стандартные стены периметра
    walls.append(VectorWall(10, 400, 20, 800))
    walls.append(VectorWall(SCREEN_WIDTH - 10, 400, 20, 800))
    walls.append(VectorWall(SCREEN_WIDTH / 2, SCREEN_HEIGHT - 10, SCREEN_WIDTH, 20))
    
    # Более узкий слив (сложнее играть)
    walls.append(VectorWall(140, 120, 250, 20, angle=-25))
    walls.append(VectorWall(SCREEN_WIDTH - 140, 120, 250, 20, angle=25))
    
    # "Змейка" из препятствий
    walls.append(VectorWall(200, 500, 150, 20, angle=15))
    walls.append(VectorWall(400, 400, 150, 20, angle=-15))
    walls.append(VectorWall(200, 300, 150, 20, angle=15))
    
    # Линия бамперов
    for y in range(500, 750, 80):
        bumpers.append(VectorBumper(SCREEN_WIDTH / 2, y))
        
    return walls, bumpers