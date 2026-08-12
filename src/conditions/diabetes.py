import random


def lab_test(condition_management: str):
    """
    Generate diabetes laboratory results.
    """

    # Generate HbA1c
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

    # Generate fasting glucose based on HbA1c
    if hba1c <= 7.0:
        fasting_glucose = random.randint(80, 130)
    elif hba1c <= 8.0:
        fasting_glucose = random.randint(131, 150)
    elif hba1c <= 9.0:
        fasting_glucose = random.randint(151, 180)
    else:
        fasting_glucose = random.randint(181, 300)

    return {
        "lab_reports": {
            "HbA1c": f"{hba1c} %",
            "Fasting Glucose": f"{fasting_glucose} mg/dL",
        }
    }
