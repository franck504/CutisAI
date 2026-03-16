# 📋 CutisAI — Plan d'Implémentation Détaillé

> **Projet** : IA de détection des maladies cutanées tropicales africaines  
> **Date** : 16 Mars 2026  
> **Statut** : Phase 1 terminée → Phase 2 à démarrer

---

## Phase 1 : Collecte d'images ✅ TERMINÉE

### Ce qui a été accompli
- **Script** : `scraper.py` — scraper multi-moteur (DDG → Bing) avec 15 threads
- **Exécution** : Google Colab → Google Drive
- **Résultat** : **3 205 images** téléchargées sur 9 maladies
- **Documentation** : `README_COLAB.md` — guide copier-coller pour Colab
- **Source de données** : `target_diseases.csv` — 9 maladies × 6 mots-clés chacune

### Améliorations optionnelles (backlog)
- [ ] Corriger la regex Yahoo dans `search_yahoo()` (actuellement 0 résultat)
- [ ] Ajouter hash perceptuel pendant le téléchargement pour éviter les doublons
- [ ] Logger les résultats en JSON (traçabilité)
- [ ] Ajouter Serpapi ou Google Custom Search API pour plus de sources
- [ ] Collecter des images supplémentaires pour les classes faibles (Leishmaniasis: 52, Scabies: 144)

---

## Phase 2 : Nettoyage du Dataset 🔜 PROCHAINE ÉTAPE

### 2.1 Script `cleaning/cleaner.py`

**Objectif** : Réduire le bruit du dataset scrapé pour ne garder que les images médicalement pertinentes.

#### Étapes du pipeline de nettoyage :

```
Images brutes (3 205)
    │
    ├── 1. Suppression doublons exacts (SHA256)
    ├── 2. Suppression doublons visuels (pHash, seuil < 5)
    ├── 3. Filtrage par taille (min 100x100 px)
    ├── 4. Détection de flou (cv2.Laplacian variance < seuil)
    ├── 5. Filtrage contenu non-photo (schémas, texte, logos)
    └── 6. Renommage standardisé : {maladie}_{index:04d}.jpg
              │
              ▼
    Dataset nettoyé (~1 600 images estimées)
```

#### Dépendances :
```
pip install opencv-python imagehash pillow numpy
```

#### Commande Colab :
```bash
!python cleaning/cleaner.py --input "/content/drive/MyDrive/Projet_Medical/Dataset_Images" --output "/content/drive/MyDrive/Projet_Medical/Dataset_Clean"
```

### 2.2 Recherche de datasets complémentaires

| Dataset | URL | Images | Pertinence |
|---------|-----|:------:|-----------|
| **Fitzpatrick17k** | github.com/mattgroh/fitzpatrick17k | 16 577 | Phototypes I-VI, labels dermatologiques |
| **ISIC Archive** | isic-archive.com | 70 000+ | Lésions cutanées, surtout mélanome |
| **DermNet NZ** | dermnetnz.org | ~20 000 | Images libres, large couverture |
| **HAM10000** | kaggle.com/kmader/skin-cancer-mnist-ham10000 | 10 015 | Lésions cutanées annotées |
| **PAD-UFES-20** | kaggle.com | 2 298 | Maladies de peau, Brésil |

> [!IMPORTANT]
> **Priorité** : Fitzpatrick17k est le dataset le plus important à intégrer car il contient des images sur peaux foncées (Fitzpatrick IV-VI), ce qui est critique pour notre cas d'usage africain.

### 2.3 Data Augmentation

**Outil** : Albumentations (Python) ou Roboflow (interface graphique)

