def credit_lineaire(taux_fixe, capital_initial, nb_mois):
    """Calcul de l'échéancier du crédit linéaire taux fixe"""
    taux_mensuel = taux_fixe / 100 / 12
    amortissement = capital_initial / nb_mois
    echeancier = []
    for mois in range(1, nb_mois + 1):
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
    """Calcul du TCI pour le crédit linéaire taux fixe."""
    if len(courbe) < len(echeancier):
        raise ValueError(f"La courbe contient {len(courbe)} taux, il en faut {len(echeancier)}.")

    cout_financement = 0.0
    for ligne in echeancier:
        mois = ligne["mois"]
        taux_marche = courbe[mois - 1] / 100
        cout_financement += ligne["amortissement"] * taux_marche * mois / 12

    encours_temps = sum(ligne["crd_debut"] / 12 for ligne in echeancier)

    tci = cout_financement / encours_temps * 100
    return tci, cout_financement


def afficher_resultats(taux_fixe, capital_initial, nb_mois, courbe):
    """Affiche les résultats"""
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