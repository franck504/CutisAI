import pandas as pd

def read_diseases(csv_path):
    print("--- Chargement de la liste des maladies ---")
    try:
        # Lire le CSV dans un DataFrame pandas
        df = pd.read_csv(csv_path)
        
        # Afficher le nombre total de maladies
        print(f"✅ {len(df)} maladies trouvées dans le fichier.\n")
        
        # Afficher la liste des maladies (Français et Anglais)
        for index, row in df.iterrows():
            print(f"[{row['id']}] {row['common_name_fr']} (EN: {row['common_name_en']})")
            print(f"    🔬 {row['scientific_name']}")
            print(f"    👀 {row['description_visual']}")
            print(f"    🔍 Mots-clés pour le scraping : {row['search_keywords']}\n")
            
        return df
        
    except FileNotFoundError:
        print(f"❌ Erreur : Le fichier {csv_path} est introuvable.")
    except Exception as e:
        print(f"❌ Erreur lors de la lecture : {e}")

if __name__ == "__main__":
    # Nom du fichier qu'on vient de créer
    fichier_csv = "target_diseases.csv"
    
    # Appel de la fonction
    dataset_maladies = read_diseases(fichier_csv)
