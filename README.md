# Green bond ciments du maroc
#  Étude de faisabilité d'un Green Bond Ciments du Maroc

**Financement d'un programme photovoltaïque (17 MW) par emprunt obligataire vert**

Étude financière complète combinant analyse d'entreprise, corporate finance, structuration obligataire, simulation probabiliste (Python) et visualisation interactive (Power BI), appliquée à un cas réel: le programme solaire Tafukt & Chems de Ciments du Maroc.

---

## Précision méthodologique

Ciments du Maroc n'a pas émis de green bond pour financer ce programme photovoltaïque l'entreprise l'a autofinancé. L'entreprise et le projet industriel étudiés ici sont **réels et sourcés**; l'émission obligataire analysée est une **hypothèse de travail** construite pour évaluer si un financement par green bond aurait constitué une alternative pertinente.

---

##  Résultats clés

| Indicateur | Valeur |
|---|---|
| Montant du Green Bond | 119 MDH |
| VAN du projet (scénario central) | 90,13 MDH |
| TRI du projet (scénario central) | 17 % |
| Probabilité de rentabilité (Monte Carlo, 10 000 simulations) | ≈ 100 % |
| CO₂ évité | ≈ 21 848 tonnes/an |
| Duration du Green Bond | 6,00 |
| Ratio Dette nette / EBITDA après émission | 0,126x |
| DSCR années 1-6 / année 7 (structure in fine)	4,47x / 0,17x |


**Recommandation : GO**, sous conditions de confirmation des hypothèses de production solaire et de prix de l'électricité (variables identifiées comme les plus déterminantes par l'analyse de sensibilité).

---

## Structure du projet

```
green-bond-ciments-maroc/
│
│
├── excel/
│   └── GREEN_BOND_MODEL.xlsx                  → Modèle financier complet (hypothèses, cash-flows, VAN/TRI, scénarios)
│
├── python/
│   ├── monte_carlo_final.py                   → Simulation Monte Carlo (10 000 tirages) + analyse Tornado
│   ├── bond_pricing.py                        → Pricing et duration du Green Bond
│   ├── monte_carlo_resultats_complets.png      → Graphique : distribution VAN + Tornado chart
│   └── bond_price_sensitivity.png              → Graphique : sensibilité du prix aux taux de marché
│
└── power-bi/
    └── Dashboard_GreenBond.pbix                → Tableau de bord interactif (KPIs, scénarios, curseur dynamique)
```

---

##  Méthodologie

1. **Analyse financière**  collecte et interprétation des données réelles de l'entreprise (rapports annuels 2022-2024), calcul des ratios de solvabilité
2. **Modélisation du projet**  hypothèses techniques documentées (production, coûts) à partir de comparables marocains réels
3. **Structuration obligataire**  construction du coupon et de la maturité par analogie avec une émission corporate marocaine comparable (OCP SA, déc. 2024)
4. **Valorisation** : calcul de la VAN et du TRI sur la durée de vie du projet (20 ans)
5. **Analyse de robustesse** : 3 scénarios (Excel) puis simulation Monte Carlo à 10 000 tirages avec corrélation entre variables (Python)
6. **Structuration obligataire avancée** : pricing théorique et duration de l'obligation (Python)
7. **Restitution** : tableau de bord interactif avec curseur de simulation en temps réel (Power BI)

Chaque hypothèse non directement observable dans les publications de l'entreprise a été construite à partir de comparables de marché documentés, avec traçabilité systématique des sources  le détail complet de cette méthodologie est disponible dans le rapport.

---

##  Outils utilisés

`Excel` (modélisation financière) · `Python` (NumPy, Matplotlib simulation Monte Carlo, pricing obligataire) · `Power BI` (DAX, dashboard interactif) · `Word` (rapport d'analyse)

---

##  À propos

Projet personnel réalisé dans le cadre de ma formation en 4ème année Finance (ENCG), pour approfondir les compétences en analyse financière, corporate finance, marché des capitaux et finance durable 

