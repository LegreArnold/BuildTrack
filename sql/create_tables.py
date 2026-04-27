# sql/create_tables.py
# Creation de la base de donnees BuildTrack

import sqlite3

# Connexion a la base de donnees
# Si le fichier n'existe pas, SQLite le cree automatiquement
conn = sqlite3.connect("data/buildtrack.db")
cursor = conn.cursor()

print("Creation des tables...")

# TABLE 1 : CHANTIERS
cursor.execute("""
CREATE TABLE IF NOT EXISTS chantiers (
    id_chantier     INTEGER PRIMARY KEY,
    nom_chantier    TEXT NOT NULL,
    ville           TEXT NOT NULL,
    type_ouvrage    TEXT NOT NULL,
    date_debut      TEXT NOT NULL,
    date_fin        TEXT NOT NULL,
    statut          TEXT NOT NULL
)
""")
print("Table chantiers creee")

# TABLE 2 : FINANCES
cursor.execute("""
CREATE TABLE IF NOT EXISTS finances (
    id_finance      INTEGER PRIMARY KEY,
    id_chantier     INTEGER NOT NULL,
    mois            TEXT NOT NULL,
    budget_prevu    REAL NOT NULL,
    budget_reel     REAL NOT NULL,
    ecart           REAL GENERATED ALWAYS AS (budget_reel - budget_prevu) VIRTUAL,
    FOREIGN KEY (id_chantier) REFERENCES chantiers(id_chantier)
)
""")
print("Table finances creee")

# TABLE 3 : EMISSIONS CO2
cursor.execute("""
CREATE TABLE IF NOT EXISTS emissions_co2 (
    id_emission     INTEGER PRIMARY KEY,
    id_chantier     INTEGER NOT NULL,
    mois            TEXT NOT NULL,
    source          TEXT NOT NULL,
    tonnes_co2      REAL NOT NULL,
    objectif_co2    REAL NOT NULL,
    FOREIGN KEY (id_chantier) REFERENCES chantiers(id_chantier)
)
""")
print("Table emissions_co2 creee")

# TABLE 4 : UNITES OPERATIONNELLES
cursor.execute("""
CREATE TABLE IF NOT EXISTS unites_operationnelles (
    id_unite        INTEGER PRIMARY KEY,
    nom_unite       TEXT NOT NULL,
    region          TEXT NOT NULL,
    responsable     TEXT NOT NULL,
    id_chantier     INTEGER NOT NULL,
    FOREIGN KEY (id_chantier) REFERENCES chantiers(id_chantier)
)
""")
print("Table unites_operationnelles creee")

conn.commit()
conn.close()

print("Base de donnees creee : data/buildtrack.db")
print("Tables disponibles : chantiers, finances, emissions_co2, unites_operationnelles")