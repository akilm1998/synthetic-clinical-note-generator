import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from functions import (
    analyze_scraped_results,
    build_coding_context,
    collect_unique_codes,
    get_data,
    get_resource_summary,
    scrape_codes_until_complete,
)
from prompt import generate_clinical_conditions
from text_to_icd10 import text_to_icd10

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

    # print(f"{coding_context}\n\n\n")
    # exit(0)

    clinical_conditions = generate_clinical_conditions(
        coding_context, client
    )  # LLM #1 JSON output from clinical condition extraction

    # print(clinical_conditions)

    # Convert string to dictionary (LLM #1 JSON) for processing in text_to_icd10.py

    try:
        data = json.loads(clinical_conditions)

    except json.JSONDecodeError as error:
        raise SystemExit(f"Invalid JSON: {error}")

    # Retrieve ICD-10 candidates from LLM #1 JSON

    icd10_candidates = text_to_icd10(data)
    # print(type(icd10_candidates))
    unique_candidate_codes = collect_unique_codes(icd10_candidates["results"])
    with open("unique_candidate_codes.txt", "w") as outfile:
        outfile.write(f"{unique_candidate_codes}\n")
    # print(f"Unique ICD-10 candidates: {unique_candidate_codes}")

    # Scrape ICD-10 codes from icd10data website

    scraped_results, failed_codes = scrape_codes_until_complete(unique_candidate_codes)

    if failed_codes:
        print("\nCodes that could not be scraped:")
        for code in failed_codes:
            print(code)
        # print(f"Scraped ICD-10 codes: \n\n{scraped_results}")
    with open("scraped_icd10_codes.json", "w") as outfile:
        json.dump(scraped_results, outfile, indent=4)

    coding_decision_context = {
        "clinical_context": coding_context,
        "clinical_extraction": clinical_conditions,
        "icd10_candidates": scraped_results,
    }

    analysis = analyze_scraped_results(scraped_results)

    print()
    print("=" * 60)
    print("SCRAPED RESULTS ANALYSIS")
    print("=" * 60)

    for key, value in analysis.items():
        print(f"{key}: {value}")
