import json
from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
from datetime import datetime, timezone

TOPIC = "bp_observations"
BOOTSTRAP_SERVERS = ["localhost:9092"]

# Connexion Elasticsearch
es = Elasticsearch("http://localhost:9200")

def is_anomalous(sys, dia):
    return sys > 140 or sys < 90 or dia > 90 or dia < 60

def save_normal(obs):
    with open("data/normal_observations.json", "a", encoding="utf-8") as f:
        f.write(json.dumps(obs) + "\n")

def send_to_elastic(obs, sys, dia):
    obs["anomaly"] = True
    obs["systolic"] = sys
    obs["diastolic"] = dia
    obs["@timestamp"] = datetime.now(timezone.utc).isoformat()

    es.index(index="bp_anomalies", document=obs)


def main():
    consumer = KafkaConsumer(
        TOPIC,
        bootstrap_servers=BOOTSTRAP_SERVERS,
        value_deserializer=lambda m: json.loads(m.decode("utf-8")),
        auto_offset_reset="earliest",
        group_id="bp-group"
    )

    print("Consumer démarré. En attente de messages...")

    for message in consumer:
        obs = message.value
        sys = obs["component"][0]["valueQuantity"]["value"]
        dia = obs["component"][1]["valueQuantity"]["value"]

        print(f"Reçu → systolique={sys}, diastolique={dia}")

        if is_anomalous(sys, dia):
            print("⚠️ Anomalie détectée → envoi vers Elasticsearch")
            send_to_elastic(obs, sys, dia)
        else:
            save_normal(obs)

if __name__ == "__main__":
    main()
