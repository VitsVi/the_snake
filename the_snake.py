from random import randint
import datetime as dt
import pygame

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

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
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pygame.display.set_caption('Змейка')

# Настройка времени:
clock = pygame.time.Clock()


# Тут опишите все классы игры.
class GameObject:
    """Родительский класс для объектов на игровом поле."""

    def __init__(self, body_color=None):
        self.position = CENTRAL_POSITION
        self.body_color = body_color

    def draw(self):
        """Метод для отрисовки игровых объектов на поле.
        Переопределяется в дочерних классах.
        """
        pass


class Snake(GameObject):
    """Класс взаимодействия змейки с игровым полем."""

    def __init__(self, body_color=SNAKE_COLOR):
        self.length = 1
        self.positions = [CENTRAL_POSITION]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
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
            current_head[0] + self.direction[0] * GRID_SIZE,
            current_head[1] + self.direction[1] * GRID_SIZE)
        if current_head in self.positions:
            self.save_score()
            self.reset()
        else:
            if current_head[1] >= SCREEN_HEIGHT:
                self.positions.insert(0, (current_head[0], 0))
            elif current_head[1] < 0:
                self.positions.insert(0, (current_head[0], SCREEN_HEIGHT))
            elif current_head[0] >= SCREEN_WIDTH:
                self.positions.insert(0, (0, current_head[1]))
            elif current_head[0] < 0:
                self.positions.insert(0, (SCREEN_WIDTH, current_head[1]))
            else:
                self.positions.insert(0, current_head)
            if self.length != len(self.positions):
                self.positions.pop()

    def draw(self):
        """Отрисовка змейки на игровом поле."""
        for position in self.positions[:-1]:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, self.body_color, rect)
            pygame.draw.rect(screen, BORDER_COLOR, rect, 1)

        head_rect = pygame.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, head_rect)
        pygame.draw.rect(screen, BORDER_COLOR, head_rect, 1)

        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод возвращает позицию 'головы' змейки на поле."""
        return self.positions[0]

    def reset(self):
        """Метод возращает начальные параметры игры при проигрыше."""
        self.positions = [CENTRAL_POSITION]
        self.direction = RIGHT
        self.length = 1

    def save_score(self):
        """Сохранение результатов игры в файл."""
        with open('snake_result.txt', 'a') as file_result:
            current_time = dt.datetime.now()
            file_result.write(
                f'Время окончания: {current_time}'
                f'\nСчет: {self.length - 1}'
                '\n--------------------\n')


class Apple(GameObject):
    """Класс поведения игрового объекта 'Яблоко'."""

    def __init__(self, body_color=APPLE_COLOR):
        self.position = None
        super().__init__(body_color)

    def randomize_position(self):
        """Получение случайных координат Яблока на поле."""
        self.position = (
            randint(0, GRID_WIDTH - 1) * GRID_SIZE,
            randint(0, GRID_HEIGHT - 1) * GRID_SIZE)

    def draw(self):
        """Отрисовка объекта 'Яблоко' на игровом поле."""
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(screen, self.body_color, rect)
        pygame.draw.rect(screen, BORDER_COLOR, rect, 1)


def handle_keys(game_object):
    """Функция для управления змейкой на поле."""
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            raise SystemExit
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pygame.K_s and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pygame.K_a and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pygame.K_d and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Основная функция реализации запуска программы."""
    # Инициализация PyGame:
    pygame.init()
    # Тут нужно создать экземпляры классов.
    snake = Snake(SNAKE_COLOR)
    apple = Apple(APPLE_COLOR)
    while True:
        clock.tick(SPEED)
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
        handle_keys(snake)
        snake.move()
        snake.update_direction()
        screen.fill(BOARD_BACKGROUND_COLOR)
        pygame.display.set_caption(f'Змейка. Счет: {snake.length - 1}')
        snake.draw()
        apple.draw()
        # Тут опишите основную логику игры.
        pygame.display.flip()


if __name__ == '__main__':
    main()
