import requests


def search_icd10(condition: str) -> list[dict[str, str]]:
    url = "https://clinicaltables.nlm.nih.gov/api/icd10cm/v3/search"

    params = {"terms": condition, "maxList": 20, "sf": "code,name"}

    try:
        response = requests.get(url, params=params, timeout=10)

        response.raise_for_status()

        data = response.json()

        # API response structure:
        # [
        #     total_matches,
        #     ["CODE1", "CODE2", ...],
        #     ...,
        #     [["CODE1", "Description1"], ...]
        # ]

        codes = data[1]
        descriptions = data[3]

        results = []

        for code, item in zip(codes, descriptions):
            results.append({"code": code, "description": item[1]})

        return results

    except requests.exceptions.RequestException as e:
        print(f"Connection/HTTP Error: {e}")
        return []

    except (ValueError, IndexError) as e:
        print(f"Response Parsing Error: {e}")
        return []


if __name__ == "__main__":
    print("Searching for 'hypertension' codes...\n")

    matches = search_icd10("hypertension")

    for match in matches[:10]:
        print(f"Code: {match['code']:<10} | {match['description']}")
