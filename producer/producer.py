import json
import time
from kafka import KafkaProducer

from fhir_generator.generator import generate_observation

TOPIC = "bp_observations"
BOOTSTRAP_SERVERS = ["localhost:9092"]

def main():
    producer = KafkaProducer(
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_serializer=lambda v: json.dumps(v).encode("utf-8"),
    )

    print("Producer démarré. Envoi d'observations toutes les 2 secondes... (Ctrl+C pour arrêter)")
    try:
        while True:
            obs = generate_observation()
            producer.send(TOPIC, obs)
            producer.flush()
            sys_val = obs["component"][0]["valueQuantity"]["value"]
            dia_val = obs["component"][1]["valueQuantity"]["value"]
            print(f"Envoyé → systolique={sys_val}, diastolique={dia_val}")
            time.sleep(0.5)
    except KeyboardInterrupt:
        print("\nArrêt du producer.")
    finally:
        producer.close()

if __name__ == "__main__":
    main()
