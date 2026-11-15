

def print_summary(result: dict) -> None:
    clean_orders = result["clean_orders"]
    rejected_orders = result["rejected_orders"]

    print(clean_orders)
    print(rejected_orders)