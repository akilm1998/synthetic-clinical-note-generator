import os

from dotenv import load_dotenv
from openai import OpenAI

from conditions.diabetes import lab_test as diabetes

# from conditions.hypertension import lab_test as hypertension
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
    condition_name = "diabetes"
    load_dotenv()
    profile_data = get_profile_data(condition_name)  # load yaml file
    # print(profile_data)
    note_generation_config = generate_documentation_config()
    patient = generate_patient_data(profile_data)
    # print(f"\n {patient} \n\n")
    condition_management_status = patient["condition_management"]
    condition_data = generate_condition_data(
        patient
    )  # primary_diagnosis_duration decided
    patient.update(condition_data)
    lab_test_results = diabetes(
        condition_management_status
    )  # medical condition's lab reports taken
    patient.update(lab_test_results)
    vitals = generate_vitals(patient)  # vitals generated based on patient object
    patient.update(vitals)
    symptoms = generate_symptoms(profile_data, patient)
    patient.update(symptoms)
    print(f"\n {patient} \n\n")
    print(f"\n{note_generation_config} \n")
    print(f"\n{condition_data} \n")
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    clinical_note = generate_clinical_note(
        profile_data, patient, client, note_generation_config
    )
    print(clinical_note)
    save_clinical_note(
        clinical_note,
        note_generation_config["documentation_depth"]["name"],
        condition_name,
    )
