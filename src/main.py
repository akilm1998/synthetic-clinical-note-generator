import os

from dotenv import load_dotenv
from openai import OpenAI

from functions import (
    build_coding_context,
    get_data,
    get_resource_summary,
)
from prompt import generate_clinical_conditions

# patient_data_file = (
#     r"C:\Users\akile\OneDrive\Desktop\medical-coding-project"
#     r"\synthetic-clinical-note-generator\src\patients"
#     r"\Earle679_Rohan584_b17949c8-25eb-0f29-f85a-11dcbf64eacd.json"
# )

patient_data_file = r"C:\Users\akile\OneDrive\Desktop\medical-coding-project\synthetic-clinical-note-generator\src\patients\Dusty207_Camie739_Borer986_cfbfafa9-f136-b5b1-0d08-1f6c2bd08eef.json"

# patient_data_file = r"C:\Users\akile\OneDrive\Desktop\medical-coding-project\synthetic-clinical-note-generator\src\patients\Hiram237_Kutch271_dd4175fd-83d4-bc95-8ff9-4943947151d5.json"
# patient_data_file = r"C:\Users\akile\OneDrive\Desktop\medical-coding-project\synthetic-clinical-note-generator\src\patients\Pasquale620_Ernser583_466a7f1d-d7ad-fae4-ccfd-2519b8e66c80.json"


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
    if not coding_context["patient"]["alive"]:
        raise SystemExit("Patient is deceased. Skipping coding pipeline.")

    print(f"{coding_context}\n\n\n")
    # exit(0)

    clinical_conditions = generate_clinical_conditions(coding_context, client)

    print(clinical_conditions)
