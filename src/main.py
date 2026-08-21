import os

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# from conditions.diabetes import lab_test as diabetes
# from conditions.ckd import lab_test as ckd
# from conditions.hyperlipidemia import lab_test as hyperlipidemia
from conditions.anemia import lab_test as anemia

# from conditions.hypertension import lab_test as hypertension
from functions import (
    generate_condition_data,
    generate_documentation_config,
    generate_patient_data,
    generate_symptoms,
    generate_vitals,
    get_profile_data,
)
from prompt import generate_clinical_note

if __name__ == "__main__":
    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    condition_name = "anemia"
    number_of_notes = 250

    profile_data = get_profile_data(condition_name)

    icd_code = profile_data["icd_code"]
    diagnosis_name = profile_data["diagnosis_name"]

    patient_counter = 1

    records = []

    for _ in range(number_of_notes):
        patient_id = f"PAT{patient_counter:06d}"

        note_generation_config = generate_documentation_config()

        patient = generate_patient_data(profile_data)

        condition_data = generate_condition_data(patient)
        patient.update(condition_data)

        lab_test_results = anemia(patient)
        patient.update(lab_test_results)

        vitals = generate_vitals(patient)
        patient.update(vitals)

        symptoms = generate_symptoms(profile_data, patient)
        patient.update(symptoms)

        clinical_note = generate_clinical_note(
            profile_data, patient, client, note_generation_config
        )

        # Store one complete record
        records.append(
            {
                "patient_id": patient_id,
                "diagnosis_name": diagnosis_name,
                "icd_code": icd_code,
                "clinical_note": clinical_note,
            }
        )

        print(f"Generated {patient_id}")

        patient_counter += 1

    # Convert all records into a DataFrame
    df = pd.DataFrame(records)

    # Save as Parquet
    df.to_parquet("anemia_dataset.parquet", engine="pyarrow", index=False)

    print("\nDataset saved successfully.")
    print(df.head())
