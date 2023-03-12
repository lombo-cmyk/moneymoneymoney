import os

import pytesseract

from money.common._parser import parser
from money.common.receipt import Receipt

args = parser.parse_args()


def main():

    if not any([args.receipt, args.city]):
        raise Exception("Receipt and city are required to run this program.")

    if args.tesseract:
        pytesseract.pytesseract.tesseract_cmd = args.tesseract

    poppler_path = args.poppler if args.poppler else None

    receipt_path = os.path.join(os.getcwd(), args.receipt)

    receipt = Receipt(receipt_path, args.city, poppler_path)
    receipt.create_receipt()
    print(receipt)


if __name__ == "__main__":
    main()
