"""
================================================================================
ETUDE DE FAISABILITE D'UN GREEN BOND - CIMENTS DU MAROC
Simulation Monte Carlo complete : distribution + correlation + analyse tornado
================================================================================

----------------------------------------------------
1. Simulation Monte Carlo de la VAN du projet solaire (10 000 tirages),
   avec des variables incertaines correlees de facon realiste
2. Calcul des statistiques cles : VAN moyenne, probabilite de rentabilite
3. Analyse tornado : quelle variable influence le plus le resultat
4. Deux graphiques : distribution complete + tornado chart

METHODE GENERALE
-----------------
Plutot que de tester 3 scenarios fixes (Pessimiste/Central/Optimiste, comme
dans le modele Excel), on simule des milliers de combinaisons aleatoires et
realistes des hypotheses incertaines, pour obtenir une vraie distribution de
probabilite de la VAN, et identifier quelle variable merite le plus
d'attention pour reduire le risque du projet.
"""

import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------
# 1. HYPOTHESES FIXES (identiques au modele Excel, onglet ASSUMPTIONS)
# ------------------------------------------------------------------------
PUISSANCE_MW = 17          # Tafukt (10 MW) + Chems (7 MW)
CAPEX = 119                # MDH, cout d'installation (~7 DH/Wc)
OPEX_PCT = 0.015           # 1.5% du CAPEX / an (benchmark international)
DUREE_PROJET = 20          # annees
OPEX = CAPEX * OPEX_PCT    # = 1.8 MDH/an, fixe

# ------------------------------------------------------------------------
# 2. HYPOTHESES INCERTAINES (moyenne et dispersion documentees dans Excel)
# ------------------------------------------------------------------------
MOY_RENDEMENT, ECART_RENDEMENT = 1700, 90      # MWh/MW/an (comparables marocains)
MOY_PRIX, ECART_PRIX = 0.80, 0.08              # MAD/kWh (tarif industriel HT)
MOY_TAUX, ECART_TAUX = 0.08, 0.005             # WACC estime

N_SIMULATIONS = 10_000
rng = np.random.default_rng(seed=42)  # seed fixe = resultats reproductibles


def calcul_van(rendement, prix, taux):
    """Calcule la VAN du projet pour des valeurs donnees des 3 variables,
    avec la formule de la rente constante actualisee sur 20 ans."""
    production_mwh = rendement * PUISSANCE_MW
    economie_annuelle = production_mwh * 1000 * prix / 1_000_000
    cash_flow_net = economie_annuelle - OPEX
    facteur_annuite = (1 - (1 + taux) ** -DUREE_PROJET) / taux
    return -CAPEX + cash_flow_net * facteur_annuite


# ------------------------------------------------------------------------
# 3. SIMULATION AVEC CORRELATION REALISTE
# ------------------------------------------------------------------------
# Le prix de l'electricite et le taux d'actualisation sont partiellement
# lies (tous deux influences par l'inflation generale) : on modelise cette
# dependance avec une correlation moderee (rho = 0.5). Le rendement solaire
# reste independant (aucun lien economique avec l'inflation).

rho = 0.5
cov_matrix = [[ECART_PRIX ** 2, rho * ECART_PRIX * ECART_TAUX],
              [rho * ECART_PRIX * ECART_TAUX, ECART_TAUX ** 2]]

prix_et_taux = rng.multivariate_normal(
    mean=[MOY_PRIX, MOY_TAUX], cov=cov_matrix, size=N_SIMULATIONS
)
prix_electricite = np.clip(prix_et_taux[:, 0], 0.40, 1.50)
taux_actualisation = np.clip(prix_et_taux[:, 1], 0.05, 0.12)
rendement_solaire = np.clip(
    rng.normal(MOY_RENDEMENT, ECART_RENDEMENT, N_SIMULATIONS), 1200, 2200
)

van_simulee = calcul_van(rendement_solaire, prix_electricite, taux_actualisation)

# ------------------------------------------------------------------------
# 4. RESULTATS STATISTIQUES
# ------------------------------------------------------------------------
van_moyenne = np.mean(van_simulee)
van_mediane = np.median(van_simulee)
van_ecart_type = np.std(van_simulee)
van_p5 = np.percentile(van_simulee, 5)
van_p95 = np.percentile(van_simulee, 95)
proba_van_negative = np.mean(van_simulee < 0) * 100
correlation_obtenue = np.corrcoef(prix_electricite, taux_actualisation)[0, 1]

