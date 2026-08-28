from collections import OrderedDict
from typing import Optional
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup, Tag

BASE_URL = "https://www.icd10data.com"


HEADERS = {
    "User-Agent": (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 "
        "(KHTML, like Gecko) "
        "Chrome/120.0 Safari/537.36"
    )
}


# ============================================================
# TEXT CLEANING
# ============================================================


def clean_text(value) -> str:
    """
    Convert a BeautifulSoup element or string into clean text.
    """

    if isinstance(value, Tag):
        return " ".join(value.stripped_strings)

    return " ".join(str(value).split())


# ============================================================
# HTTP SESSION
# ============================================================


def create_session() -> requests.Session:

    session = requests.Session()

    session.headers.update(HEADERS)

    return session


# ============================================================
# REMOVE UNWANTED / HIDDEN CONTENT
# ============================================================


def remove_unwanted_content(
    soup: BeautifulSoup,
) -> None:
    """
    Remove hidden popovers, scripts, ads, and other elements
    that can pollute text extraction.
    """

    selectors = [
        ".z32",
        ".inPopover",
        ".tip",
        ".tipHelp",
        ".images-note",
        "script",
        "style",
        "noscript",
        "iframe",
    ]

    for selector in selectors:
        for element in soup.select(selector):
            element.decompose()


# ============================================================
# FIND EXACT ICD-10 URL
# ============================================================


