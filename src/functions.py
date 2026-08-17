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


def get_random_age(min_age=31, max_age=98):
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


DOCUMENTATION_DEPTHS = {
    "concise": {
        "weight": 20,
        "instructions": [
            "Brief clinic documentation",
            "Essential positives and negatives only",
            "Short assessment and plan",
            "Avoid lengthy explanations",
        ],
    },
    "standard": {
        "weight": 65,
        "instructions": [
            "Routine outpatient documentation",
            "Focus on clinically relevant findings",
            "Moderate detail",
        ],
    },
    "comprehensive": {
        "weight": 15,
        "instructions": [
            "Comprehensive history",
            "Full ROS",
            "Complete physical exam",
            "Expanded reasoning",
        ],
    },
}


ENCOUNTER_TYPES = {
    "routine_follow_up": {
        "weight": 55,
        "instructions": [
            "Routine outpatient follow-up",
            "Focus on interval history",
            "Review disease control",
            "Update assessment and management",
        ],
    },
    "annual_review": {
        "weight": 15,
        "instructions": [
            "Comprehensive annual review",
            "Include preventive care where appropriate",
            "Review chronic disease status",
        ],
    },
    "new_patient": {
        "weight": 10,
        "instructions": [
            "Initial outpatient consultation",
            "Include comprehensive history",
            "Provide detailed assessment",
        ],
    },
    "medication_review": {
        "weight": 10,
        "instructions": [
            "Focus on medication effectiveness",
            "Assess adherence",
            "Review treatment tolerance",
        ],
    },
    "urgent_follow_up": {
        "weight": 10,
        "instructions": [
            "Focused outpatient follow-up",
            "Address acute concern",
            "Keep documentation concise",
        ],
    },
}


NARRATIVE_STYLES = {
    "soap": {
        "weight": 60,
        "instructions": [
            "Use standard SOAP format",
            "Include Subjective, Objective, Assessment, and Plan sections",
        ],
    },
    "problem_oriented": {
        "weight": 20,
        "instructions": [
            "Organize documentation by active medical problems",
            "Discuss assessment and management for each problem",
        ],
    },
    "narrative": {
        "weight": 10,
        "instructions": [
            "Use a flowing narrative style",
            "Maintain standard clinical sections where appropriate",
        ],
    },
    "clinic_note": {
        "weight": 10,
        "instructions": [
            "Use a concise outpatient clinic note style",
            "Emphasize efficiency and readability",
        ],
    },
}


PHYSICIAN_STYLES = {
    "family_medicine": {
        "weight": 45,
        "instructions": [
            "Write in the style of an experienced family medicine physician",
            "Use balanced clinical detail",
            "Maintain a practical outpatient focus",
        ],
    },
    "internal_medicine": {
        "weight": 30,
        "instructions": [
            "Write in the style of an experienced internal medicine physician",
            "Provide systematic clinical reasoning",
            "Integrate comorbidities into the assessment and plan",
        ],
    },
    "specialist": {
        "weight": 15,
        "instructions": [
            "Write in the style of an experienced specialist physician",
            "Emphasize disease-specific assessment and management",
            "Use precise specialty terminology where appropriate",
        ],
    },
    "academic": {
        "weight": 10,
        "instructions": [
            "Write in the style of an experienced academic physician",
            "Include concise clinical reasoning",
            "Use precise medical terminology",
        ],
    },
}


def weighted_choice(config: dict):
    choice = random.choices(
        population=list(config.keys()),
        weights=[v["weight"] for v in config.values()],
        k=1,
    )[0]

    return {
        "name": choice,
        "instructions": config[choice]["instructions"],
    }


def generate_encounter_type():
    return weighted_choice(ENCOUNTER_TYPES)


def generate_narrative_style():
    return weighted_choice(NARRATIVE_STYLES)


def generate_physician_style():
    return weighted_choice(PHYSICIAN_STYLES)


def generate_documentation_depth():
    return weighted_choice(DOCUMENTATION_DEPTHS)


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
        "Type 2 diabetes mellitus": 30,
        "Hyperlipidemia": 35,
        "Coronary artery disease": 45,
    }
    comorbidity_details = {}

    for comorbidity in comorbidities:
        onset = ONSET_AGE[comorbidity]

        max_duration = max(1, age - onset)

        duration = random.randint(1, max_duration)

        comorbidity_details[comorbidity] = {"duration": duration}

    return comorbidity_details


