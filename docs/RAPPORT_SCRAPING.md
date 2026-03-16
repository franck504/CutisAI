# 📊 CutisAI — Rapport de Scraping Phase 1

> **Date d'exécution** : 16 Mars 2026  
> **Plateforme** : Google Colab (CPU, 15 threads)  
> **Destination** : `/content/drive/MyDrive/Projet_Medical/Dataset_Images`  
> **Script** : `scraper.py` v1.0

---

## Résumé exécutif

| Métrique | Valeur |
|----------|:------:|
| **Total images téléchargées** | **3 205** |
| **Nombre de maladies** | 9 |
| **Nombre de mots-clés** | 54 (6 par maladie) |
| **Moteur principal** | DuckDuckGo (avec fallback Bing) |
| **Durée totale estimée** | ~15-20 minutes |
| **Taux de succès global** | ~65% (images valides / URLs trouvées) |

---

## Résultats détaillés par maladie

### 1. Buruli Ulcer (~385 images)

| Mot-clé | URLs trouvées | Images téléchargées | Moteur utilisé |
|---------|:------------:|:-------------------:|:--------------:|
| Buruli ulcer lesion | 57 | 1 | DDG → Bing (bloqué) |
| Mycobacterium ulcerans skin ulcer | 300 | 208 | DDG ✅ |
| Buruli nodule | 53 | 42 | DDG → Bing |
| Buruli ulcer dark skin | 62 | 57 | DDG → Bing |
| Buruli ulcer Africa | 56 | 34 | DDG → Bing |
| fery Buruli madagascar | 61 | 43 | DDG → Bing |
| **Total** | **589** | **~385** | |

### 2. Leprosy (~627 images)

| Mot-clé | URLs trouvées | Images téléchargées | Moteur utilisé |
|---------|:------------:|:-------------------:|:--------------:|
| Leprosy skin lesions | 300 | 195 | DDG ✅ |
| Hansen's disease macules | 65 | 0 | DDG → Bing |
| lepromatous leprosy skin | 235 | 162 | DDG ✅ |
| Leprosy african skin | 300 | 223 | DDG ✅ |
| habokana lesion madagascar | 38 | 0 | DDG → Bing |
| leprosy dark skin | 55 | 47 | DDG → Bing |
| **Total** | **993** | **~627** | |

### 3. Cutaneous Leishmaniasis (~52 images)

| Mot-clé | URLs trouvées | Images téléchargées | Moteur utilisé |
|---------|:------------:|:-------------------:|:--------------:|
| Cutaneous leishmaniasis ulcer | 59 | 0 | DDG → Bing |
| oriental sore lesion | 65 | 0 | DDG → Bing |
| leishmania skin nodule | 54 | 29 | DDG → Bing |
| Cutaneous leishmaniasis africa | 44 | 23 | DDG → Bing |
| leishmaniasis dark skin lesion | 44 | 0 | DDG → Bing |
| **Total** | **266** | **~52** | |

> [!WARNING]
> Classe critique — seulement 52 images. Nécessite une collecte supplémentaire urgente ou l'intégration de datasets médicaux existants.

### 4. Yaws (~215 images)

| Mot-clé | URLs trouvées | Images téléchargées | Moteur utilisé |
|---------|:------------:|:-------------------:|:--------------:|
| Yaws skin lesions | 60 | 7 | DDG → Bing |
| Treponema pallidum pertenue framboesia | 300 | 75 | DDG ✅ |
| primary yaws papilloma | 63 | 34 | DDG → Bing |
| Yaws african child | 69 | 57 | DDG → Bing |
| Yaws skin lesions dark skin | 53 | 42 | DDG → Bing |
| **Total** | **545** | **~215** | |

### 5. Scabies (~144 images)

| Mot-clé | URLs trouvées | Images téléchargées | Moteur utilisé |
|---------|:------------:|:-------------------:|:--------------:|
| Scabies rash | 54 | 41 | DDG → Bing |
| Sarcoptes scabiei skin burrows | 51 | 35 | DDG → Bing |
| scabies crusted | 58 | 28 | DDG → Bing |
| Scabies rash dark skin | 46 | 40 | DDG → Bing |
| lagaly skin madagascar | 55 | 0 | DDG → Bing |
| scabies african skin | 52 | 0 | DDG → Bing |
| **Total** | **316** | **~144** | |

### 6. Ringworm (~202 images)

