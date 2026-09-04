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
- Review the historical conditions and include a historical condition when
  the supplied clinical note or encounter data provides evidence that it is
  relevant to the current encounter.
- Do not exclude a historical condition merely because it is not the primary
  reason for the encounter.
- Do not include historical conditions solely because they are present in the
  patient record.
- Identify the status of each condition from the supplied context.
- Preserve the supplied condition status; do not convert condition status
  into a final coding decision.
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
- Use procedures, assessment/plan, and the clinical note as evidence when
  determining whether a historical condition is relevant to the current
  encounter.
  
The number of conditions and relationships is dynamic:
- Do not assume or enforce a fixed number of conditions.
- Include every condition supported by the supplied coding context that
  meets the criteria.
- The lists may contain zero, one, or multiple conditions.
- Do not add, remove, or limit conditions to match the number of items
  shown in the example structure.
- The number of historical conditions may differ from the number of
  current conditions.
- The number of relationships may differ from the number of conditions.
- Only include relationships that are supported by the supplied context.
- If no supported relationships exist, return an empty relationships list.

Return ONLY valid JSON using this structure:

{{
    "current_conditions": [
        {{
            "name": "<condition name from the supplied context>",
            "status": "<status supported by the supplied context>",
            "encounter_relevance": true
        }}
    ],
    "historical_conditions": [
        {{
            "name": "<condition name from the supplied context>",
            "status": "<status supported by the supplied context>",
            "encounter_relevance": true
        }}
    ],
    "relationships": [
        {{
            "condition_1": "<condition name>",
            "condition_2": "<condition name>",
            "relationship": "<supported relationship between the conditions>"
        }}
    ]
}}

Important:
- The values shown above are placeholders demonstrating the required
  JSON structure only.
- Do not copy the placeholder values into the output.
- Populate all values dynamically from the supplied coding context.
- Do not invent placeholder conditions.
- Do not assume the example contains the correct number of conditions.
- If there are no relevant current conditions, return an empty list.
- If there are no relevant historical conditions, return an empty list.
- If there are no supported relationships, return an empty list.
- Do not include Markdown code fences.
- Do not include explanations before or after the JSON.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt,
    )

    return response.output_text
