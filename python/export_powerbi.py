# python/export_powerbi.py
# Export des donnees pour Power BI

import sqlite3
import pandas as pd

conn = sqlite3.connect("data/buildtrack.db")

# --- EXPORT 1 : Chantiers ---
df_chantiers = pd.read_sql_query("SELECT * FROM chantiers", conn)
df_chantiers.to_excel("data/chantiers.xlsx", index=False)
print("chantiers.xlsx exporte")

# --- EXPORT 2 : Finances avec nom du chantier ---
df_finances = pd.read_sql_query("""
    SELECT
        f.id_finance,
        c.nom_chantier,
        c.ville,
        c.type_ouvrage,
        c.statut,
        f.mois,
        f.budget_prevu,
        f.budget_reel,
        ROUND(f.budget_reel - f.budget_prevu, 2) AS ecart,
        ROUND((f.budget_reel - f.budget_prevu) / f.budget_prevu * 100, 2) AS ecart_pct
    FROM finances f
    JOIN chantiers c ON f.id_chantier = c.id_chantier
""", conn)
df_finances.to_excel("data/finances.xlsx", index=False)
print("finances.xlsx exporte")

# --- EXPORT 3 : Emissions CO2 avec nom du chantier ---
df_co2 = pd.read_sql_query("""
    SELECT
        e.id_emission,
        c.nom_chantier,
        c.ville,
        c.type_ouvrage,
        e.mois,
        e.source,
        e.tonnes_co2,
        e.objectif_co2,
        ROUND(e.tonnes_co2 - e.objectif_co2, 2) AS ecart_co2
    FROM emissions_co2 e
    JOIN chantiers c ON e.id_chantier = c.id_chantier
""", conn)
df_co2.to_excel("data/emissions_co2.xlsx", index=False)
print("emissions_co2.xlsx exporte")

# --- EXPORT 4 : Unites operationnelles ---
df_unites = pd.read_sql_query("""
    SELECT
        u.nom_unite,
        u.region,
        u.responsable,
        c.nom_chantier,
        c.ville,
        c.statut
    FROM unites_operationnelles u
    JOIN chantiers c ON u.id_chantier = c.id_chantier
""", conn)
df_unites.to_excel("data/unites_operationnelles.xlsx", index=False)
print("unites_operationnelles.xlsx exporte")

conn.close()

print("\nExport termine - 4 fichiers Excel disponibles dans data/")