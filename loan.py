import json
import random
from datetime import datetime, timedelta
import logging
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import sys

from loan_utils import get_random_dob, get_random_name
def generate_loan():
    # Borrower details
    loan_id = f"L{random.randint(100000, 999999)}"
    first_name = get_random_name()
    last_name = get_random_name()
    email = f"{first_name.lower()}.{last_name.lower()}@example.com"
    phone = f"{random.randint(100, 999)}-{random.randint(100, 999)}-{random.randint(1000, 9999)}"
    address = f"{random.randint(1, 999)} {get_random_name()} St, Cityville"
    dob = get_random_dob()

    borrower = {
        "loanId": loan_id,
        "firstName": first_name,
        "lastName": last_name,
        "email": email,
        "phone": phone,
        "address": address,
        "dob": dob
    }

    # Loan details
    loan_amount = random.randint(20000, 50000)
    loan_type = "Auto Loan"
    term_months = random.choice([24, 36])
    application_date = "2023-04-15"
    disbursement_date = (datetime.strptime(application_date, "%Y-%m-%d") + timedelta(days=15)).strftime("%Y-%m-%d")

    loan_details = {
        "loanAmount": loan_amount,
        "loanType": loan_type,
        "termMonths": term_months,
        "applicationDate": application_date,
        "disbursementDate": disbursement_date
    }

    # Credit details
    credit_score = random.randint(400, 820)
    credit_history = "CCCCCCCCCCCCCCCCCC"
    credit_utilization = round(random.uniform(0.28, 0.90), 2)
    monthly_income = random.randint(3000, 9000)

    # Adjust 30% of loans to meet the specified criteria
    if random.random() <= 0.3:
        credit_score = random.randint(601, 820)
        credit_exposure = round(random.uniform(0.28, 0.39), 2)

    credit = {
        "creditScore": credit_score,
        "creditHistory": credit_history,
        "creditUtilization": credit_utilization,
        "monthlyIncome": monthly_income
    }

    # Create the loan JSON object
    loan_json = {
        "borrower": borrower,
        "loanDetails": loan_details,
        "credit": credit
    }

    return loan_json

if __name__ == '__main__':
    log = logging.getLogger("transactions")
    logging.basicConfig(level=logging.INFO)

    # set up the default values, will be overwritten by command line args

    # Parse command line arguments
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-D", "--debug", default=logging.INFO, type=int,
                        help=f"debug level Debug:{logging.DEBUG} to Info:{logging.INFO}")
    parser.add_argument("-n", "--number_loans", default=20, type=int, help="Number of Loan Applications to create")


    args = vars(parser.parse_args())

    source_file = sys.argv[0].split('/')[-1]
    log.info(f'{source_file} is startup')

    logging.getLogger().setLevel(args["debug"])
    number_loan_applications = args["number_loans"]
    # set to level passed in


    log.debug(f'{args}')

    # Generate 10 loan JSON objects
    loan_objects = [generate_loan() for _ in range(number_loan_applications)]
    # Print the generated JSON objects
    for index, loan_json_object in enumerate(loan_objects, start=1):
        fname_loanId = loan_json_object['borrower']['loanId']
        json_fname =f"/tmp/{fname_loanId}.json"
        with open(f'{json_fname}', "w") as f:
            f.write(json.dumps(loan_json_object, indent=2))

        log.debug(f"Loan {index}:\n{json.dumps(loan_json_object, indent=2)}\n")
