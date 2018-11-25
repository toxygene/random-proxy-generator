#!/usr/bin/env python
from argparse import ArgumentParser
from escpos.printer import Serial
from io import BytesIO
from PIL import Image
from sqlite3 import connect, Row


if __name__ == "__main__":
    parser = ArgumentParser(description="Print an illustration for a card by ID")
    parser.add_argument("id", help="ID of the card to print")
    parser.add_argument("-d", "--database-path", help="Path to RandomProxyPrinter basic database", required=True, dest="database_path")
    parser.add_argument("-p", "--printer", help="Path to printer device", required=True)

    args = parser.parse_args()

    printer = Serial(args.printer, baudrate=19200)
    connection = connect(args.database_path)
    connection.row_factory = Row
    cursor = connection.cursor()

    cursor.execute("SELECT illustration FROM cards WHERE id = ?", (args.id,))
    row = cursor.fetchone()

    printer.image(Image.open(BytesIO(row["illustration"])), impl="bitImageColumn")

