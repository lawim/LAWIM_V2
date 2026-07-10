import json
import random
import os


def generate_demo_properties() -> list[dict]:
    data_path = os.path.join(os.path.dirname(__file__), "data", "cameroon_locations.json")
    with open(data_path) as f:
        data = json.load(f)

    neighborhoods = {}
    for n in data["neighborhoods"]:
        city = n["city"]
        if city not in neighborhoods:
            neighborhoods[city] = []
        neighborhoods[city].append(n["name"])

    city_type_plan = {
        "Douala": {"terrain": 15, "maison": 15, "appartement": 12, "immeuble": 6, "villa": 6, "local commercial": 6},
        "Yaounde": {"terrain": 13, "maison": 12, "appartement": 10, "immeuble": 5, "villa": 5, "local commercial": 5},
        "Bafoussam": {"terrain": 5, "maison": 5, "appartement": 3, "immeuble": 3, "villa": 2, "local commercial": 2},
        "Bamenda": {"terrain": 5, "maison": 5, "appartement": 4, "immeuble": 2, "villa": 2, "local commercial": 2},
        "Garoua": {"terrain": 4, "maison": 4, "appartement": 4, "immeuble": 2, "villa": 1, "local commercial": 1},
        "Maroua": {"terrain": 3, "maison": 3, "appartement": 3, "immeuble": 1, "villa": 2, "local commercial": 2},
        "Buea": {"terrain": 1, "maison": 2, "appartement": 1, "immeuble": 0, "villa": 1, "local commercial": 0},
        "Kribi": {"terrain": 2, "maison": 1, "appartement": 1, "immeuble": 0, "villa": 0, "local commercial": 1},
        "Nkongsamba": {"terrain": 1, "maison": 1, "appartement": 1, "immeuble": 0, "villa": 1, "local commercial": 1},
        "Limbe": {"terrain": 1, "maison": 2, "appartement": 1, "immeuble": 1, "villa": 0, "local commercial": 0},
    }

    type_config = {
        "terrain": {
            "price_range": (5_000_000, 100_000_000),
            "surface_range": (200, 2000),
            "bedrooms": 0,
            "bathrooms": 0,
        },
        "maison": {
            "price_range": (15_000_000, 150_000_000),
            "surface_range": (80, 500),
            "bedrooms": (2, 5),
            "bathrooms": (1, 3),
        },
        "appartement": {
            "price_range": (10_000_000, 80_000_000),
            "surface_range": (30, 200),
            "bedrooms": (1, 4),
            "bathrooms": (1, 2),
        },
        "immeuble": {
            "price_range": (50_000_000, 500_000_000),
            "surface_range": (200, 1000),
            "bedrooms": 0,
            "bathrooms": 0,
        },
        "villa": {
            "price_range": (30_000_000, 200_000_000),
            "surface_range": (150, 600),
            "bedrooms": (3, 6),
            "bathrooms": (2, 5),
        },
        "local commercial": {
            "price_range": (10_000_000, 100_000_000),
            "surface_range": (30, 300),
            "bedrooms": 0,
            "bathrooms": 1,
        },
    }

    title_templates = {
        "terrain": [
            "Terrain constructible à {neighborhood}, {city}",
            "Terrain à vendre - {neighborhood} ({city})",
            "Parcelle de terrain - {city} - {neighborhood}",
            "Terrain nu à {neighborhood}",
            "Terrain viabilisé - {neighborhood}",
            "Lotissement {neighborhood} - parcelles disponibles",
            "Terrain résidentiel à {city}",
        ],
        "maison": [
            "Maison à vendre - {neighborhood}, {city}",
            "Belle maison {bedrooms} pièces à {neighborhood}",
            "Maison familiale - {neighborhood} ({city})",
            "Maison d'habitation à {city}",
            "Maison avec jardin - {neighborhood}",
            "Vente maison - {city} quartier {neighborhood}",
        ],
        "appartement": [
            "Appartement à vendre - {neighborhood}, {city}",
            "Bel appartement {bedrooms} pièces - {neighborhood}",
            "Appartement moderne - {city} centre",
            "Appartement à {neighborhood} - {city}",
            "Appartement meublé - {neighborhood} ({city})",
        ],
        "immeuble": [
            "Immeuble rapport - {neighborhood}, {city}",
            "Immeuble commercial et résidentiel - {city}",
            "Immeuble à vendre - {neighborhood} ({city})",
            "Investissement immobilier - immeuble {city}",
            "Immeuble à usage mixte - {neighborhood}",
        ],
        "villa": [
            "Villa de luxe - {neighborhood}, {city}",
            "Magnifique villa avec piscine - {neighborhood}",
            "Villa haut standing - {city}",
            "Villa contemporaine - {neighborhood} ({city})",
            "Belle villa {bedrooms} chambres - {neighborhood}",
        ],
        "local commercial": [
            "Local commercial - {neighborhood}, {city}",
            "Boutique à vendre - {neighborhood} ({city})",
            "Espace commercial - {city} centre",
            "Local professionnel - {neighborhood}",
            "Magasin à céder - {neighborhood} - {city}",
        ],
    }

    desc_templates = {
        "terrain": [
            "Superbe terrain constructible situé dans un quartier en pleine expansion. Idéal pour projet immobilier.",
            "Terrain viabilisé avec tous les raccordements disponibles. Parfait pour construction immédiate.",
            "Parcelle bien située, accès facile, cadre calme et sécurisé. Bon potentiel de valorisation.",
            "Terrain résidentiel dans un lotissement moderne. Bornage effectué, titre foncier disponible.",
        ],
        "maison": [
            "Belle maison d'habitation offrant un cadre de vie agréable. Grand salon, cuisine équipée, cour intérieure.",
            "Maison familiale bien entretenue avec jardin. Quartier résidentiel calme et sécurisé.",
            "Maison moderne avec finitions de qualité. Prestations haut de gamme pour un confort optimal.",
            "Vente maison individuelle avec dépendances. Terrain clôturé, portail électrique.",
        ],
        "appartement": [
            "Appartement lumineux et bien agencé. Séjour spacieux, chambres confortables, cuisine équipée.",
            "Bel appartement en résidence sécurisée. Prestations modernes, proche commodités.",
            "Appartement idéalement situé à proximité des commerces et transports. Excellent rapport qualité-prix.",
        ],
        "immeuble": [
            "Immeuble de rapport composé d'appartements et de locaux commerciaux. Excellent rendement locatif.",
            "Immeuble moderne avec ascenseur et parking souterrain. Situation stratégique en centre-ville.",
            "Immeuble à usage mixte idéal pour investisseur. Revenus locatifs stables et sécurisés.",
        ],
        "villa": [
            "Magnifique villa haut standing avec piscine et jardin paysager. Prestations de luxe, finitions soignées.",
            "Villa contemporaine offrant des espaces de vie généreux. Quartier résidentiel prisé.",
            "Superbe villa avec vue imprenable. Terrasse, piscine, garage pour plusieurs véhicules.",
        ],
        "local commercial": [
            "Local commercial bien situé avec forte affluence. Vitrine généreuse, espace de vente lumineux.",
            "Boutique en plein centre-ville idéale pour commerce de détail. Surface modulable.",
            "Local professionnel avec mezzanine. Parfait pour activité commerciale ou bureau.",
        ],
    }

    feature_pool = {
        "terrain": [
            "Viabilisé", "Borné", "Accès route", "Clôturé", "Titre foncier",
            "Constructible", "Plan de bornage", "Proximité école", "Proximité marché",
        ],
        "maison": [
            "Garage", "Jardin", "Cuisine équipée", "Climatisation", "Placards",
            "Carrelage", "Portail électrique", "Terrasse", "Buanderie", "Citerne d'eau",
        ],
        "appartement": [
            "Cuisine équipée", "Balcon", "Parking", "Climatisation", "Placards",
            "Carrelage", "Groupe électrogène", "Interphone", "Garde",
        ],
        "immeuble": [
            "Ascenseur", "Parking", "Sécurité", "Groupe électrogène", "Citerne d'eau",
            "Vidéophone", "Local poubelle", "Toiture terrasse",
        ],
        "villa": [
            "Piscine", "Jardin", "Garage", "Climatisation", "Cuisine équipée",
            "Terrasse", "Placards", "Groupe électrogène", "Portail électrique",
            "Système d'alarme", "Citerne d'eau", "Carrelage haut de gamme",
        ],
        "local commercial": [
            "Vitrine", "Parking", "Climatisation", "Mezzanine", "Alarme",
            "Éclairage", "Réserve", "Sanitaires privés",
        ],
    }

    properties = []

    for city, types in city_type_plan.items():
        for prop_type, count in types.items():
            for _ in range(count):
                cfg = type_config[prop_type]
                city_neighborhoods = neighborhoods.get(city, [])
                neighborhood = random.choice(city_neighborhoods) if city_neighborhoods else city

                price = random.randint(*cfg["price_range"])
                price = round(price / 500_000) * 500_000

                surface = random.randint(*cfg["surface_range"])

                bedrooms = 0
                bathrooms = 0
                if isinstance(cfg["bedrooms"], tuple):
                    bedrooms = random.randint(*cfg["bedrooms"])
                if isinstance(cfg["bathrooms"], tuple):
                    bathrooms = random.randint(*cfg["bathrooms"])
                elif cfg["bathrooms"]:
                    bathrooms = cfg["bathrooms"]

                title = random.choice(title_templates[prop_type]).format(
                    neighborhood=neighborhood, city=city, bedrooms=bedrooms
                )
                description = random.choice(desc_templates[prop_type])

                pool = feature_pool[prop_type]
                n_features = random.randint(2, min(5, len(pool)))
                features = random.sample(pool, n_features)

                status = random.choices(
                    ["available", "reserved", "sold"],
                    weights=[70, 20, 10],
                    k=1,
                )[0]

                properties.append({
                    "title": title,
                    "type": prop_type,
                    "city": city,
                    "price": price,
                    "surface": surface,
                    "bedrooms": bedrooms,
                    "bathrooms": bathrooms,
                    "status": status,
                    "description": description,
                    "features": features,
                    "images": [],
                })

    random.shuffle(properties)
    return properties
