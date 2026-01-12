class Calculator:

    @staticmethod
    def multiply(a: int, b: int) -> int:
        return a * b

    @staticmethod
    def calculate_total(*values: float) -> float:
        return sum(values)

    @staticmethod
    def per_day(total: float, days: int) -> float:
        return total / days if days > 0 else 0