| Mot-clé | URLs trouvées | Images téléchargées | Moteur utilisé |
|---------|:------------:|:-------------------:|:--------------:|
| Tinea corporis lesion | 38 | 2 | DDG → Bing |
| Ringworm skin patch | 49 | 4 | DDG → Bing |
| tinea capitis scalp | 58 | 47 | DDG → Bing |
| Ringworm black skin | 60 | 51 | DDG → Bing |
| Ringworm african scalp | 51 | 43 | DDG → Bing |
| tinea capitis dark skin | 65 | 55 | DDG → Bing |
| **Total** | **321** | **~202** | |

### 7. Tungiasis / Jigger Fleas (~655 images)

| Mot-clé | URLs trouvées | Images téléchargées | Moteur utilisé |
|---------|:------------:|:-------------------:|:--------------:|
| Tungiasis foot | 300 | 232 | DDG ✅ |
| Jigger flea lesions | 41 | 38 | DDG → Bing |
| Tunga penetrans sole | 54 | 37 | DDG → Bing |
| Tungiasis foot africa | 300 | 256 | DDG ✅ |
| jigger flea foot dark skin | 52 | 49 | DDG → Bing |
| parasy jigger madagascar | 55 | 43 | DDG → Bing |
| **Total** | **802** | **~655** | |

### 8. Atopic Dermatitis (~482 images)

| Mot-clé | URLs trouvées | Images téléchargées | Moteur utilisé |
|---------|:------------:|:-------------------:|:--------------:|
| Atopic dermatitis skin | 73 | 64 | DDG → Bing |
| eczema lesions dark skin | 68 | 61 | DDG → Bing |
| eczema erythema | 300 | 225 | DDG ✅ |
| eczema black skin | 50 | 45 | DDG → Bing |
| atopic dermatitis african skin | 39 | 29 | DDG → Bing |
| eczema madagascar | 64 | 58 | DDG → Bing |
| **Total** | **594** | **~482** | |

### 9. Mpox / Monkeypox (~443 images)

| Mot-clé | URLs trouvées | Images téléchargées | Moteur utilisé |
|---------|:------------:|:-------------------:|:--------------:|
| Mpox skin lesions | 47 | 24 | DDG → Bing |
| Monkeypox pustules | 40 | 30 | DDG → Bing |
| monkeypox rash | 300 | 275 | DDG ✅ |
| Mpox dark skin | 62 | 49 | DDG → Bing |
| monkeypox african skin lesions | 40 | 35 | DDG → Bing |
| varioleun'ny rajako madagascar | 38 | 30 | DDG → Bing |
| **Total** | **527** | **~443** | |

---

## Observations techniques

### DuckDuckGo — Comportement de rate limiting
- **Bloqué dans ~70% des requêtes** (erreur 403 ou timeout)
- Quand il fonctionne : retourne jusqu'à 300 URLs (très performant)
- Le package est déprécié : `duckduckgo_search` → renommé en `ddgs`

### Bing Async — Fallback fiable
- Pagination par sauts de 150 images
- Retourne typiquement 38-73 URLs par requête
- Regex d'extraction `murl&quot;:&quot;(.*?)&quot;` fonctionne bien

### Mots-clés malgaches — Résultats décevants
- `lagaly skin madagascar` → 0 images
- `habokana lesion madagascar` → 0 images  
- `fery Buruli madagascar` → 43 images (exception positive)
- `parasy jigger madagascar` → 43 images
- **Conclusion** : Les termes vernaculaires malgaches sont trop spécialisés pour les moteurs de recherche généralistes

---

## Distribution des classes

```
Tungiasis        : ████████████████████████████████████████████████ 655 (20.4%)
Leprosy          : ████████████████████████████████████████         627 (19.6%)
Atopic Derm.     : ███████████████████████████████                  482 (15.0%)
Mpox             : ████████████████████████████                     443 (13.8%)
Buruli Ulcer     : ████████████████████████                         385 (12.0%)
Yaws             : █████████████                                    215 (6.7%)
Ringworm         : ████████████                                     202 (6.3%)
Scabies          : ████████                                         144 (4.5%)
Leishmaniasis    : ███                                               52 (1.6%)
```

**Ratio max/min** : 655 / 52 = **12.6:1** → déséquilibre sévère

---

## Recommandations

1. **🔴 Urgente** : Collecter plus d'images de Cutaneous Leishmaniasis (52) et Scabies (144)
2. **🔴 Urgente** : Vérifier manuellement la qualité des images par dossier (estimated ~30% non pertinentes)
3. **🟠 Importante** : Intégrer le dataset Fitzpatrick17k pour les classes faibles
4. **🟡 Utile** : Optimiser le scraper pour DDG v2 (`pip install ddgs`) et corriger Yahoo/Google

---

*Rapport généré à partir des logs d'exécution Google Colab du 16 Mars 2026.*
