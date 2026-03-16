import os
import argparse
import time
import random
import re
import json
import hashlib
import pandas as pd
import requests
from io import BytesIO
from PIL import Image
from urllib.parse import quote_plus
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# ==========================================
# CONFIGURATION
# ==========================================
MAX_IMAGES_PER_KEYWORD = 300  # Nombre maximum d'images à chercher par mot-clé
MAX_WORKERS = 15              # Nombre de threads pour le téléchargement parallèle (Idéal Colab)
TIMEOUT = 10                  # Temps d'attente maximum par image (secondes)
MIN_IMAGE_SIZE = 5 * 1024     # Taille minimum d'une image en octets (5 KB)
MIN_RESOLUTION = 100          # Résolution minimum (100x100 pixels)

# User-Agent réaliste (Chrome 120 sur Windows)
DEFAULT_UA = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"

# ==========================================
# VALIDATION & DOWNLOAD
# ==========================================

def is_valid_image(content):
    """
    Vérifie si le contenu téléchargé est bien une image valide, non corrompue,
    avec une résolution minimum acceptable.
    """
    try:
        img = Image.open(BytesIO(content))
        w, h = img.size
        if w < MIN_RESOLUTION or h < MIN_RESOLUTION:
            return False
        img.verify()
        return True
    except Exception:
        return False

def download_and_check(url, save_path, seen_hashes):
    """
    Télécharge une image, vérifie sa validité, déduplique par SHA256,
    puis sauvegarde sur disque.
    Retourne (True, hash) si succès, (False, None) sinon.
    """
    try:
        headers = {"User-Agent": DEFAULT_UA}
        response = requests.get(url, headers=headers, timeout=TIMEOUT, stream=True)
        response.raise_for_status()
        content = response.content

        # Vérifier la taille minimum
        if len(content) < MIN_IMAGE_SIZE:
            return False, None

        # Vérifier que c'est une image valide
        if not is_valid_image(content):
            return False, None

        # Déduplication par hash SHA256
        img_hash = hashlib.sha256(content).hexdigest()
        if img_hash in seen_hashes:
            return False, None

        # Écriture sur le disque (Google Drive si Colab)
        with open(save_path, 'wb') as f:
            f.write(content)

        return True, img_hash
    except Exception:
        return False, None

# ==========================================
# MOTEURS DE RECHERCHE
# ==========================================

def search_duckduckgo(keyword, max_results):
    """DuckDuckGo — Rapide mais rate-limité fréquemment."""
    try:
        from duckduckgo_search import DDGS
    except ImportError:
        from ddgs import DDGS
    
    with DDGS() as ddgs:
        results = list(ddgs.images(
            keyword,
            region="wt-wt",
            safesearch="off",
            size="Medium",
            type_image="photo",
            max_results=max_results
        ))
    return [res['image'] for res in results]

def search_bing(keyword, max_results):
    """Bing Async — Pagination par sauts de 150. Très fiable en fallback."""
    urls = []
    headers = {"User-Agent": DEFAULT_UA}
    encoded_kw = quote_plus(keyword)
    
    for offset in range(1, max_results + 100, 150):
        url = f"https://www.bing.com/images/async?q={encoded_kw}&first={offset}&count=150&qft=+filterui:photo-photo"
        try:
            response = requests.get(url, headers=headers, timeout=15)
            response.raise_for_status()
            batch = re.findall(r'murl&quot;:&quot;(.*?)&quot;', response.text)
            if not batch:
                break
            urls.extend(batch)
        except Exception:
            break
    
    urls = [u for u in urls if u.startswith("http")]
    urls = list(dict.fromkeys(urls))  # Déduplique en préservant l'ordre
    return urls[:max_results]

