import random
from datetime import datetime, timedelta
from pathlib import Path

import pandas as pd

from config import (
    START_DATE,
    NUMBER_OF_DAYS,
    ROWS_PER_DAY,
    OUTPUT_FOLDER,
    RANDOM_SEED,
)

from master_data import (
    get_random_product,
    get_random_store,
    get_random_payment_mode,
    get_random_discount,
    get_price,
)

random.seed(RANDOM_SEED)


def generate_sale(sale_number, sale_date):

    sale_id = f"S{sale_number:09d}"

    customer_id = f"C{random.randint(1,50000):05d}"

    product_id, product_name, category = get_random_product()

    store_id, city, state = get_random_store()

    payment_mode = get_random_payment_mode()

    quantity = random.randint(1, 5)

    unit_price = get_price(category)

    discount = get_random_discount()

    total_amount = round(
        quantity * unit_price * (1 - discount / 100),
        2
    )

    return {
        "sale_id": sale_id,
        "sale_date": sale_date.strftime("%Y-%m-%d"),
        "customer_id": customer_id,
        "product_id": product_id,
        "product_name": product_name,
        "category": category,
        "quantity": quantity,
        "unit_price": unit_price,
        "discount_pct": discount,
        "total_amount": total_amount,
        "city": city,
        "state": state,
        "store_id": store_id,
        "payment_mode": payment_mode,
    }


def main():

    OUTPUT_FOLDER.mkdir(exist_ok=True)

    start_date = datetime.strptime(
        START_DATE,
        "%Y-%m-%d"
    )

    sale_counter = 1

    for day in range(NUMBER_OF_DAYS):

        current_date = start_date + timedelta(days=day)

        records = []

        for _ in range(ROWS_PER_DAY):

            records.append(
                generate_sale(
                    sale_counter,
                    current_date
                )
            )

            sale_counter += 1

        df = pd.DataFrame(records)

        file_name = (
            f"sales_{current_date.strftime('%Y_%m_%d')}.csv"
        )

        df.to_csv(
            OUTPUT_FOLDER / file_name,
            index=False
        )

        print(f"Generated {file_name}")


if __name__ == "__main__":
    main()