import os

import pytesseract

from money.k._parser import args
from money.k.receipt import Receipt


def main():

    if args.tesseract:
        pytesseract.pytesseract.tesseract_cmd = args.tesseract

    poppler_path = args.poppler if args.poppler else None

    receipt_path = os.path.join(os.getcwd(), args.receipt)

    receipt = Receipt(receipt_path, args.city, poppler_path)
    receipt.create_receipt()
    print(receipt)


if __name__ == "__main__":
    main()
