"""
Module pour générer un ensemble de données de distances complètes entre des villes.
Utilisé pour tester la résolution du TSP avec un graphe dense.
"""

import pandas as pd
import random
from typing import List

from utils.logger import logger

def generate_sample_distance_matrix(
    villes: List[str], min_dist: int = 100, max_dist: int = 1000
) -> pd.DataFrame:
    """
    Génère une matrice de distances symétrique pour un ensemble de villes.

    Args:
        villes (List[str]): Liste des villes.
        min_dist (int, optional): Distance minimale entre deux villes. Default à 100.
        max_dist (int, optional): Distance maximale entre deux villes. Default à 1000.

    Returns:
        pd.DataFrame: Matrice de distances symétrique.
    """
    try:
        if not villes or len(villes) < 2:
            raise ValueError("La liste des villes doit contenir au moins deux éléments.")

        n = len(villes)
        matrix = pd.DataFrame(float("inf"), index=villes, columns=villes)

        for i in range(n):
            for j in range(i + 1, n):
                dist = random.randint(min_dist, max_dist)
                matrix.iloc[i, j] = dist
                matrix.iloc[j, i] = dist

        logger.success(f"Matrice de distances générée avec {n} villes.")
        return matrix

    except Exception as e:
        logger.exception(f"Erreur lors de la génération de la matrice de distances : {e}")
        raise

