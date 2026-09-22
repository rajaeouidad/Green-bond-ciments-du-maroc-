"""
================================================================================
ETUDE DE FAISABILITE D'UN GREEN BOND - CIMENTS DU MAROC
Pricing obligataire et calcul de duration
================================================================================

OBJECTIF
--------
Excel calcule bien le tableau de remboursement du Green Bond (coupon annuel,
remboursement in fine), mais ne calcule pas nativement deux informations
essentielles pour un investisseur ou un analyste marche des capitaux :

    1. Le PRIX theorique de l'obligation si le taux de marche (le rendement
       exige par les investisseurs) est different du coupon facial (4.0%)
    2. La DURATION : la sensibilite du prix de l'obligation a une variation
       des taux d'interet sur le marche

METHODE
-------
Le prix d'une obligation est la somme actualisee de tous ses flux futurs
(coupons + remboursement du capital), actualises au taux de rendement exige
par le marche (le "yield to maturity", note YTM).

    Prix = somme des [Coupon / (1+YTM)^t]  pour t = 1 a N
           + Nominal / (1+YTM)^N

Si YTM = coupon facial (4.0%) -> le prix = 100% du nominal (obligation "au pair")
Si YTM > coupon facial -> le prix < 100% (l'obligation se negocie "en dessous du pair")
Si YTM < coupon facial -> le prix > 100% (l'obligation se negocie "au dessus du pair")

La DURATION DE MACAULAY mesure la duree moyenne ponderee de recuperation des
flux. La DURATION MODIFIEE, derivee de la precedente, donne directement la
sensibilite du prix : "si le taux de marche bouge de 1%, le prix de
l'obligation bouge d'environ (duration modifiee) %."
"""

import numpy as np
import matplotlib.pyplot as plt

# ------------------------------------------------------------------------
# 1. CARACTERISTIQUES DU GREEN BOND (identiques au modele Excel)
# ------------------------------------------------------------------------
NOMINAL = 100          # on raisonne pour 100 MAD de nominal (= % du montant total)
COUPON_FACIAL = 0.04   # 4.0%, tel que construit par comparable OCP
MATURITE = 7           # ans


def prix_obligation(nominal, coupon_facial, maturite, ytm):
    """Calcule le prix d'une obligation in fine (bullet) pour un taux de
    marche (ytm) donne."""
    coupon_annuel = nominal * coupon_facial
    annees = np.arange(1, maturite + 1)
    flux = np.full(maturite, coupon_annuel)
    flux[-1] += nominal  # le dernier flux inclut le remboursement du capital
    prix = np.sum(flux / (1 + ytm) ** annees)
    return prix


def duration_macaulay(nominal, coupon_facial, maturite, ytm):
    """Calcule la duration de Macaulay (en annees) et la duration modifiee."""
    coupon_annuel = nominal * coupon_facial
    annees = np.arange(1, maturite + 1)
    flux = np.full(maturite, coupon_annuel)
    flux[-1] += nominal
    valeurs_actualisees = flux / (1 + ytm) ** annees
    prix = np.sum(valeurs_actualisees)
    duration_mac = np.sum(annees * valeurs_actualisees) / prix
    duration_mod = duration_mac / (1 + ytm)
    return duration_mac, duration_mod, prix


# ------------------------------------------------------------------------
# 2. PRIX DE L'OBLIGATION SELON DIFFERENTS SCENARIOS DE TAUX DE MARCHE
# ------------------------------------------------------------------------
scenarios_ytm = {
    "Marche exige 3.0% (detente des taux)": 0.030,
    "Marche exige 4.0% (= coupon facial, prix au pair)": 0.040,
    "Marche exige 5.0% (tension des taux)": 0.050,
    "Marche exige 6.0% (forte tension)": 0.060,
}

print("=" * 78)
print("PRIX DE L'OBLIGATION SELON LE TAUX EXIGE PAR LE MARCHE (YTM)")
print("=" * 78)
print(f"{'Scenario':<45}{'YTM':>8}{'Prix (% du nominal)':>25}")
for label, ytm in scenarios_ytm.items():
    prix = prix_obligation(NOMINAL, COUPON_FACIAL, MATURITE, ytm)
    print(f"{label:<45}{ytm*100:>7.1f}%{prix:>24.2f}%")

# ------------------------------------------------------------------------
# 3. DURATION AU TAUX DE REFERENCE (YTM = coupon facial = 4.0%)
# ------------------------------------------------------------------------
duration_mac, duration_mod, prix_ref = duration_macaulay(NOMINAL, COUPON_FACIAL, MATURITE, COUPON_FACIAL)

print("\n" + "=" * 78)
print("DURATION DU GREEN BOND (au taux de reference 4.0%)")
print("=" * 78)
print(f"Duration de Macaulay           : {duration_mac:.2f} annees")
print(f"Duration modifiee              : {duration_mod:.2f}")
print(f"Interpretation : une hausse de 1% des taux de marche ferait baisser")
print(f"le prix de l'obligation d'environ {duration_mod:.2f}%.")
print("=" * 78)

# ------------------------------------------------------------------------
# 4. GRAPHIQUE : SENSIBILITE DU PRIX AU TAUX DE MARCHE
# ------------------------------------------------------------------------
ytm_range = np.linspace(0.01, 0.09, 100)
prix_range = [prix_obligation(NOMINAL, COUPON_FACIAL, MATURITE, y) for y in ytm_range]

plt.figure(figsize=(10, 6))
plt.plot(ytm_range * 100, prix_range, color="#1565C0", linewidth=2.5)
plt.axhline(100, color="gray", linestyle=":", linewidth=1)
plt.axvline(COUPON_FACIAL * 100, color="red", linestyle="--", linewidth=1.5,
            label=f"Coupon facial ({COUPON_FACIAL*100:.1f}%) -> prix au pair")
plt.title("Sensibilite du prix du Green Bond au taux de marche (YTM)\nMaturite 7 ans, coupon 4.0%, remboursement in fine",
          fontsize=12, fontweight="bold")
plt.xlabel("Taux de marche exige (YTM, %)")
plt.ylabel("Prix de l'obligation (% du nominal)")
plt.legend()
plt.grid(alpha=0.3)
plt.tight_layout()
plt.savefig("bond_price_sensitivity.png", dpi=150)
print("\nGraphique enregistre : bond_price_sensitivity.png")
