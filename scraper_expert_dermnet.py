import os
import requests
import re
import time
import random
import hashlib
from bs4 import BeautifulSoup
from urllib.parse import urljoin
from concurrent.futures import ThreadPoolExecutor

# ==========================================
# CONFIGURATION
# ==========================================
# Notre mapping Maladie -> Slugs DermNet NZ
DERMNET_MAPPING = {
    "Buruli_Ulcer": ["buruli-ulcer"],
    "Leprosy": ["leprosy"],
    "Cutaneous_Leishmaniasis": ["leishmaniasis"],
    "Yaws": ["yaws"],
    "Scabies": ["scabies"],
    "Ringworm": ["tinea-corporis", "tinea-capitis", "tinea-faciei", "tinea-cruris"],
    "Tungiasis_-_Jigger_fleas": ["tungiasis"],
    "Atopic_dermatitis": ["atopic-dermatitis"],
    "Mpox_-_Monkeypox": ["monkeypox"]
}

BASE_URL = "https://dermnetnz.org/topics/"
DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
DRIVE_BASE_DIR = "/content/drive/MyDrive/Projet_Medical/Dataset_Images"
TIMEOUT = 10

def get_image_urls(slug):
    """Extrait les URLs des images d'une page topic DermNet NZ."""
    url = urljoin(BASE_URL, slug)
    headers = {"User-Agent": DEFAULT_UA}
    urls = []
    
    try:
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Chercher dans les carrousels et les balises img
        # DermNet utilise souvent des balises <picture> ou des <img> avec data-src
        for img in soup.find_all('img'):
            src = img.get('src') or img.get('data-src') or img.get('data-srcset')
            if src and not src.startswith('data:') and any(x in src.lower() for x in ['.jpg', '.jpeg', '.png']):
                if src.startswith('//'):
                    src = 'https:' + src
                elif src.startswith('/'):
                    src = urljoin("https://dermnetnz.org", src)
                
                # Filtrer les icônes et logos
                if "logo" not in src.lower() and "icon" not in src.lower() and "adrit" not in src.lower():
                    urls.append(src)
        
        return list(dict.fromkeys(urls))
    except Exception as e:
        print(f"❌ Erreur sur {slug}: {e}")
        return []

def download_expert_img(url, disease_folder):
    """Télécharge une image experte avec préfixe."""
    dest_dir = os.path.join(DRIVE_BASE_DIR, disease_folder)
    os.makedirs(dest_dir, exist_ok=True)
    
    try:
        headers = {"User-Agent": DEFAULT_UA}
        response = requests.get(url, headers=headers, timeout=TIMEOUT)
        response.raise_for_status()
        content = response.content
        
        # Hash pour unicité
        h = hashlib.md5(content).hexdigest()[:8]
        ext = url.split('.')[-1].split('?')[0].lower()
        if ext not in ['jpg', 'jpeg', 'png', 'webp']:
            ext = 'jpg'
            
        filename = f"EXPERT_DERMNET_{h}.{ext}"
        path = os.path.join(dest_dir, filename)
        
        if not os.path.exists(path):
            with open(path, 'wb') as f:
                f.write(content)
            return True
    except Exception:
        pass
    return False

def scrape_disease(disease, slugs):
    """Gère le scraping d'une maladie (plusieurs slugs possibles)."""
    all_urls = []
    for slug in slugs:
        print(f"  🔍 Scan topic: {slug}...", end=" ", flush=True)
        found = get_image_urls(slug)
        print(f"✅ {len(found)} images")
        all_urls.extend(found)
        time.sleep(random.uniform(1, 4)) # Politesse
        
    all_urls = list(dict.fromkeys(all_urls))
    if not all_urls:
        return 0
    
    print(f"  ⬇️  Téléchargement de {len(all_urls)} images expertes pour {disease}...")
    count = 0
    with ThreadPoolExecutor(max_workers=5) as executor:
        results = [executor.submit(download_expert_img, url, disease) for url in all_urls]
        for r in results:
            if r.result():
                count += 1
    return count

def main():
    print("="*60)
    print("🏥 SCRAPER EXPERT DERMNET NZ")
    print("="*60)
    
    total = 0
    for disease, slugs in DERMNET_MAPPING.items():
        print(f"\n🧬 Maladie : {disease}")
        count = scrape_disease(disease, slugs)
        print(f"✅ {count} nouvelles images expertes ajoutées.")
        total += count
        
    print(f"\n🎉 TERMINÉ. Total images expertes : {total}")

if __name__ == "__main__":
    main()