def search_google(keyword, max_results):
    """
    Google Images — Utilise le nouveau format udm=2 (2025+).
    Extraction des URLs via les structures JSON embarquées dans le HTML.
    """
    encoded_kw = quote_plus(keyword)
    url = f"https://www.google.com/search?q={encoded_kw}&udm=2&biw=1920&bih=1080"
    headers = {
        "User-Agent": DEFAULT_UA,
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        "Accept-Language": "en-US,en;q=0.9,fr;q=0.8",
    }
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text
        
        # Regex 1 : Format JSON embarqué ["url",width,height]
        urls = re.findall(r'\["(https?://[^"]+\.(?:jpg|jpeg|png|webp)(?:\?[^"]*)?)",\d+,\d+\]', html, re.IGNORECASE)
        
        # Regex 2 : Extraction depuis les data attributes
        if len(urls) < 10:
            urls2 = re.findall(r'"(https?://[^"]+\.(?:jpg|jpeg|png|webp)(?:\?[^"]*)?)"', html, re.IGNORECASE)
            urls.extend(urls2)
        
        # Regex 3 : Format alternatif avec ou= (original url) encodé
        if len(urls) < 10:
            urls3 = re.findall(r'imgurl=(https?://[^&"]+)', html)
            urls.extend(urls3)
        
        # Filtrer les URLs Google internes
        urls = [u for u in urls if
                "gstatic.com" not in u and
                "google.com" not in u and
                "googleapis.com" not in u and
                "googleusercontent" not in u and
                "schema.org" not in u and
                len(u) > 20]
        
        urls = list(dict.fromkeys(urls))  # Déduplique
        return urls[:max_results]
    except Exception:
        return []

def search_yahoo(keyword, max_results):
    """Yahoo Images — Regex corrigée pour le nouveau format HTML."""
    encoded_kw = quote_plus(keyword)
    url = f"https://images.search.yahoo.com/search/images?p={encoded_kw}&imgsz=medium"
    headers = {"User-Agent": DEFAULT_UA}
    
    try:
        response = requests.get(url, headers=headers, timeout=15)
        response.raise_for_status()
        html = response.text
        
        # Nouvelle regex (testée dans test_yahoo_2.py) — capture les src des thumbnails
        urls = re.findall(r'src="(https?://[^"]+)"', html)
        
        # Filtrer uniquement les vraies images (pas les icônes Yahoo)
        urls = [u for u in urls if
                any(ext in u.lower() for ext in ['.jpg', '.jpeg', '.png', '.webp']) or
                'images' in u.lower()]
        urls = [u for u in urls if
                "yahoo.com" not in u and
                "yimg.com" not in u and
                len(u) > 30]
        
        urls = list(dict.fromkeys(urls))
        return urls[:max_results]
    except Exception:
        return []

# ==========================================
# ORCHESTRATION — RECHERCHE MULTI-MOTEUR
# ==========================================

