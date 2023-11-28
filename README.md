
# loan_origination.py 
Generates Loan Origination JSON object, stores in directory (-d /tmp/). JSON files are unique LoanID for running many times (uses Linux epoc timestamp)

```
$ python loan_origination.py -d /tmp/ -n 100    # note: tested on macos ... windows path separator may cause issue
INFO:loan_origination.py:loan_origination.py startup
INFO:loan_origination.py:Generated 100 Loan Origination JSON files in [/tmp/]
```

# loan_process.py
Processes Loan Origination JSON files from above generator.

## loan 'scoring' for Approval
extracts attributes from the Loan Origination JSON, credit_score (aka fico), credit_utiliization, and monthly_income
| test/rules | status |
| ----- | ----- |
| if credit_score > MINIMUM_CREDIT_SCORE | __Approved__ |
| if credit_utilization < MAXIMUM_CREDIT_UTILIZATION | __Approved__ |
| if monthly_income > MINIMUM_MONTHLY_INCOME | __Approved__ |
| if above rules fail ... | __Rejected__ |

if above 'test/rules' do not pass, JSON "Reason" is populated and Loan is __Rejected__

file name is **/tmp/\<LoanID>_accepted.json** or **/tmp/\<LoanID>_rejected.json**

```
$ python loan_process.py      
INFO:loan_process.py:loan_process.py is startup
INFO:loan_process.py:Loan applications processed: 100, approved: 68, rejected: 32
```
