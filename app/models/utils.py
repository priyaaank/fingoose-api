class RoundingMixin:
    def round_amount(self, amount):
        """Round amount to nearest rupee"""
        return round(amount) if amount is not None else None 