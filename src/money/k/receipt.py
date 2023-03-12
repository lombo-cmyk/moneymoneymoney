import tempfile
from math import isclose
from typing import List, Optional

import pytesseract
from pdf2image import convert_from_path
from PIL import Image

from money.k.exceptions import ParsingException
from money.k.product import Product


class Receipt:
    def __init__(
        self, receipt_path: str, city: str, poppler_path: Optional[str] = None
    ) -> None:
        self._receipt_path = receipt_path
        self._poppler = poppler_path
        self._city = city
        self._products: Optional[List[Product]] = None
        self._total: Optional[str] = None
        self._date: Optional[str] = None

    @property
    def products(self):
        if self._products is None:
            raise ValueError("Products don't exist. Did you run create_receipt?")
        return self._products

    @property
    def total(self):
        if self._total is None:
            raise ValueError("Total doesn't exist. Did you run create_receipt?")
        return self._total

    @property
    def date(self):
        if self._total is None:
            raise ValueError("Date doesn't exist. Did you run create_receipt?")
        return self._total

    def create_receipt(self, validate: Optional[bool] = True) -> None:
        receipt_raw = self._get_raw_receipt()

        products = self._extract_products(receipt_raw)
        prices = self._extract_prices(receipt_raw)
        date = self._extract_date(receipt_raw)

        receipt_total = prices.pop()
        if validate:
            self._validate_parsing(products, prices, receipt_total)

        self._products = [
            Product(article, price) for article, price in zip(products, prices)
        ]
        self._total = receipt_total
        self._date = date

    def _get_raw_receipt(self):
        page = convert_from_path(self._receipt_path, 500, poppler_path=self._poppler)[0]
        with tempfile.TemporaryDirectory() as tmpd:
            tmp_path = f"{tmpd}out.png"
            page.save(tmp_path, "PNG")
            return pytesseract.image_to_string(Image.open(tmp_path))

    def _extract_products(self, receipt: str) -> List[str]:
        return (
            receipt.replace("\n\n", "\n")
            .split(f"{self._city}\n")[1]
            .split("Total")[0]
            .splitlines()
        )

    @staticmethod
    def _extract_prices(receipt: str) -> List[str]:
        return (
            receipt.replace("\n\n", "\n")
            .split("Price PLN\n")[1]
            .split("Tax")[0]
            .replace(",", ".")
            .splitlines()
        )

    @staticmethod
    def _extract_date(receipt: str) -> str:
        return (
            receipt.replace("\n\n", "\n")
            .split("Date: ")[1]
            .split("Receipt:")[0]
            .strip()
        )

    @staticmethod
    def _validate_parsing(products, prices, receipt_total) -> bool:
        if not len(prices) == len(products):
            raise ParsingException(
                f"Number of products {products} != {prices} Number of " f"prices found!"
            )

        calculated_sum = sum([float(el) for el in prices])

        if not isclose(float(receipt_total), calculated_sum, abs_tol=0.01):
            raise ParsingException(
                f"Calculated sum {calculated_sum} != {receipt_total} "
                f"Receipt total sum!"
            )

        return True

    def __repr__(self):
        if not self._products or not self._total:
            return ""
        r = "".join([str(el) + "\n" for el in self._products])
        r += Product.REPR_SIZE * "-" + "\n"
        empty_space_total = Product.REPR_SIZE - len("Total") - len(self._total)
        r += f"Total{empty_space_total * ' '}{self._total}\n"
        empty_space_date = Product.REPR_SIZE - len("Date") - len(self._date)
        r += f"Date{empty_space_date * ' '}{self._date}"
        return r
