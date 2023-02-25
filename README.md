# MoneyMoneyMoney
Simple parser created to categorize customer transaction data that can be
imported by user from one on the Polish banks.

## Installation:
1. ``git clone https://github.com/lombo-cmyk/moneymoneymoney``
2. ``cd moneymoneymoney``
3. ``pip install .``


## Structure:
    .
    ├── output           # Rules and output file from execution will be stored here by default
    ├── logs             # Place for execution logs
    ├── transaction      # Default place to store transactions csv
    ├── src/money        # Sources, not interesting
    ├── test             # Empty, POG
    └── README.md        # We're here
While running the package from repo root directory it will utilise the
already existing folder structure (`output` and `logs` directories). If not it
will create these directories in place relative to current working
directory of execution.

## How to run:
1. Create rules by invoking:
```python -m money --create-rules```
   - It will create empty rules file and fill it with content provided
   throughout the execution.
   - Structure of the file will be as follows:

    | ID                                    | Dane kontrahenta                                       | Tytuł                          | Where                |
    |---------------------------------------|--------------------------------------------------------|--------------------------------|----------------------|
    | INT, Rule ID, generated automatically | STR, what to look for in money receiver / sender colum | STR, what to look for in title | STR, destination sum |
    | 1                                     | Janusz Papaj                                           | Czynsz                         | Opłaty               |

   - The sum summary of money from transactions to / from `Janusz Papaj` with
     `Czynsz` in title will be stored in `Opłaty`.
2. Process transactions file:
```python -m money -f path_to_transactions_file.csv```
    - Transaction file is expected to have column names starting at row 11
      (counting from 0) - The rows before are filled with some junk data
      about account owner :)

    | Dane kontrahenta     | Tytuł                      | Kwota transakcji  ( waluta rachunku ) | Waluta        |
    |----------------------|----------------------------|---------------------------------------|---------------|
    | STR, Contractor data | STR, Title                 | float, Amount                         | STR, Currency |
    | Janusz Papaj, Krakow | Czynsz - opłaty podstawowe | -2000                                 | PLN           |
    | Janusz Papaj, Krakow | Czynsz - opłaty dodatkowe  | -137,50                               | PLN           |
    | Janusz Maj, Krakow   | Media                      | -100                                  | PLN           |
    | Medioszex            | Wynagrodzenie              | 3100                                  | PLN           |
   - In this case the output will be:
   ```
                     sum
   General          3000
   Opłaty       -2137.50
   ```
