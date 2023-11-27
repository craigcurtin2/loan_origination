import csv
import random
import sys
from datetime import datetime, timedelta
import collections
import time

from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import warnings
import errno
import logging


warnings.simplefilter("ignore")

# Define the CSV headers
csv_headers = [
    "DateOfService",
    "TimeOfService",
    "sourceMerchant",
    "merchantId",
    "merchantZip",
    "accountNumber",
    "accountName",
    "accountZipcode",
    "amount",
    "tip",
    "finalAmount"
]

# Generate and format ISO8601 timestamp for today


# Create a list of source merchants
Merchant = collections.namedtuple("Merchant", "name merchantId merchantZip merchantType")

source_merchants = [
    Merchant("B&H Video", "01234", 10024, 1),
    Merchant("Best Buy", "12345", 10023, 1),
    Merchant("Binny's Liquor Store", "67899", 10027, 1),
    Merchant("Ulysses", "98765", 10028, 0),
    Merchant("Red Lion", "87654", 10029, 0),
    Merchant("Terra Blues", "76543", 10022, 0)
]


def csv_writer(out_file_name, date_of_service, number_transactions):
    # test to see if we can write the output by ... yeah, writing the output
    try:
        with open(out_file_name, 'w') as f:
            # file opened for writing. write to it here
            log.debug(f"success opening [{out_file_name}]")
            pass
    except FileNotFoundError as exc:
        log.exception(f'if we are in Container is volume mounted? ... error {exc.errno} {exc.strerror}')
        if exc.errno == errno.EACCES:
            log.exception(f'{out_file_name} no perms')
        elif exc.errno == errno.EISDIR:
            log.exception(f'{out_file_name} is directory')
    except IOError as exc:
        log.exception(f'if we are in Container ... error {exc.errno} {exc.strerror}')
        if exc.errno == errno.EACCES:
            log.exception(f'{out_file_name} no perms')
        elif exc.errno == errno.EISDIR:
            log.exception(f'{out_file_name} is directory')

    # Open a CSV file for writing
    with open(out_file_name, mode="w", newline="") as csv_file:
        writer = csv.writer(csv_file)

        # Write the CSV headers
        writer.writerow(csv_headers)

        # Generate 10 transactions
        for _ in range(number_transactions):
            # Generate random data
            merchant_info = random.choice(source_merchants)
            account_number = "L" + str(random.randint(1000, 1050))
            account_name = ""
            account_zipcode = "accountZipcode = 10020"

            if account_number == "L1000":
                account_name = "Fred Blogs"
            elif account_number == "L1001":
                account_name = "Donald Trump"
            elif account_number == "L1002":
                account_name = "Greg Abbot"
            elif account_number == "L1003":
                account_name = "Joe Biden"
            elif account_number == "L1010":
                account_name = "Barack Obama"
            elif account_number == "L1020":
                account_name = "Jerry Springer"
            elif account_number == "L1030":
                account_name = "RL Burnside"
            elif account_number == "L1031":
                account_name = "David Muir"
            elif account_number == "L1032":
                account_name = "Lester Holt"
            elif account_number == "L1033":
                account_name = "Nora ODonnell"
            elif account_number == "L1034":
                account_name = "Eric Adams"
            elif account_number == "L1035":
                account_name = "Eric Adams"
            elif account_number == "L1036":
                account_name = "Eric Adams"
            elif account_number == "L1049":
                account_name = "Stevie Ray Vaughn"
            else:
                account_name = "Unknown Hooligan"

            time_of_service = today - timedelta(hours=random.randint(0, 23))
            # remove the date, just take time component
            formatted_time = time_of_service.strftime("%X")
            amount = round(random.uniform(0.01, 100), 2)
            tip = 0.2 * amount if "merchantType=0" in merchant_info else 0.0
            final_amount = amount + tip

            # Write the transaction to the CSV file
            transaction = [
                date_of_service,
                formatted_time,
                merchant_info.name,
                merchant_info.merchantId,
                merchant_info.merchantZip,
                account_number,
                account_name,
                account_zipcode,
                amount,
                tip,
                final_amount
            ]
            writer.writerow(transaction)


# some cmd line args for copy/paste testing
# -o "/tmp/transactions.csv" --number_transactions 23 --date_of_service "1970-01-01"
# --debug 10 -u -o "/tmp/transactions.csv" --number_transactions 12345 --date_of_service "1970-01-01"

if __name__ == '__main__':
    log = logging.getLogger("transactions")
    logging.basicConfig(level=logging.INFO)

    # set up the default values, will be overwritten by command line args
    file_name = "transactions.csv"
    number_transactions = 20
    today = datetime.now()
    formatted_date = today.strftime("%Y-%m-%d")

    # Parse command line arguments
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-D", "--debug", default=logging.INFO, type=int,
                        help=f"debug level Debug:{logging.DEBUG} to Info:{logging.INFO}")
    parser.add_argument("-d", "--date_of_service", default=formatted_date, type=str,
                        help="Date of service format: YYYY-MM-DD")

    parser.add_argument("-n", "--number_transactions", default=20, type=int, help="Number of Transactions to create")
    parser.add_argument("-o", "--out_file_name", default="transactions.csv", type=str, help="File name for output file")
    parser.add_argument("-u", "--unique", action="store_true", default=False,
                        help="Mangle File name with linux timestamp in output file name")

    args = vars(parser.parse_args())

    source_file = sys.argv[0].split('/')[-1]
    log.info(f'{source_file} is startup')

    logging.getLogger().setLevel(args["debug"])         # set to level passed in
    date_of_service = args["date_of_service"]
    number_transactions = args["number_transactions"]
    out_file_name = args["out_file_name"]
    make_file_name_unique = args["unique"]

    log.debug(f'{args}')
    out_file_name = out_file_name.strip()               # saw strange leading space from Container inserted lstrip()
    if make_file_name_unique:
        linux_ts = time.time()
        out_file_name = out_file_name[:-4] + f"_{linux_ts}" + out_file_name[-4:]
    log.debug(f'startup: outfile: [{out_file_name}], dateOfService: [{date_of_service}], numTransactions: [{number_transactions}]')
    csv_writer(out_file_name, date_of_service, number_transactions)

    log.info(f"{number_transactions} Transactions generated and written to [{out_file_name}]")
