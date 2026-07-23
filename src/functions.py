import random
from pathlib import Path

import yaml

from extractor import condition_extractor

FEMALE_NAMES = [
    "Jane Watson",
    "Alice Mathew",
    "Diana Prince",
]

MALE_NAMES = [
    "John Jacob",
    "Bob Hill",
    "Charlie Brown",
]


def get_random_name(sex=None):
    if sex == "Male":
        return random.choice(MALE_NAMES)
    elif sex == "Female":
        return random.choice(FEMALE_NAMES)
    else:
        return random.choice(MALE_NAMES + FEMALE_NAMES)


def get_random_age(min_age=30, max_age=90):
    return random.randint(min_age, max_age)


def get_random_sex():
    return random.choice(["Male", "Female"])


def get_random_smoking_status():
    return random.choice(["Yes", "No"])


def generate_condition_status():
    return random.choice(
        ["good", "moderate", "poor", "not managed", "first identification"]
    )


def generate_clinical_note_documentaion_style():
    choice = random.choice(["comprehensive", "standard", "concise"])
    if choice == "standard":
        return {
            "name": choice,
            "instructions": [
                "Routine outpatient documentation",
                "Focus on clinically relevant findings",
                "Moderate detail",
            ],
        }
    elif choice == "comprehensive":
        return {
            "name": choice,
            "instructions": [
                "Comprehensive history",
                "Full ROS",
                "Complete physical exam",
                "Expanded reasoning",
            ],
        }
    else:
        return {
            "name": choice,
            "instructions": [
                "Brief clinic documentation",
                "Essential positives and negatives only",
                "Short assessment and plan",
                "Avoid lengthy explanations",
            ],
        }


def generate_comorbidities_details(comorbidities, age):
    """
    Generate structured details for each comorbidity.

    Currently stores only the duration (in years).
    Additional metadata (e.g., stage, severity, management)
    can be added later.
    """
    comorbidity_details = {}

    max_duration = age - 30
    if max_duration <= 14:
        max_duration = 15

    for comorbidity in comorbidities:
        duration = random.randint(1, max_duration)

        comorbidity_details[comorbidity] = {"duration": duration}

    return comorbidity_details


def generate_patient_data(profile_data):
    patient_sex = get_random_sex()
    patient_age = get_random_age()
    condition_management_status = generate_condition_status()
    comorbidities_present = random.sample(
        profile_data["common_comorbidities"], k=random.randint(1, 3)
    )
    patient = {
        "age": patient_age,
        "sex": patient_sex,
        "name": get_random_name(sex=patient_sex),
        "smoking_status": get_random_smoking_status(),
        "comorbidities_details": generate_comorbidities_details(
            comorbidities_present, patient_age
        ),
        "condition_management": condition_management_status,
    }
    return patient


def get_profile_data(a: str):
    BASE_DIR = Path(__file__).resolve().parent.parent
    profile_path = BASE_DIR / "diagnosis_profiles" / "profiles" / f"{a}.yaml"
    profile_data = yaml.safe_load(profile_path.read_text())
    return profile_data


def generate_condition_data(patient):
    if patient["condition_management"] == "first identification":
        return {}
    else:
        condition_data = condition_extractor(patient)
        return condition_data


def save_clinical_note(clinical_note: str, documentation_style: str):

    base_dir = Path(__file__).resolve().parent.parent
    notes_dir = base_dir / "notes" / documentation_style
    notes_dir.mkdir(parents=True, exist_ok=True)
    existing_notes = list(notes_dir.glob("note_*.txt"))
    next_number = len(existing_notes) + 1
    file_path = notes_dir / f"note_{next_number}.txt"
    file_path.write_text(clinical_note, encoding="utf-8")
    return file_path


# print(__name__)
