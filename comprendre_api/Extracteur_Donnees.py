import requests
import pandas as pd

def liste_donnees(code_commune=None,taille_echantillon=3000):
    # liste_donnees prend par défaut aucune condition donc on pioche dans la France, on peut aussi imposer une condition de code postal
    params_lines = {
        "page": 1,
        "size": taille_echantillon,
        "select": ",".join([
            "_id", "consommation_energie", "classe_consommation_energie", "surface_thermique_lot",
            "estimation_ges", "classe_estimation_ges",
            "annee_construction", "tr002_type_batiment_description",
            "code_insee_commune_actualise", "geo_adresse", "latitude", "longitude"
        ]),
        "q": f"code_insee_commune_actualise:{code_commune}" if code_commune else None,
    }

    url_lines = "https://data.ademe.fr/data-fair/api/v1/datasets/dpe-france/lines"

    response_lines = requests.get(url_lines, params=params_lines)

    if response_lines.status_code == 200:
        data_lines = response_lines.json()

        # Créez un DataFrame avec les données associées à chaque ID
        df = pd.DataFrame([
            {
                '_id': entry['_id'],
                'consommation_energie': entry.get('consommation_energie'),
                'classe_consommation_energie': entry.get('classe_consommation_energie'),
                'estimation_ges': entry.get('estimation_ges'),
                'surface_thermique_lot': entry.get('surface_thermique_lot'),
                'classe_estimation_ges': entry.get('classe_estimation_ges'),
                'annee_construction': entry.get('annee_construction'),
                'tr002_type_batiment_description': entry.get('tr002_type_batiment_description'),
                'code_insee_commune_actualise': entry.get('code_insee_commune_actualise'),
                'latitude': entry.get('latitude'),
                'longitude': entry.get('longitude'),
                'geo_adresse': entry.get('geo_adresse'),
                # Ajoutez d'autres colonnes pertinentes selon vos besoins
            }
            for entry in data_lines['results']
        ])

        # Enregistrez le DataFrame au format Excel avec le nom de fichier 'donnees_associées.xlsx'
        #filename = f'liste_finale_{code_commune}.xlsx' if code_commune else 'liste_finale_France.xlsx'
        #df.to_excel(filename, index=False)

        return df

    else:
        return f"Erreur {response_lines.status_code}: {response_lines.text}"

