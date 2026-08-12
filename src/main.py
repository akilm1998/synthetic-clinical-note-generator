# import os

from dotenv import load_dotenv

# from openai import OpenAI
from conditions.diabetes import lab_test as diabetes
from functions import (
    generate_clinical_note_documentaion_style,
    generate_condition_data,
    generate_patient_data,
    get_profile_data,
    # save_clinical_note,
)

# from prompt import generate_clinical_note


if __name__ == "__main__":
    condition_name = "diabetes"
    load_dotenv()
    profile_data = get_profile_data(condition_name)  # load yaml file
    # print(profile_data)
    documentation_style = (
        generate_clinical_note_documentaion_style()
    )  # select documentation style
    patient = generate_patient_data(profile_data)
    condition_management_status = patient["condition_management"]
    condition_data = generate_condition_data(patient)
    patient.update(condition_data)
    lab_test_results = diabetes(condition_management_status)
    patient.update(lab_test_results)
    print(f"\n {patient} \n\n")
    # print(f"\n{documentation_style} \n")
    # print(f"\n{condition_data} \n")
    # api_key = os.getenv("OPENAI_API_KEY")
    # client = OpenAI(api_key=api_key)
    # clinical_note = generate_clinical_note(
    #     profile_data, patient, client, documentation_style
    # )
    # print(clinical_note)
    # save_clinical_note(clinical_note, documentation_style["name"])
