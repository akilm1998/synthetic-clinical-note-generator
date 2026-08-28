import spacy

nlp = spacy.load("en_core_web_sm")


def extract_clinical_terms(text: str) -> list[str]:

    doc = nlp(text)

    terms = []

    # ----------------------------------------
    # 1. Extract noun phrases
    # ----------------------------------------

    for chunk in doc.noun_chunks:
        phrase = chunk.text.strip().lower()

        # Ignore patient identifiers
        if phrase.startswith("patient"):
            continue

        terms.append(phrase)

    # ----------------------------------------
    # 2. Extract important adjectives
    # ----------------------------------------

    for token in doc:
        if token.pos_ == "ADJ":
            adjective = token.text.lower()

            terms.append(adjective)

    # ----------------------------------------
    # 3. Extract important verbs
    # ----------------------------------------

    for token in doc:
        if token.pos_ == "VERB":
            verb = token.lemma_.lower()

            terms.append(verb)

    # ----------------------------------------
    # Remove duplicates
    # ----------------------------------------

    unique_terms = []

    for term in terms:
        if term not in unique_terms:
            unique_terms.append(term)

    return unique_terms


if __name__ == "__main__":
    text = (
        "Patient A is 22 weeks pregnant having hypertension "
        "with pre-existing heart disease coupled with chronic back pain."
    )

    terms = extract_clinical_terms(text)

    print("\nExtracted clinical terms:\n")

    for term in terms:
        print(term)
