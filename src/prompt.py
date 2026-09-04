def generate_clinical_conditions(coding_context, client):
    prompt = f"""
You are an experienced clinical documentation reviewer.

Review the supplied coding context and identify the clinically relevant
conditions for the current encounter.

Your task is to:

1. Identify conditions relevant to the current encounter.
2. Distinguish current conditions from historical conditions.
3. Identify clinically meaningful relationships between conditions when
   supported by the supplied evidence.
4. Enrich conditions and relationships with medically precise terminology
   that can improve downstream ICD-10-CM candidate retrieval.

Coding context:
{coding_context}


CORE RULES:

- Use the supplied coding context as the source of truth.
- Return only conditions supported by the supplied clinical context.
- Consider the current encounter issues first.
- Include historical conditions when the supplied encounter information,
  clinical note, assessment/plan, procedures, observations, or other
  supplied evidence establishes that they are relevant to the current
  encounter.
- Do not include historical conditions merely because they exist somewhere
  in the patient's record.
- Preserve the condition status supported by the supplied context.
- Distinguish medical conditions from social, demographic, administrative,
  or other non-medical findings.
- Do not assign ICD-10, ICD-9, CPT, SNOMED, or other billing codes.
- Do not make the final coding decision.
- Do not determine primary or secondary diagnosis sequencing.
- Do not determine billing reportability.


CLINICAL TERMINOLOGY:

For each condition, provide:

- "clinical_terms": medically precise terminology and clinically relevant
  synonyms supported by the supplied clinical context.
- "search_terms": terminology useful for retrieving ICD-10-CM candidates.

For each relationship, provide:

- "relationship": a concise description of the supported clinical
  relationship.
- "clinical_terms": medically precise terminology describing the
  relationship.
- "search_terms": terminology useful for retrieving ICD-10-CM candidates
  for that relationship.

Use the most clinically specific terminology that is supported by the
supplied evidence.

Do not introduce new clinical facts while enriching terminology.

A qualifier or characteristic may be included only when it is explicitly
documented or directly and unambiguously derivable from the supplied
clinical context.

This applies to characteristics such as:

- severity
- stage
- laterality
- anatomical site
- acuity
- chronicity
- recurrence
- timing
- duration
- pregnancy characteristics
- gestational information
- pregnancy order
- number of occurrences
- complications
- manifestations
- underlying conditions
- other clinically relevant qualifiers

Do not infer missing specificity simply because it is clinically plausible,
commonly associated with the condition, or useful for finding a more
specific ICD-10-CM code.

If the evidence does not support greater specificity, use the more general
medically accurate terminology supported by the source.

Clinical terminology may improve the wording of a documented concept, but
must not change its factual meaning.

Keep qualifiers attached to the condition or clinical event they actually
describe. Do not transfer characteristics from one condition or event to
another.


RELATIONSHIPS:

Identify a relationship only when it is supported by the supplied clinical
context.

A relationship should describe the actual clinical connection between the
identified conditions rather than simply stating that they coexist.

The relationship may represent a documented or directly derivable:

- causal relationship
- etiological relationship
- underlying condition and manifestation
- complication
- associated condition
- current condition and relevant historical condition
- other clinically meaningful relationship

Do not infer a relationship solely because two conditions commonly occur
together or are present in the same patient.

Relationship terminology and search terms must follow the same
evidence-grounding rule as condition terminology.

Do not use relationships to introduce clinical facts that are absent from
the supplied context.


SEARCH TERMS:

Search terms are for retrieval only.

They should help a downstream ICD-10-CM search find plausible candidate
codes representing the documented clinical concept.

Search terms may include:

- the original condition terminology
- standard medical terminology
- supported clinical synonyms
- supported qualifiers
- supported relationship terminology

Do not include ICD-10-CM codes in the output.

Do not choose a code based on the search terms.


DYNAMIC CARDINALITY:

- Do not assume a fixed number of conditions.
- Include every condition supported by the supplied context that meets the
  relevance criteria.
- There may be zero, one, or multiple current conditions.
- There may be zero, one, or multiple historical conditions.
- There may be zero, one, or multiple relationships.
- Multiple relationships may involve the same condition.
- A condition does not require a relationship with another condition.
- If no supported relationships exist, return an empty relationships list.


FIELD DEFINITIONS:

- "name": the condition identified from the supplied clinical context.
- "status": the status supported by the supplied clinical context.
- "encounter_relevance": whether the condition is relevant to the current
  encounter.
- "clinical_terms": medically precise terminology representing the same
  documented clinical concept.
- "search_terms": retrieval terminology for finding plausible ICD-10-CM
  candidates.
- "condition_1": first condition participating in the relationship.
- "condition_2": second condition participating in the relationship.
- "relationship": clinically meaningful description of the supported
  relationship between the conditions.

None of these fields represent a final ICD-10-CM coding decision.


OUTPUT:

Return ONLY valid JSON using this structure:

{{
    "current_conditions": [
        {{
            "name": "<condition name from the supplied context>",
            "status": "<status supported by the supplied context>",
            "encounter_relevance": true,
            "clinical_terms": [
                "<medically precise supported term>"
            ],
            "search_terms": [
                "<useful supported ICD-10-CM retrieval term>"
            ]
        }}
    ],
    "historical_conditions": [
        {{
            "name": "<condition name from the supplied context>",
            "status": "<status supported by the supplied context>",
            "encounter_relevance": true,
            "clinical_terms": [
                "<medically precise supported term>"
            ],
            "search_terms": [
                "<useful supported ICD-10-CM retrieval term>"
            ]
        }}
    ],
    "relationships": [
        {{
            "condition_1": "<condition name>",
            "condition_2": "<condition name>",
            "relationship": "<supported clinical relationship>",
            "clinical_terms": [
                "<medically precise supported relationship term>"
            ],
            "search_terms": [
                "<useful supported ICD-10-CM retrieval term>"
            ]
        }}
    ]
}}

IMPORTANT:

- Populate all values dynamically from the supplied coding context.
- Do not copy the placeholder values into the output.
- Do not invent conditions or relationships.
- Do not invent clinical qualifiers.
- Do not include unsupported specificity.
- If no additional clinical terminology is supported, return an empty
  "clinical_terms" list.
- If no useful supported retrieval terminology exists, return an empty
  "search_terms" list.
- If there are no relevant current conditions, return an empty list.
- If there are no relevant historical conditions, return an empty list.
- If there are no supported relationships, return an empty list.
- Do not include ICD-10-CM codes anywhere in the output.
- Do not include Markdown code fences.
- Do not include explanations before or after the JSON.
- Do not use terminology that implies a clinical relationship, complication, encounter subtype, temporal state, or other qualifier unless that implication is supported by the supplied evidence.
"""

    response = client.responses.create(
        model="gpt-5.6-luna",
        input=prompt,
    )

    return response.output_text
