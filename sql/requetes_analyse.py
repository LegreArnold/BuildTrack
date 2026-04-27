# sql/requetes_analyse.py
# Requetes SQL d'analyse metier - BuildTrack

import sqlite3
import pandas as pd

conn = sqlite3.connect("data/buildtrack.db")

print("=" * 55)
print("ANALYSE BUILDTRACK - Requetes SQL")
print("=" * 55)

# --- REQUETE 1 : Vue generale des chantiers ---
# Compter les chantiers par statut
print("\n[1] Repartition des chantiers par statut")
q1 = """
    SELECT
        statut,
        COUNT(*) AS nombre_chantiers
    FROM chantiers
    GROUP BY statut
    ORDER BY nombre_chantiers DESC
"""
df1 = pd.read_sql_query(q1, conn)
print(df1.to_string(index=False))

# --- REQUETE 2 : Performance financiere ---
# Chantiers avec le plus grand depassement de budget
print("\n[2] Top 10 chantiers avec depassement de budget")
q2 = """
    SELECT
        c.nom_chantier,
        c.ville,
        c.type_ouvrage,
        ROUND(SUM(f.budget_prevu), 0)   AS total_prevu,
        ROUND(SUM(f.budget_reel), 0)    AS total_reel,
        ROUND(SUM(f.budget_reel - f.budget_prevu), 0) AS ecart_total
    FROM finances f
    JOIN chantiers c ON f.id_chantier = c.id_chantier
    GROUP BY c.id_chantier
    ORDER BY ecart_total DESC
    LIMIT 10
"""
df2 = pd.read_sql_query(q2, conn)
print(df2.to_string(index=False))

# --- REQUETE 3 : Analyse CO2 par source ---
# Quelles sources emettent le plus de CO2
print("\n[3] Emissions CO2 totales par source")
q3 = """
    SELECT
        source,
        ROUND(SUM(tonnes_co2), 2)    AS total_co2,
        ROUND(SUM(objectif_co2), 2)  AS total_objectif,
        ROUND(SUM(tonnes_co2) - SUM(objectif_co2), 2) AS ecart_co2
    FROM emissions_co2
    GROUP BY source
    ORDER BY total_co2 DESC
"""
df3 = pd.read_sql_query(q3, conn)
print(df3.to_string(index=False))

# --- REQUETE 4 : Evolution mensuelle du budget ---
# Comparer budget prevu vs reel mois par mois
print("\n[4] Evolution mensuelle budget prevu vs reel (tous chantiers)")
q4 = """
    SELECT
        mois,
        ROUND(SUM(budget_prevu), 0) AS total_prevu,
        ROUND(SUM(budget_reel), 0)  AS total_reel,
        ROUND(SUM(budget_reel - budget_prevu), 0) AS ecart
    FROM finances
    GROUP BY mois
    ORDER BY mois
"""
df4 = pd.read_sql_query(q4, conn)
print(df4.to_string(index=False))

# --- REQUETE 5 : Chantiers qui depassent l'objectif CO2 ---
print("\n[5] Chantiers qui depassent leur objectif CO2")
q5 = """
    SELECT
        c.nom_chantier,
        c.ville,
        ROUND(SUM(e.tonnes_co2), 2)   AS co2_reel,
        ROUND(SUM(e.objectif_co2), 2) AS co2_objectif,
        ROUND(SUM(e.tonnes_co2) - SUM(e.objectif_co2), 2) AS depassement
    FROM emissions_co2 e
    JOIN chantiers c ON e.id_chantier = c.id_chantier
    GROUP BY c.id_chantier
    HAVING depassement > 0
    ORDER BY depassement DESC
    LIMIT 10
"""
df5 = pd.read_sql_query(q5, conn)
print(df5.to_string(index=False))

conn.close()

print("\nAnalyse terminee")