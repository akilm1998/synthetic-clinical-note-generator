import base64
import json
from datetime import date, datetime


def get_data(patient_data: str):
    with open(patient_data, "r") as file:
        data = json.load(file)
        return data


def normalize_patient_data(data):
    """
    Normalize a Synthea FHIR Bundle into a patient-centric structure
    suitable for downstream clinical-document generation.

    Input:
        data: parsed FHIR Bundle (dict)

    Returns:
        dict containing patient demographics and encounter-linked
        clinical resources.
    """

    resources = [
        entry["resource"] for entry in data.get("entry", []) if "resource" in entry
    ]

    patient = next((r for r in resources if r.get("resourceType") == "Patient"), None)

    if patient is None:
        raise ValueError("FHIR Bundle does not contain a Patient resource.")

    normalized = {
        "patient": _normalize_patient(patient),
        "encounters": [],
    }

    for encounter in (r for r in resources if r.get("resourceType") == "Encounter"):
        normalized["encounters"].append(_normalize_encounter(encounter, resources))

    return normalized


def _normalize_patient(patient):
    """Extract patient-level information relevant to clinical context."""

    name = patient.get("name", [{}])[0]

    full_name = (
        name.get("prefix", [""])[0]
        + " "
        + name.get("given", [""])[0]
        + " "
        + name.get("family", "")
    ).strip()

    birth_date = patient.get("birthDate")
    alive = is_patient_alive(patient)

    return {
        "name": full_name,
        "gender": patient.get("gender"),
        "birth_date": birth_date,
        "alive": alive,
        "marital_status": patient.get("maritalStatus", {}).get("text"),
        "language": _get_language(patient),
        "race": _get_extension_value(patient, "us-core-race"),
        "ethnicity": _get_extension_value(patient, "us-core-ethnicity"),
    }


def is_patient_alive(patient):
    if patient.get("deceasedBoolean") is True:
        return False

    if patient.get("deceasedDateTime") is not None:
        return False

    return True


def _normalize_encounter(encounter, resources):
    """Build the clinical context associated with one encounter."""

    encounter_id = encounter.get("id")

    return {
        "id": encounter_id,
        "status": encounter.get("status"),
        "class": encounter.get("class", {}).get("code"),
        "type": _extract_codeable_concept(encounter.get("type", [])),
        "period": encounter.get("period"),
        "reason": _extract_codeable_concept(encounter.get("reasonCode", [])),
        "conditions": _find_resources_for_encounter(
            "Condition", encounter_id, resources
        ),
        "medications": _find_resources_for_encounter(
            "MedicationRequest", encounter_id, resources
        ),
        "observations": _find_resources_for_encounter(
            "Observation", encounter_id, resources
        ),
        "diagnostic_reports": _find_resources_for_encounter(
            "DiagnosticReport", encounter_id, resources
        ),
        "procedures": _find_resources_for_encounter(
            "Procedure", encounter_id, resources
        ),
        "notes": _find_resources_for_encounter(
            "DocumentReference", encounter_id, resources
        ),
    }


def calculate_age_at_encounter(birth_date, encounter_date):
    if not birth_date or not encounter_date:
        return None

    birth = date.fromisoformat(birth_date)
    encounter = date.fromisoformat(encounter_date)

    return (
        encounter.year
        - birth.year
        - ((encounter.month, encounter.day) < (birth.month, birth.day))
    )


def _find_resources_for_encounter(resource_type, encounter_id, resources):
    """Find resources explicitly linked to an encounter."""

    matches = []

    for resource in resources:
        if resource.get("resourceType") != resource_type:
            continue

        encounter = resource.get("encounter", {})
        reference = encounter.get("reference", "")

        if reference.endswith(encounter_id):
            matches.append(resource)

    return matches


def _extract_codeable_concept(items):
    """Extract coding information from CodeableConcept-like structures."""

    result = []

    for item in items or []:
        for coding in item.get("coding", []):
            result.append(
                {
                    "system": coding.get("system"),
                    "code": coding.get("code"),
                    "display": coding.get("display"),
                }
            )

        if item.get("text"):
            result.append({"text": item["text"]})

    return result


