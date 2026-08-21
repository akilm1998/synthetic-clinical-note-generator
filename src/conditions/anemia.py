import random


def lab_test(patient: dict):
    """
    Generate laboratory results relevant to anemia of chronic disease.

    Values are generated with internal relationships consistent with
    anemia of chronic inflammation/disease.
    """

    condition_management = patient["condition_management"]
    patient_sex = patient["sex"]

    # Generate hemoglobin.
    # Anemia of chronic disease is generally mild to moderate.
    # Sex-specific ranges keep the generated value below the usual
    # anemia threshold while avoiding unnecessarily severe anemia.
    if patient_sex == "Male":
        if condition_management == "good":
            hemoglobin = random.uniform(11.0, 12.9)
        elif condition_management == "moderate":
            hemoglobin = random.uniform(9.8, 11.5)
        elif condition_management == "poor":
            hemoglobin = random.uniform(8.5, 10.5)
        elif condition_management == "not managed":
            hemoglobin = random.uniform(8.0, 9.8)
        else:  # first identification
            hemoglobin = random.uniform(10.0, 12.0)

    else:  # Female
        if condition_management == "good":
            hemoglobin = random.uniform(10.5, 11.9)
        elif condition_management == "moderate":
            hemoglobin = random.uniform(9.5, 11.0)
        elif condition_management == "poor":
            hemoglobin = random.uniform(8.5, 10.2)
        elif condition_management == "not managed":
            hemoglobin = random.uniform(8.0, 9.6)
        else:  # first identification
            hemoglobin = random.uniform(9.8, 11.5)

    hemoglobin = round(hemoglobin, 1)

    # Hematocrit is generated in relation to hemoglobin.
    # A hematocrit around 3 times the hemoglobin is a useful
    # approximation for synthetic CBC generation.
    hematocrit = hemoglobin * random.uniform(2.9, 3.1)
    hematocrit = round(hematocrit, 1)

    # Anemia of chronic disease is usually normocytic, although
    # mild microcytosis can occur.
    mcv = random.randint(80, 94)

    # Derive RBC count from hematocrit and MCV.
    # RBC (million/uL) = Hct (%) / MCV (fL) * 10
    rbc = (hematocrit / mcv) * 10
    rbc = round(rbc, 2)

    # Serum iron is typically reduced in anemia of chronic disease.
    if condition_management == "good":
        serum_iron = random.randint(45, 80)

    elif condition_management == "moderate":
        serum_iron = random.randint(35, 65)

    elif condition_management == "poor":
        serum_iron = random.randint(25, 55)

    elif condition_management == "not managed":
        serum_iron = random.randint(20, 50)

    else:  # first identification
        serum_iron = random.randint(35, 70)

    # TIBC is typically low or low-normal in anemia of chronic disease.
    if condition_management == "good":
        tibc = random.randint(240, 320)

    elif condition_management == "moderate":
        tibc = random.randint(220, 300)

    elif condition_management == "poor":
        tibc = random.randint(200, 280)

    elif condition_management == "not managed":
        tibc = random.randint(190, 270)

    else:  # first identification
        tibc = random.randint(220, 300)

    # Ferritin is generally normal or elevated because it acts
    # as an acute-phase reactant.
    if condition_management == "good":
        ferritin = random.randint(80, 250)

    elif condition_management == "moderate":
        ferritin = random.randint(100, 300)

    elif condition_management == "poor":
        ferritin = random.randint(120, 400)

    elif condition_management == "not managed":
        ferritin = random.randint(150, 500)

    else:  # first identification
        ferritin = random.randint(80, 300)

    # Transferrin saturation is derived from serum iron and TIBC.
    # TSAT (%) = Serum Iron / TIBC × 100
    transferrin_saturation = (serum_iron / tibc) * 100
    transferrin_saturation = round(transferrin_saturation, 1)

    return {
        "lab_reports": {
            "Hemoglobin": f"{hemoglobin} g/dL",
            "Hematocrit": f"{hematocrit} %",
            "Red Blood Cell Count (RBC)": f"{rbc} million/µL",
            "Mean Corpuscular Volume (MCV)": f"{mcv} fL",
            "Serum Iron": f"{serum_iron} µg/dL",
            "Ferritin": f"{ferritin} ng/mL",
            "Total Iron-Binding Capacity (TIBC)": f"{tibc} µg/dL",
            "Transferrin Saturation": f"{transferrin_saturation} %",
        }
    }
