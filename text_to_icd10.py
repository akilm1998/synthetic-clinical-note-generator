import re
from typing import Optional

import requests
from bs4 import BeautifulSoup

BASE_URL = "https://www.icd10data.com"


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


# Words that are usually too common to be useful
STOP_WORDS = {
    "and",
    "or",
    "of",
    "the",
    "with",
    "without",
    "in",
    "on",
    "for",
    "a",
    "an",
}


def clean_text(text: str) -> str:
    """
    Normalize whitespace.
    """

    return " ".join(text.split())


def text_to_words(text: str) -> list[str]:
    """
    Convert text into a normalized list of words.

    Example:

    "Type 2 Diabetes Mellitus"
        ->
    ["type", "2", "diabetes", "mellitus"]
    """

    text = text.lower()

    # Keep letters and numbers
    words = re.findall(
        r"[a-z0-9]+",
        text,
    )

    # Remove very common words
    words = [word for word in words if word not in STOP_WORDS]

    return words


def calculate_match_score(
    input_words: list[str],
    candidate_text: str,
) -> int:
    """
    Compare input words with a candidate condition.

    Score = number of matching words.
    """

    candidate_words = text_to_words(candidate_text)

    input_set = set(input_words)

    candidate_set = set(candidate_words)

    matching_words = input_set & candidate_set

    return len(matching_words)


def get_icd10_code(
    condition: str,
) -> Optional[dict]:
    """
    Search ICD10Data for a condition name.

    Compare the user's condition against all search results.

    Return the result with the highest keyword match.
    """

    condition = clean_text(condition)

    print(f"Searching for condition: {condition}")

    input_words = text_to_words(condition)

    response = requests.get(
        f"{BASE_URL}/search",
        params={"s": condition},
        headers=HEADERS,
        timeout=15,
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    candidates = []

    # ---------------------------------------------
    # GET ALL SEARCH RESULTS
    # ---------------------------------------------

    for search_line in soup.select(".searchLine"):
        identifier = search_line.select_one("span.identifier")

        link = search_line.select_one("strong a[href]")

        if not identifier or not link:
            continue

        code = clean_text(
            identifier.get_text(
                " ",
                strip=True,
            )
        ).upper()

        # Get the result title
        title = clean_text(
            link.get_text(
                " ",
                strip=True,
            )
        )

        if not title:
            continue

        # Calculate similarity score
        score = calculate_match_score(
            input_words,
            title,
        )

        candidates.append(
            {
                "code": code,
                "description": title,
                "score": score,
            }
        )
        print(candidates)

    if not candidates:
        print("No ICD-10 results found.")

        return None

    # ---------------------------------------------
    # SORT BY HIGHEST SCORE
    # ---------------------------------------------

    candidates.sort(
        key=lambda item: item["score"],
        reverse=True,
    )

    best_match = candidates[0]

    return best_match


if __name__ == "__main__":
    condition = input("Enter condition name: ")

    result = get_icd10_code(condition)

    if result:
        print()

        print("=" * 60)

        print(f"INPUT: {condition}")

        print(f"BEST MATCH: {result['description']}")

        print(f"ICD-10 CODE: {result['code']}")

        print(f"MATCH SCORE: {result['score']}")

        print("=" * 60)
