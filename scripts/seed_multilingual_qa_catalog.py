#!/usr/bin/env python3
"""
Seed 90 test properties + 10 test services (100 QA entries) for LAWIM_V2.
Idempotent, deterministic, QA-only. Never modifies real production data.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import sys
import time
from dataclasses import dataclass, field, asdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

SEED_VERSION = "1.0.0"
TEST_PREFIX = "QA-"
DEFAULT_ENVIRONMENT = os.environ.get("LAWIM_ENV", "development")
DEFAULT_LOCALE = "fr"

TRANSACTION_TYPES = ("rent", "sale", "short_term", "commercial_lease", "investment")
PROPERTY_TYPES = ("apartment", "house", "studio", "room", "villa", "duplex", "land", "building", "office", "shop", "warehouse", "furnished")
PROPERTY_TYPES_SHORT = ("apartment", "house", "studio", "room", "villa", "duplex", "land", "building", "office", "shop", "warehouse")

CITIES = {
    "douala": {
        "districts": ("bonamoussadi", "kotto", "makepe", "logpom", "denver", "bonapriso", "bonanjo", "akwa", "deido", "bassa", "japoma", "yassa", "nyalla", "pk12"),
        "lat": 4.05, "lon": 9.70, "count": 28,
    },
    "yaounde": {
        "districts": ("bastos", "odza", "mvan", "nlongkak", "essos", "omnisports", "etoudi", "mendong", "biyem-assi", "nkolbisson", "nsimeyong", "ekounou", "emana"),
        "lat": 3.87, "lon": 11.52, "count": 24,
    },
    "bafoussam": {
        "districts": ("tamdja", "banengo", "djeleng", "famla", "kamkop", "tougang"),
        "lat": 5.48, "lon": 10.42, "count": 9,
    },
    "kribi": {
        "districts": ("centre-ville", "dombe", "bwambe", "grand batanga", "mpolongwe"),
        "lat": 2.94, "lon": 9.91, "count": 7,
    },
    "limbe": {
        "districts": ("mile 4", "bota", "molyko road axis", "down beach", "bonadikombo"),
        "lat": 4.02, "lon": 9.19, "count": 6,
    },
    "buea": {
        "districts": ("molyko", "bonduma", "great soppo", "bomaka", "clerks quarters"),
        "lat": 4.16, "lon": 9.23, "count": 6,
    },
    "bamenda": {"districts": ("up station", "nkwen", "mbatu"), "lat": 5.96, "lon": 10.15, "count": 3},
    "garoua": {"districts": ("pitoare", "roumde adia"), "lat": 9.30, "lon": 13.40, "count": 2},
    "ngaoundere": {"districts": ("baladji", "malang"), "lat": 7.32, "lon": 13.58, "count": 2},
    "ebolowa": {"districts": ("nkoetye",), "lat": 2.90, "lon": 11.15, "count": 1},
    "foumban": {"districts": ("mankong",), "lat": 5.73, "lon": 10.90, "count": 1},
    "mbandjock": {"districts": ("centre",), "lat": 4.10, "lon": 11.50, "count": 1},
}

TARGET_TYPES = [
    ("apartment", 18), ("house", 15), ("studio", 10), ("room", 8),
    ("villa", 10), ("duplex", 7), ("land", 8), ("building", 4),
    ("office", 4), ("shop", 3), ("warehouse", 2), ("furnished", 1),
]

TARGET_TRANSACTIONS = [
    ("rent", 50), ("sale", 25), ("short_term", 8),
    ("commercial_lease", 4), ("investment", 3),
]

PRICE_RANGES = {
    "rent": {"economic": (25000, 80000), "mid": (80000, 200000), "superior": (200000, 500000), "premium": (500000, 1500000)},
    "sale": {"economic": (5000000, 15000000), "mid": (15000000, 40000000), "superior": (40000000, 80000000), "premium": (80000000, 250000000)},
    "short_term": {"economic": (15000, 40000), "mid": (40000, 100000), "superior": (100000, 250000), "premium": (250000, 800000)},
    "commercial_lease": {"economic": (100000, 300000), "mid": (300000, 800000), "superior": (800000, 2000000), "premium": (2000000, 5000000)},
    "investment": {"economic": (10000000, 30000000), "mid": (30000000, 60000000), "superior": (60000000, 100000000), "premium": (100000000, 500000000)},
}

SERVICES = [
    {
        "code": "SRV-PERSO-SEARCH",
        "fr": ("Recherche personnalisée de biens", "Nous trouvons le bien idéal selon vos critères avec une recherche sur mesure."),
        "en": ("Personalized property search", "We find the ideal property according to your criteria with a tailored search."),
        "pcm": ("Personal search for property", "We go find the property wey fit you according to wetin you want."),
    },
    {
        "code": "SRV-QUALIFICATION",
        "fr": ("Qualification d'un besoin immobilier", "Analyse complète de votre projet immobilier pour identifier vos besoins réels."),
        "en": ("Real estate needs qualification", "Complete analysis of your real estate project to identify your actual needs."),
        "pcm": ("Understand your property need", "We go check your property project well to know wetin you really want."),
    },
    {
        "code": "SRV-MATCH-OWNER",
        "fr": ("Mise en relation avec un propriétaire", "Nous vous mettons directement en contact avec le propriétaire du bien."),
        "en": ("Connection with property owner", "We put you in direct contact with the property owner."),
        "pcm": ("Connect you with owner", "We go connect you direct with di owner of di property."),
    },
    {
        "code": "SRV-MATCH-AGENT",
        "fr": ("Mise en relation avec un agent immobilier", "Contactez un agent professionnel pour vous accompagner."),
        "en": ("Connection with a real estate agent", "Contact a professional agent to assist you."),
        "pcm": ("Connect you with agent", "Contact professional agent wey go help you."),
    },
    {
        "code": "SRV-VISIT",
        "fr": ("Organisation d'une visite", "Nous organisons une visite du bien à la date et l'heure de votre choix."),
        "en": ("Visit arrangement", "We arrange a property visit at your preferred date and time."),
        "pcm": ("Arrange visit", "We go arrange visit to see di property for time wey you want."),
    },
    {
        "code": "SRV-RENT-SUPPORT",
        "fr": ("Accompagnement à la location", "Assistance complète pour la signature de votre bail et l'état des lieux."),
        "en": ("Rental support", "Full assistance for signing your lease and inventory of fixtures."),
        "pcm": ("Help for renting", "We go help you with everything from signing lease to checking di house."),
    },
    {
        "code": "SRV-BUY-SUPPORT",
        "fr": ("Accompagnement à l'achat", "Suivi de votre dossier d'achat de la visite à la signature chez le notaire."),
        "en": ("Purchase support", "Follow-up of your purchase file from visit to notary signature."),
        "pcm": ("Help for buying", "We go follow your transaction from visit go to notary."),
    },
    {
        "code": "SRV-DOCUMENT",
        "fr": ("Assistance documentaire", "Nous vous aidons à rassembler et vérifier tous les documents nécessaires."),
        "en": ("Document assistance", "We help you gather and verify all required documents."),
        "pcm": ("Document help", "We go help you collect and check all di papers wey you need."),
    },
    {
        "code": "SRV-TRANSACTION-FOLLOW",
        "fr": ("Assistance au suivi d'une transaction", "Suivi personnalisé de votre transaction jusqu'à sa conclusion."),
        "en": ("Transaction follow-up assistance", "Personalized monitoring of your transaction until completion."),
        "pcm": ("Follow your transaction", "We go follow your transaction from start to finish."),
    },
    {
        "code": "SRV-ANALYSIS",
        "fr": ("Analyse immobilière et reporting", "Rapport détaillé sur le marché immobilier et les opportunités disponibles."),
        "en": ("Real estate analysis and reporting", "Detailed report on the real estate market and available opportunities."),
        "pcm": ("Property analysis and report", "We go give you full report on property market and wetin dey available."),
    },
]


def _stable_id(prefix: str, index: int) -> str:
    raw = f"{TEST_PREFIX}{prefix}-{SEED_VERSION}-{index:03d}"
    short = hashlib.sha256(raw.encode()).hexdigest()[:12]
    return f"{TEST_PREFIX}{prefix}-{short}"


def _deterministic_price(transaction_type: str, index: int) -> float:
    ranges = PRICE_RANGES[transaction_type]
    segments = list(ranges.values())
    segment = segments[index % len(segments)]
    lo, hi = segment
    span = hi - lo
    offset = (index * 7919) % span
    return round(lo + offset, -3)


def _deterministic_coord(city_info: dict, index: int) -> tuple[float, float]:
    lat_offset = (index * 7) % 100 / 1000.0
    lon_offset = (index * 13) % 100 / 1000.0
    return round(city_info["lat"] + lat_offset, 4), round(city_info["lon"] + lon_offset, 4)


@dataclass
class QAProperty:
    test_id: str
    property_type: str
    transaction_type: str
    city: str
    district: str
    price: float
    currency: str = "XAF"
    surface_area: int = 0
    bedrooms: int = 0
    bathrooms: int = 0
    parking: bool = False
    furnished: bool = False
    amenities: list[str] = field(default_factory=list)
    availability: str = "immediate"
    latitude: float | None = None
    longitude: float | None = None
    is_test: bool = True
    qa_visibility: str = "QA_ONLY"
    qa_label: str = "TEST DATA"
    seed_version: str = SEED_VERSION

    def title_fr(self) -> str:
        ttype = {"rent": "Location", "sale": "Vente", "short_term": "Location courte durée", "commercial_lease": "Bail commercial", "investment": "Investissement"}
        ptype = {"apartment": "Appartement", "house": "Maison", "studio": "Studio", "room": "Chambre", "villa": "Villa", "duplex": "Duplex", "land": "Terrain", "building": "Immeuble", "office": "Bureau", "shop": "Boutique", "warehouse": "Entrepôt", "furnished": "Résidence meublée"}
        return f"{ttype.get(self.transaction_type, self.transaction_type)} - {ptype.get(self.property_type, self.property_type)} à {self.district.title()}, {self.city.title()}"

    def title_en(self) -> str:
        ttype = {"rent": "Rent", "sale": "Sale", "short_term": "Short-term rent", "commercial_lease": "Commercial lease", "investment": "Investment"}
        ptype = {"apartment": "Apartment", "house": "House", "studio": "Studio", "room": "Room", "villa": "Villa", "duplex": "Duplex", "land": "Land", "building": "Building", "office": "Office", "shop": "Shop", "warehouse": "Warehouse", "furnished": "Furnished residence"}
        return f"{ttype.get(self.transaction_type, self.transaction_type)} - {ptype.get(self.property_type, self.property_type)} in {self.district.title()}, {self.city.title()}"

    def title_wes(self) -> str:
        ttype = {"rent": "Rent", "sale": "Sale", "short_term": "Short-time rent", "commercial_lease": "Commercial lease", "investment": "Investment"}
        ptype = {"apartment": "Apartment", "house": "House", "studio": "Studio", "room": "Room", "villa": "Villa", "duplex": "Duplex", "land": "Land", "building": "Building", "office": "Office", "shop": "Shop", "warehouse": "Warehouse", "furnished": "Furnished house"}
        return f"{ttype.get(self.transaction_type, self.transaction_type)} - {ptype.get(self.property_type, self.property_type)} for {self.district.title()}, {self.city.title()}"

    def description_fr(self) -> str:
        return f"{'Meublé' if self.furnished else 'Non meublé'} - {self.surface_area} m² - {self.bedrooms} chambre(s) - {self.bathrooms} salle(s) de bain - {'Parking disponible' if self.parking else 'Sans parking'}. Disponible {self.availability}. Prix : {self.price:,.0f} F CFA."

    def description_en(self) -> str:
        return f"{'Furnished' if self.furnished else 'Unfurnished'} - {self.surface_area} m² - {self.bedrooms} bedroom(s) - {self.bathrooms} bathroom(s) - {'Parking available' if self.parking else 'No parking'}. Available {self.availability}. Price: {self.price:,.0f} F CFA."

    def description_wes(self) -> str:
        return f"{'E get furniture' if self.furnished else 'No get furniture'} - {self.surface_area} m² - {self.bedrooms} bedroom(s) - {self.bathrooms} bathroom(s) - {'Parking dey' if self.parking else 'No parking'}. E dey available {self.availability}. Price: {self.price:,.0f} F CFA."

    def to_dict(self) -> dict[str, Any]:
        return {
            "test_id": self.test_id,
            "title_fr": self.title_fr(),
            "title_en": self.title_en(),
            "title_wes": self.title_wes(),
            "description_fr": self.description_fr(),
            "description_en": self.description_en(),
            "description_wes": self.description_wes(),
            "property_type": self.property_type,
            "transaction_type": self.transaction_type,
            "city": self.city,
            "district": self.district,
            "price": self.price,
            "currency": self.currency,
            "surface_area": self.surface_area,
            "bedrooms": self.bedrooms,
            "bathrooms": self.bathrooms,
            "parking": self.parking,
            "furnished": self.furnished,
            "amenities": list(self.amenities),
            "availability": self.availability,
            "latitude": self.latitude,
            "longitude": self.longitude,
            "is_test": self.is_test,
            "qa_visibility": self.qa_visibility,
            "qa_label": self.qa_label,
            "seed_version": self.seed_version,
            "test_owner": "QA-Test-Owner",
            "test_agent": "QA-Test-Agent",
            "documents_status": "test_only",
        }


@dataclass
class QAService:
    service_code: str
    name_fr: str
    name_en: str
    name_wes: str
    description_fr: str
    description_en: str
    description_wes: str
    is_test: bool = True
    eligibility: str = "all_users"
    workflow: str = "automated"
    payment_mode: str = "sandbox_only"
    currency: str = "XAF"
    qa_visibility: str = "QA_ONLY"
    seed_version: str = SEED_VERSION

    def to_dict(self) -> dict[str, Any]:
        return {k: v for k, v in asdict(self).items()}


def build_properties(rng_seed: int = 42) -> list[QAProperty]:
    props: list[QAProperty] = []
    idx = 0

    def city_cycle():
        nonlocal idx
        for city_name, city_info in CITIES.items():
            for _ in range(city_info["count"]):
                yield city_name, city_info

    city_gen = list(city_cycle())

    type_pool: list[str] = []
    for ptype, count in TARGET_TYPES:
        type_pool.extend([ptype] * count)

    tx_pool: list[str] = []
    for tx, count in TARGET_TRANSACTIONS:
        tx_pool.extend([tx] * count)

    for i, (city_name, city_info) in enumerate(city_gen):
        ptype = type_pool[i % len(type_pool)]
        tx = tx_pool[i % len(tx_pool)]
        district = city_info["districts"][i % len(city_info["districts"])]
        price = _deterministic_price(tx, i)
        lat, lon = _deterministic_coord(city_info, i)

        room_defaults = {
            "apartment": (80, 2, 1), "house": (120, 3, 2), "studio": (30, 1, 1),
            "room": (20, 1, 1), "villa": (250, 4, 3), "duplex": (180, 3, 2),
            "land": (300, 0, 0), "building": (500, 6, 4), "office": (50, 0, 1),
            "shop": (40, 0, 1), "warehouse": (200, 0, 1), "furnished": (60, 2, 1),
        }
        surface, beds, baths = room_defaults.get(ptype, (60, 2, 1))
        parking = ptype in ("house", "villa", "duplex", "building", "office")
        furnished_flag = ptype in ("furnished", "studio") or (ptype == "apartment" and i % 3 == 0)
        amenities_list = ["electricity"]
        if "water" in district or i % 3 == 0:
            amenities_list.append("water")
        if i % 5 == 0:
            amenities_list.append("security")

        prop = QAProperty(
            test_id=_stable_id("PROP", i),
            property_type=ptype,
            transaction_type=tx,
            city=city_name.title(),
            district=district.title(),
            price=price,
            surface_area=surface,
            bedrooms=beds,
            bathrooms=baths,
            parking=parking,
            furnished=furnished_flag,
            amenities=amenities_list,
            availability="immediate",
            latitude=lat,
            longitude=lon,
        )
        props.append(prop)

    return props


def build_services() -> list[QAService]:
    return [
        QAService(
            service_code=srv["code"],
            name_fr=srv["fr"][0],
            name_en=srv["en"][0],
            name_wes=srv["pcm"][0],
            description_fr=srv["fr"][1],
            description_en=srv["en"][1],
            description_wes=srv["pcm"][1],
        )
        for srv in SERVICES
    ]


def verify_counts(props: list[QAProperty], services: list[QAService]) -> list[str]:
    errors: list[str] = []

    if len(props) != 90:
        errors.append(f"Expected 90 properties, got {len(props)}")
    if len(services) != 10:
        errors.append(f"Expected 10 services, got {len(services)}")

    type_counts: dict[str, int] = {}
    for p in props:
        type_counts[p.property_type] = type_counts.get(p.property_type, 0) + 1
    for ptype, expected in TARGET_TYPES:
        actual = type_counts.get(ptype, 0)
        if actual != expected:
            errors.append(f"Property type {ptype}: expected {expected}, got {actual}")

    tx_counts: dict[str, int] = {}
    for p in props:
        tx_counts[p.transaction_type] = tx_counts.get(p.transaction_type, 0) + 1
    for tx, expected in TARGET_TRANSACTIONS:
        actual = tx_counts.get(tx, 0)
        if actual != expected:
            errors.append(f"Transaction type {tx}: expected {expected}, got {actual}")

    city_counts: dict[str, int] = {}
    for p in props:
        city_counts[p.city] = city_counts.get(p.city, 0) + 1
    for cname, cinfo in CITIES.items():
        actual = city_counts.get(cname.title(), 0)
        expected = cinfo["count"]
        if actual != expected:
            errors.append(f"City {cname}: expected {expected}, got {actual}")

    return errors


def checksum(props: list[QAProperty], services: list[QAService]) -> str:
    raw = json.dumps([p.test_id for p in props] + [s.service_code for s in services], sort_keys=True)
    return hashlib.sha256(raw.encode()).hexdigest()


def report(props: list[QAProperty], services: list[QAService], env: str) -> dict[str, Any]:
    type_counts: dict[str, int] = {}
    tx_counts: dict[str, int] = {}
    city_counts: dict[str, int] = {}
    for p in props:
        type_counts[p.property_type] = type_counts.get(p.property_type, 0) + 1
        tx_counts[p.transaction_type] = tx_counts.get(p.transaction_type, 0) + 1
        city_counts[p.city] = city_counts.get(p.city, 0) + 1

    price_summary: dict[str, dict[str, float]] = {}
    for tx in TRANSACTION_TYPES:
        prices = [p.price for p in props if p.transaction_type == tx and p.price > 0]
        if prices:
            price_summary[tx] = {"min": min(prices), "max": max(prices), "avg": round(sum(prices) / len(prices), 0)}

    return {
        "seed_version": SEED_VERSION,
        "environment": env,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "properties_total": len(props),
        "services_total": len(services),
        "checksum": checksum(props, services),
        "property_type_distribution": {k: v for k, v in sorted(type_counts.items())},
        "transaction_distribution": {k: v for k, v in sorted(tx_counts.items())},
        "city_distribution": {k: v for k, v in sorted(city_counts.items())},
        "price_summary": price_summary,
        "all_qa_visibility": "QA_ONLY",
        "is_test": True,
    }


def cmd_dry_run() -> None:
    props = build_properties()
    services = build_services()
    errors = verify_counts(props, services)
    chk = checksum(props, services)
    rpt = report(props, services, DEFAULT_ENVIRONMENT)

    print(f"=== DRY RUN - Seed v{SEED_VERSION} ===")
    print(f"Properties: {len(props)}")
    print(f"Services: {len(services)}")
    print(f"Checksum: {chk}")
    print(f"Errors: {len(errors)}")
    for err in errors:
        print(f"  ERROR: {err}")
    if not errors:
        print("All counts verified OK.")
    print(f"\nPreview: {json.dumps(rpt, indent=2, ensure_ascii=False)}")
    if errors:
        sys.exit(1)


def cmd_apply(env: str, qa_only: bool = False, confirm: bool = False) -> None:
    if env == "production" and not qa_only:
        print("ERROR: Production without --qa-only is forbidden.")
        sys.exit(1)
    if env == "production" and qa_only and not confirm:
        print("ERROR: Production QA requires --confirm-test-data.")
        sys.exit(1)

    props = build_properties()
    services = build_services()
    errors = verify_counts(props, services)
    if errors:
        print("ERRORS in data generation:")
        for err in errors:
            print(f"  {err}")
        sys.exit(1)

    output = {
        "version": SEED_VERSION,
        "environment": env,
        "generated_at": datetime.now(timezone.utc).isoformat(),
        "properties": [p.to_dict() for p in props],
        "services": [s.to_dict() for s in services],
        "checksum": checksum(props, services),
    }

    output_dir = Path("deployment/qa-catalog")
    output_dir.mkdir(parents=True, exist_ok=True)
    output_path = output_dir / f"qa-catalog-{env}.json"
    output_path.write_text(json.dumps(output, indent=2, ensure_ascii=False), encoding="utf-8")
    print(f"QA catalog written to {output_path}")
    print(f"  Properties: {len(props)}")
    print(f"  Services: {len(services)}")
    print(f"  Checksum: {output['checksum']}")
    print(f"  QA-only: {qa_only}")


def cmd_verify() -> None:
    env = os.environ.get("LAWIM_ENV", "development")
    catalog_path = Path(f"deployment/qa-catalog/qa-catalog-{env}.json")
    if not catalog_path.exists():
        print(f"No catalog found for environment '{env}' at {catalog_path}")
        sys.exit(1)
    data = json.loads(catalog_path.read_text(encoding="utf-8"))
    props_list = data.get("properties", [])
    services_list = data.get("services", [])
    stored_checksum = data.get("checksum", "")

    from dataclasses import field as _f
    mock_props = [QAProperty(**{k: v for k, v in p.items() if k in QAProperty.__dataclass_fields__}) for p in props_list]
    mock_services = [QAService(**{k: v for k, v in s.items() if k in QAService.__dataclass_fields__}) for s in services_list]
    expected_checksum = checksum(mock_props, mock_services)

    errors = verify_counts(mock_props, mock_services)

    print(f"=== VERIFY - {catalog_path} ===")
    print(f"Properties: {len(mock_props)}")
    print(f"Services: {len(mock_services)}")
    print(f"Stored checksum: {stored_checksum}")
    print(f"Expected checksum: {expected_checksum}")
    print(f"Integrity: {'OK' if stored_checksum == expected_checksum else 'FAILED'}")
    if stored_checksum != expected_checksum:
        errors.append("Checksum mismatch")
    print(f"Errors: {len(errors)}")
    for err in errors:
        print(f"  ERROR: {err}")
    if not errors:
        print("QA catalog verification PASSED.")
    else:
        sys.exit(1)


def cmd_cleanup(env: str) -> None:
    catalog_path = Path(f"deployment/qa-catalog/qa-catalog-{env}.json")
    if catalog_path.exists():
        catalog_path.unlink()
        print(f"Removed: {catalog_path}")
    print("Cleanup complete.")


def main() -> None:
    parser = argparse.ArgumentParser(description="Seed multilingual QA catalog for LAWIM_V2")
    parser.add_argument("--dry-run", action="store_true", help="Validate counts and print report")
    parser.add_argument("--apply", action="store_true", help="Generate QA catalog file")
    parser.add_argument("--verify", action="store_true", help="Verify existing catalog integrity")
    parser.add_argument("--cleanup", action="store_true", help="Remove QA catalog file")
    parser.add_argument("--environment", default=DEFAULT_ENVIRONMENT, help="Target environment")
    parser.add_argument("--qa-only", action="store_true", help="Restrict to QA visibility")
    parser.add_argument("--confirm-test-data", action="store_true", help="Confirm test data for production")
    args = parser.parse_args()

    if args.dry_run:
        cmd_dry_run()
    elif args.apply:
        cmd_apply(args.environment, args.qa_only, args.confirm_test_data)
    elif args.verify:
        cmd_verify()
    elif args.cleanup:
        cmd_cleanup(args.environment)
    else:
        parser.print_help()


if __name__ == "__main__":
    main()
