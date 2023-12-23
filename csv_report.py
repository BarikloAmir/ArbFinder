import csv
from datetime import datetime


def sum_benefits(csv_filename):
    rial_total_benefit = 0
    usdt_total_benefit = 0

    with open(csv_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        # Extract times from the 'Time' column and convert them to datetime objects
        times = [datetime.strptime(row['Timestamp'], '%Y-%m-%d %H:%M:%S') for row in reader]

    # Find the minimum and maximum timestamps
    min_time = min(times)
    max_time = max(times)

    # Read the CSV file again to process rows
    with open(csv_filename, 'r') as csvfile:
        reader = csv.DictReader(csvfile)

        for row in reader:
            # Assuming the column names are 'Symbol', 'Action', 'Benefit', and 'Time'
            symbol = row['Symbol (NOBITEX)']
            action = int(row['Action'])
            benefit = float(row['Benefit'])
            percent = float(row["Percent"])
            sell_price = float(row["Sell Price"])
            buy_price = float(row["Buy Price"])
            buy_side, sell_side = str(row["Buy Side"]), str(row["Sell Side"])
            volume = float(row["Our trading volume"])

            quote = "tether"
            fe = 0.0013
            if "IRT" in symbol:
                quote = "rial"
                fe = 0.0025

            if buy_side == "nobitex":
                wage = buy_price * volume * fe
            else:
                wage = sell_price * volume * fe

            if "IRT" in symbol and action == 1 and percent > 1 + fe:
                if benefit - wage > 0:
                    rial_total_benefit += benefit - wage
                if benefit - wage < 0:
                    print(benefit - wage)
                continue
            if "USDT" in symbol and action == 1 and percent > 1 + fe:
                if benefit - wage > 0:
                    usdt_total_benefit += benefit - wage
                if benefit - wage < 0:
                    print(benefit - wage)

    time_diff = max_time - min_time

    print('Total Benefit for IRT Symbols with Action 1:', rial_total_benefit, 'RIAL')
    print('Total Benefit for USDT Symbols with Action 1:', usdt_total_benefit, 'USDT')
    print('Time difference between the first and last timestamps:', time_diff)


csv_filename = 'arbitrage_data_v2.csv'
sum_benefits(csv_filename)
