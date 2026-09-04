def generate_clinical_conditions(coding_context, client):
    prompt = f"""
    You are an experienced clinical documentation reviewer.

    Review the supplied coding context and identify the clinically relevant
    conditions for the current encounter.

    Your task is to understand the patient's current clinical situation,
    distinguish current encounter issues from historical information, and
    identify relationships between conditions when they are supported by
    the supplied context.

    Coding context:
    {coding_context}

    Rules:
    - Use the supplied coding context as the source of truth.
    - Identify conditions that are relevant to the current encounter.
    - Consider the current encounter issues first.
    - Consider historical active conditions only when they are clinically
      relevant to the current encounter.
    - Identify the status of each condition from the supplied context.
    - Preserve the supplied condition status; do not convert condition status into a
      final coding decision.
    - Distinguish medical conditions from social, demographic, or other
      non-medical findings.
    - Do not invent diagnoses, symptoms, relationships, severity, stages,
      complications, or clinical findings.
    - Do not assign ICD-10, ICD-9, CPT, SNOMED, or other billing codes.
    - If a condition relationship is not supported by the supplied context,
      do not infer one.
    - Use the clinical note as supporting evidence for the current encounter.
    - Do not treat every item in the patient's history as a condition that
      should be coded.
    - Return only conditions supported by the supplied clinical context.
    - Do not determine whether a condition should ultimately be coded.
    - Do not determine primary or secondary diagnosis sequencing.
    - Do not determine whether a condition is reportable for billing.
    - Do not make final ICD-10 coding decisions.

    Return the result in a clear structured format containing:
    1. Current encounter conditions
    2. Relevant historical conditions
    3. Condition relationships
    """

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt,
    )

    return response.output_text
