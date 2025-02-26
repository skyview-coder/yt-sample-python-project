import random
import time
from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text
from luma.core.legacy.font import proportional, LCD_FONT

WIDTH = 32
HEIGHT = 8
CASCADED_DEVICE = 4

class ClsSnakeDemo:
    def __init__(self):
        self.m_test = 0
        # Initialize the MAX7219 device
        self.m_serial = spi(port=0, device=0, gpio=noop())
        self.m_device = max7219(self.m_serial, cascaded=CASCADED_DEVICE, block_orientation=0, rotate=0)

    # Function to initialize the snake and food
    def initialize_game(self):
        self.m_test = 0
        snake = [(5, 4), (4, 4), (3, 4)]  # Initial snake with 3 dots
        food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))  # Initial food position
        growth_counter = 1  # Number of dots to grow on the next collision
        return snake, food, growth_counter


    # Function to draw the snake and food on the display
    def draw_game(self, device, snake, food):
        self.m_test = 0
        with canvas(device) as draw:
            # Draw the snake
            for segment in snake:
                draw.point(segment, fill="white")
            # Draw the food
            draw.point(food, fill="white")


    # Function to check if a position is safe (not occupied by the snake or out of bounds)
    def is_safe(self, position, snake):
        self.m_test = 0
        x, y = position
        if (x < 0 or x >= WIDTH or y < 0 or y >= HEIGHT):
            return False  # Out of bounds
        if position in snake:
            return False  # Occupied by the snake
        return True


    # Function to choose a safe direction towards the food
    def choose_direction(self, snake, food):
        head_x, head_y = snake[0]
        food_x, food_y = food

        # Possible directions (up, down, left, right)
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        # Prioritize directions that move closer to the food
        preferred_directions = []
        if food_x > head_x:
            preferred_directions.append((1, 0))  # Right
        elif food_x < head_x:
            preferred_directions.append((-1, 0))  # Left
        if food_y > head_y:
            preferred_directions.append((0, 1))  # Down
        elif food_y < head_y:
            preferred_directions.append((0, -1))  # Up

        # Try preferred directions first
        for direction in preferred_directions:
            new_head = (head_x + direction[0], head_y + direction[1])
            if self.is_safe(new_head, snake):
                return direction

        # If no preferred direction is safe, choose any safe direction
        for direction in directions:
            new_head = (head_x + direction[0], head_y + direction[1])
            if self.is_safe(new_head, snake):
                return direction

        # If no safe direction is found, return None (game over)
        return None


    # Function to update the snake's position
    def update_snake(self, snake, food, growth_counter):
        # Choose a safe direction
        direction = self.choose_direction(snake, food)
        if direction is None:
            return False, food, growth_counter  # No safe direction (game over)

        # Calculate new head position
        new_head = (snake[0][0] + direction[0], snake[0][1] + direction[1])

        # Add new head to the snake
        snake.insert(0, new_head)

        # Check if the snake eats the food
        if new_head == food:
            # Grow the snake by `growth_counter` dots
            for _ in range(growth_counter):
                snake.append(snake[-1])  # Add a new segment at the tail
            # Generate new food position
            while True:
                food = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
                if food not in snake:
                    break
            # Increase growth counter for the next collision
            growth_counter += 1
        else:
            # Remove the tail (snake moves forward)
            snake.pop()

        return True, food, growth_counter


    # Main game loop
    def fun_main_snake_demo_game(self):
        l_loop = 2
        while l_loop:
            l_loop -= 1
            # Initialize the game
            snake, food, growth_counter = self.initialize_game()

            while True:
                # Update snake position
                game_running, food, growth_counter = self.update_snake(snake, food, growth_counter)
                if not game_running:
                    break  # Restart the game

                # Draw the game
                self.draw_game(self.m_device, snake, food)

                # Check if the snake fills the entire matrix
                if len(snake) == WIDTH * HEIGHT:
                    break  # Restart the game (snake filled the matrix)

                # Control the speed of the game
                time.sleep(0.2)

            # Snake filled the matrix or no safe direction
            with canvas(self.m_device) as draw:
                text(draw, (0, 0), "init", fill="white", font=proportional(LCD_FONT))
            time.sleep(2)

        self.m_device.clear()
        self.m_device.cleanup()

        print("Function -> fun_main_snake_demo_game exit as normal...")
