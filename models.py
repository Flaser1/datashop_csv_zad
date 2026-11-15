

from decimal import Decimal

class Order:
    def __init__(self, order_id: int, customer_name: str, status: str, amount: Decimal, country: str, note: str):
        if type(order_id) is not int:
            raise TypeError(f"order_id: {order_id} type must be int")
        if not isinstance(customer_name, str):
            raise TypeError(f"customer_name: {customer_name} must be str")
        if customer_name.strip() == "":
            raise ValueError(f"customer_name: {customer_name!r} cannot be empty")
        if not isinstance(status, str):
            raise TypeError(f"status: {status} must be str")
        if status.strip() == "":
            raise ValueError(f"status: {status!r} cannot be empty")
        if not isinstance(amount, Decimal):
            raise TypeError(f"amount: {amount} must be Decimal")
        if amount < 0 or not amount.is_finite():
            raise ValueError(f"amount: {amount} cannot be negative and must be finite")
        if not isinstance(country, str):
            raise ValueError(f"country {country} must be str")
        if country.strip() == "":
            raise ValueError(f"country: {country!r} cannot be empty")
        if not isinstance(note, str):
            raise ValueError(f"note: {note} must be str")
        self.order_id = order_id
        self.customer_name = customer_name.capitalize()
        self.status = status.strip().lower()
        self.amount = amount
        self.country = country.strip().upper()
        self.note = note.strip()
