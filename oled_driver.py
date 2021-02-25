#!/usr/bin/env python3

from board import SCL, SDA
import busio
from oled_text import OledText, Layout32, BigLine, SmallLine
import os
import time

display_width = [12, 16, 18]
layouts = [{0: BigLine(0, 8, font='DejaVuSans.ttf', size=20)},
           {0: BigLine(0, 1, font='DejaVuSans.ttf', size=14), 1: BigLine(0, 17, font='DejaVuSans.ttf', size=14)},
           {0: SmallLine(0, 0, font='DejaVuSans.ttf', size=10), 1: SmallLine(0, 11, font='DejaVuSans.ttf', size=10), 2: SmallLine(0, 22, font='DejaVuSans.ttf', size=10)}
           ]
WIDTH = 18
HEIGHT = 3
logFile = "/tmp/display"
i2c = busio.I2C(SCL, SDA)
# Create the display, pass its pixel dimensions
oled = OledText(i2c, 128, 32)
oled.layout = layouts[0]
data = []
current_row = 0


def split_to_width(input_text):
    parsed_len = 0
    in_len = len(input_text)
    ret_data = []
    while parsed_len < in_len:
        ret_data.append(input_text[0:WIDTH])
        parsed_len += WIDTH
        input_text = input_text[WIDTH:]

    return ret_data


def parse_data():
    global data

    data = []
    # Populate rows to display
    file = open(logFile, "r")
    lines = file.readlines()
    for line in lines:
        text_data = line.strip().replace('\n', '')
        data.extend(split_to_width(text_data))

    file.close()


def populate_data():
    global HEIGHT
    global WIDTH

    layout_id = 0
    while layout_id < len(display_width):
        HEIGHT = layout_id + 1
        WIDTH = display_width[layout_id]
        oled.layout = layouts[layout_id]

        parse_data()

        if len(data) > HEIGHT:
            layout_id += 1
        else:
            break


try:
    while True:
        time.sleep(2)
        data = []

        # Populate rows to display
        if os.path.exists(logFile):
            populate_data()
            row_count = len(data)

            # display HEIGHT number of rows starting from current
            for row in range(0, HEIGHT):
                if current_row >= row_count:
                    oled.text("", row)
                else:
                    oled.text(data[current_row], row)
                    current_row += 1
                    if row == 2:
                        current_row -= 1

            if (current_row >= row_count) or (row_count < 4):
                current_row = 0
                time.sleep(1)

except KeyboardInterrupt:
    pass
finally:
    oled.layout = layouts[0]
    oled.text("------------", row)

