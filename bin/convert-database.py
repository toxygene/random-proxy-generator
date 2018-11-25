#!/usr/bin/env python
from argparse import ArgumentParser
from io import BytesIO
from PIL import Image
from sqlite3 import Binary, connect, Row
from sys import stderr, stdout
from traceback import print_exc
from unidecode import unidecode


if __name__ == "__main__":
    parser = ArgumentParser(description="Converts the contents of the database for final usage")
    parser.add_argument("-d", "--database-path", help="Path to random proxy printer SQLite database", required=True)
    parser.add_argument("-v", "--verbose", action="store_true")

    args = parser.parse_args()

    with connect(args.database_path, isolation_level=None) as connection:
        connection.row_factory = Row

        cursor = connection.cursor()

        cursor.execute("SELECT * FROM cards")
        cards = cursor.fetchall()

        for card in cards:
            if args.verbose:
                print(f"resizing and converting '{card[name]}' ({card[id]})", file=stdout)

            try:
                with Image.open(BytesIO(card["illustration"])) as image:
                    if image.width > 384:
                        height = image.height * int(384/image.width)
                        image.thumbnail((384, height), Image.BICUBIC)

                    image = image.convert("L")
                    image = image.quantize(colors=8)

                    with BytesIO() as converted_image:
                        image.save(converted_image, format="PNG", optimize=True)

                        cursor.execute("UPDATE cards SET description = ?, illustration = ? WHERE id = ?", (unidecode(card["description"]), Binary(converted_image.getvalue()), card["id"]))
            except:
                print(f"An error occurred while resizing and converting '{card[1]}'", file=stderr)

                if args.verbose:
                    print_exc(file=stderr)
        
        cursor.execute("VACUUM")
        cursor.close()
