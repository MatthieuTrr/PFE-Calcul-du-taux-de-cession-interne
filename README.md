# PFE : Calcul du taux de cession interne (TCI)

Projet de fin d'études, Polytech Nice Sophia, MAM5 (co-projet n°2).

**Équipe :** Robin Miconi, Petru Piculescu, Matthieu Terrier
**Encadrant :** Zakaria Kardou
**Période :** du 23/11/2026 au 07/02/2027

---

## Contexte

Le **taux de cession interne (TCI)** est le taux auquel la trésorerie centrale d'une banque « prête » les ressources aux agences qui accordent des crédits, ou « rémunère » les agences qui collectent des dépôts.

Il sert à :

- **calculer la marge réelle** d'un produit, une fois retiré le coût de son financement ;
- **comparer les agences** en séparant la performance commerciale des effets de taux et de liquidité ;
- **valoriser l'épargne collectée**, surtout lorsqu'elle est stable ;
- **centraliser les risques** de taux et de liquidité à la trésorerie.

Exemple : un crédit de 100 000 € accordé à 4 %, financé par la trésorerie avec un TCI de 3 %, donne une marge commerciale de 1 %, soit 1 000 € par an.

## Objectif

Calculer le TCI du **Livret A**, en procédant par étapes :

1. **Crédit à taux fixe** à amortissement linéaire : construction de l'échéancier (capital restant dû, intérêts, mensualités).
2. **TCI du crédit à taux fixe** : adossement de l'encours à la courbe des taux de marché.
3. **TCI d'un crédit à taux variable** : calcul du TCI pour un produit un peu plus complexe.
4. **Livret A** : séparation de l'encours en une part volatile et une part stable écoulée par strates, puis calcul du TCI du stock et de la production nouvelle, et enfin leur moyenne pondérée.
5. **Validation** : comparaison avec un crédit fictif indexé sur le Livret A, avec des spreads fictifs.

## Structure du dépôt

```
.
├── src/                 # Code source du projet
│   └── credit_lineaire.py   # Échéancier d'un crédit à taux fixe amortissable linéairement
├── data/                # Séries de données (voir « Données » ci-dessous)
├── notebooks/           # Explorations et graphiques
├── docs/                # Comptes rendus de réunion et présentations
└── README.md
```

*Structure amenée à évoluer au fil du projet.*

## Installation

Python 3.10 ou plus récent.

```bash
git clone <url-du-depot>
cd <nom-du-depot>
pip install -r requirements.txt   # quand le fichier sera ajouté (pandas, numpy, matplotlib…)
```

## Utilisation

Exemple : échéancier d'un crédit de 100 € à 5 % sur 3 mois.

```bash
python credit_lineaire.py
```

```
Mois 1: CRD début = 100.00 €, Intérêts = 0.42 €, Mensualité = 33.75 €, CRD fin = 66.67 €
Mois 2: CRD début = 66.67 €, Intérêts = 0.28 €, Mensualité = 33.61 €, CRD fin = 33.33 €
Mois 3: CRD début = 33.33 €, Intérêts = 0.14 €, Mensualité = 33.47 €, CRD fin = 0.00 €
```

## Données

| Série | Usage | Source |
|---|---|---|
| Encours mensuels du Livret A | Modélisation de l'écoulement | Banque de France (Webstat) |
| Taux du Livret A | Rémunération versée au client | Banque de France |
| Euribor 1 mois | Taux de la part volatile | EMMI |

Les données Euribor sont soumises aux conditions d'utilisation d'EMMI. Elles ne sont pas redistribuées dans ce dépôt : chacun les télécharge depuis la source.

## Avancement

- [x] Définition du TCI et cadrage
- [x] Échéancier d'un crédit à taux fixe linéaire
- [ ] TCI d'un crédit à taux fixe
- [ ] Collecte et nettoyage des données (Banque de France, EMMI)
- [ ] Modèle d'écoulement du Livret A
- [ ] TCI du Livret A (stock et production nouvelle)
- [ ] Vérification des résultats
- [ ] Rédaction des rendus et soutenance

## Références

- Demey, Frachot, Riboulet, *Introduction à la gestion actif-passif bancaire*, Economica
- Bessis, *Risk Management in Banking*, Wiley
- CEBS/EBA, *Guidelines on Liquidity Cost Benefit Allocation* (2010)
- Commission bancaire, *Livre blanc sur la rentabilité* (1998)
- Banque de France, *Rapport annuel sur l'épargne réglementée*

## Licence

Voir le fichier [LICENSE](LICENSE).
