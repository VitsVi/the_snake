from random import randint
import datetime as dt
import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Пустые координаты на поле.
EMPTY_BLOCKS = [(grid_part_width, grid_part_height)
                for grid_part_width in range(0,
                SCREEN_WIDTH, GRID_SIZE)
                for grid_part_height in range(0,
                SCREEN_HEIGHT, GRID_SIZE)]

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Регулировка передвижения змейки.
TURNS = {
    (pg.K_w, LEFT): UP,
    (pg.K_w, RIGHT): UP,
    (pg.K_s, LEFT): DOWN,
    (pg.K_s, RIGHT): DOWN,
    (pg.K_a, UP): LEFT,
    (pg.K_a, DOWN): LEFT,
    (pg.K_d, UP): RIGHT,
    (pg.K_d, DOWN): RIGHT}

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки:
BORDER_COLOR = (93, 216, 228)

# Цвет яблока:
APPLE_COLOR = (255, 0, 150)

# Цвет змейки:
SNAKE_COLOR = (0, 255, 255)

# Скорость движения змейки:
SPEED = 20

# Начальная позиция змейки:
CENTRAL_POSITION = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс для объектов на игровом поле."""

    def __init__(self, body_color=None):
        self.position = CENTRAL_POSITION
        self.body_color = body_color

    def draw(self):
        """Абстрактный метод для визуализации объектов на поле.
        Переопределяется в дочерних классах.
        """
        raise NotImplementedError

    def draw_object(self, position):
        """Метод отрисовки игровых объектов на поле."""
        rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)

    def clear_object(self, position):
        """Метод закрашивания объектов на поле."""
        if position:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)


class Snake(GameObject):
    """Класс взаимодействия змейки с игровым полем."""

    def __init__(self, body_color=SNAKE_COLOR):
        self.length = 0
        self.positions = [CENTRAL_POSITION]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
        self.save_result = None
        super().__init__(body_color)

    def update_direction(self):
        """Обновление направления двиежния змейки."""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Логика передвижения змейки на игровом поле."""
        current_head = self.get_head_position()
        current_head = (
            (current_head[0] + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH,
            (current_head[1] + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, current_head)
        if self.length != len(self.positions):
            self.last = self.positions[len(self.positions) - 1]
            self.positions.pop()

    def draw(self):
        """Отрисовка змейки на игровом поле."""
        super().draw_object(self.positions[0])
        super().clear_object(self.last)

    def get_head_position(self):
        """Метод возвращает позицию 'головы' змейки на поле."""
        return self.positions[0]

    def reset(self):
        """Метод возращает начальные параметры игры при проигрыше."""
        self.positions = [CENTRAL_POSITION]
        self.direction = RIGHT
        self.length = 1


class Apple(GameObject):
    """Класс поведения игрового объекта 'Яблоко'."""

    def __init__(self, body_color=APPLE_COLOR):
        self.position = None
        super().__init__(body_color)

    def randomize_position(self, empty_blocks):
        """Получение координат Яблока на поле, исходя из свободных клеток"""
        empty_position_iter = randint(0, len(empty_blocks))
        self.position = (
            empty_blocks[empty_position_iter][0],
            empty_blocks[empty_position_iter][1])

    def draw(self):
        """Отрисовка объекта на игровом поле,
        вызов метода родительского класса.
        """
        super().draw_object(self.position)


def handle_keys(game_object):
    """Функция для управления змейкой на поле."""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
        elif event.type == pg.KEYDOWN:
            try:
                game_object.next_direction = TURNS[
                    (event.key, game_object.direction)]
            except KeyError:
                None


def save_score(length):
    """Сохранение результатов игры в файл."""
    with open('snake_result.txt', 'a') as file_result:
        current_time = dt.datetime.now()
        file_result.write(
            f'Время окончания: {current_time}'
            f'\nСчет: {length - 1}'
            '\n--------------------\n')


def get_empty_blocks(snake_positions):
    """Получение свободных блоков на карте для генерации яблока."""
    empty_blocks = list(set(EMPTY_BLOCKS) - set(snake_positions))
    return empty_blocks


def main():
    """Основная функция реализации запуска программы."""
    pg.init()
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR)
    while True:
        clock.tick(SPEED)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            # Передача в метод результата функции с пустыми клетками на карте.
            apple.randomize_position(get_empty_blocks(snake.positions))
        handle_keys(snake)
        snake.move()
        # Проверка условия проигрыша и запись результата игры
        for snake_pos in snake.positions[1:]:
            if snake_pos == snake.get_head_position():
                save_score(snake.length)
                screen.fill(BOARD_BACKGROUND_COLOR)
                snake.reset()
        snake.update_direction()
        pg.display.set_caption(f'Змейка. Счет: {snake.length - 1}')
        apple.draw()
        snake.draw()
        pg.display.flip()


if __name__ == '__main__':
    main()
