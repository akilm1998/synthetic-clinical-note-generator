# import pprint
# import json

from functions import (
    get_data,
    get_encounter_data,
    get_resource_summary,
    normalize_patient_data,
)

if __name__ == "__main__":
    patient_data_file = r"C:\Users\akile\OneDrive\Desktop\medical-coding-project\synthetic-clinical-note-generator\src\patients\Yong583_Jerde200_ae2c0ccb-742b-f5c3-9406-69541702580a.json"
    patient_data_file = r"C:\Users\akile\OneDrive\Desktop\medical-coding-project\synthetic-clinical-note-generator\src\patients\Earle679_Rohan584_b17949c8-25eb-0f29-f85a-11dcbf64eacd.json"
    data = get_data(patient_data_file)

    normalized_data = normalize_patient_data(data)
    resource_summary = get_resource_summary(data)
    # print(normalized_data)
    print(type(resource_summary))
    # with open("normalized_patient_data.json", "w") as outfile:
    #     json.dump(normalized_data, outfile, indent=4)
    # with open("resource_summary.json", "w") as outfile:
    #     json.dump(resource_summary, outfile, indent=4)
    # pprint.pprint(normalized_data, sort_dicts=False)

    e_list = []
    count = 0

    for each_resource in resource_summary.values():
        if each_resource["resourceType"] == "Encounter":
            count += 1
            e_list.append(each_resource["id"])
    # print(e_list)
    print(f"Total encounters: {count}")

    with open("encounter_data.txt", "w") as outfile:
        for encounter_id in e_list:
            encounter_data = get_encounter_data(data, encounter_id)
            outfile.write(f"{encounter_data}\n")
