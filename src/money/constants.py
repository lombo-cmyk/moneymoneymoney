from enum import Enum


class Header(str, Enum):
    TRANSACTION_DATE = "Data transakcji"
    POSTING_DATE = "Data księgowania"
    RECEIVER_DATA = "Dane kontrahenta"
    TITLE = "Tytuł"
    ACCOUNT_NR = "Nr rachunku"
    BANK_NAME = "Nazwa banku"
    DETAILS = "Szczegóły"
    TRANSACTION_NR = "Nr transakcji"
    AMOUNT = "Kwota transakcji (waluta rachunku)"
    CURRENCY_AMOUNT = "Waluta"
    BLOCKED_AMOUNT = "Kwota blokady/zwolnienie blokady"
    CURRENCY_BLOCKED = "Waluta.1"
    PAYMENT_AMOUNT_IN_CURRENCY = "Kwota płatności w walucie"
    CURRENCY_PAYMENT_AMOUNT_IN_CURRENCY = "Waluta.2"
    BALANCE_AFTER_TRANSACTION = "Saldo po transakcji"
    CURRENCY_BALANCE_AFTER_TRANSACTION = "Waluta.3"
