

from decimal import Decimal, InvalidOperation
from models import Order

def normalize_orders(raw_orders: list[dict]) -> tuple[list[Order], list[dict]]:
    clean_orders = []
    rejected_orders = []
    for raw_order in raw_orders:
        order_id = int(raw_order["order_id"])
        if order_id <= 0:
            raise ValueError(f"order_id: {order_id} must be positive")
        customer_name = raw_order["customer_name"].strip()
        if customer_name == "":
            rejected_orders.append(raw_order)
        status = raw_order["status"].strip()
        if status not in {"paid", "pending", "cancelled"}:
            rejected_orders.append(raw_order)
        amount = Decimal(raw_order["amount"].replace(",", "."))
        if amount < 0 or not amount.is_finite():
            rejected_orders.append(raw_order)
        country = raw_order.get("country", "UNKNOWN")
        if country is None or country.strip() == "":
            country = "UNKNOWN"
        note = raw_order.get("note", "").strip()

        clean_order = {
            "order_id": order_id,
            "customer_name": customer_name,
            "status": status,
            "amount": amount,
            "country": country,
            "note": note,
        }
        clean_orders.append(clean_order)

    return build_orders_obj(clean_orders), rejected_orders



def build_orders_obj(orders: list[Order]) -> list[Order]:
    orders_obj = []
    for order in orders:
        order_obj = Order(order["order_id"], order["customer_name"], order["status"], order["amount"], order["country"], order["note"])
        orders_obj.append(order_obj)
    return orders_obj


def normalize_order(raw_order: dict) -> dict:
    for field in ("order_id", "customer_name", "status", "amount", "country", "note"):
        if not isinstance(raw_order[field], str):
            raise TypeError(f"{field} must be text")

    order_id = int(raw_order["order_id"].strip())
    if order_id < 0:
        raise ValueError(f"order_id: {order_id} must be positive")

    customer_name = raw_order["customer_name"].strip().title()
    if customer_name == "":
        raise ValueError(f"customer_name: {customer_name} cannot be empty")

    status = raw_order["status"].strip().lower()
    if status not in {"paid", "pending", "cancelled"}:
        raise ValueError(f"Unsupported status: {status!r}")

    try:
        amount = Decimal(raw_order["amount"].strip().replace(",","."))
    except InvalidOperation as exc:
        raise ValueError(f"Invalid amount: {raw_order["amount"]}") from exc
    if not amount.is_finite() or amount < 0:
        raise ValueError(f"Amount: {amount} must be finite and non-negative")

    return {
        "order_id": order_id,
        "customer_name": customer_name,
        "status": status,
        "amount": amount,
        "country": raw_order["country"].strip().upper() or "UNKNOWN",
        "note": raw_order["note"].strip(),
    }

def transform_orders(raw_orders: list[dict], source_file: str) -> tuple[list[dict], list[dict]]:
    clean_orders = []
    rejected_orders = []
    accepted_ids = set()

    for record_number, raw_order in enumerate(raw_orders, start=1):
        try:
            clean_order = normalize_order(raw_order)
            if raw_order["order_id"] in accepted_ids:
                raise ValueError(f"Duplicate order_id: {raw_order["order_id"]}")
        except (ValueError, TypeError) as exc:
            rejected_orders.append({
                "source_file": source_file,
                "record_number": record_number,
                "raw_order_id": raw_order.get("order_id"),
                "error_type": type(exc).__name__,
                "reason": str(exc),
            })
        else:
            accepted_ids.add(raw_order["order_id"])
            clean_orders.append(clean_order)

    return clean_orders, rejected_orders



