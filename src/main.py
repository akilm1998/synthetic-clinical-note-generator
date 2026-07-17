import yaml
import random
from pathlib import Path
import functions


BASE_DIR = Path(__file__).resolve().parent.parent
profile = open(BASE_DIR / "diagnosis_profiles" / "profiles" / "E11_9.yaml", "r")
profile_data = yaml.safe_load(profile)

if __name__ == "__main__":
    patient = {
        "name": functions.get_random_name(),
        "age": functions.get_random_age(),
        "sex": functions.get_random_sex(),
        "smoking_status": functions.get_random_smoking_status(),
        "comorbidities": random.sample(
            profile_data["common_comorbidities"], k=random.randint(0, 2)
        ),
    }

    print(patient)
