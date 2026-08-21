import random


def lab_test(patient: dict):
    """
    Generate laboratory results relevant to hypertension.
    """

    # Generate serum electrolytes

    condition_management = patient["condition_management"]

    if condition_management == "first identification":
        sodium = random.randint(137, 145)
        potassium = round(random.uniform(3.7, 5.0), 1)
    elif condition_management == "good":
        sodium = random.randint(138, 144)
        potassium = round(random.uniform(3.8, 5.0), 1)
    elif condition_management == "moderate":
        sodium = random.randint(137, 145)
        potassium = round(random.uniform(3.7, 5.1), 1)
    elif condition_management == "poor":
        sodium = random.randint(136, 146)
        potassium = round(random.uniform(3.6, 5.2), 1)
    else:  # not managed
        sodium = random.randint(135, 147)
        potassium = round(random.uniform(3.5, 5.3), 1)

    return {
        "lab_reports": {
            "Serum Electrolytes": {
                "Sodium": f"{sodium} mmol/L",
                "Potassium": f"{potassium} mmol/L",
            },
        }
    }
