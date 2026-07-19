import os

from dotenv import load_dotenv
from openai import OpenAI

from functions import generate_patient_data, get_profile_data
from prompt import generate_clinical_note

if __name__ == "__main__":
    load_dotenv()
    profile_data = get_profile_data("E11_9")
    patient = generate_patient_data(profile_data)
    api_key = os.getenv("OPENAI_API_KEY")
    client = OpenAI(api_key=api_key)

    print(patient)

    clinical_note = generate_clinical_note(profile_data, patient, client)
    print(clinical_note)
