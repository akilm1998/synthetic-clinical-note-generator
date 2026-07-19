def generate_clinical_note(profile_data, patient, client):
    prompt = f"""
    You are an experienced physician.

    Generate a realistic outpatient clinical note written in the style of an experienced physician.

    Diagnosis profile:
    {profile_data}

    Patient:
    {patient}

    Rules:
    - Use the diagnosis profile as the medical reference.
    - Use the supplied patient information.
    - Do not invent another primary diagnosis.
    - Do not include ICD-10 codes, ICD-9 codes, CPT codes, SNOMED codes, or billing information
    - Produce only the clinical note as plain text. Do not use Markdown formatting, headings beginning with #, bold text (**), bullet points, or code fences.
    """

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt,
    )
    return response.output_text
