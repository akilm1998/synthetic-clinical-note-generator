import random


def lab_test(patient: dict):
    """
    Generate laboratory results relevant to unspecified chronic kidney disease.
    """

    condition_management = patient["condition_management"]
    patient_age = patient["age"]
    patient_sex = patient["sex"]

    # Generate eGFR according to condition management.
    if condition_management == "first identification":
        egfr = random.randint(45, 90)
        bun = random.randint(18, 38)

    elif condition_management == "good":
        egfr = random.randint(60, 95)
        bun = random.randint(12, 26)

    elif condition_management == "moderate":
        egfr = random.randint(30, 59)
        bun = random.randint(24, 45)

    elif condition_management == "poor":
        egfr = random.randint(15, 29)
        bun = random.randint(40, 65)

    else:  # not managed
        egfr = random.randint(5, 20)
        bun = random.randint(60, 95)

    # Generate serum creatinine in a directionally consistent relationship
    # with eGFR, while allowing variation based on age and sex.
    if patient_sex == "Male":
        sex_factor = 1.0
    else:
        sex_factor = 0.85

    age_factor = 1 + max(patient_age - 40, 0) * 0.005

    creatinine = (90 / egfr) ** 0.7 * age_factor * sex_factor

    # Add random biological variation.
    creatinine *= random.uniform(0.90, 1.10)

    # Keep the generated value within a reasonable synthetic range.
    creatinine = max(0.7, min(creatinine, 6.0))
    serum_creatinine = round(creatinine, 2)

    return {
        "lab_reports": {
            "Serum Creatinine": f"{serum_creatinine} mg/dL",
            "Estimated Glomerular Filtration Rate (eGFR)": (f"{egfr} mL/min/1.73 m²"),
            "Blood Urea Nitrogen (BUN)": f"{bun} mg/dL",
        }
    }
