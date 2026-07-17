import random

NAMES = [
    "John Jacob",
    "Jane Watson",
    "Alice Mathew",
    "Bob Hill",
    "Charlie Brown",
    "Diana Prince",
]


def get_random_name():
    return random.choice(NAMES)


def get_random_age(min_age=30, max_age=70):
    return random.randint(min_age, max_age)


def get_random_sex():
    return random.choice([" Male", "Female"])


def get_random_smoking_status():
    return random.choice(["Yes", "No"])


print(__name__)
