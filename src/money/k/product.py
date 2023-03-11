class Product:
    REPR_SIZE = 35

    def __init__(self, name: str, price: str) -> None:
        self.name = name
        self.price = price

    def __repr__(self):
        spaces = self.REPR_SIZE - len(self.name) - len(self.price)
        spaces = spaces if spaces else 0
        return f"{self.name}{spaces * ' '}{self.price}"
