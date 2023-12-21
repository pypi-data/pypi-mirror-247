class Reverse:
    def __init__(self, value) -> None:
        self.value = -value

    def __add__(self, other):
        return self.value - other.value

    def __sub__(self, other):
        return self.value + other.value

    def __repr__(self) -> str:
        return str(self.value)
