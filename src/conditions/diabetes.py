import random


def lab_test(patient: dict):
    """Generate diabetes laboratory results."""

    condition_management = patient["condition_management"]

    if condition_management == "first identification":
        hba1c = round(random.uniform(6.5, 8.0), 1)

    elif condition_management == "good":
        hba1c = round(random.uniform(6.5, 7.0), 1)

    elif condition_management == "moderate":
        hba1c = round(random.uniform(7.1, 8.0), 1)

    elif condition_management == "poor":
        hba1c = round(random.uniform(8.1, 9.0), 1)

    else:  # not managed
        hba1c = round(random.uniform(9.1, 10.0), 1)

    # Approximate fasting glucose from HbA1c.
    # Add random variation so the relationship isn't deterministic.
    estimated_glucose = 28.7 * hba1c - 46.7
    fasting_glucose = round(random.gauss(estimated_glucose, 15))

    fasting_glucose = max(fasting_glucose, 70)

    return {
        "lab_reports": {
            "HbA1c": f"{hba1c} %",
            "Fasting Glucose": f"{fasting_glucose} mg/dL",
        }
    }
