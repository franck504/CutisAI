"""
CutisAI - Analyse statistique du dataset d'images.
Scanne un dossier d'images organisé par maladie et affiche :
- Nombre d'images par classe
- Doublons SHA256
- Statistiques de résolution
- Distribution visuelle (histogramme ASCII)

Usage :
    python dataset_stats.py --input ./dataset_images
"""
import os
import argparse
import hashlib
from PIL import Image
from collections import defaultdict

# Extensions d'images prises en charge
IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff'}

def scan_dataset(input_dir):
    """
    Parcourt le dossier racine du dataset pour extraire des statistiques
    détaillées sur chaque classe (maladie).
    """
    stats = {}
    all_hashes = defaultdict(list)  # hash -> [(maladie, chemin_fichier), ...]
    
    if not os.path.exists(input_dir):
        print(f"Erreur : Dossier introuvable : {input_dir}")
        return
    
    # On récupère la liste des dossiers de maladies
    diseases = sorted([d for d in os.listdir(input_dir)
                       if os.path.isdir(os.path.join(input_dir, d))])
    
    if not diseases:
        print(f"Erreur : Aucun sous-dossier (classe) trouvé dans {input_dir}")
        return
    
    print(f"\nAnalyse du dossier : {input_dir}")
    print(f"{len(diseases)} classes détectées au total.\n")
    
    total_images = 0
    total_duplicates = 0
    
    for disease in diseases:
        disease_dir = os.path.join(input_dir, disease)
        # On ne garde que les fichiers images valides
        files = [f for f in os.listdir(disease_dir)
                 if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS]
        
        widths, heights, sizes = [], [], []
        disease_hashes = set()
        duplicates = 0
        
        for f in files:
            filepath = os.path.join(disease_dir, f)
            
            # Calcul du hash SHA256 pour détecter les doublons exacts
            try:
                with open(filepath, 'rb') as fh:
                    h = hashlib.sha256(fh.read()).hexdigest()
                if h in disease_hashes:
                    duplicates += 1
                disease_hashes.add(h)
                all_hashes[h].append((disease, filepath))
            except Exception:
                pass
            
            # Analyse de la résolution de l'image
            try:
                img = Image.open(filepath)
                w, h_px = img.size
                widths.append(w)
                heights.append(h_px)
                sizes.append(os.path.getsize(filepath))
            except Exception:
                pass
        
        # Agrégation des statistiques par maladie
        stats[disease] = {
            'count': len(files),
            'duplicates': duplicates,
            'min_w': min(widths) if widths else 0,
            'max_w': max(widths) if widths else 0,
            'avg_w': int(sum(widths) / len(widths)) if widths else 0,
            'min_h': min(heights) if heights else 0,
            'max_h': max(heights) if heights else 0,
            'avg_h': int(sum(heights) / len(heights)) if heights else 0,
            'avg_size_kb': int(sum(sizes) / len(sizes) / 1024) if sizes else 0,
        }
        total_images += len(files)
        total_duplicates += duplicates
    
    # Détection des doublons présents dans plusieurs classes
    cross_dupes = sum(1 for h, locs in all_hashes.items() 
                      if len(set(d for d, _ in locs)) > 1)
    
    # Affichage du tableau récapitulatif
    print(f"{'Classe':<30} {'Images':>8} {'Doublons':>10} {'Résolution moy.':>18} {'Taille moy.':>12}")
    print(f"{'-'*78}")
    
    max_count = max(s['count'] for s in stats.values()) if stats else 1
    
    # Tri par nombre d'images décroissant
    for disease, s in sorted(stats.items(), key=lambda x: -x[1]['count']):
        res = f"{s['avg_w']}x{s['avg_h']}" if s['avg_w'] else "N/A"
        size = f"{s['avg_size_kb']} Ko" if s['avg_size_kb'] else "N/A"
        print(f"{disease:<30} {s['count']:>8} {s['duplicates']:>10} {res:>18} {size:>12}")
    
    print(f"{'-'*78}")
    print(f"{'TOTAL':<30} {total_images:>8} {total_duplicates:>10}")
    
    # Histogramme simple en ASCII pour visualiser la distribution
    print(f"\nDistribution des classes :")
    bar_width = 50
    for disease, s in sorted(stats.items(), key=lambda x: -x[1]['count']):
        bar_len = int(s['count'] / max_count * bar_width)
        bar = '#' * bar_len
        print(f"  {disease:<28} {bar} {s['count']}")
    
    # Alertes sur le volume de données
    print(f"\nAlertes de volume :")
    for disease, s in stats.items():
        if s['count'] < 100:
            print(f"  [Critique] {disease} : seulement {s['count']} images (seuil recommandé : 100)")
        elif s['count'] < 200:
            print(f"  [Attention] {disease} : {s['count']} images (seuil recommandé : 200)")
    
    if cross_dupes > 0:
        print(f"  [Alerte] {cross_dupes} images se retrouvent dans plusieurs classes.")
    
    print(f"\nAnalyse terminée. {total_images} images réparties en {len(diseases)} classes.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyse statistique du dataset CutisAI")
    parser.add_argument("--input", type=str, required=True,
                       help="Dossier racine du dataset")
    args = parser.parse_args()
    scan_dataset(args.input)
