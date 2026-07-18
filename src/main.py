import os
import random
from pathlib import Path

import yaml
from dotenv import load_dotenv
from openai import OpenAI

import functions

load_dotenv()

api_key = os.getenv("OPENAI_API_KEY")
client = OpenAI(api_key=api_key)

BASE_DIR = Path(__file__).resolve().parent.parent
profile_path = BASE_DIR / "diagnosis_profiles" / "profiles" / "E11_9.yaml"

with open(profile_path, "r") as f:
    profile_data = yaml.safe_load(f)

if __name__ == "__main__":
    patient = {
        "name": functions.get_random_name(),
        "age": functions.get_random_age(),
        "sex": functions.get_random_sex(),
        "smoking_status": functions.get_random_smoking_status(),
        "comorbidities": random.sample(
            profile_data["common_comorbidities"], k=random.randint(0, 2)
        ),
    }

    print(patient)

    prompt = f"""
    You are an experienced physician.

    Generate a realistic outpatient clinical note.

    Diagnosis profile:
    {profile_data}

    Patient:
    {patient}

    Rules:
    - Use the diagnosis profile as the medical reference.
    - Use the supplied patient information.
    - Do not invent another primary diagnosis.
    - Produce only the clinical note.
    """

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt,
    )

    clinical_note = response.output_text
    print(clinical_note)
