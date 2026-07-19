def generate_clinical_note(profile_data, patient, client):
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
    return response.output_text
