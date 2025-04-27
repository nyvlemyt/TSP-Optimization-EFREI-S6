"""
Module de construction du modèle TSP avec Docplex.

Ce module fournit une fonction unique pour :
- créer un modèle TSP avec la méthode de Miller–Tucker–Zemlin (MTZ)
- intégrer les distances entre villes
- garantir l'absence de sous-tours

Aucun test n'est intégré ici : ce fichier est destiné à être importé.
"""

from docplex.mp.dvar import Var
from docplex.mp.model import Model
import pandas as pd
from typing import Dict, Tuple, List
from utils.logger import logger

def build_tsp_model(cities: List[str], distance_matrix: pd.DataFrame) -> Tuple[Model, Dict[Tuple[str, str], Var]]:
    """
    Construit un modèle de résolution du problème du voyageur de commerce (TSP) via Docplex.

    Args:
        cities (List[str]): Liste ordonnée des villes à parcourir.
        distance_matrix (pd.DataFrame): Matrice symétrique des distances entre les villes.

    Returns:
        Tuple contenant :
            - Le modèle Docplex prêt à être résolu (Model)
            - Un dictionnaire des variables de décision (x[i, j]) représentant les trajets
    """
    try:
        model = Model(name="TSP")

        # Variables de décision x[i,j] : 1 si le trajet i -> j est pris, sinon 0
        x = {(i, j): model.binary_var(name=f"x_{i}_{j}") for i in cities for j in cities if i != j}

        # Variables auxiliaires u[i] pour appliquer les contraintes MTZ (éliminer les sous-tours)
        u = {i: model.integer_var(lb=0, ub=len(cities) - 1, name=f"u_{i}") for i in cities}

        # Définir la fonction objectif : minimiser la distance totale
        model.minimize(
            model.sum(distance_matrix.loc[i, j] * x[i, j] for (i, j) in x)
        )

        # Contraintes de départ et d'arrivée uniques pour chaque ville
        for i in cities:
            model.add_constraint(
                model.sum(x[i, j] for j in cities if i != j) == 1,
                ctname=f"depart_{i}"
            )
            model.add_constraint(
                model.sum(x[j, i] for j in cities if i != j) == 1,
                ctname=f"arrivee_{i}"
            )

        # Contraintes MTZ : éviter les sous-cycles
        n = len(cities)
        for i in cities:
            for j in cities:
                if i != j and (i != cities[0] and j != cities[0]):
                    model.add_constraint(
                        u[i] - u[j] + n * x[i, j] <= n - 1,
                        ctname=f"mtz_{i}_{j}"
                    )

        logger.success(f"Modèle TSP construit avec {len(cities)} villes et {len(x)} variables.")
        return model, x

    except Exception as e:
        logger.exception(f"Erreur lors de la construction du modèle TSP avec Docplex : {e}")
        raise