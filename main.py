

from config import load_config
from pipeline import run_pipeline
from reporting import print_summary



def main():
    orders_config, expected_columns_orders = load_config("ORDERS")
    result = run_pipeline(orders_config.input_path, orders_config.output_dir, expected_columns_orders)

    print_summary(result)



if __name__ == "__main__":
    main()