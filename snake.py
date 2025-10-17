import pygame
from pygame.math import Vector2
import settings

class Snake:
    def __init__(self):
        self.grid_pos = Vector2(settings.grid_size[0] // 2, settings.grid_size[1] // 2)
        # Treat real_pos as the CENTER point of the snake's head (pixels)
        half = settings.GRID_SQUARE_SIZE / 2
        self.real_pos = self.grid_pos * settings.GRID_SQUARE_SIZE + Vector2(half, half)
        # relative_pos remains the offset from the cell top-left (pixels)
        self.relative_pos = Vector2(0, 0)
        self.direction =  Vector2(1, 0)
        self.turn_buffer = None
        # How close (in pixels) to the cell center we must be to accept a buffered turn
        self._turn_snap_threshold = settings.SNAKE_TURN_SNAP_TRHRESHOLD

        self.is_dead = False

    def update(self, delta_time):
        # Move the snake center in real (pixel) space
        if not self.is_dead:
            self.real_pos = self.real_pos + settings.SNAKE_SPEED * self.direction * delta_time

        # Update grid cell position (integer cell coordinates) based on center
        self.grid_pos.x = int(self.real_pos.x // settings.GRID_SQUARE_SIZE)
        self.grid_pos.y = int(self.real_pos.y // settings.GRID_SQUARE_SIZE)

        if self.grid_pos.x < 0 or self.grid_pos.x >= settings.grid_size[0] or \
           self.grid_pos.y < 0 or self.grid_pos.y >= settings.grid_size[1]:
            self.is_dead = True

        # Compute relative position inside the current grid square in pixels (from top-left)
        cell_origin = self.grid_pos * settings.GRID_SQUARE_SIZE
        self.relative_pos = Vector2(self.real_pos.x - cell_origin.x, self.real_pos.y - cell_origin.y)

        # If a turn is buffered, check whether we're close enough to the cell center to perform it
        if self.turn_buffer is not None:
            cell_center = cell_origin + Vector2(settings.GRID_SQUARE_SIZE / 2, settings.GRID_SQUARE_SIZE / 2)
            distance_to_center = (self.real_pos - cell_center).length()
            if distance_to_center <= self._turn_snap_threshold:
                # Snap to exact cell center and apply buffered turn
                self.real_pos = cell_center
                self.direction = self.turn_buffer
                self.turn_buffer = None

    def turn(self, new_direction):

        # normalize inputs to Vector2
        nd = Vector2(new_direction)

        # don't allow reversing 180 degrees
        if nd == -self.direction or nd == self.direction:
            return

        # If already close to center, apply immediately
        cell_origin = self.grid_pos * settings.GRID_SQUARE_SIZE
        cell_center = cell_origin + Vector2(settings.GRID_SQUARE_SIZE / 2, settings.GRID_SQUARE_SIZE / 2)
        if (self.real_pos - cell_center).length() <= self._turn_snap_threshold:
            self.real_pos = cell_center
            self.direction = nd
            self.turn_buffer = None
        else:
            # buffer for later
            self.turn_buffer = nd

    def draw(self, surface, offset = Vector2(0, 0)):
        # Draw the snake centered at self.real_pos
        half = settings.GRID_SQUARE_SIZE / 2
        top_left = Vector2(self.real_pos.x - half + offset.x, self.real_pos.y - half + offset.y)
        pygame.draw.rect(
            surface,
            (0, 255, 0),
            (top_left.x, top_left.y, settings.GRID_SQUARE_SIZE, settings.GRID_SQUARE_SIZE)
        )

    def reset(self):
        self.grid_pos = Vector2(settings.grid_size[0] // 2, settings.grid_size[1] // 2)
        half = settings.GRID_SQUARE_SIZE / 2
        self.real_pos = self.grid_pos * settings.GRID_SQUARE_SIZE + Vector2(half, half)
        self.relative_pos = Vector2(0, 0)
        self.direction =  Vector2(1, 0)
        self.turn_buffer = None
        self.is_dead = False