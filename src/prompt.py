def generate_clinical_note(profile_data, patient, client, note_generation_config):
    prompt = f"""
    You are an experienced physician.

    Generate a realistic outpatient clinical note written in the style of an experienced physician.

    Diagnosis profile:
    {profile_data}

    Patient:
    {patient}

    Encounter Type: {note_generation_config["encounter_type"]["name"]}
    Instructions:
    {note_generation_config["encounter_type"]["instructions"]}

    Documentation Depth: {note_generation_config["documentation_depth"]["name"]}
    Instructions:
    {note_generation_config["documentation_depth"]["instructions"]}

    Narrative Style: {note_generation_config["narrative_style"]["name"]}
    Instructions:
    {note_generation_config["narrative_style"]["instructions"]}

    Physician Style: {note_generation_config["physician_style"]["name"]}
    Instructions:
    {note_generation_config["physician_style"]["instructions"]}

    Adapt the amount of detail, sentence length, and documentation depth to match the requested style while preserving all clinically important information.

    Rules:
    - Use the diagnosis profile as the medical reference.
    - Use ONLY the supplied patient information.
    - Do not invent another primary diagnosis.
    - Incorporate every relevant patient attribute naturally into the note whenever clinically appropriate (age, sex, smoking status, BMI, duration of disease, comorbidities, laboratory values, etc.).
    - Do not contradict any supplied patient information.
    - If laboratory values are provided, use only those values. Do not invent additional laboratory results.
    - If vital signs are provided, use them. Otherwise, generate realistic vital signs appropriate for the patient's age and condition.
    - Do not invent medications, allergies, imaging findings, procedures, surgeries, specialist recommendations, hospitalizations, family history, social history, or physical examination findings unless they are explicitly provided or directly implied by the diagnosis profile.
    - Do not mention tests, screenings, referrals, or follow-up investigations unless they are clinically appropriate and clearly presented as recommendations rather than completed findings.
    - Do not state that information is unavailable, missing, or due unless explicitly indicated.
    - Keep the note internally consistent.
    - Ensure all generated values are physiologically plausible and consistent with the patient's demographics, diagnoses, BMI, laboratory values, and disease duration.
    - Do not include ICD-10 codes, ICD-9 codes, CPT codes, SNOMED codes, billing information, or administrative text.
    - Format the note using standard clinical documentation sections with clear headings (e.g., Chief Complaint, Subjective, Objective, Assessment, Plan). Place each section on its own line.
    - Produce only the clinical note as plain text. Do not use Markdown formatting, headings beginning with #, bold text (**), bullet points, or code fences.
    - Every field in the supplied Patient object should either:
        (a) appear naturally in the clinical note, or
        (b) be intentionally omitted because it is not clinically relevant.
        Do not ignore patient attributes without reason.
    - Use the provided condition management field to influence the tone of the assessment and plan, but do not simply restate it verbatim unless it reads naturally.
    """
    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt,
    )
    return response.output_text
