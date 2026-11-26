from pathlib import Path

import pandas as pd

DOSSIER_DATA = Path(__file__).resolve().parent.parent / "data"

FICHIERS_EURIBOR = {
    1: "euribor_1m.csv",
    3: "euribor_3m.csv",
    6: "euribor_6m.csv",
    12: "euribor_12m.csv",
}


def lire_serie_bce(chemin):
    """Lecture des taux Euribor téléchargés depuis la BCE"""
    df = pd.read_csv(chemin)
    serie = pd.Series(
        pd.to_numeric(df["OBS_VALUE"], errors="coerce").values,
        index=pd.PeriodIndex(df["TIME_PERIOD"].astype(str), freq="M"),
    )
    return serie.dropna().sort_index()


def fusionner_euribor(fichiers=FICHIERS_EURIBOR, dossier=DOSSIER_DATA, sortie="euribor_data.csv"):
    """Fusion des fichiers CSV en un seul dataset .CSV"""
    series = {mat: lire_serie_bce(Path(dossier) / nom) for mat, nom in fichiers.items()}
    tableau = pd.DataFrame(series).dropna().sort_index()
    tableau.index.name = "date"

    chemin_sortie = Path(dossier) / sortie
    tableau.to_csv(chemin_sortie)
    print(f"{len(tableau)} mois enregistres dans {chemin_sortie} "
          f"({tableau.index.min()} -> {tableau.index.max()})")
    return tableau


def charger_euribor(dossier=DOSSIER_DATA, nom="euribor_data.csv"):
    """Renvoie le tableau des données brut Euribor"""
    tableau = pd.read_csv(Path(dossier) / nom, index_col="date")
    tableau.index = pd.PeriodIndex(tableau.index, freq="M")
    tableau.columns = [int(c) for c in tableau.columns]
    return tableau


if __name__ == "__main__":
    fusionner_euribor()