def get_icd10data_url(
    session: requests.Session,
    code: str,
) -> Optional[str]:

    code = code.strip().upper()

    response = session.get(
        f"{BASE_URL}/search",
        params={
            "s": code,
        },
        timeout=20,
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    # --------------------------------------------------------
    # Search results
    # --------------------------------------------------------

    for search_line in soup.select(".searchLine"):
        identifier = search_line.select_one("span.identifier")

        if not identifier:
            continue

        found_code = clean_text(identifier).upper()

        # Exact match only
        if found_code != code:
            continue

        # Prefer the main result link
        link = search_line.select_one("strong a[href]")

        # Fallback
        if not link:
            link = search_line.select_one("a[href]")

        if not link:
            continue

        href = link.get("href")

        if isinstance(href, str):
            return urljoin(
                BASE_URL,
                href,
            )

    return None


# ============================================================
# FIND THE EXACT MAIN ICD HEADING
# ============================================================


def get_main_heading_container(
    soup: BeautifulSoup,
    code: str,
) -> Optional[Tag]:

    code = code.strip().upper()

    for container in soup.select("div.headingContainer"):
        identifier = container.select_one("span.identifierDetail")

        if not identifier:
            continue

        found_code = clean_text(identifier).upper()

        if found_code == code:
            return container

    return None


# ============================================================
# GET DESCRIPTION
# ============================================================


def get_description(
    heading_container: Tag,
) -> Optional[str]:

    description_tag = heading_container.find_next_sibling(
        "h2",
        class_="codeDescription",
    )

    if description_tag:
        return clean_text(description_tag)

    return None


# ============================================================
# FIND THE END OF THIS ICD CODE'S CONTENT
# ============================================================


def is_next_code_heading(
    tag: Tag,
    main_heading: Tag,
) -> bool:

    if tag is main_heading:
        return False

    if tag.name != "div":
        return False

    classes = tag.get("class")

    if not isinstance(classes, list):
        return False

    return "headingContainer" in classes


# ============================================================
# DETECT POSSIBLE SECTION HEADINGS
# ============================================================


def looks_like_section_heading(
    tag: Tag,
) -> bool:
    """
    Dynamically determine whether a tag looks like an ICD
    section heading.

    We deliberately do not use a fixed set of section names.
    """

    if tag.name not in {
        "span",
        "div",
        "h2",
        "h3",
        "h4",
        "strong",
    }:
        return False

    text = clean_text(tag)

    if not text:
        return False

    # Avoid very long text blocks
    if len(text) > 100:
        return False

    # Known structural classes frequently used by ICD10Data
    classes = tag.get("class")

    if isinstance(classes, list):
        class_string = " ".join(classes).lower()

        keywords = [
            "heading",
            "annotation",
            "section",
        ]

        if any(keyword in class_string for keyword in keywords):
            return True

    # Common ICD annotation heading patterns
    heading_keywords = [
        "includes",
        "excludes",
        "code first",
        "code also",
        "use additional",
        "use external cause",
        "approximate synonyms",
        "clinical information",
        "coding rules",
        "code history",
        "applicable to",
        "parent code notes",
    ]

    text_lower = text.lower()

    if any(keyword in text_lower for keyword in heading_keywords):
        return True

    return False


# ============================================================
# GET SECTION NAME
# ============================================================


def get_section_name(
    tag: Tag,
) -> Optional[str]:

    if not looks_like_section_heading(tag):
        return None

    text = clean_text(tag)

    if not text:
        return None

    return text


# ============================================================
# EXTRACT DIRECT LIST ITEMS
# ============================================================


def extract_list_items(
    ul: Tag,
) -> list[str]:

    items = []

    for li in ul.find_all(
        "li",
        recursive=False,
    ):
        text = clean_text(li)

        if text:
            items.append(text)

    return items


# ============================================================
# EXTRACT TEXT FROM A SINGLE TAG
# ============================================================


def extract_tag_content(
    tag: Tag,
) -> list[str]:

    # --------------------------------------------------------
    # UL
    # --------------------------------------------------------

    if tag.name in {
        "ul",
        "ol",
    }:
        return extract_list_items(tag)

    # --------------------------------------------------------
    # Paragraph / div
    # --------------------------------------------------------

    if tag.name in {
        "p",
        "div",
    }:
        text = clean_text(tag)

        if text:
            return [text]

    return []


# ============================================================
# EXTRACT ALL SECTIONS DYNAMICALLY
# ============================================================


def extract_dynamic_sections(
    heading_container: Tag,
) -> dict[str, list[str]]:
    """
    Extract all sections dynamically.

    A section starts when a section heading is detected.

    Its content continues until:

    - another section heading begins
    - another ICD headingContainer begins
    """

    sections = OrderedDict()

    current_section = None

    for tag in heading_container.find_all_next():
        if not isinstance(tag, Tag):
            continue

        # ----------------------------------------------------
        # STOP AT NEXT ICD CODE
        # ----------------------------------------------------

        if is_next_code_heading(
            tag,
            heading_container,
        ):
            break

        # ----------------------------------------------------
        # IGNORE POPUP / HIDDEN CONTENT
        # ----------------------------------------------------

        classes = tag.get("class")

        if isinstance(classes, list):
            if "z32" in classes:
                continue

        # ----------------------------------------------------
        # CHECK FOR NEW SECTION
        # ----------------------------------------------------

        section_name = get_section_name(tag)

        if section_name:
            current_section = section_name

            if current_section not in sections:
                sections[current_section] = []

            continue

        # ----------------------------------------------------
        # NO CURRENT SECTION
        # ----------------------------------------------------

        if current_section is None:
            continue

        # ----------------------------------------------------
        # LIST CONTENT
        # ----------------------------------------------------

        if tag.name in {
            "ul",
            "ol",
        }:
            items = extract_list_items(tag)

            for item in items:
                if item not in sections[current_section]:
                    sections[current_section].append(item)

        # ----------------------------------------------------
        # PARAGRAPH CONTENT
        # ----------------------------------------------------

        elif tag.name == "p":
            text = clean_text(tag)

            if text:
                if text not in sections[current_section]:
                    sections[current_section].append(text)

    return dict(sections)


# ============================================================
# MAIN ICD EXTRACTION FUNCTION
# ============================================================


def get_icd10_info(
    code: str,
) -> Optional[dict]:

    code = code.strip().upper()

    print(f"Searching for ICD code: {code}")

    session = create_session()

    # --------------------------------------------------------
    # STEP 1: FIND EXACT URL
    # --------------------------------------------------------

    url = get_icd10data_url(
        session,
        code,
    )

    if not url:
        print(f"Could not find ICD code: {code}")

        return None

    print(f"Found URL: {url}")

    # --------------------------------------------------------
    # STEP 2: OPEN ICD PAGE
    # --------------------------------------------------------

    response = session.get(
        url,
        timeout=20,
    )

    response.raise_for_status()

    soup = BeautifulSoup(
        response.text,
        "html.parser",
    )

    # --------------------------------------------------------
    # STEP 3: REMOVE HIDDEN CONTENT
    # --------------------------------------------------------

    remove_unwanted_content(soup)

    # --------------------------------------------------------
    # STEP 4: FIND EXACT CODE
    # --------------------------------------------------------

    heading_container = get_main_heading_container(
        soup,
        code,
    )

    if not heading_container:
        print("Could not find the main ICD heading.")

        return None

    # --------------------------------------------------------
    # STEP 5: EXTRACT ALL SECTIONS
    # --------------------------------------------------------

    sections = extract_dynamic_sections(heading_container)

    # --------------------------------------------------------
    # FINAL DATA
    # --------------------------------------------------------

    data = {
        "code": code,
        "description": get_description(heading_container),
        "url": url,
        "sections": sections,
    }

    return data


# ============================================================
# PRINT RESULTS
# ============================================================


def print_icd10_info(
    data: dict,
) -> None:

    print()

    print("=" * 70)

    print(f"CODE: {data['code']}")

    print(f"DESCRIPTION: {data['description']}")

    print(f"URL: {data['url']}")

    # --------------------------------------------------------
    # PRINT ALL SECTIONS DYNAMICALLY
    # --------------------------------------------------------

    for section_name, items in data["sections"].items():
        print()

        print(f"{section_name.upper()}:")

        if not items:
            print("  None")

            continue

        for item in items:
            print(f"  - {item}")

    print()

    print("=" * 70)


# ============================================================
# MAIN
# ============================================================

if __name__ == "__main__":
    code = input("Enter ICD-10 code: ").strip().upper()

    data = get_icd10_info(code)

    if data:
        print_icd10_info(data)