def get_patient_height(patient_sex: str):
    """
    Generate a structured representation of patient demographics.
    """
    if patient_sex == "Male":
        patient_height = random.randint(160, 190)  # cm
    else:
        patient_height = random.randint(150, 180)  # cm
    # return str(patient_height) + " cm"
    return patient_height


def get_weight_and_bmi(
    comorbidities_present: list[str],
    patient_height: int,
    patient_sex: str,
):
    """
    Generate a clinically plausible BMI and corresponding weight.

    Parameters
    ----------
    comorbidities_present : list[str]
        List of patient comorbidities.
    patient_height : int
        Height in centimeters.
    patient_sex : str
        "Male" or "Female".
    """

    # Select BMI range
    if "Obesity" in comorbidities_present:
        bmi = round(random.uniform(30.0, 40.0), 1)

    elif "Underweight" in comorbidities_present:
        bmi = round(random.uniform(16.0, 18.4), 1)

    else:
        # Slightly different distributions by sex
        if patient_sex == "Male":
            bmi = round(random.uniform(21.0, 29.9), 1)
        else:
            bmi = round(random.uniform(20.0, 29.9), 1)

    # Calculate weight from BMI
    height_m = patient_height / 100
    weight = round(bmi * (height_m**2), 1)

    return weight, bmi


def generate_documentation_config():
    return {
        "encounter_type": generate_encounter_type(),
        "documentation_depth": generate_documentation_depth(),
        "narrative_style": generate_narrative_style(),
        "physician_style": generate_physician_style(),
    }


