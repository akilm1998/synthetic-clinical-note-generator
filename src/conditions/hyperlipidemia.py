import random


def lab_test(patient: dict):
    """
    Generate laboratory results relevant to unspecified hyperlipidemia.
    """

    condition_management = patient["condition_management"]
    patient_sex = patient["sex"]

    # Generate LDL-C according to condition management.
    if condition_management == "first identification":
        ldl = random.randint(130, 190)

    elif condition_management == "good":
        ldl = random.randint(60, 100)

    elif condition_management == "moderate":
        ldl = random.randint(100, 159)

    elif condition_management == "poor":
        ldl = random.randint(160, 220)

    else:  # not managed
        ldl = random.randint(190, 280)

    # Generate HDL-C with sex-specific ranges.
    if patient_sex == "Female":
        if condition_management == "good":
            hdl = random.randint(50, 70)
        elif condition_management == "moderate":
            hdl = random.randint(45, 60)
        elif condition_management == "poor":
            hdl = random.randint(40, 55)
        elif condition_management == "not managed":
            hdl = random.randint(35, 50)
        else:  # first identification
            hdl = random.randint(40, 60)

    else:  # Male
        if condition_management == "good":
            hdl = random.randint(45, 65)
        elif condition_management == "moderate":
            hdl = random.randint(40, 55)
        elif condition_management == "poor":
            hdl = random.randint(35, 50)
        elif condition_management == "not managed":
            hdl = random.randint(30, 45)
        else:  # first identification
            hdl = random.randint(35, 55)

    # Generate triglycerides according to management.
    if condition_management == "first identification":
        triglycerides = random.randint(150, 250)

    elif condition_management == "good":
        triglycerides = random.randint(80, 150)

    elif condition_management == "moderate":
        triglycerides = random.randint(130, 220)

    elif condition_management == "poor":
        triglycerides = random.randint(180, 300)

    else:  # not managed
        triglycerides = random.randint(220, 400)

    # Keep total cholesterol internally consistent with the
    # generated LDL-C, HDL-C, and triglycerides.
    total_cholesterol = round(ldl + hdl + (triglycerides / 5))

    return {
        "lab_reports": {
            "Total Cholesterol": f"{total_cholesterol} mg/dL",
            "Low-Density Lipoprotein Cholesterol (LDL-C)": f"{ldl} mg/dL",
            "High-Density Lipoprotein Cholesterol (HDL-C)": f"{hdl} mg/dL",
            "Triglycerides": f"{triglycerides} mg/dL",
        }
    }
