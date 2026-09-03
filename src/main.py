import os

from functions import (
    get_data,
    get_encounter_data,
    get_resource_summary,
    normalize_patient_data,
)

file_paths = [
    "encounter_data.txt",
    "patient_encounter_notes.txt",
]


if __name__ == "__main__":
    # Check if the file exists before deleting
    for file_path in file_paths:
        if os.path.exists(file_path):
            os.remove(file_path)
            print(f"Deleted: {file_path}")

    patient_data_file = (
        r"C:\Users\akile\OneDrive\Desktop\medical-coding-project"
        r"\synthetic-clinical-note-generator\src\patients"
        r"\Earle679_Rohan584_b17949c8-25eb-0f29-f85a-11dcbf64eacd.json"
    )

    data = get_data(patient_data_file)

    normalized_data = normalize_patient_data(data)

    resource_summary = get_resource_summary(data)

    print(type(resource_summary))

    e_list = []
    count = 0

    for each_resource in resource_summary.values():
        if each_resource["resourceType"] == "Encounter":
            count += 1
            e_list.append(each_resource["id"])

    print(f"Total encounters: {count}")

    with open("encounter_data.txt", "w") as outfile:
        with open("patient_encounter_notes.txt", "w") as note_file:
            for encounter_id in e_list:
                encounter_data = get_encounter_data(data, encounter_id)
                print(encounter_data)

                # Write clean clinical notes for inspection
                for note in encounter_data["notes"]:
                    clinical_note = note.get("clinical_note")

                    if clinical_note is not None:
                        note_file.write(f"Encounter ID: {encounter_id}\n")

                        note_file.write(
                            f"DiagnosticReport ID: {note.get('source_id')}\n"
                        )

                        note_file.write(f"Clinical Note:\n{clinical_note}\n\n")

                outfile.write(f"{encounter_data}\n")
