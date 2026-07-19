import random
from pathlib import Path

import yaml

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


def generate_patient_data(profile_data):
    patient = {
        "name": get_random_name(),
        "age": get_random_age(),
        "sex": get_random_sex(),
        "smoking_status": get_random_smoking_status(),
        "comorbidities": random.sample(
            profile_data["common_comorbidities"], k=random.randint(0, 2)
        ),
    }
    return patient


def get_profile_data(a: str):
    BASE_DIR = Path(__file__).resolve().parent.parent
    profile_path = BASE_DIR / "diagnosis_profiles" / "profiles" / f"{a}.yaml"
    profile_data = yaml.safe_load(profile_path.read_text())
    return profile_data


# print(__name__)
