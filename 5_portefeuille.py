#Optimisation du ratio de Sharpe et Analyse de Composantes Principales (ACP)
#importation des modules 
import pandas as pd
import numpy as np
from sklearn.decomposition import PCA
from scipy.optimize import linprog

# Importation des données, valeurs des actifs
# Précisez le chemin utilisé
data = pd.read_csv("data.csv")

# Rendements journaliers (en %)
datareturns = data.pct_change(1)

# Centrage et réduction des données
from sklearn.preprocessing import StandardScaler
data_s = StandardScaler().fit_transform(datareturns)

# Modélisation de la composition de notre portefeuille en utilisant l'ACP
pca = PCA()
principal_components = pca.fit_transform(data_s)

# Meilleur vecteur propre (première composante principale)
best_poids = principal_components[:, 0]
best_poids /= np.sum(best_poids)

# Modélisons la performance par le ratio de Sharpe
sharpe = pd.DataFrame()
cycle_annuel = 252
nombre_annee = len(datareturns) // cycle_annuel
data_annuel = [datareturns[i:i+cycle_annuel] for i in range(0, len(datareturns), cycle_annuel)]

# Rendements annuels
annuel_returns = pd.DataFrame(data_annuel).mean() * cycle_annuel

# Volatilité annuelle
annuel_volatility = pd.DataFrame(data_annuel).std() * np.sqrt(cycle_annuel)

# Calcul du Ratio de Sharpe pour chaque année
for k in range(nombre_annee):
    sharpe[f"sharpe{k}"] = annuel_returns[k] / annuel_volatility[k]

# Facteur de variation (±15 %)
variation = 0.15

# Calcul des bornes en utilisant des opérations vectorielles
bornes_min = best_poids - variation * best_poids
bornes_max = best_poids + variation * best_poids

# Création d'un tableau de bornes
bornes = np.column_stack((bornes_min, bornes_max))

# Contraintes : somme des poids = 1
v1 = np.ones(nombre_annee)
v2 = [1]

# Optimisation sous contraintes, méthode simplex
poids_final = linprog(-sharpe, A_eq=[v1], b_eq=v2, bounds=bornes, method='simplex')

print("Volatilité du portefeuille (en %): ", 100 * np.dot(poids_final.x, annuel_volatility))
print("Performance annuelle du portefeuille (en %): ", 100 * np.dot(poids_final.x, annuel_returns))
