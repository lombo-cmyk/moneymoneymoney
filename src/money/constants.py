from enum import Enum
from itertools import chain


class IrrelevantHeader(str, Enum):
    POSTING_DATE = "Data księgowania"
    ACCOUNT_NR = "Nr rachunku"
    BANK_NAME = "Nazwa banku"
    DETAILS = "Szczegóły"
    TRANSACTION_NR = "Nr transakcji"
    BLOCKED_AMOUNT = "Kwota blokady/zwolnienie blokady"
    CURRENCY_BLOCKED = "Waluta.1"
    PAYMENT_AMOUNT_IN_CURRENCY = "Kwota płatności w walucie"
    CURRENCY_PAYMENT_AMOUNT_IN_CURRENCY = "Waluta.2"
    BALANCE_AFTER_TRANSACTION = "Saldo po transakcji"
    CURRENCY_BALANCE_AFTER_TRANSACTION = "Waluta.3"


class RelevantHeader(str, Enum):
    TRANSACTION_DATE = "Data transakcji"
    RECEIVER_DATA = "Dane kontrahenta"
    TITLE = "Tytuł"
    AMOUNT = "Kwota transakcji (waluta rachunku)"
    CURRENCY_AMOUNT = "Waluta"


Header = Enum(
    "Header", [(i.name, i.value) for i in chain(IrrelevantHeader, RelevantHeader)]
)


class RULES(str, Enum):
    ID = "ID"
    RECEIVER_DATA = "Dane kontrahenta"
    TITLE = "Tytuł"
    WHERE = "Where"
