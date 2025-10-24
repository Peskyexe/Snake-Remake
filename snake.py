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
        # number of segments the snake currently has (visual segments)
        self.segment_count = 0
        # number of segments to add when the snake next moves into a new cell
        self._grow_pending = 0
        # path of head positions (pixel coordinates). We store recent head centers to place segments smoothly.
        self._path = [Vector2(self.real_pos)]
        # remember previous grid pos to detect when we've entered a new cell
        self._prev_grid_pos = Vector2(self.grid_pos)

    def update(self, delta_time):
        # Move the snake center in real (pixel) space
        if not self.is_dead:
            self.real_pos = self.real_pos + settings.SNAKE_SPEED * self.direction * delta_time

        # Update grid cell position (integer cell coordinates) based on center
        self.grid_pos.x = int(self.real_pos.x // settings.GRID_SQUARE_SIZE)
        self.grid_pos.y = int(self.real_pos.y // settings.GRID_SQUARE_SIZE)

        # record head center in the path for smooth following
        self._path.append(Vector2(self.real_pos))

        # If we've moved into a new grid cell, apply growth (one segment per cell-move) as before
        if self.grid_pos != self._prev_grid_pos:
            if self._grow_pending > 0:
                self._grow_pending -= 1
                self.segment_count += 1
            # remember this grid pos for next update
            self._prev_grid_pos = Vector2(self.grid_pos)

        # prune path to only what's needed: we need at most segment_count+2 cells worth of distance
        max_needed = (self.segment_count + 2) * settings.GRID_SQUARE_SIZE
        # compute total length of path from oldest to newest
        total = 0.0
        for i in range(len(self._path) - 1, 0, -1):
            total += (self._path[i] - self._path[i-1]).length()
            if total > max_needed:
                # remove older points before i-1
                if i-1 > 0:
                    del self._path[0:i-1]
                break

        # self-collision detection: compute segment grid positions and compare to head grid
        # helper to get a position along the path at distance `d` behind head
        def _get_pos_at_distance(d):
            # traverse path from newest to oldest, accumulating distance
            acc = 0.0
            if len(self._path) == 0:
                return Vector2(self.real_pos)
            for i in range(len(self._path)-1, 0, -1):
                p1 = self._path[i]
                p0 = self._path[i-1]
                seg_len = (p1 - p0).length()
                if acc + seg_len >= d:
                    # interpolate between p0 and p1
                    remain = d - acc
                    if seg_len == 0:
                        return Vector2(p0)
                    t = remain / seg_len
                    return Vector2(p1 + (p0 - p1) * t)
                acc += seg_len
            # if path not long enough, return oldest point
            return Vector2(self._path[0])

        # check for collision: if any segment occupies same grid cell as head
        for i in range(self.segment_count):
            dist = (i+1) * settings.GRID_SQUARE_SIZE
            seg_pos = _get_pos_at_distance(dist)
            seg_grid_x = int(seg_pos.x // settings.GRID_SQUARE_SIZE)
            seg_grid_y = int(seg_pos.y // settings.GRID_SQUARE_SIZE)
            if seg_grid_x == self.grid_pos.x and seg_grid_y == self.grid_pos.y:
                self.is_dead = True
                break

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

    def grow(self, amount=1):
        """Request the snake to grow by `amount` segments. Growth is applied one per cell-move."""
        if amount <= 0:
            return
        self._grow_pending += int(amount)

    def draw(self, surface, offset = Vector2(0, 0)):
        # Draw the snake centered at self.real_pos
        half = settings.GRID_SQUARE_SIZE / 2
        # helper to get a position along the head path at distance d behind head
        def _get_pos_at_distance(d):
            acc = 0.0
            if len(self._path) == 0:
                return Vector2(self.real_pos)
            for i in range(len(self._path)-1, 0, -1):
                p1 = self._path[i]
                p0 = self._path[i-1]
                seg_len = (p1 - p0).length()
                if acc + seg_len >= d:
                    remain = d - acc
                    if seg_len == 0:
                        return Vector2(p0)
                    t = remain / seg_len
                    return Vector2(p1 + (p0 - p1) * t)
                acc += seg_len
            return Vector2(self._path[0])

        # draw segments from tail to just behind head
        for i in reversed(range(self.segment_count)):
            dist = (i+1) * settings.GRID_SQUARE_SIZE
            seg_center = _get_pos_at_distance(dist) + offset
            top_left = Vector2(seg_center.x - half, seg_center.y - half)
            pygame.draw.rect(
                surface,
                (0, 180, 0),
                (top_left.x, top_left.y, settings.GRID_SQUARE_SIZE, settings.GRID_SQUARE_SIZE),
            )

        # draw head on top
        head_top_left = Vector2(self.real_pos.x - half + offset.x, self.real_pos.y - half + offset.y)
        pygame.draw.rect(
            surface,
            (0, 255, 0),
            (head_top_left.x, head_top_left.y, settings.GRID_SQUARE_SIZE, settings.GRID_SQUARE_SIZE),
        )

    def reset(self):
        self.grid_pos = Vector2(settings.grid_size[0] // 2, settings.grid_size[1] // 2)
        half = settings.GRID_SQUARE_SIZE / 2
        self.real_pos = self.grid_pos * settings.GRID_SQUARE_SIZE + Vector2(half, half)
        self.relative_pos = Vector2(0, 0)
        self.direction =  Vector2(1, 0)
        self.turn_buffer = None
        self.is_dead = False
        self.segment_count = 0
        self._grow_pending = 0
        self._path = [Vector2(self.real_pos)]
        self._prev_grid_pos = Vector2(self.grid_pos)