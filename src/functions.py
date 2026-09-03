import base64
import json
from datetime import date


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
    age = None

    if birth_date:
        birth = date.fromisoformat(birth_date)
        today = date.today()

        age = (
            today.year
            - birth.year
            - ((today.month, today.day) < (birth.month, birth.day))
        )

    return {
        "name": full_name,
        "gender": patient.get("gender"),
        "birth_date": birth_date,
        "age": age,
        "marital_status": (patient.get("maritalStatus", {}).get("text")),
        "language": _get_language(patient),
        "race": _get_extension_value(patient, "us-core-race"),
        "ethnicity": _get_extension_value(patient, "us-core-ethnicity"),
    }


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

    return {
        "encounter": encounter,
        "conditions": _find_resources_for_encounter(
            "Condition", encounter_id, resources
        ),
        "notes": _find_resources_for_encounter(
            "DiagnosticReport", encounter_id, resources
        ),
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