print("=" * 78)
print("RESULTATS DE LA SIMULATION MONTE CARLO (10 000 tirages, avec correlation)")
print("=" * 78)
print(f"Correlation prix/taux (cible 0.50)  : {correlation_obtenue:.2f}")
print(f"VAN moyenne                          : {van_moyenne:.2f} MDH")
print(f"VAN mediane                          : {van_mediane:.2f} MDH")
print(f"Ecart-type                           : {van_ecart_type:.2f} MDH")
print(f"Intervalle de confiance 90%          : [{van_p5:.2f} ; {van_p95:.2f}] MDH")
print(f"Probabilite que la VAN < 0           : {proba_van_negative:.2f} %")
print(f"Probabilite que le projet soit rentable (VAN > 0) : {100 - proba_van_negative:.2f} %")
print("=" * 78)

# ------------------------------------------------------------------------
# 5. ANALYSE TORNADO : IMPACT INDIVIDUEL DE CHAQUE VARIABLE
# ------------------------------------------------------------------------
van_centrale = calcul_van(MOY_RENDEMENT, MOY_PRIX, MOY_TAUX)

variables_test = {
    "Rendement solaire\n(MWh/MW/an)": (
        MOY_RENDEMENT - 1.2815 * ECART_RENDEMENT,
        MOY_RENDEMENT + 1.2815 * ECART_RENDEMENT, "rendement",
    ),
    "Prix electricite\n(MAD/kWh)": (
        MOY_PRIX - 1.2815 * ECART_PRIX,
        MOY_PRIX + 1.2815 * ECART_PRIX, "prix",
    ),
    "Taux d'actualisation\n(WACC)": (
        MOY_TAUX - 1.2815 * ECART_TAUX,
        MOY_TAUX + 1.2815 * ECART_TAUX, "taux",
    ),
}

resultats_tornado = []
for nom_variable, (val_basse, val_haute, type_var) in variables_test.items():
    if type_var == "rendement":
        van_basse = calcul_van(val_basse, MOY_PRIX, MOY_TAUX)
        van_haute = calcul_van(val_haute, MOY_PRIX, MOY_TAUX)
    elif type_var == "prix":
        van_basse = calcul_van(MOY_RENDEMENT, val_basse, MOY_TAUX)
        van_haute = calcul_van(MOY_RENDEMENT, val_haute, MOY_TAUX)
    else:  # taux : une hausse du taux fait BAISSER la VAN (relation inverse)
        van_basse = calcul_van(MOY_RENDEMENT, MOY_PRIX, val_haute)
        van_haute = calcul_van(MOY_RENDEMENT, MOY_PRIX, val_basse)
    resultats_tornado.append((nom_variable, van_basse, van_haute))

resultats_tornado.sort(key=lambda x: abs(x[2] - x[1]), reverse=True)

print("\nRESULTATS DE L'ANALYSE TORNADO (impact sur la VAN, classe par importance)")
print("-" * 78)
for nom, van_basse, van_haute in resultats_tornado:
    print(f"{nom.replace(chr(10), ' '):<35} VAN basse: {van_basse:>7.1f} MDH   VAN haute: {van_haute:>7.1f} MDH")

# ------------------------------------------------------------------------
# 6. GRAPHIQUES (distribution + tornado, cote a cote)
# ------------------------------------------------------------------------
fig, axes = plt.subplots(1, 2, figsize=(15, 6))

axes[0].hist(van_simulee, bins=80, color="#2E7D32", alpha=0.75, edgecolor="white")
axes[0].axvline(0, color="red", linestyle="--", linewidth=2, label="VAN = 0")
axes[0].axvline(van_moyenne, color="black", linewidth=2,
                 label=f"VAN moyenne = {van_moyenne:.1f} MDH")
axes[0].set_title("Distribution de la VAN\n(10 000 simulations, avec correlation prix/taux)", fontweight="bold")
axes[0].set_xlabel("VAN (MDH)")
axes[0].set_ylabel("Nombre de scenarios")
axes[0].legend()

noms = [r[0] for r in resultats_tornado]
van_basses = [r[1] - van_centrale for r in resultats_tornado]
van_hautes = [r[2] - van_centrale for r in resultats_tornado]
y_pos = np.arange(len(noms))

axes[1].barh(y_pos, van_hautes, left=van_centrale, color="#2E7D32", label="Scenario favorable (90e percentile)")
axes[1].barh(y_pos, van_basses, left=van_centrale, color="#C62828", label="Scenario defavorable (10e percentile)")
axes[1].axvline(van_centrale, color="black", linewidth=1.5, label=f"VAN centrale = {van_centrale:.1f} MDH")
axes[1].set_yticks(y_pos)
axes[1].set_yticklabels(noms)
axes[1].set_xlabel("VAN (MDH)")
axes[1].set_title("Analyse Tornado\nImpact individuel de chaque variable sur la VAN", fontweight="bold")
axes[1].legend(loc="lower right", fontsize=8)

plt.tight_layout()
plt.savefig("monte_carlo_resultats_complets.png", dpi=150)
print("\nGraphique enregistre : monte_carlo_resultats_complets.png")
