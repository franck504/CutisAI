# 🏥 CutisAI — Guide des Datasets Médicaux Experts

Ce document répertorie les sources de données vérifiées (expert-labeled) identifiées pour enrichir le dataset CutisAI.

## 🌟 La "Mine d'Or" : eSkinHealth
- **Description** : Dataset multimodal (MTDN) Côte d'Ivoire & Ghana.
- **Fiabilité Labels** : 🟢 **100% (Expertise Médicale)**
- **Propreté Image** : 🟢 **Très haute (Clichés cliniques sans bruit)**
- **Action** : Téléchargement prioritaire.

## 🗂️ Sources par Maladie

### Mpox (Variole du Singe)
- **MPox-Vision** : 🟢 **Clean** (Label vérifié, sans watermarks).
- **MSLD v2.0** : 🟡 **Moderately Clean** (Issu du web mais filtré par des experts).

### Leishmaniose Cutanée
- **Zenodo (ID 4004724)** : 🟢 **Clean** (Microscopie, annotations précises).

### Lèpre (Leprosy)
- **Leprosy-Skin-Lesion (GitHub)** : 🟢 **Clean** (Dataset clinique).
- **Extended Chronic Wounds (Kaggle)** : 🟢 **Clean** (Segmenté, usage médical).

### Gale (Scabies)
- **Roboflow Universe** : Plusieurs datasets (Scabies Detection), ~1 500 images open-source.

## 🏛️ Bibliothèques Institutionnelles

### DermNet NZ
- **Fiabilité Labels** : 🟢 **Très haute** (Validé par dermatologues).
- **Propreté Image** : 🟡 **Moyenne** (Présence de **watermarks** textuels sur les images).
- **Action** : Scraper spécifique (besoin de filtrage pour les filigranes).

### WHO (OMS) — Multimedia Library
- **Fiabilité Labels** : 🟢 **Indiscutable**.
- **Propreté Image** : 🟠 **Variable** (Photos historiques, parfois basse résolution ou noir & blanc).

---

## 🛠️ Plan d'Intégration (Phase 3)
1. **Scripts Spécifiques** : Créer un scraper pour DermNet NZ et WHO.
2. **Kaggle CLI** : Automatiser le téléchargement des segments Mpox et Leprosy.
3. **Fusion & Dédup** : Intégrer ces images dans l'arborescence `/Dataset_Images` en utilisant de nouveaux préfixes (ex: `expert_WHO_`, `expert_eSkin_`).
