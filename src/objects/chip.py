class Chip:
    def __init__(self, count: int):
        self.count = count

    def __add__(self, other):
        if isinstance(other, Chip):
            return Chip(self.count + other.count)
        if isinstance(other, int):
            return Chip(self.count + other)
        raise ValueError()

    def __repr__(self):
        return f"Chip(count={self.count})"

    def __str__(self):
        return f"{self.count}"
