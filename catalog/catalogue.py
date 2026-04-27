# catalog/catalogue.py
# Catalogue de donnees - BuildTrack

import pandas as pd
import json

catalogue = [
    {
        "table": "chantiers",
        "colonne": "id_chantier",
        "nom_complet": "Identifiant chantier",
        "description": "Identifiant unique de chaque chantier",
        "type": "Entier",
        "obligatoire": True,
        "regle_qualite": "Doit etre unique et non nul"
    },
    {
        "table": "chantiers",
        "colonne": "nom_chantier",
        "nom_complet": "Nom du chantier",
        "description": "Denomination officielle du chantier",
        "type": "Texte",
        "obligatoire": True,
        "regle_qualite": "Ne doit pas etre vide"
    },
    {
        "table": "chantiers",
        "colonne": "ville",
        "nom_complet": "Ville",
        "description": "Ville d'implantation du chantier",
        "type": "Texte",
        "obligatoire": True,
        "regle_qualite": "Ne doit pas etre vide"
    },
    {
        "table": "chantiers",
        "colonne": "type_ouvrage",
        "nom_complet": "Type d'ouvrage",
        "description": "Categorie de l'ouvrage construit",
        "type": "Texte",
        "obligatoire": True,
        "regle_qualite": "Valeurs autorisees : Logement, Bureau, Hopital, Ecole, Centre commercial, Hotel, Infrastructure publique"
    },
    {
        "table": "chantiers",
        "colonne": "statut",
        "nom_complet": "Statut du chantier",
        "description": "Etat d'avancement du chantier",
        "type": "Texte",
        "obligatoire": True,
        "regle_qualite": "Valeurs autorisees : En cours, Termine, En pause, Planifie"
    },
    {
        "table": "finances",
        "colonne": "budget_prevu",
        "nom_complet": "Budget prevu",
        "description": "Budget initialement alloue au chantier pour le mois concerne, en euros",
        "type": "Decimal",
        "obligatoire": True,
        "regle_qualite": "Doit etre positif et superieur a 0"
    },
    {
        "table": "finances",
        "colonne": "budget_reel",
        "nom_complet": "Budget reel",
        "description": "Depenses reelles constatees sur le chantier pour le mois concerne, en euros",
        "type": "Decimal",
        "obligatoire": True,
        "regle_qualite": "Doit etre positif"
    },
    {
        "table": "finances",
        "colonne": "ecart",
        "nom_complet": "Ecart budgetaire",
        "description": "Difference entre budget reel et budget prevu. Positif = depassement, Negatif = economie",
        "type": "Decimal",
        "obligatoire": False,
        "regle_qualite": "Calcule automatiquement : budget_reel - budget_prevu"
    },
    {
        "table": "emissions_co2",
        "colonne": "source",
        "nom_complet": "Source d'emission",
        "description": "Origine des emissions de CO2 sur le chantier",
        "type": "Texte",
        "obligatoire": True,
        "regle_qualite": "Valeurs autorisees : Transport, Materiaux, Energie, Engins de chantier"
    },
    {
        "table": "emissions_co2",
        "colonne": "tonnes_co2",
        "nom_complet": "Tonnes de CO2 emises",
        "description": "Quantite de CO2 effectivement emise sur le chantier pour le mois concerne",
        "type": "Decimal",
        "obligatoire": True,
        "regle_qualite": "Doit etre positif ou nul"
    },
    {
        "table": "emissions_co2",
        "colonne": "objectif_co2",
        "nom_complet": "Objectif CO2",
        "description": "Seuil d'emissions CO2 a ne pas depasser dans le cadre des engagements RSE de Bouygues",
        "type": "Decimal",
        "obligatoire": True,
        "regle_qualite": "Doit etre positif et superieur a 0"
    },
    {
        "table": "unites_operationnelles",
        "colonne": "region",
        "nom_complet": "Region",
        "description": "Region geographique de l'unite operationnelle responsable du chantier",
        "type": "Texte",
        "obligatoire": True,
        "regle_qualite": "Doit correspondre a une region administrative francaise"
    },
    {
        "table": "unites_operationnelles",
        "colonne": "responsable",
        "nom_complet": "Responsable",
        "description": "Nom du responsable de l'unite operationnelle",
        "type": "Texte",
        "obligatoire": True,
        "regle_qualite": "Ne doit pas etre vide"
    },
]

df_catalogue = pd.DataFrame(catalogue)

print("=" * 60)
print("CATALOGUE DE DONNEES - BuildTrack")
print("=" * 60)
print(df_catalogue[["table", "colonne", "nom_complet", "type", "obligatoire"]].to_string(index=False))

df_catalogue.to_csv("catalog/catalogue.csv", index=False)

with open("catalog/catalogue.json", "w", encoding="utf-8") as f:
    json.dump