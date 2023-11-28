import json
import random
from datetime import date, datetime, timedelta
from calendar import monthrange
import logging
from argparse import ArgumentParser, ArgumentDefaultsHelpFormatter
import os, sys
import glob

LOAN_REJECT_TEMPLATE = "./rejected.json"
LOAN_APPROVE_TEMPLATE = "./approved.json"
APPROVED_LABEL = 'Approved'
REJECTED_LABEL = 'Rejected'

# magic numbers ... define here, use in code
MINIMUM_CREDIT_SCORE = 600
MAXIMUM_CREDIT_UTILIZATION = 0.25
MINIMUM_MONTHLY_INCOME = 10000

def process_loans(loan_dir):
    """process_loans(loan_dir), reads from directory, generates Approval/Reject of loan criteria ... well, criteria is limited
       returns a tuple of (loans_approved, loans_rejected)
    """
    loans_approved: int = 0
    loans_rejected: int = 0

    # to whoever read this module ... glob() is a great function for reading directory entries, it does NOT support
    # full regular expressions ... below mask will handle file system files ... TODO: test with S3fs module ...
    for loan_application_file_name in glob.glob(f"{loan_dir}/L*[0-9].json"):
        # validate we can read the file ...
        if not os.access(loan_application_file_name, os.R_OK):
            log.exception(f'Exception: cannot read input file or directory [{loan_application_file_name}] ...')
            continue
        with open(loan_application_file_name, "r") as input_file:
            loan_application_json = json.loads(input_file.read())
            log.debug(f"{json.dumps(loan_application_json, indent=2)}\n")
            try:
                credit_score = loan_application_json['credit']['creditScore']
                credit_utilization = loan_application_json['credit']['creditUtilization']
                monthly_income = loan_application_json['credit']['monthlyIncome']
            except KeyError as ke:
                log.exception(ke)
                log.exception(f'exception processing JSON application file [{loan_application_file_name}], {ke}')

            if credit_score > MINIMUM_CREDIT_SCORE:
                loan_status = (APPROVED_LABEL)
                loan_reason = ('Approved credit_score')
            else:
                loan_reason = "credit_score insufficient"
                if credit_utilization < MAXIMUM_CREDIT_UTILIZATION:
                    loan_status = (APPROVED_LABEL)
                    loan_reason = ('Approved creditUtilization')
                else:
                    loan_reason = f"{loan_reason}, creditUtilization exceeded"
                    if monthly_income > MINIMUM_MONTHLY_INCOME:   # yeah, its a big number ... I gave myself a raise!
                        loan_status = (APPROVED_LABEL)
                        loan_reason = ('Approved monthlyIncome')
                    else:
                        loan_status = (REJECTED_LABEL)
                        loan_reason = ('below credit_score, creditUtilization exceeded, income not sufficient')

            if loan_status == APPROVED_LABEL:
                fname = LOAN_APPROVE_TEMPLATE
                loans_approved += 1
            else:
                fname = LOAN_REJECT_TEMPLATE
                loans_rejected += 1

            with open(fname, "r") as f:
                loan_response_json = json.loads(f.read())
                if loan_status == APPROVED_LABEL:
                    loan_response_json[0]["status"] = APPROVED_LABEL
                else:
                    loan_response_json[0]["status"] = REJECTED_LABEL
                # copy some details from Application to Response ...
                loan_response_json[0]['borrower'] = loan_application_json['borrower']
                loan_response_json[0]['loanId'] = loan_application_json['borrower']['loanId']
                loan_response_json[0]["loanDetails"] = loan_application_json['loanDetails']
                loan_response_json[0]["ficoScore"] = loan_application_json['credit']['creditScore']
                loan_response_json[0]["Reason"] = loan_reason

                today = datetime.now()
                application_date = today.strftime("%Y-%m-%d")
                disbursement_date = (datetime.strptime(application_date, "%Y-%m-%d") + timedelta(days=3)).strftime("%Y-%m-%d")
                loan_response_json[0]["disbursementDate"] = disbursement_date

                days_in_month = lambda dt: monthrange(dt.year, dt.month)[1]
                first_day = today.replace(day=1) + timedelta(days_in_month(today))
                loan_response_json[0]["firstDueDate"] = first_day.strftime("%Y-%m-%d")
                loan_response_json[0]["firstPaymentAmount"] = 1500
                logging.debug(f'populating the response [{fname}] file')

                # write the response JSON object (to same directory)
                loan_id = loan_application_json['borrower']['loanId']
                loan_status = loan_response_json[0]["status"].lower()
                response_file = f"{loan_dir}/{loan_id }_{loan_status}.json"
                try:
                    with open(response_file, "w") as outfile:
                        json.dump(loan_response_json[0], outfile)
                        log.debug(f'wrote the JSON response [{response_file}] file')
                except (FileNotFoundError, PermissionError, OSError):
                    log.exception(f"Exception writing JSON output file[{response_file}]")

    return (loans_approved, loans_rejected)

# some arguments here to change the run-time of the function
# -D 20
# -D 10 --loan_dir /tmp
if __name__ == '__main__':
    '''start-up logger, parse arguments and kick off processing of loans!'''
    source_file = sys.argv[0].split('/')[-1]
    log = logging.getLogger(source_file)
    logging.basicConfig(level=logging.INFO)
    #logging.basicConfig(level=logging.DEBUG)

    # Parse command line arguments
    parser = ArgumentParser(formatter_class=ArgumentDefaultsHelpFormatter)
    parser.add_argument("-D", "--debug", default=logging.INFO, type=int,
                        help=f"debug level Debug:{logging.DEBUG} to Info:{logging.INFO}")
    parser.add_argument("-l", "--loan_dir", default='/tmp/', type=str, help="loan dir to process")

    args = vars(parser.parse_args())

    log.info(f'{source_file} is startup')

    # set to level passed in
    logging.getLogger().setLevel(args["debug"])
    # if you get tired of passing in DEBUG flag for Logging ...
    #logging.getLogger().setLevel(logging.DEBUG)
    loan_dir = args["loan_dir"]

    log.debug(f'{args}')

    loans_approved, loans_rejected = process_loans(loan_dir)
    log.info(f'Loan applications processed: {loans_approved+loans_rejected}, approved: {loans_approved}, rejected: {loans_rejected}')
    sys.exit(0)
