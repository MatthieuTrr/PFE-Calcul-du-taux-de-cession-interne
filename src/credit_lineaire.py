"""Credit a taux fixe amortissable lineairement et calcul de son TCI (adossement flux par flux)."""


def credit_lineaire(taux_fixe, capital_initial, nb_mois):
    """Calcule l'echeancier d'un credit a amortissement lineaire.

    taux_fixe : taux d'interet annuel du pret, en pourcentage (ex. 5 pour 5 %)
    capital_initial : montant emprunte, en euros
    nb_mois : nombre de mois sur lequel le pret est rembourse

    Renvoie une liste de dictionnaires, un par mois, avec :
    mois, crd_debut, interets, amortissement, mensualite, crd_fin
    (crd = capital restant du).
    """
    taux_mensuel = taux_fixe / 100 / 12
    amortissement = capital_initial / nb_mois
    echeancier = []
    for mois in range(1, nb_mois + 1):
        # Calcul a partir du capital initial pour eviter les erreurs d'arrondi (-0.00 €)
        crd_debut = capital_initial - (mois - 1) * amortissement
        crd_fin = capital_initial - mois * amortissement
        interets = crd_debut * taux_mensuel
        echeancier.append({
            "mois": mois,
            "crd_debut": crd_debut,
            "interets": interets,
            "amortissement": amortissement,
            "mensualite": amortissement + interets,
            "crd_fin": crd_fin,
        })
    return echeancier


def tci_naif(echeancier, courbe):
    """Calcule le TCI d'un credit taux fixe.

    Chaque remboursement de capital du mois i est vu comme une tranche financee
    par la tresorerie du mois 0 au mois i, au taux de marche de maturite i mois.

    echeancier : liste renvoyee par credit_lineaire
    courbe : liste des taux de marche annuels en pourcentage ;
             courbe[i - 1] est le taux de maturite i mois
             (ex. [2.0, 2.1, 2.2] : 1 mois = 2,0 %, 2 mois = 2,1 %, 3 mois = 2,2 %)

    Renvoie (tci en %, cout total du financement en euros).
    """
    if len(courbe) < len(echeancier):
        raise ValueError(
            f"La courbe contient {len(courbe)} taux, il en faut au moins {len(echeancier)} "
            "(un par mois de l'echeancier)."
        )

    # Cout reel du financement : chaque tranche x son taux de marche x sa duree (en annees)
    cout_financement = 0.0
    for ligne in echeancier:
        mois = ligne["mois"]
        taux_marche = courbe[mois - 1] / 100
        cout_financement += ligne["amortissement"] * taux_marche * mois / 12

    # Encours dans le temps : somme des capitaux restant dus x duree de chaque mois
    encours_temps = sum(ligne["crd_debut"] / 12 for ligne in echeancier)

    # TCI : taux unique qui, applique a l'encours, redonne le cout reel du financement
    tci = cout_financement / encours_temps * 100
    return tci, cout_financement


def afficher_resultats(taux_fixe, capital_initial, nb_mois, courbe):
    """Affiche l'echeancier, le TCI et la marge de l'agence."""
    echeancier = credit_lineaire(taux_fixe, capital_initial, nb_mois)

    print(f"Credit lineaire : {capital_initial} € sur {nb_mois} mois au taux fixe de {taux_fixe} %")
    for ligne in echeancier:
        print(f"Mois {ligne['mois']}: CRD debut = {ligne['crd_debut']:.2f} €, "
              f"Interets = {ligne['interets']:.2f} €, Mensualite = {ligne['mensualite']:.2f} €, "
              f"CRD fin = {ligne['crd_fin']:.2f} €")

    tci, cout_financement = tci_naif(echeancier, courbe)
    interets_client = sum(ligne["interets"] for ligne in echeancier)
    marge = interets_client - cout_financement

    print(f"\nCourbe de taux (mois 1 a {len(courbe)}) : {courbe}")
    print(f"Interets payes par le client  = {interets_client:.4f} €")
    print(f"Cout du financement           = {cout_financement:.4f} €")
    print(f"TCI                           = {tci:.4f} %")
    print(f"Marge de l'agence             = {marge:.4f} € (soit {taux_fixe - tci:.4f} %)")



afficher_resultats(taux_fixe=5, capital_initial=100, nb_mois=3, courbe=[2.0, 2.1, 2.2])

# Test : avec une courbe plate, le TCI doit etre egal au taux de la courbe
tci_plat, _ = tci_naif(credit_lineaire(5, 100, 3), [2.0, 2.0, 2.0])
assert abs(tci_plat - 2.0) < 1e-12, f"Test courbe plate echoue : TCI = {tci_plat}"
print("\nTest courbe plate : OK (TCI = 2 %)")