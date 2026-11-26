import pandas as pd

from src.donnees import charger_euribor


def interpoler_euribor(tableau, maturite_max=12):
    """Interpolation linéaire pour combler les trous dans la courbe Euribor.
    Permet  d'avoir les taux pour des maturités de 1 à 12 mois."""
    colonnes = range(1, maturite_max + 1)
    return tableau.reindex(columns=colonnes).interpolate(method="index", axis=1)


def charger_courbe(date, nb_mois, methode=interpoler_euribor, tableau=None):
    """Renvoie le courbe euribor pour une date donnée jusqu'à une maturité demandée."""
    if not 1 <= nb_mois <= 12:
        raise ValueError(f"nb_mois = {nb_mois} : l'Euribor ne va que de 1 a 12 mois.")

    if tableau is None:
        tableau = charger_euribor()

    periode = pd.Period(date, freq="M")
    if periode not in tableau.index:
        raise KeyError(f"Pas de donnees Euribor pour {periode}.")

    courbe_complete = methode(tableau, maturite_max=12)
    return courbe_complete.loc[periode, list(range(1, nb_mois + 1))].tolist()