import time
import gpiod
from gpiod.line import Direction, Value


def fun_led_gpiod_test():
    with gpiod.Chip("/dev/gpiochip0") as chip:
        info = chip.get_info()

        print("name      : ", info.name)
        print("label     : ", info.label)
        print("num_lines : ", info.num_lines)

        led_0 = 4       # GPIO 4
        led_1 = 17      # GPIO 17
        led_2 = 27      # GPIO 27
        led_3 = 22      # GPIO 22

        led_4 = 14      # GPIO 14
        led_5 = 15      # GPIO 15
        led_6 = 18      # GPIO 18
        led_7 = 23      # GPIO 23

        with gpiod.request_lines(
                "/dev/gpiochip0",
                consumer="blink-example",
                config={
                    led_0: gpiod.LineSettings(
                        direction=Direction.OUTPUT, output_value=Value.ACTIVE
                    ),
                    led_1: gpiod.LineSettings(
                        direction=Direction.OUTPUT, output_value=Value.ACTIVE
                    ),
                    led_2: gpiod.LineSettings(
                        direction=Direction.OUTPUT, output_value=Value.ACTIVE
                    ),
                    led_3: gpiod.LineSettings(
                        direction=Direction.OUTPUT, output_value=Value.ACTIVE
                    ),
                    led_4: gpiod.LineSettings(
                        direction=Direction.OUTPUT, output_value=Value.ACTIVE
                    ),
                    led_5: gpiod.LineSettings(
                        direction=Direction.OUTPUT, output_value=Value.ACTIVE
                    ),
                    led_6: gpiod.LineSettings(
                        direction=Direction.OUTPUT, output_value=Value.ACTIVE
                    ),
                    led_7: gpiod.LineSettings(
                        direction=Direction.OUTPUT, output_value=Value.ACTIVE
                    )

                },
        ) as request:
            try:
                while True:

                    for ii in range(256):
                        b_value = "{:08b}".format(ii)

                        print("b_value : {}, 0x{:02X}, {}".format(b_value, ii, ii))

                        # eg: b_value,  BIN : 00001011, HEX : 0x0B, DEC : 11

                        request.set_value(led_0, Value(int(b_value[7])))
                        request.set_value(led_1, Value(int(b_value[6])))
                        request.set_value(led_2, Value(int(b_value[5])))
                        request.set_value(led_3, Value(int(b_value[4])))

                        request.set_value(led_4, Value(int(b_value[3])))
                        request.set_value(led_5, Value(int(b_value[2])))
                        request.set_value(led_6, Value(int(b_value[1])))
                        request.set_value(led_7, Value(int(b_value[0])))



                        time.sleep(1/10)

            except KeyboardInterrupt:
                print("Program interrupted")

            finally:
                # Release the pin when finished
                request.release()
                chip.close()


if __name__ == '__main__':
    fun_led_gpiod_test()
