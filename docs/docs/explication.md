# Explication du fonctionnement du système

## 1. Génération des données médicales
Un script Python simule des patients et génère des observations de pression artérielle au format FHIR (Observation).
Chaque message contient :
- identifiant patient
- pression systolique
- pression diastolique
- date de mesure

Les données sont réalistes et générées en continu.

---

## 2. Transmission avec Kafka
Le producer Python envoie chaque observation dans un topic Kafka.

Kafka joue le rôle de bus de données temps réel :
il découple la génération et l’analyse.

---

## 3. Analyse des données
Le consumer Python lit les messages et applique des règles médicales :

- Hypotension : systolique < 90 ou diastolique < 60
- Hypertension : systolique > 140 ou diastolique > 90
- Sinon : normal

Chaque observation est classée automatiquement.

---

## 4. Traitement
Si NORMAL :
→ stocké dans un fichier JSON local

Si ANORMAL :
→ envoyé dans Elasticsearch avec :
- valeurs tension
- type anomalie
- timestamp

---

## 5. Visualisation
Kibana lit les données Elasticsearch et permet :
- visualisation des anomalies
- évolution temporelle
- monitoring temps réel

Le rafraîchissement automatique permet de voir les nouvelles anomalies en direct.

---

## Architecture globale
Generator → Kafka → Consumer → Elasticsearch → Kibana

Le système simule un système hospitalier de surveillance temps réel.