import os
import time

import pandas as pd
from dotenv import load_dotenv
from openai import OpenAI

# Import condition-specific lab functions
# from conditions.anemia import lab_test as anemia
# from conditions.diabetes import lab_test as diabetes
from conditions.hypertension import lab_test as hypertension
from functions import (
    generate_condition_data,
    generate_documentation_config,
    generate_patient_data,
    generate_symptoms,
    generate_vitals,
    get_profile_data,
    save_clinical_note,
)
from prompt import generate_clinical_note

if __name__ == "__main__":
    # -----------------------------
    # Configuration
    # -----------------------------
    start_time = time.time()
    condition_name = "hypertension"
    number_of_notes = 250

    dataset_file = "clinical_notes.parquet"

    # -----------------------------
    # Load environment variables
    # -----------------------------

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)

    # -----------------------------
    # Load condition profile
    # -----------------------------

    profile_data = get_profile_data(condition_name)

    icd_code = profile_data["icd10_code"]
    diagnosis_name = profile_data["diagnosis_name"]

    # -----------------------------
    # Determine starting patient ID
    # -----------------------------

    if os.path.exists(dataset_file):
        existing_df = pd.read_parquet(dataset_file)

        patient_counter = len(existing_df) + 1

    else:
        existing_df = pd.DataFrame()

        patient_counter = 1

    # -----------------------------
    # Store newly generated records
    # -----------------------------

    records = []

    # -----------------------------
    # Generate clinical notes
    # -----------------------------

    for _ in range(number_of_notes):
        # Generate unique patient ID
        patient_id = f"PAT{patient_counter:06d}"

        # Generate documentation configuration
        note_generation_config = generate_documentation_config()

        # Generate patient data
        patient = generate_patient_data(profile_data)

        # Generate condition-related data
        condition_data = generate_condition_data(patient)

        patient.update(condition_data)

        # Generate condition-specific laboratory results
        lab_test_results = hypertension(patient)

        patient.update(lab_test_results)

        # Generate vital signs
        vitals = generate_vitals(patient)

        patient.update(vitals)

        # Generate symptoms
        symptoms = generate_symptoms(profile_data, patient)

        patient.update(symptoms)

        # -----------------------------
        # Generate clinical note
        # -----------------------------

        clinical_note = generate_clinical_note(
            profile_data,
            patient,
            client,
            note_generation_config,
        )

        # -----------------------------
        # Add record to dataset
        # -----------------------------

        records.append(
            {
                "patient_id": patient_id,
                "diagnosis_name": diagnosis_name,
                "icd_code": icd_code,
                "clinical_note": clinical_note,
            }
        )

        # -----------------------------
        # Save individual TXT note
        # -----------------------------

        save_clinical_note(
            clinical_note,
            note_generation_config["documentation_depth"]["name"],
            condition_name,
            patient_id,
        )

        print(f"Generated {patient_id} | {condition_name} | {icd_code}")

        # Move to next patient ID
        patient_counter += 1

    new_df = pd.DataFrame(records)

    if not existing_df.empty:
        final_df = pd.concat(
            [existing_df, new_df],
            ignore_index=True,
        )

    else:
        final_df = new_df

    # -----------------------------
    # Save complete dataset
    # -----------------------------

    final_df.to_parquet(
        dataset_file,
        engine="pyarrow",
        index=False,
    )

    print("\nGeneration completed successfully.")

    print(f"New records generated: {len(new_df)}")

    print(f"Total records in dataset: {len(final_df)}")

    print(f"Dataset saved as: {dataset_file}")

    print("\nPreview:")

    print(final_df.head())

    print(final_df.tail())

    end_time = time.time()
    time_taken = end_time - start_time
    print(f"\nTime taken: {time_taken:.2f} seconds")
