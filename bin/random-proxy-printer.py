#!/usr/bin/env python
import asyncio
from Adafruit_LED_Backpack import SevenSegment
from argparse import ArgumentParser
from atexit import register
from escpos.printer import Serial
from evdev import InputDevice, categorize, ecodes
from io import BytesIO
from json import loads
from PIL import Image
from sqlite3 import connect, Row


class RandomProxyPrinter:
    def __init__(self, printer, display, knob, button, connection, asyncio):
        self.printer = printer
        self.display = display
        self.knob = knob
        self.button = button
        self.connection = connection
        self.asyncio = asyncio
        self.value = 0

        self.update_display()

    def __del__(self):
        self.clear_display()

    async def _handle_event(self, device):
        async for event in device.async_read_loop():
            if event.type == 1 and event.value == 1:
                cursor = self.connection.cursor()
                cursor.execute("SELECT * FROM cards WHERE value = ? ORDER BY RANDOM() LIMIT 1", (str(self.value)))
                card = cursor.fetchone()

                self.printer.image(Image.open(BytesIO(card["illustration"])), impl="bitImageColumn")
                self.printer.text(card["description"] + "\n\n\n\n")

                cursor.close()
            elif event.type == 2:
                if event.value == 1:
                    self.value += 1

                    if self.value == 14:
                        self.value = 15
                    else:
                        self.value %= 17
                else:
                    self.value -= 1

                    if self.value == 14:
                        self.value = 13
                    else:
                        self.value %= 17

                self.update_display()

    def clear_display(self):
        self.display.clear()
        self.display.write_display()

    def update_display(self):
        display.clear()

        tens = int(self.value/10)
        if tens > 0:
            display.set_digit(2, tens)

        display.set_digit(3, self.value % 10)
        display.write_display()

    def run(self):
        asyncio.ensure_future(self._handle_event(self.knob))
        asyncio.ensure_future(self._handle_event(self.button))

        loop = self.asyncio.get_event_loop()
        loop.run_forever()


if __name__ == "__main__":
    parser = ArgumentParser(description="Random proxy printer daemon")
    parser.add_argument("-d", "--database-path", help="Path to random proxy printer SQLite database", required=True, dest="database_path")
    parser.add_argument("-k", "--knob", help="Path to input event device for the knob", required=True)
    parser.add_argument("-b", "--button", help="Path to input event device for the button", required=True)
    parser.add_argument("-a", "--display-address", help="I2C address for the seven segment display", dest="display_address", required=True)
    parser.add_argument("-p", "--printer", help="Path to printer device", required=True)
    parser.add_argument("-r", "--printer-baudrate", help="Printer baudrate", default=19200, dest="baudrate")

    args = parser.parse_args()

    display = SevenSegment.SevenSegment(address=int(args.display_address, 16))
    display.begin()
    display.clear()

    knob = InputDevice(args.knob)
    knob.grab()

    button = InputDevice(args.button)
    button.grab()

    printer = Serial(args.printer, baudrate=args.baudrate)
    printer.hw("RESET")

    connection = connect(args.database_path)
    connection.row_factory = Row

    proxy_printer = RandomProxyPrinter(printer, display, knob, button, connection, asyncio)
    register(proxy_printer.clear_display)
    proxy_printer.run()
