import random
import settings
from pygame.math import Vector2
from fruits import Fruit_1


class ScoreController:
    def __init__(self):
        self.score = 0
        # Timers track seconds since last spawn
        self._timer_f1 = 0.0
        self._timer_f2 = 0.0
        # Active fruit instances
        self.fruits = []

    def update(self, delta_time, snake):
        # Advance timers
        self._timer_f1 += delta_time
        self._timer_f2 += delta_time

        # Spawn Fruit_1 when timer exceeds interval
        if self._timer_f1 >= settings.FRUIT_1_SPAWN_INTERVAL:
            if snake.is_dead == False:
                self._timer_f1 = 0.0
                self._spawn_fruit_1(snake)
        
        # Spawn Fruit_2 when timer exceeds interval
        if self._timer_f2 >= settings.FRUIT_2_SPAWN_INTERVAL:
            if snake.is_dead == False:
                self._timer_f2 = 0.0
                self._spawn_fruit_2(snake)

        # Check collisions: any fruit on the same grid tile as the snake head
        eaten = []
        for f in self.fruits:
            if f.grid_pos == snake.grid_pos:
                self.score += f.value
                # grow the snake for the points/value of the fruit
                try:
                    snake.grow(f.value)
                except AttributeError:
                    # if snake doesn't implement grow, ignore
                    pass
                eaten.append(f)

        # Remove eaten fruits
        for f in eaten:
            if f in self.fruits:
                self.fruits.remove(f)

    def _spawn_fruit_1(self, snake):
        # Try to find an unoccupied grid cell; give up after a number of attempts
        max_attempts = 100
        cols, rows = settings.grid_size[0], settings.grid_size[1]
        for _ in range(max_attempts):
            x = random.randrange(cols)
            y = random.randrange(rows)
            pos = Vector2(x, y)
            # avoid spawning on the snake head or on an existing fruit
            if pos == snake.grid_pos:
                continue
            if any(f.grid_pos == pos for f in self.fruits):
                continue
            # place the fruit
            self.fruits.append(Fruit_1(pos))
            return

    def _spawn_fruit_2(self, snake):
        # Try to find an unoccupied grid cell; give up after a number of attempts
        max_attempts = 100
        cols, rows = settings.grid_size[0], settings.grid_size[1]
        for _ in range(max_attempts):
            x = random.randrange(cols)
            y = random.randrange(rows)
            pos = Vector2(x, y)
            # avoid spawning on the snake head or on an existing fruit
            if pos == snake.grid_pos:
                continue
            if any(f.grid_pos == pos for f in self.fruits):
                continue
            # place the fruit
            from fruits import Fruit_2
            self.fruits.append(Fruit_2(pos))
            return

    def draw(self, screen, offset=Vector2(0, 0)):
        # offset: Vector2 pixel offset for where the grid starts on the screen
        for f in self.fruits:
            f.draw(screen, offset)

    def reset(self):
        """Reset score controller state: score, timers and active fruits."""
        self.score = 0
        self._timer_f1 = 0.0
        self._timer_f2 = 0.0
        self.fruits = []
