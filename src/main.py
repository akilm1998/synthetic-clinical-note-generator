import os

from dotenv import load_dotenv
from openai import OpenAI

from functions import (
    generate_clinical_note_documentaion_style,
    generate_condition_data,
    generate_patient_data,
    get_profile_data,
    save_clinical_note,
)
from prompt import generate_clinical_note

# from prompt import generate_clinical_note

if __name__ == "__main__":
    load_dotenv()
    profile_data = get_profile_data("E11_9")
    # print(profile_data)
    documentation_style = generate_clinical_note_documentaion_style()
    patient = generate_patient_data(profile_data)
    condition_data = generate_condition_data(patient)
    patient.update(condition_data)
    # print(patient)
    print(documentation_style)
    print(condition_data)
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)
    clinical_note = generate_clinical_note(
        profile_data, patient, client, documentation_style
    )
    print(clinical_note)
    save_clinical_note(clinical_note, documentation_style["name"])