def search_all_engines(keyword, max_results):
    """
    Recherche en cascade sur 4 moteurs. Combine tous les résultats
    en supprimant les doublons d'URL.
    
    Stratégie : DDG d'abord (le plus riche), puis Bing, Google, Yahoo
    pour compléter avec des images uniques.
    """
    all_urls = []
    engines_used = []
    
    # 1. DuckDuckGo — souvent le plus riche quand il fonctionne
    print(f"    [🔍] DuckDuckGo...", end=" ", flush=True)
    try:
        ddg_urls = search_duckduckgo(keyword, max_results)
        print(f"✅ {len(ddg_urls)} URLs")
        all_urls.extend(ddg_urls)
        engines_used.append(f"DDG:{len(ddg_urls)}")
    except Exception as e:
        err_str = str(e).lower()
        if any(x in err_str for x in ["403", "ratelimit", "429", "timeout"]):
            print(f"⚠️ Bloqué (RateLimit)")
        else:
            print(f"❌ Erreur: {e}")
        engines_used.append("DDG:0")
    
    # 2. Bing — fallback principal, très fiable
    print(f"    [🔍] Bing...", end=" ", flush=True)
    try:
        bing_urls = search_bing(keyword, max_results)
        print(f"✅ {len(bing_urls)} URLs")
        all_urls.extend(bing_urls)
        engines_used.append(f"Bing:{len(bing_urls)}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        engines_used.append("Bing:0")
    
    # 3. Google — nouveau format udm=2
    print(f"    [🔍] Google (udm=2)...", end=" ", flush=True)
    try:
        google_urls = search_google(keyword, max_results)
        print(f"✅ {len(google_urls)} URLs")
        all_urls.extend(google_urls)
        engines_used.append(f"Google:{len(google_urls)}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        engines_used.append("Google:0")
    
    # 4. Yahoo — complément
    print(f"    [🔍] Yahoo...", end=" ", flush=True)
    try:
        yahoo_urls = search_yahoo(keyword, max_results)
        print(f"✅ {len(yahoo_urls)} URLs")
        all_urls.extend(yahoo_urls)
        engines_used.append(f"Yahoo:{len(yahoo_urls)}")
    except Exception as e:
        print(f"❌ Erreur: {e}")
        engines_used.append("Yahoo:0")
    
    # Déduplique les URLs (supprime doublons inter-moteurs)
    unique_urls = list(dict.fromkeys(all_urls))
    
    print(f"    📊 Résumé : {len(unique_urls)} URLs uniques (total brut: {len(all_urls)}) [{', '.join(engines_used)}]")
    
    return unique_urls

# ==========================================
# SCRAPING D'UN MOT-CLÉ
# ==========================================

def scrape_keyword(keyword, disease_name, output_dir, global_hashes):
    """
    Cherche et télécharge les images pour un mot-clé en multi-threading,
    multi-moteur, avec déduplication SHA256 globale.
    """
    print(f"\n{'='*60}")
    print(f"[*] Mot-clé : '{keyword}'")
    print(f"{'='*60}")
    
    # Création du dossier pour cette maladie
    safe_disease_name = str(disease_name).strip().replace(" ", "_").replace("/", "-")
    disease_dir = os.path.join(output_dir, safe_disease_name)
    os.makedirs(disease_dir, exist_ok=True)
    
    try:
        # Recherche multi-moteur
        urls = search_all_engines(keyword, MAX_IMAGES_PER_KEYWORD)
        
        if not urls:
            print(f"    [-] Aucune image trouvée pour '{keyword}'.")
            return 0, 0
        
        # Préparation des tâches de téléchargement
        tasks = []
        safe_keyword = str(keyword).strip().replace(" ", "_").replace("/", "-").replace("'", "")
        
        for i, url in enumerate(urls):
            ext = url.split('.')[-1].split('?')[0].lower()
            if ext not in ['jpg', 'jpeg', 'png', 'webp']:
                ext = "jpg"
            
            filename = f"{safe_keyword}_{str(i).zfill(4)}.{ext}"
            save_path = os.path.join(disease_dir, filename)
            
            # Ne pas re-télécharger si l'image existe déjà (reprise sur erreur)
            if not os.path.exists(save_path):
                tasks.append((url, save_path))
        
        if not tasks:
            print(f"    [ℹ] Toutes les images existent déjà. Rien à télécharger.")
            return 0, len(urls)
        
        print(f"    ⬇️  Téléchargement de {len(tasks)} images (Threads: {MAX_WORKERS})...")
        
        downloaded = 0
        duplicates = 0
        
        # Téléchargement multi-thread avec déduplication
        with ThreadPoolExecutor(max_workers=MAX_WORKERS) as executor:
            future_to_url = {
                executor.submit(download_and_check, url, path, global_hashes): url
                for url, path in tasks
            }
            
            for future in tqdm(as_completed(future_to_url), total=len(tasks),
                             desc=f"    Tél. {safe_keyword[:30]}", ncols=100):
                success, img_hash = future.result()
                if success and img_hash:
                    global_hashes.add(img_hash)
                    downloaded += 1
                elif img_hash is None and not success:
                    pass  # Erreur de téléchargement ou image invalide
        
        print(f"    [+] ✅ {downloaded}/{len(tasks)} nouvelles images uniques pour '{keyword}'")
        return downloaded, len(urls)
        
    except Exception as e:
        print(f"    [-] ❌ Erreur critique : {e}")
        return 0, 0

# ==========================================
# MAIN
# ==========================================

def main(csv_path, output_dir):
    print("=" * 60)
    print("🚀 SCRAPER V2 — IMAGES MÉDICALES (MULTI-MOTEUR)")
    print("=" * 60)
    print(f"📁 Destination : {output_dir}")
    print(f"📄 Source CSV  : {csv_path}")
    print(f"🔧 Config      : max_images={MAX_IMAGES_PER_KEYWORD}, threads={MAX_WORKERS}")
    print(f"🔍 Moteurs     : DuckDuckGo → Bing → Google (udm=2) → Yahoo")
    print(f"🔒 Dédup       : SHA256 (globale inter-mots-clés)")
    print()
    
    if not os.path.exists(csv_path):
        print(f"❌ Erreur : Le fichier CSV '{csv_path}' est introuvable !")
        return
    
    df = pd.read_csv(csv_path)
    
    # Hashes globaux pour la déduplication inter-mots-clés et inter-maladies
    global_hashes = set()
    
    # Statistiques par maladie
    stats = {}
    total_downloaded = 0
    total_urls = 0
    
    for index, row in df.iterrows():
        disease_name = row['common_name_en']
        keywords = str(row['search_keywords']).split('|')
        
        print(f"\n{'#' * 60}")
        print(f"🧬 MALADIE {index+1}/{len(df)}: {disease_name}")
        print(f"   Mots-clés : {len(keywords)}")
        print(f"{'#' * 60}")
        
        disease_downloaded = 0
        disease_urls = 0
        
        for kw in keywords:
            kw = kw.strip()
            if kw:
                # Pause stratégique entre les requêtes (éviter ban IP)
                time.sleep(random.uniform(3.0, 7.0))
                dl_count, url_count = scrape_keyword(kw, disease_name, output_dir, global_hashes)
                disease_downloaded += dl_count
                disease_urls += url_count
        
        stats[disease_name] = {
            "keywords": len(keywords),
            "urls_found": disease_urls,
            "downloaded": disease_downloaded,
            "unique_hashes": len(global_hashes)
        }
        total_downloaded += disease_downloaded
        total_urls += disease_urls
        
        print(f"\n    📊 Bilan {disease_name}: {disease_downloaded} images uniques téléchargées")
    
    # ==========================================
    # RÉSUMÉ FINAL
    # ==========================================
    print("\n" + "=" * 60)
    print("🎉 EXÉCUTION TERMINÉE !")
    print("=" * 60)
    print(f"\n📊 STATISTIQUES GLOBALES:")
    print(f"   Total URLs trouvées     : {total_urls}")
    print(f"   Total images téléchargées: {total_downloaded}")
    print(f"   Total hashes uniques    : {len(global_hashes)}")
    print(f"\n📊 PAR MALADIE:")
    print(f"   {'Maladie':<30} {'URLs':>8} {'Téléchargées':>14}")
    print(f"   {'-'*52}")
    for disease, s in stats.items():
        print(f"   {disease:<30} {s['urls_found']:>8} {s['downloaded']:>14}")
    
    # Sauvegarder les stats en JSON
    stats_path = os.path.join(output_dir, "scraping_stats.json")
    stats["_summary"] = {
        "total_urls": total_urls,
        "total_downloaded": total_downloaded,
        "total_unique_hashes": len(global_hashes),
        "csv_source": csv_path,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }
    with open(stats_path, 'w') as f:
        json.dump(stats, f, indent=2, ensure_ascii=False)
    print(f"\n💾 Statistiques sauvées dans : {stats_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Scraper V2 multi-moteur pour images médicales")
    parser.add_argument("--csv", type=str, default="target_diseases.csv",
                       help="Chemin vers le fichier CSV des maladies")
    parser.add_argument("--out", type=str, default="./dataset_images",
                       help="Dossier de sortie principal")
    args = parser.parse_args()
    
    os.makedirs(args.out, exist_ok=True)
    main(args.csv, args.out)
