"""
CutisAI — Analyse statistique du dataset d'images.
Scanne un dossier d'images organisé par maladie et affiche :
- Nombre d'images par classe
- Doublons SHA256
- Statistiques de résolution
- Distribution visuelle (histogramme ASCII)

Usage (Colab) :
    !python dataset_stats.py --input "/content/drive/MyDrive/Projet_Medical/Dataset_Images"
Usage (local) :
    python dataset_stats.py --input ./dataset_images
"""
import os
import argparse
import hashlib
from PIL import Image
from collections import defaultdict

IMAGE_EXTENSIONS = {'.jpg', '.jpeg', '.png', '.webp', '.bmp', '.tiff'}

def scan_dataset(input_dir):
    """Scanne le dataset et retourne les statistiques."""
    stats = {}
    all_hashes = defaultdict(list)  # hash -> [(disease, filepath), ...]
    
    if not os.path.exists(input_dir):
        print(f"❌ Dossier introuvable : {input_dir}")
        return
    
    diseases = sorted([d for d in os.listdir(input_dir)
                       if os.path.isdir(os.path.join(input_dir, d))])
    
    if not diseases:
        print(f"❌ Aucun sous-dossier trouvé dans {input_dir}")
        return
    
    print(f"\n📁 Analyse de : {input_dir}")
    print(f"   {len(diseases)} classes détectées\n")
    
    total_images = 0
    total_duplicates = 0
    
    for disease in diseases:
        disease_dir = os.path.join(input_dir, disease)
        files = [f for f in os.listdir(disease_dir)
                 if os.path.splitext(f)[1].lower() in IMAGE_EXTENSIONS]
        
        widths, heights, sizes = [], [], []
        disease_hashes = set()
        duplicates = 0
        
        for f in files:
            filepath = os.path.join(disease_dir, f)
            
            # Hash SHA256
            try:
                with open(filepath, 'rb') as fh:
                    h = hashlib.sha256(fh.read()).hexdigest()
                if h in disease_hashes:
                    duplicates += 1
                disease_hashes.add(h)
                all_hashes[h].append((disease, filepath))
            except Exception:
                pass
            
            # Résolution
            try:
                img = Image.open(filepath)
                w, h_px = img.size
                widths.append(w)
                heights.append(h_px)
                sizes.append(os.path.getsize(filepath))
            except Exception:
                pass
        
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
    
    # Cross-disease duplicates
    cross_dupes = sum(1 for h, locs in all_hashes.items() 
                      if len(set(d for d, _ in locs)) > 1)
    
    # Affichage
    print(f"{'Classe':<30} {'Images':>8} {'Doublons':>10} {'Résolution moy.':>18} {'Taille moy.':>12}")
    print(f"{'-'*78}")
    
    max_count = max(s['count'] for s in stats.values()) if stats else 1
    
    for disease, s in sorted(stats.items(), key=lambda x: -x[1]['count']):
        res = f"{s['avg_w']}×{s['avg_h']}" if s['avg_w'] else "N/A"
        size = f"{s['avg_size_kb']} KB" if s['avg_size_kb'] else "N/A"
        print(f"{disease:<30} {s['count']:>8} {s['duplicates']:>10} {res:>18} {size:>12}")
    
    print(f"{'-'*78}")
    print(f"{'TOTAL':<30} {total_images:>8} {total_duplicates:>10}")
    
    # Histogramme
    print(f"\n📊 Distribution des classes :")
    bar_width = 50
    for disease, s in sorted(stats.items(), key=lambda x: -x[1]['count']):
        bar_len = int(s['count'] / max_count * bar_width)
        bar = '█' * bar_len
        print(f"  {disease:<28} {bar} {s['count']}")
    
    # Alertes
    print(f"\n⚠️  Alertes :")
    for disease, s in stats.items():
        if s['count'] < 100:
            print(f"  🔴 {disease}: seulement {s['count']} images (< 100)")
        elif s['count'] < 200:
            print(f"  🟠 {disease}: {s['count']} images (< 200)")
    
    if cross_dupes > 0:
        print(f"  🟡 {cross_dupes} images dupliquées entre différentes classes")
    
    print(f"\n✅ Analyse terminée. {total_images} images, {len(diseases)} classes.")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyse statistique du dataset CutisAI")
    parser.add_argument("--input", type=str, required=True,
                       help="Dossier racine du dataset (contient un sous-dossier par maladie)")
    args = parser.parse_args()
    scan_dataset(args.input)
