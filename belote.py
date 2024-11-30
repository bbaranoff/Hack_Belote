import numpy as np
import random

# Fonction pour résoudre les probabilités
def calcul_probabilites():
    coefficients = np.array([
        [1, 1, 1, 1],          # Somme des probabilités égale à 1
        [-2/3, 1, -1/3, 0],    # Équation pour P_00
        [0, -1/3, 1, -1/3],    # Équation pour P_01
        [-1/3, 0, -2/3, 1]     # Équation pour P_10
    ])
    rhs = np.array([1, 0, 0, 0])  # Côté droit des équations
    solutions = np.linalg.solve(coefficients, rhs)  # Résolution des équations linéaires
    return solutions

# Génération des cartes avec emojis pour les couleurs
def creer_jeu_de_cartes():
    couleurs = {"♥️": "Cœurs", "♦️": "Carreaux", "♣️": "Trèfles"}
    valeurs = {"A": "🂡", "10": "🔟", "K": "👑", "Q": "👸", "J": "🤵", "9": "9️⃣", "8": "8️⃣", "7": "7️⃣"}
    jeu = [f"{valeurs[valeur]} {couleur}" for couleur in couleurs for valeur in valeurs]
    return jeu

# Fonction pour prendre l'ordre des cartes en texte
def saisir_ordre_cartes(cartes):
    print("\nOptions pour l'ordre des cartes :")
    print("1. Conserver l'ordre actuel")
    print("2. Mélanger les cartes de manière aléatoire")
    print("3. Saisir un ordre personnalisé en texte")

    choix = input("Entrez votre choix (1, 2 ou 3) : ").strip()
    
    if choix == '3':  # Saisie d'un ordre personnalisé
        print("\nOrdre actuel des cartes (format '🂡 ♥️') :")
        print(' | '.join(cartes))
        
        print("\nEntrez le nouvel ordre en copiant-collant les cartes, séparées par ' | '.")
        try:
            nouvel_ordre = input("Nouvel ordre : ").strip().split(' | ')
            if len(nouvel_ordre) != len(cartes):
                print("❌ Entrée invalide. L'ordre sera conservé.")
                return cartes
            return nouvel_ordre
        except ValueError:
            print("❌ Entrée invalide. L'ordre sera conservé.")
            return cartes
    
    elif choix == '2':  # Mélange complet aléatoire
        random.shuffle(cartes)
        print("\nLes cartes ont été mélangées de manière aléatoire.")
        return cartes
    
    else:  # Conserver l'ordre actuel
        print("L'ordre actuel est conservé.")
        return cartes

# Fonction pour afficher les cartes horizontalement avec emojis
def afficher_cartes_horizontal(cartes, message):
    print(f"{message} : {' | '.join(cartes)}")

# Fonction pour simuler la distribution des cartes avec coupe et probabilités
def distribution_cartes_belote_avec_probas(probabilites):
    cartes = creer_jeu_de_cartes()
    cartes = saisir_ordre_cartes(cartes)  # Prendre l'ordre personnalisé ou aléatoire des cartes
    
    # Afficher l'ordre initial des cartes
    afficher_cartes_horizontal(cartes, "🔢 Ordre initial des cartes")

    n_joueurs = 4  # Nombre de joueurs
    joueurs = {f"Joueur {i+1}": [] for i in range(n_joueurs)}  # Dictionnaire pour les cartes des joueurs

    # Coupe influencée par les probabilités
    P_00, P_01, P_10, P_11 = probabilites
    choix_coupe = random.choices(['P_00', 'P_01', 'P_10', 'P_11'], weights=[P_00, P_01, P_10, P_11])[0]

    # Définir l'ordre des cartes après la coupe
    if choix_coupe == 'P_00':
        milieu = len(cartes) // 2
        cartes_coupees = cartes[milieu:] + cartes[:milieu]  # Coupe au milieu
    elif choix_coupe == 'P_01':
        cartes_coupees = cartes[::-1]  # Renverser complètement le paquet
    elif choix_coupe == 'P_10':
        cartes_coupees = cartes[:len(cartes)//2] + cartes[len(cartes)//2:]  # Garder l'ordre initial
    else:  # P_11
        random.shuffle(cartes)  # Mélanger complètement
        cartes_coupees = cartes

    # Afficher l'ordre des cartes après la coupe
    afficher_cartes_horizontal(cartes_coupees, "✂️ Ordre des cartes après la coupe")

    # Distribution des cartes
    index_carte = 0  # Index pour suivre la carte dans le paquet

    # Distribution de 2 cartes par joueur, puis 3 cartes par joueur
    for tour in range(2):  # Deux tours de distribution (2 cartes puis 3 cartes)
        for i in range(n_joueurs):  # Pour chaque joueur
            for j in range(2 + tour):  # Distribution de 2 cartes pour le 1er tour, puis 3 cartes pour le 2e
                carte = cartes_coupees[index_carte]  # Prendre la carte suivante dans le paquet coupé
                index_carte += 1  # Passer à la carte suivante
                joueurs[f"Joueur {i+1}"].append(carte)

    # Détection des belotes
    detecter_belote(joueurs)

    # Afficher les cartes distribuées à chaque joueur
    for joueur, cartes_joueur in joueurs.items():
        print(f"{joueur} a reçu les cartes : {', '.join(cartes_joueur)}")

    # Afficher le type de coupe effectuée
    print(f"\nCoupe effectuée basée sur l'état : {choix_coupe}")

# Fonction pour détecter la belote
def detecter_belote(joueurs):
    for joueur, cartes in joueurs.items():
        # Vérifier pour chaque couleur si la Reine et le Roi sont présents
        couleurs = ["♥️", "♦️", "♣️"]
        noms_couleurs = ["Cœurs", "Carreaux", "Trèfles"]
        for couleur, nom_couleur in zip(couleurs, noms_couleurs):
            if f"👸 {couleur}" in cartes and f"👑 {couleur}" in cartes:
                print(f"🔔 {joueur} a une belote dans la couleur {nom_couleur} !")

# Fonction principale combinée
def simulation_belote_et_probabilites():
    print("Calcul des probabilités...")
    P_00, P_01, P_10, P_11 = calcul_probabilites()
    print(f"Probabilités calculées : P_00={P_00:.2f}, P_01={P_01:.2f}, P_10={P_10:.2f}, P_11={P_11:.2f}")

    print("\nDistribution des cartes avec coupe influencée par les probabilités...")
    distribution_cartes_belote_avec_probas([P_00, P_01, P_10, P_11])

# Exécution de la simulation
simulation_belote_et_probabilites()
