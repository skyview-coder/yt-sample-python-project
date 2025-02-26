from luma.led_matrix.device import max7219
from luma.core.interface.serial import spi, noop
from luma.core.render import canvas
from luma.core.legacy import text, show_message
from luma.core.legacy.font import proportional, CP437_FONT, TINY_FONT, SINCLAIR_FONT
import time
import random

from test_only_snake import ClsSnakeDemo

TOTAL_LED_WIDTH = 32
TOTAL_LED_HEIGHT = 8
TOTAL_CASCADED_DEVICE = 4

# Number of dots
NUM_DOTS = 10

# Dot class to store position and velocity
class Dot:
    def __init__(self):
        self.x = random.randint(0, TOTAL_LED_WIDTH - 1)  # Random initial x position
        self.y = random.randint(0, TOTAL_LED_HEIGHT - 1)  # Random initial y position
        self.vx = random.choice([-1, 1])  # Random initial x velocity (-1 or 1)
        self.vy = random.choice([-1, 1])  # Random initial y velocity (-1 or 1)

    def move(self):
        # Update position based on velocity
        self.x += self.vx
        self.y += self.vy

        # Elastic collision with borders
        if self.x <= 0 or self.x >= TOTAL_LED_WIDTH - 1:
            self.vx *= -1  # Reverse x velocity
        if self.y <= 0 or self.y >= TOTAL_LED_HEIGHT - 1:
            self.vy *= -1  # Reverse y velocity

        # Ensure the dot stays within the display bounds
        self.x = max(0, min(self.x, TOTAL_LED_WIDTH - 1))
        self.y = max(0, min(self.y, TOTAL_LED_HEIGHT - 1))

class ClsMax7219:
    def __init__(self):
        self.m_test = 0
        self.m_serial_spi = None
        self.m_device = None

    def fun_init_max7219(self):
        self.m_test = 0
        # Initialize SPI and MAX7219 device
        self.m_serial_spi = spi(port=0, device=0, gpio=noop())
        self.m_device = max7219(self.m_serial_spi,
                                width=TOTAL_LED_WIDTH,
                                height=TOTAL_LED_HEIGHT,
                                cascaded=TOTAL_CASCADED_DEVICE,
                                block_orientation=0,
                                rotate=0)


    def fun_scroll_text_as_normal(self, input_text, scroll_delay_secs):
        self.m_test = 0
        l_loop = 2
        try:
            while l_loop:
                print("Start of loop...")
                show_message(self.m_device,
                             msg=input_text,
                             fill="white",
                             font=proportional(CP437_FONT),
                             scroll_delay=scroll_delay_secs)
                print("End of loop...")
                l_loop -= 1
        except KeyboardInterrupt:
            print("Got KeyboardInterrupt...")

        self.m_device.clear()
        self.m_device.cleanup()

        print("Function -> fun_scroll_text_as_normal exit as normal...")

    # Function to draw all dots on the display
    def fun_draw_dots(self, dots):
        with canvas(self.m_device) as draw:
            for dot in dots:
                draw.point((dot.x, dot.y), fill="white")

    def fun_bouncing_balls(self):
        self.m_test = 0
        try:
            l_loop = 2
            while l_loop:
                l_loop -= 1
                time.sleep(0.02)
                ii = 50
                dots = [Dot() for _ in range(NUM_DOTS)]

                while True and ii:
                    # Move all dots
                    for dot in dots:
                        dot.move()

                    # Draw all dots
                    self.fun_draw_dots(dots)

                    # Control the speed of the animation
                    time.sleep(0.09)

                    ii -= 1

        except KeyboardInterrupt:
            print("Got KeyboardInterrupt...")

        self.m_device.clear()
        self.m_device.cleanup()

        print("Function -> fun_bouncing_balls exit as normal...")

    def fun_initialize_column(self):
        self.m_test = 0
        return [random.randint(0, TOTAL_LED_HEIGHT - 1) for _ in range(TOTAL_LED_WIDTH)]

    def fun_draw_matrix(self, column):
        with canvas(self.m_device) as draw:
            for x in range(TOTAL_LED_WIDTH):
                y = column[x]
                draw.point((x, y), fill="white")  # Draw the dot
                # Optional: Add a fading trail
                if y > 0:
                    draw.point((x, y - 1), fill="gray")
                if y > 1:
                    draw.point((x, y - 2), fill="darkgray")

    def fun_update_column(self, column):
        self.m_test = 0
        for x in range(TOTAL_LED_WIDTH):
            if column[x] < TOTAL_LED_HEIGHT - 1:
                column[x] += 1  # Move dot down
            else:
                column[x] = 0  # Reset dot to the top
        return column

    def fun_matrix_raining_code_effect(self):
        self.m_test = 0
        try:
            l_loop = 100
            column = self.fun_initialize_column()  # Initialize the falling dots
            while l_loop:
                l_loop -= 1
                self.fun_draw_matrix(column)  # Draw the current state
                column = self.fun_update_column(column)  # Update the positions
                time.sleep(0.1)  # Control the speed of the animation
        except KeyboardInterrupt:
            print("Got KeyboardInterrupt...")

        self.m_device.clear()
        self.m_device.cleanup()

        print("Function -> fun_matrix_raining_code_effect exit as normal...")

if __name__ == '__main__':

    text_to_be_scrolled = """Raspberry Pi 5 Project by @MrAudioAndCircuits"""
    obj = ClsMax7219()

    # to display text scrolling : fun_scroll_text_as_normal
    obj.fun_init_max7219()
    obj.fun_scroll_text_as_normal(input_text=text_to_be_scrolled,
                                  scroll_delay_secs=.05)

    # to display bouncing balls effect : fun_bouncing_balls
    obj.fun_init_max7219()
    obj.fun_bouncing_balls()

    # to display english film matrix raining code effect : fun_matrix_raining_code_effect
    obj.fun_init_max7219()
    obj.fun_matrix_raining_code_effect()

    # to display old mobile game snake effect as demo : fun_main_snake_demo_game
    # this is written in test_only_snake.py as class ClsSnakeDemo
    obj_snake = ClsSnakeDemo()
    obj_snake.fun_main_snake_demo_game()

    print("Main program exit as normal and success...")