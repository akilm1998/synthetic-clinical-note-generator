import os

from dotenv import load_dotenv
from openai import OpenAI

from functions import (
    build_coding_context,
    get_data,
    get_resource_summary,
)
from prompt import generate_clinical_conditions

patient_data_file = (
    r"C:\Users\akile\OneDrive\Desktop\medical-coding-project"
    r"\synthetic-clinical-note-generator\src\patients"
    r"\Earle679_Rohan584_b17949c8-25eb-0f29-f85a-11dcbf64eacd.json"
)


if __name__ == "__main__":
    # -----------------------------------
    # Load environment variables
    # -----------------------------------

    load_dotenv()

    api_key = os.getenv("OPENAI_API_KEY")

    client = OpenAI(api_key=api_key)

    data = get_data(patient_data_file)

    resource_summary = get_resource_summary(data)

    encounters = [
        entry["resource"]
        for entry in data.get("entry", [])
        if entry.get("resource", {}).get("resourceType") == "Encounter"
    ]

    latest_encounter = max(
        encounters, key=lambda encounter: encounter["period"]["start"]
    )

    latest_encounter_id = latest_encounter["id"]

    coding_context = build_coding_context(data, latest_encounter_id)
    # print(coding_context)

    clinical_conditions = generate_clinical_conditions(coding_context, client)

    print(clinical_conditions)
