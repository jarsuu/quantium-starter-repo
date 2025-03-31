import csv
import pandas as pd
import glob

PRODUCT_FILTER = "pink morsel"

def concat_data():
    path = "data/*.csv"
    data_files = sorted(glob.glob(path))

    li = []
    for data_file in data_files:
        df = pd.read_csv(data_file, index_col=None, header=0)
        li.append(df)

    frame = pd.concat(li, axis=0, ignore_index=True)

    return frame


def filter_pink_morsel(frame):
    return frame[frame["product"] == PRODUCT_FILTER]


def calculate_sale(quantity: int, price: str):
    price = float(price[1:])
    sales = round(quantity * price, 2)

    return "{:.2f}".format(sales)

def extract_data(frame):
    with open("processed_data.csv", mode="w") as processed_file:
        processed_writer = csv.writer(
            processed_file, delimiter=",", quotechar='"', quoting=csv.QUOTE_MINIMAL)

        processed_writer.writerow(["sales", "date", "region"])

        for _, row in frame.iterrows():
            sales = calculate_sale(row["quantity"], row["price"])
            processed_writer.writerow([sales, row["date"], row["region"]])

if __name__ == "__main__":
    frame = concat_data()
    pink_morsel_only_frame = filter_pink_morsel(frame)
    
    extract_data(pink_morsel_only_frame)
