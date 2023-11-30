# Delta Hedging d'une option
# Importation des modules
import requests  # Connexion à l'API de AlphaVantage
import schedule
import time
from scipy.stats import norm
import numpy as np

# Clé perso API AlphaVantage
key_API = 'LYMJQ6KR5QPKJ8W3'

# Caractéristiques de l'option
K = float(input("Entrez le strike : "))
equity = input("Entrez le nom de l'equity : ")
T = float(input("Entrez la maturité (en jours) : "))
r = float(input("Entrez le taux sans risque : "))  # Supposé constant
v = float(input("Entrez la volatilité : "))  # Supposée constante (très faux)

# Fonction de calcul de D1
def D1(S, T):
    return (((v * np.sqrt(T / 365)) ** -1) * (np.log(S / K) + (r + 0.5 * (v ** 2)) * (T / 365)))

# Initialisation
delta = 0
ex = True

# Fonction de calcul du delta quotidien
def calcul_delta():
    url = f'https://www.alphavantage.co/query?function=GLOBAL_QUOTE&symbol={equity}&apikey={key_API}'
    r = requests.get(url)
    data = r.json()

    # Accédez au sous-dictionnaire "Global Quote" dans les données
    global_quote = data['Global Quote']

    # Obtenez la valeur de "previous close"
    S = global_quote['08. previous close']
    S = float(S)
    delta_actuel = norm.cdf(D1(S, T))

    operation_buy_sell = max(0, delta_actuel) - delta  # on utilise max pour éviter les ventes à découvert
    if operation_buy_sell >= 0:
        print("Buy :", operation_buy_sell)
    else:
        print("Sell :", abs(operation_buy_sell))
    delta = max(0, delta_actuel)
    T -= 1  # Décrémentez T d'une journée

    # Test de sortie :
    if T <= 0:
        ex = False

# Automatisation du programme
schedule.every(1).day.do(calcul_delta)

while ex:
    schedule.run_pending()
    time.sleep(1)  # Pause d'une seconde, éviter que le programme boucle trop vite
