# python/generate_data.py
# Generation de donnees realistes pour BuildTrack

import sqlite3
import random
from faker import Faker

fake = Faker("fr_FR")
random.seed(42)

conn = sqlite3.connect("data/buildtrack.db")
cursor = conn.cursor()

# --- DONNEES DE REFERENCE ---

types_ouvrages = [
    "Logement", "Bureau", "Hopital", "Ecole",
    "Centre commercial", "Hotel", "Infrastructure publique"
]

statuts = ["En cours", "Termine", "En pause", "Planifie"]

sources_co2 = ["Transport", "Materiaux", "Energie", "Engins de chantier"]

regions = ["Ile-de-France", "Auvergne-Rhone-Alpes", "Provence-Alpes-Cote-Azur",
           "Nouvelle-Aquitaine", "Occitanie", "Hauts-de-France"]

mois_liste = [
    "2023-01", "2023-02", "2023-03", "2023-04", "2023-05", "2023-06",
    "2023-07", "2023-08", "2023-09", "2023-10", "2023-11", "2023-12"
]

# --- TABLE CHANTIERS : 50 chantiers ---
print("Insertion des chantiers...")
chantiers = []
for i in range(1, 51):
    date_debut = fake.date_between(start_date="-3y", end_date="-1y")
    date_fin = fake.date_between(start_date="-1y", end_date="+2y")
    chantier = (
        i,
        f"Chantier {fake.city()} {i}",
        fake.city(),
        random.choice(types_ouvrages),
        str(date_debut),
        str(date_fin),
        random.choice(statuts)
    )
    chantiers.append(chantier)

cursor.executemany("""
    INSERT OR IGNORE INTO chantiers
    (id_chantier, nom_chantier, ville, type_ouvrage, date_debut, date_fin, statut)
    VALUES (?, ?, ?, ?, ?, ?, ?)
""", chantiers)
print(f"{len(chantiers)} chantiers inseres")

# --- TABLE FINANCES : 1 ligne par mois par chantier ---
print("Insertion des donnees financieres...")
finances = []
id_finance = 1
for id_chantier in range(1, 51):
    for mois in mois_liste:
        budget_prevu = round(random.uniform(500_000, 5_000_000), 2)
        variation = random.uniform(-0.20, 0.30)
        budget_reel = round(budget_prevu * (1 + variation), 2)
        finances.append((id_finance, id_chantier, mois, budget_prevu, budget_reel))
        id_finance += 1

cursor.executemany("""
    INSERT OR IGNORE INTO finances
    (id_finance, id_chantier, mois, budget_prevu, budget_reel)
    VALUES (?, ?, ?, ?, ?)
""", finances)
print(f"{len(finances)} lignes financieres inserees")

# --- TABLE EMISSIONS CO2 ---
print("Insertion des emissions CO2...")
emissions = []
id_emission = 1
for id_chantier in range(1, 51):
    for mois in mois_liste:
        for source in sources_co2:
            tonnes = round(random.uniform(10, 500), 2)
            objectif = round(tonnes * random.uniform(0.7, 1.1), 2)
            emissions.append((id_emission, id_chantier, mois, source, tonnes, objectif))
            id_emission += 1

cursor.executemany("""
    INSERT OR IGNORE INTO emissions_co2
    (id_emission, id_chantier, mois, source, tonnes_co2, objectif_co2)
    VALUES (?, ?, ?, ?, ?, ?)
""", emissions)
print(f"{len(emissions)} lignes CO2 inserees")

# --- TABLE UNITES OPERATIONNELLES ---
print("Insertion des unites operationnelles...")
unites = []
for id_chantier in range(1, 51):
    unite = (
        id_chantier,
        f"Unite {random.choice(regions)}",
        random.choice(regions),
        fake.name(),
        id_chantier
    )
    unites.append(unite)

cursor.executemany("""
    INSERT OR IGNORE INTO unites_operationnelles
    (id_unite, nom_unite, region, responsable, id_chantier)
    VALUES (?, ?, ?, ?, ?)
""", unites)
print(f"{len(unites)} unites inserees")

conn.commit()
conn.close()

print("\nBase de donnees remplie avec succes")
print(f"Total : {len(chantiers)} chantiers | {len(finances)} lignes finances | {len(emissions)} lignes CO2")