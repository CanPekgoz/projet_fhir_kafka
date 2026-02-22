import random
import json
from datetime import datetime, timezone
from faker import Faker

fake = Faker()

def generate_observation():
    systolic = random.randint(80, 180)
    diastolic = random.randint(50, 120)

    obs = {
        "resourceType": "Observation",
        "id": fake.uuid4(),
        "status": "final",
        "category": [{
            "coding": [{
                "system": "http://terminology.hl7.org/CodeSystem/observation-category",
                "code": "vital-signs"
            }]
        }],
        "code": {
            "coding": [{
                "system": "http://loinc.org",
                "code": "85354-9",
                "display": "Blood pressure panel"
            }]
        },
        "subject": {"reference": f"Patient/{fake.uuid4()}"},
        "effectiveDateTime": datetime.now(timezone.utc).isoformat(),
        "component": [
            {"code": {"text": "Systolic"}, "valueQuantity": {"value": systolic, "unit": "mmHg"}},
            {"code": {"text": "Diastolic"}, "valueQuantity": {"value": diastolic, "unit": "mmHg"}}
        ]
    }
    return obs

if __name__ == "__main__":
    print(json.dumps(generate_observation(), indent=2))