def _get_language(patient):

    communication = patient.get("communication", [])

    if not communication:
        return None

    return communication[0].get("language", {}).get("text")


def _get_extension_value(patient, extension_name):
    """Extract the text value from a US Core patient extension."""

    for extension in patient.get("extension", []):
        if extension_name not in extension.get("url", ""):
            continue

        for nested in extension.get("extension", []):
            if nested.get("url") == "text":
                return nested.get("valueString")

    return None


def get_resource_summary(data):
    result = {}

    for entry in data.get("entry", []):
        full_url = entry.get("fullUrl")
        resource = entry.get("resource", {})

        if full_url:
            result[full_url] = {
                "resourceType": resource.get("resourceType"),
                "id": resource.get("id"),
                "status": resource.get("status"),
            }

    return result


def get_encounter_data(data, encounter_id):
    resources = [
        entry["resource"] for entry in data.get("entry", []) if "resource" in entry
    ]

    encounter = next(
        (
            resource
            for resource in resources
            if resource.get("resourceType") == "Encounter"
            and resource.get("id") == encounter_id
        ),
        None,
    )

    if encounter is None:
        raise ValueError(f"Encounter not found: {encounter_id}")

    diagnostic_reports = _find_resources_for_encounter(
        "DiagnosticReport",
        encounter_id,
        resources,
    )

    notes = []

    for report in diagnostic_reports:
        clinical_note = decode_note(report)

        if clinical_note is not None:
            notes.append(
                {
                    "source": "DiagnosticReport",
                    "source_id": report.get("id"),
                    "clinical_note": clinical_note,
                }
            )

    return {
        "encounter": encounter,
        "encounter_reason": _extract_codeable_concept(encounter.get("reasonCode", [])),
        "conditions": _find_resources_for_encounter(
            "Condition",
            encounter_id,
            resources,
        ),
        "procedures": _find_resources_for_encounter(
            "Procedure",
            encounter_id,
            resources,
        ),
        "observations": _find_resources_for_encounter(
            "Observation",
            encounter_id,
            resources,
        ),
        "medications": _find_resources_for_encounter(
            "MedicationRequest",
            encounter_id,
            resources,
        ),
        "diagnostic_reports": diagnostic_reports,
        "notes": notes,
    }


def decode_note(note):
    """Decode the Base64-encoded clinical note from a DiagnosticReport."""

    presented_form = note.get("presentedForm", [])

    if not presented_form:
        return None

    encoded_data = presented_form[0].get("data")

    if not encoded_data:
        return None

    return base64.b64decode(encoded_data).decode("utf-8")


def build_coding_context(data, encounter_id):
    """
    Build the clinical context for the latest/current encounter.

    Includes:
        - patient demographics
        - patient age at encounter
        - current encounter
        - conditions linked to the current encounter
        - active/unresolved conditions as of the current encounter
        - current clinical note
    """

    normalized_data = normalize_patient_data(data)

    encounter_data = get_encounter_data(data, encounter_id)

    encounter_date = encounter_data["encounter"]["period"]["start"]

    current_date = datetime.fromisoformat(encounter_date)

    age_at_encounter = calculate_age_at_encounter(
        normalized_data["patient"]["birth_date"],
        encounter_date[:10],
    )

    active_conditions = []

    resources = [
        entry["resource"] for entry in data.get("entry", []) if "resource" in entry
    ]

    for resource in resources:
        if resource.get("resourceType") != "Condition":
            continue

        condition_status = (
            resource.get("clinicalStatus", {}).get("coding", [{}])[0].get("code")
        )

        if condition_status != "active":
            continue

        onset = resource.get("onsetDateTime")

        if onset:
            onset_date = datetime.fromisoformat(onset)

            if onset_date > current_date:
                continue

        active_conditions.append(resource)

    clinical_notes = [
        note["clinical_note"]
        for note in encounter_data["notes"]
        if note.get("clinical_note")
    ]

    return {
        "patient": {
            **normalized_data["patient"],
            "age": age_at_encounter,
        },
        "current_encounter": encounter_data["encounter"],
        "encounter_reason": (encounter_data["encounter_reason"]),
        "current_issues": encounter_data["conditions"],
        "historical_active_conditions": active_conditions,
        "clinical_notes": clinical_notes,
    }
