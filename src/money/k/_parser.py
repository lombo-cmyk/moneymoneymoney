import argparse

parser = argparse.ArgumentParser(
    prog="MoneyMoneyMoney.k",
    description="Parse receipts",
)

parser.add_argument(
    "-r",
    "--receipt",
    dest="receipt",
    help="Path to the receipt to parse. Relative to execution directory.",
    type=str,
)

parser.add_argument(
    "-c",
    "--city",
    dest="city",
    help="Shop's city. Needed for parsing purposes.",
    type=str,
)

parser.add_argument(
    "-t",
    "--tesseract",
    dest="tesseract",
    default="",
    help="Path to tesseract-OCR executable. Must be provided if not in PATH.",
    type=str,
)

parser.add_argument(
    "-p",
    "--poppler",
    dest="poppler",
    default="",
    help="Path to poppler executable. Must be provided if not in PATH.",
    type=str,
)

args = parser.parse_args()
