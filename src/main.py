from functions import (
    decode_note,
    get_data,
    get_encounter_data,
    get_resource_summary,
    normalize_patient_data,
)

if __name__ == "__main__":
    patient_data_file = r"C:\Users\akile\OneDrive\Desktop\medical-coding-project\synthetic-clinical-note-generator\src\patients\Earle679_Rohan584_b17949c8-25eb-0f29-f85a-11dcbf64eacd.json"

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
        for encounter_id in e_list:
            encounter_data = get_encounter_data(data, encounter_id)

            # Decode Base64 clinical notes
            for note in encounter_data["notes"]:
                decoded_note = decode_note(note)

                if decoded_note is not None:
                    note["presentedForm"][0]["data"] = decoded_note

            outfile.write(f"{encounter_data}\n")
