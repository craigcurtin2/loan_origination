import random
from datetime import datetime, timedelta


def get_random_name():
    names = ["John", "Jane", "Bob", "Alice", "Charlie", "Eve", "Susan", "Julie", "Linda", "Charles"]
    return random.choice(names)

def get_random_dob():
    start_date = datetime(1950, 1, 1)
    end_date = datetime(2002, 12, 31)
    random_dob = start_date + timedelta(days=random.randint(0, (end_date - start_date).days))
    return random_dob.strftime("%Y-%m-%d")
