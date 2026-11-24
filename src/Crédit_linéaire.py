def crédit_linéaire(taux_fixe,capital,nb_mois):
    """calcul, pour chaque mois, la mensualité, le capital restant dû et les intérêts puis les affiche.
    taux_fixe : taux d'intérêt du prêt en pourcentage
    capital : montant initial dû en euros
    nb_mois : nombre de mois sur lequel le prêt est remboursé"""
    print(f"Calcul du crédit linéaire pour un capital de {capital} € sur {nb_mois} mois avec un taux fixe de {taux_fixe}%")
    taux_mensuel=taux_fixe/100/12
    capital_remboursé_mensuel=capital/nb_mois
    for mois in range(1,nb_mois+1):
        intérêts=capital*taux_mensuel
        mensualité=capital_remboursé_mensuel+intérêts
        capital-=capital_remboursé_mensuel
        print(f"Mois {mois}: Mensualité = {mensualité:.2f} €, Capital restant dû = {capital:.2f} €, Intérêts = {intérêts:.2f} €")
    return None
crédit_linéaire(5,100,3)
