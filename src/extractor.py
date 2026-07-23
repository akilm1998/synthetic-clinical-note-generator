import random


def generate_primary_diagnosis_duration(age):
    """
    Generate the duration (in years) of the primary diagnosis.
    """
    max_duration = age - 30
    if max_duration <= 14:
        max_duration = 15

    return random.randint(1, max_duration)


def condition_extractor(patient):
    condition_data = {
        "primary_diagnosis_duration": generate_primary_diagnosis_duration(
            patient["age"]
        )
    }
    return condition_data
