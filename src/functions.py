import random
from pathlib import Path

import yaml

from extractor import condition_extractor

FEMALE_NAMES = [
    "Jane Watson",
    "Alice Mathew",
    "Diana Prince",
    "Emma Carter",
    "Olivia Brooks",
    "Sophia Turner",
    "Isabella Parker",
    "Ava Mitchell",
    "Mia Collins",
    "Charlotte Bailey",
    "Amelia Foster",
    "Harper Bennett",
    "Evelyn Hayes",
    "Abigail Reed",
    "Emily Cooper",
    "Elizabeth Perry",
    "Ella Morris",
    "Avery Ward",
    "Scarlett Hughes",
    "Grace Powell",
    "Chloe Cox",
    "Victoria Richardson",
    "Lily Peterson",
    "Hannah Simmons",
    "Zoe Butler",
    "Natalie Ross",
    "Leah Coleman",
    "Audrey Jenkins",
    "Claire PriceLucy Sanders",
    "Nora Kelly",
    "Stella Gray",
    "Brooklyn Barnes",
    "Ellie Wood",
    "Violet Murphy",
    "Savannah Bell",
    "Anna Cook",
    "Caroline Rivera",
    "Sarah Griffin",
    "Allison Hamilton",
    "Madelyn Stewart",
    "Maya Russell",
    "Aria Patterson",
    "Penelope Long",
    "Hazel Fisher",
    "Ruby Marshall",
    "Alice Freeman",
    "Ivy Henderson",
    "Naomi Myers",
    "Julia Stone",
    "Eliana Matthews",
    "Faith Hawkins",
    "Lydia Ford",
    "Autumn West",
    "Sophie Bryant",
    "Kennedy Walters",
    "Bella Dean",
    "Sadie Hunter",
    "Jasmine Spencer",
    "Madeline Warren",
    "Paige Palmer",
    "Ariana Lawson",
    "Gabriella Holland",
    "Brianna Gibson",
    "Valeria Ellis",
    "Maria Armstrong",
    "Adriana Wells",
    "Rachel Graham",
    "Rebecca Burke",
    "Melanie Knight",
    "Lauren Lawson",
    "Nicole Harper",
    "Kayla Pierce",
    "Diana Black",
    "Vanessa Warren",
    "Erica Chapman",
    "Michelle Cross",
    "Christina Pierce",
    "Veronica Davidson",
    "Julia Holland",
    "Alexandra Boyd",
    "Simone Bishop",
    "Eliza Chandler",
    "Brooke Snyder",
    "Kelsey Porter",
    "Ashley Murray",
    "Hailey Johnston",
    "Sydney Fuller",
    "Morgan Oliver",
    "Kimberly Franklin",
    "Chelsea Benson",
    "Shannon Douglas",
    "Monica Shaw",
    "Patricia Greene",
    "Margaret Walsh",
    "Catherine Nichols",
    "Teresa Cunningham",
    "Angela Holland",
    "Deborah Lawson",
    "Cynthia Montgomery",
    "Denise Wheeler",
    "Janet McKenzie",
    "Pamela Donovan",
]

MALE_NAMES = [
    "John Jacob",
    "Bob Hill",
    "Charlie Brown",
    "James Carter",
    "Michael Brooks",
    "William Turner",
    "David Parker",
    "John Mitchell",
    "Robert Collins",
    "Joseph Bailey",
    "Thomas Foster",
    "Charles Bennett",
    "Daniel Hayes",
    "Matthew Reed",
    "Anthony Cooper",
    "Christopher Perry",
    "Andrew Morris",
    "Joshua Ward",
    "Ryan Hughes",
    "Nicholas Powell",
    "Brandon Cox",
    "Justin Richardson",
    "Kevin Peterson",
    "Brian Simmons",
    "Eric Butler",
    "Adam Ross",
    "Jason Coleman",
    "Nathan Jenkins",
    "Aaron Price",
    "Kyle Sanders",
    "Tyler Kelly",
    "Jonathan Gray",
    "Zachary Barnes",
    "Samuel Wood",
    "Benjamin Murphy",
    "Patrick Bell",
    "Christian Cook",
    "Dylan Rivera",
    "Ethan Griffin",
    "Noah Hamilton",
    "Logan Stewart",
    "Mason Russell",
    "Lucas Patterson",
    "Jacob Long",
    "Alexander Fisher",
    "Gabriel Marshall",
    "Caleb Freeman",
    "Isaac Henderson",
    "Owen Myers",
    "Elijah Stone",
    "Liam Matthews",
    "Aiden Hawkins",
    "Hunter Ford",
    "Cameron West",
    "Evan Bryant",
    "Connor Walters",
    "Austin Dean",
    "Blake Hunter",
    "Jordan Spencer",
    "Trevor Warren",
    "Sean Palmer",
    "Ian Lawson",
    "Gavin Holland",
    "Nathaniel Gibson",
    "Dominic Ellis",
    "Vincent Armstrong",
    "Adrian Wells",
    "Colin Graham",
    "Tristan Burke",
    "Maxwell Knight",
    "Spencer Lawson",
    "Patrick Harper",
    "Joel Pierce",
    "Derek Black",
    "Cody Warren",
    "Jesse Chapman",
    "Marcus Cross",
    "Victor Pierce",
    "Leo Davidson",
    "Julian Holland",
    "Damian Boyd",
    "Simon Bishop",
    "Elliot Chandler",
    "Wesley Snyder",
    "Grant Porter",
    "Ashton Murray",
    "Hayden Johnston",
    "Chase Fuller",
    "Preston Oliver",
    "Gavin Franklin",
    "Riley Benson",
    "Scott Douglas",
    "Martin Shaw",
    "Peter Greene",
    "Henry Walsh",
    "Arthur Nichols",
    "George Cunningham",
    "Edward Holland",
    "Richard Lawson",
    "Frank Montgomery",
    "Alan Wheeler",
    "Bruce McKenzie",
    "Philip Donovan",
]


def get_random_name(sex=None):
    if sex == "Male":
        return random.choice(MALE_NAMES)
    elif sex == "Female":
        return random.choice(FEMALE_NAMES)
    else:
        return random.choice(MALE_NAMES + FEMALE_NAMES)


def get_random_age(min_age=30, max_age=96):
    return random.randint(min_age, max_age)


def get_random_sex():
    return random.choice(["Male", "Female"])


def get_random_smoking_status():
    return random.choice(["Yes", "No"])


def generate_condition_status():
    condition_management = [
        "good",
        "moderate",
        "poor",
        "not managed",
        "first identification",
    ]

    condition_management_weights = [
        35,
        30,
        20,
        10,
        5,
    ]

    return random.choices(
        condition_management,
        weights=condition_management_weights,
        k=1,
    )[0]


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
    ONSET_AGE = {
        "Hypertension": 35,
        "Dyslipidemia": 35,
        "Obesity": 20,
        "Chronic kidney disease": 40,
        "Anxiety": 18,
        "Depression": 20,
        "Obstructive sleep apnea": 35,
        "Non-alcoholic fatty liver disease": 30,
    }
    comorbidity_details = {}

    for comorbidity in comorbidities:
        onset = ONSET_AGE[comorbidity]

        max_duration = max(1, age - onset)

        duration = random.randint(1, max_duration)
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
        condition_data = {"primary_diagnosis_duration": 0}
        return condition_data
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