def generate_patient_data(profile_data):
    condition = profile_data["condition_name"]
    patient_sex = get_random_sex()
    patient_age = get_random_age()
    condition_management_status = generate_condition_status()
    comorbidities_present = random.sample(
        profile_data["common_comorbidities"], k=random.randint(1, 3)
    )
    patient_height = get_patient_height(patient_sex)
    patient_weight, bmi = get_weight_and_bmi(
        comorbidities_present, patient_height, patient_sex
    )
    patient = {
        "age": patient_age,
        "sex": patient_sex,
        "height": f"{patient_height} cm",
        "weight": f"{patient_weight} kg",
        "bmi": f"{bmi} kg/m²",
        "name": get_random_name(sex=patient_sex),
        "smoking_status": get_random_smoking_status(),
        "condition_name": condition,
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


VITAL_BASELINES = {
    "blood_pressure": {
        "systolic": (115, 125),
        "diastolic": (75, 82),
    },
    "pulse": (68, 76),
    "respiratory_rate": (14, 18),
    "temperature": (36.6, 37.0),
    "oxygen_saturation": (97, 99),
}

AGE_MODIFIERS = [
    {
        "min": 18,
        "max": 29,
        "blood_pressure": {
            "systolic": (-5, -2),
        },
    },
    {
        "min": 30,
        "max": 44,
        "blood_pressure": {
            "systolic": (0, 0),
        },
    },
    {
        "min": 45,
        "max": 59,
        "blood_pressure": {
            "systolic": (2, 5),
        },
    },
    {
        "min": 60,
        "max": 74,
        "blood_pressure": {
            "systolic": (5, 10),
        },
        "oxygen_saturation": (-1, 0),
    },
    {
        "min": 75,
        "max": 120,
        "blood_pressure": {
            "systolic": (8, 15),
        },
        "respiratory_rate": (0, 2),
        "oxygen_saturation": (-2, -1),
    },
]


def generate_vitals(patient):
    vitals = {
        "blood_pressure": {
            "systolic": random.randint(*VITAL_BASELINES["blood_pressure"]["systolic"]),
            "diastolic": random.randint(
                *VITAL_BASELINES["blood_pressure"]["diastolic"]
            ),
        },
        "pulse": random.randint(*VITAL_BASELINES["pulse"]),
        "respiratory_rate": random.randint(*VITAL_BASELINES["respiratory_rate"]),
        "temperature": round(random.uniform(*VITAL_BASELINES["temperature"]), 1),
        "oxygen_saturation": random.randint(*VITAL_BASELINES["oxygen_saturation"]),
    }

    vitals = apply_age_modifiers(vitals, patient)
    vitals = apply_bmi_modifiers(vitals, patient)
    vitals = apply_smoking_modifiers(vitals, patient)
    vitals = apply_comorbidity_modifiers(vitals, patient)
    vitals = apply_condition_modifiers(vitals, patient)
    # vitals = apply_medication_modifiers(vitals, patient)

    return {
        "vital_signs": {
            "blood_pressure": (
                f"{vitals['blood_pressure']['systolic']}/"
                f"{vitals['blood_pressure']['diastolic']} mmHg"
            ),
            "pulse": f"{vitals['pulse']} bpm",
            "respiratory_rate": f"{vitals['respiratory_rate']}/min",
            "temperature": f"{vitals['temperature']:.1f}°C",
            "oxygen_saturation": f"{vitals['oxygen_saturation']}%",
        }
    }


def apply_age_modifiers(vitals, patient):
    age = patient["age"]

    modifier = next(
        (band for band in AGE_MODIFIERS if band["min"] <= age <= band["max"]),
        None,
    )

    if modifier is None:
        return vitals

    if "blood_pressure" in modifier:
        bp = modifier["blood_pressure"]

        if "systolic" in bp:
            low, high = bp["systolic"]
            vitals["blood_pressure"]["systolic"] += random.randint(low, high)

        if "diastolic" in bp:
            low, high = bp["diastolic"]
            vitals["blood_pressure"]["diastolic"] += random.randint(low, high)

    if "pulse" in modifier:
        low, high = modifier["pulse"]
        vitals["pulse"] += random.randint(low, high)

    if "respiratory_rate" in modifier:
        low, high = modifier["respiratory_rate"]
        vitals["respiratory_rate"] += random.randint(low, high)

    if "temperature" in modifier:
        low, high = modifier["temperature"]
        vitals["temperature"] += round(random.uniform(low, high), 1)

    if "oxygen_saturation" in modifier:
        low, high = modifier["oxygen_saturation"]
        vitals["oxygen_saturation"] += random.randint(low, high)

    return vitals


def apply_bmi_modifiers(vitals, patient):
    bmi = float(patient["bmi"].split()[0])

    if bmi >= 30:
        vitals["pulse"] += random.randint(2, 5)

        vitals["respiratory_rate"] += random.randint(0, 2)

        vitals["oxygen_saturation"] -= random.randint(0, 1)

    elif bmi < 18.5:
        vitals["pulse"] += random.randint(0, 2)

    return vitals


def apply_smoking_modifiers(vitals, patient):
    if patient["smoking_status"] == "Yes":
        vitals["pulse"] += random.randint(2, 5)

        vitals["oxygen_saturation"] -= random.randint(0, 1)

    return vitals


def apply_comorbidity_modifiers(vitals, patient):
    comorbidities = patient["comorbidities_details"]

    if "Hypertension" in comorbidities:
        vitals["blood_pressure"]["systolic"] += random.randint(10, 20)
        vitals["blood_pressure"]["diastolic"] += random.randint(5, 10)

    if "Type 2 diabetes mellitus" in comorbidities:
        vitals["pulse"] += random.randint(0, 2)

    if "Hyperlipidemia" in comorbidities:
        # No major direct vital-sign effect
        pass

    if "Chronic kidney disease" in comorbidities:
        vitals["blood_pressure"]["systolic"] += random.randint(5, 15)
        vitals["blood_pressure"]["diastolic"] += random.randint(2, 8)

    if "Coronary artery disease" in comorbidities:
        vitals["pulse"] += random.randint(2, 5)

    if "Heart failure" in comorbidities:
        vitals["pulse"] += random.randint(3, 8)
        vitals["respiratory_rate"] += random.randint(2, 4)

    if "COPD" in comorbidities:
        vitals["respiratory_rate"] += random.randint(2, 5)
        vitals["oxygen_saturation"] -= random.randint(2, 5)

    if "Asthma" in comorbidities:
        vitals["respiratory_rate"] += random.randint(1, 3)

    if "Hyperthyroidism" in comorbidities:
        vitals["pulse"] += random.randint(8, 15)

    if "Hypothyroidism" in comorbidities:
        vitals["pulse"] -= random.randint(4, 8)

    return vitals


def apply_condition_modifiers(vitals, patient):
    condition = patient["condition_name"]
    management = patient["condition_management"]

    if condition == "hypertension":
        if management == "good":
            systolic = random.randint(0, 5)
            diastolic = random.randint(0, 3)

        elif management == "moderate":
            systolic = random.randint(5, 15)
            diastolic = random.randint(3, 8)

        elif management == "poor":
            systolic = random.randint(15, 25)
            diastolic = random.randint(8, 12)

        elif management == "not managed":
            systolic = random.randint(20, 35)
            diastolic = random.randint(10, 18)

        else:  # first identification
            systolic = random.randint(10, 25)
            diastolic = random.randint(5, 12)

        vitals["blood_pressure"]["systolic"] += systolic
        vitals["blood_pressure"]["diastolic"] += diastolic

    elif condition == "diabetes":
        pass

    return vitals


def generate_symptoms(profile_data, patient):
    """
    Generate symptoms using disease-specific rules defined in the
    condition YAML profile.

    Management and duration probabilities are treated as independent
    modifiers. When both are present, they are multiplied together.
    """

    symptoms_config = profile_data.get("symptoms", {})
    common_symptoms = symptoms_config.get("common", [])
    symptom_groups = symptoms_config.get("groups", {})

    condition_management = patient.get(
        "condition_management",
        "moderate",
    )

    disease_duration = patient.get(
        "primary_diagnosis_duration",
        0,
    )

    symptoms = {symptom: False for symptom in common_symptoms}

    for group_data in symptom_groups.values():
        group_symptoms = group_data.get("symptoms", [])

        if not group_symptoms:
            continue

        probability_factors = []

        # Management-based probability
        management_probability = group_data.get("management_probability")

        if management_probability:
            probability = management_probability.get(condition_management)

            if probability is not None:
                probability_factors.append(probability)

        # Duration-based probability
        duration_probability = group_data.get("duration_probability")

        if duration_probability:
            for duration_rule in duration_probability:
                max_years = duration_rule.get("max_years")

                if max_years is None or disease_duration <= max_years:
                    probability_factors.append(duration_rule.get("probability", 0.0))
                    break

        # No generation rules configured for this group
        if not probability_factors:
            continue

        # Combine independent probability factors
        group_probability = 1.0

        for probability in probability_factors:
            group_probability *= probability

        # Activate group
        if random.random() >= group_probability:
            continue

        # Select symptoms within the activated group
        selected_symptoms = [
            symptom for symptom in group_symptoms if random.random() < 0.65
        ]

        # Ensure an activated group produces at least one symptom
        if not selected_symptoms:
            selected_symptoms = [random.choice(group_symptoms)]

        for symptom in selected_symptoms:
            if symptom in symptoms:
                symptoms[symptom] = True

    return {"symptoms": symptoms}


# def save_clinical_note(clinical_note: str, documentation_style: str):

#     base_dir = Path(__file__).resolve().parent.parent
#     notes_dir = base_dir / "notes" / documentation_style
#     notes_dir.mkdir(parents=True, exist_ok=True)
#     existing_notes = list(notes_dir.glob("note_*.txt"))
#     next_number = len(existing_notes) + 1
#     file_path = notes_dir / f"note_{next_number}.txt"
#     file_path.write_text(clinical_note, encoding="utf-8")
#     return file_path


def save_clinical_note(
    clinical_note: str,
    documentation_style: str,
    condition_name: str,
):
    base_dir = Path(__file__).resolve().parent.parent
    notes_dir = base_dir / "notes" / documentation_style
    notes_dir.mkdir(parents=True, exist_ok=True)

    existing_notes = list(notes_dir.glob(f"{condition_name}_*.txt"))
    next_number = len(existing_notes) + 1

    file_path = notes_dir / f"{condition_name}_{next_number}.txt"
    file_path.write_text(clinical_note, encoding="utf-8")

    return file_path
