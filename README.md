# 🚗 GetAround : Analyse des retards et API de Pricing

Ce projet est réalisé dans le cadre de la certification **Jedha Bootcamp - Bloc 5 : Déploiement d'un modèle de Machine Learning en production**.

## 📋 Contexte & Objectifs
GetAround est une plateforme de location de voitures entre particuliers. Pour garantir une expérience utilisateur fluide, ce projet s'attaque à deux défis :
1. **Gestion des retards** : Analyser les délais entre les locations pour suggérer un seuil de sécurité minimum.
2. **Aide au pricing** : Fournir un outil d'estimation de prix automatique pour les propriétaires via une API.

## 🚀 Livrables du Projet

### 1. Dashboard d'Analyse (Business Intelligence)
Un tableau de bord interactif pour explorer les données de retards et simuler l'impact des décisions stratégiques.
* **Outil** : Streamlit
* **Analyse clé** : Comparaison des flux "Connect" vs "Mobile" et calcul du taux de collision.
* **Lien** : https://huggingface.co/spaces/AliciaD/getaround_dashboard

### 2. API de Machine Learning (Production)
Une API robuste qui prédit le prix journalier suggéré pour une voiture en fonction de 14 caractéristiques techniques.
* **Techno** : FastAPI
* **Modèle** : Régression Ridge (entraînée via Scikit-Learn)
* **Déploiement** : https://aliciad-getaround-pricing-api.hf.space/docs

### 3. Infrastructure & DevOps
* **Docker** : L'API est entièrement containerisée pour assurer la reproductibilité sur n'importe quel serveur.
* **MLflow** : Utilisé pour le suivi des métriques ($R^2$, MAE) et le versioning du modèle.

## 📊 Résultats Clés (Insight Business)
D'après l'Analyse Exploratoire des Données (EDA) :
* **Problème** : 57% des locations subissent un retard.
* **Solution recommandée** : Mise en place d'un seuil de sécurité de **120 minutes**.
* **Impact** : Ce seuil permet de résoudre **92,2% des collisions** (conflits entre deux locataires) tout en ne bloquant que **7,25% du volume d'affaires**.

## 🛠️ Installation locale

### Avec Docker (Recommandé)
# Build de l'image
docker build -t getaround-api .

# Lancement du container
docker run -p 8000:8000 getaround-api

MLflow a été utilisé en phase de développement pour le suivi des expérimentations et la sélection du modèle Ridge.

# L'API sera disponible sur http://localhost:8000/docs

