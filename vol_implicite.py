#importation des modules
import math
import numpy as np
from scipy.stats import norm

#entrée de caractéristiques de l'option
S0=float(input("entrez cour actuel de l'action : "))
T=float(input("entrez temps avant échéance (en année): "))
K=float(input("Prix fixé par l'option : "))
v0=float(input("entrez volatilité historique v0 au moment de l'émission : "))
r_=float(input("entrez taux sans risque : "))
P=float(input("entrez le prix de l'option affiché par la banque : "))
M=K/S0

#fonction B&S
def BS(M,t,v,r):
    D1=(np.log(1/M)+(r+np.square(v))*t)/(v*np.sqrt(t))
    D2=D1-v*(t)**0.5
    N_D1 = norm.cdf(D1)
    N_D2 = norm.cdf(D2)
    return (N_D1 - M * np.exp(-r*t) * N_D2)


#programme dichotomie


if BS(M,T,v0,r_)<P:
    #la volatilité implicite est > que la volatilité v0, v0 est minorant
    m=v0
    #recherche d'un majorant
    Ma=v0
    while BS(M,T,Ma,r_)<P:
        Ma+=1
        print (Ma)
        print (BS(M,T,Ma,r_))
    while abs(BS(M,T,Ma,r_)-BS(M,T,m,r_))>10**-5:
        h=(m+Ma)/2
        print (h)
        if BS(M,T,h,r_)<P:
            m=h
        else:
            Ma=h
    print ((m+Ma)/2)

else:
    #la volatilité implicite est < que v0, v0 est majorant
    Ma=v0
    #recherche d'un minorant
    m=v0
    while BS(M,T,m,r_)>P:
        m-=0.1
    while abs(BS(M,T,Ma,r_)-BS(M,T,m,r_))>10**-5:
        h=(m+Ma)/2
        if BS(M,T,h,r_)<P:
            m=h
        else:
            Ma=h
    print ((m+Ma)/2)