**Transformations recommandées** :
- Rotation (0-360°)
- Flip horizontal/vertical
- Variation de luminosité (-30% à +30%)
- Variation de contraste
- Bruit gaussien (simule caméra mobile basse qualité)
- Crop aléatoire + resize
- Changement de teinte (léger, pour simuler différentes conditions d'éclairage)

**Facteur de multiplication cible** : ×5 → ~8 000 images finales

---

## Phase 3 : Entraînement du Modèle

### 3.1 Configuration

| Paramètre | Valeur |
|-----------|--------|
| **Modèle base** | MobileNetV3-Small (pré-entraîné ImageNet) |
| **Framework** | TensorFlow 2.x / Keras |
| **Plateforme** | Google Colab (GPU T4) |
| **Résolution entrée** | 224 × 224 × 3 |
| **Nombre de classes** | 9 |
| **Batch size** | 32 |
| **Learning rate** | 1e-3 (warmup) → 1e-4 (fine-tuning) |
| **Epochs** | 50 (early stopping patience=10) |
| **Optimiseur** | Adam |
| **Loss** | Categorical Crossentropy (weighted) |

### 3.2 Stratégie d'entraînement en 2 étapes

**Étape 1 — Feature extraction** (5-10 epochs)
- Geler toutes les couches du MobileNetV3
- Entraîner uniquement la tête de classification (Dense + Softmax)
- LR = 1e-3

**Étape 2 — Fine-tuning** (20-40 epochs)
- Dégeler les 30% dernières couches du MobileNetV3
- LR = 1e-4 avec ReduceLROnPlateau
- Early stopping sur val_loss (patience=10)

### 3.3 Validation

- **Split** : 70% train / 15% validation / 15% test
- **Stratification** : Stratifié par classe pour maintenir les proportions
- **Cross-validation** : K-Fold stratifié (k=5) si le dataset est petit

### 3.4 Métriques à calculer

- Accuracy globale
- F1-score par classe (micro, macro, weighted)
- Matrice de confusion
- Courbes ROC/AUC par classe
- Rapport de classification complet (precision, recall, f1)

### 3.5 Conversion TFLite

```python
# Conversion TFLite avec quantization INT8
converter = tf.lite.TFLiteConverter.from_saved_model(saved_model_dir)
converter.optimizations = [tf.lite.Optimize.DEFAULT]
converter.target_spec.supported_types = [tf.int8]
tflite_model = converter.convert()
# Taille cible : < 5 MB
```

---

## Phase 4 : Application Mobile Flutter

### 4.1 Fonctionnalités v1.0

| Fonctionnalité | Priorité | Description |
|---------------|:--------:|-------------|
| Prise de photo | 🔴 P0 | Caméra + galerie |
| Inférence TFLite | 🔴 P0 | Diagnostic offline < 500ms |
| Affichage résultat | 🔴 P0 | Maladie + confiance + infos |
| Historique patients | 🟠 P1 | Stockage local SQLite |
| Traduction Malgache | 🟡 P2 | API Cloud (Gemini/Claude) |
| Mode sombre | 🟢 P3 | Confort d'utilisation |

### 4.2 Dépendances Flutter

```yaml
dependencies:
  camera: ^0.10.0          # Accès caméra
  tflite_flutter: ^0.10.0  # Inférence TFLite
  image: ^4.0.0            # Manipulation d'images
  sqflite: ^2.0.0          # Base locale (historique)
  http: ^1.0.0             # API Cloud
  provider: ^6.0.0         # State management
```

### 4.3 Flux utilisateur

```
[Accueil] → [Prendre Photo] → [Analyse IA (< 500ms)]
                                       │
                               ┌───────┴───────┐
                               │               │
                        [Résultat]       [Pas de match]
                               │               │
                    [Score > 70%]    [Recommander consultation]
                               │
                     [Infos maladie]
                               │
                  [Recommandations soins]
                               │
              [Traduction Malgache (si online)]
```

---

## Calendrier prévisionnel

| Semaine | Phase | Tâches clés |
|:-------:|-------|------------|
| S1 | Phase 2.1 | Créer `cleaner.py`, nettoyer le dataset |
| S1-S2 | Phase 2.2 | Rechercher et intégrer datasets complémentaires |
| S2 | Phase 2.3 | Data augmentation, dataset final |
| S3-S4 | Phase 3.1-3.2 | Entraînement MobileNetV3 sur Colab |
| S4 | Phase 3.3 | Évaluation, ajustements, conversion TFLite |
| S5-S6 | Phase 4.1 | Développement Flutter (caméra + inférence) |
| S7 | Phase 4.2 | Intégration API traduction + polish |
| S8 | | Tests, documentation, soutenance |

---

## Ressources et références

- [TensorFlow Lite Guide](https://www.tensorflow.org/lite/guide)
- [MobileNetV3 Paper](https://arxiv.org/abs/1905.02244)
- [Flutter TFLite Plugin](https://pub.dev/packages/tflite_flutter)
- [Fitzpatrick17k Dataset](https://github.com/mattgroh/fitzpatrick17k)
- [Albumentations Library](https://albumentations.ai/)
- [WHO NTDs Skin Diseases](https://www.who.int/activities/integrating-skin-ntds)

---

*Ce plan est un document vivant. À adapter selon les résultats de chaque phase.*
