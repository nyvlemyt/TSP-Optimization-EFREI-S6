"""
Module de résolution du problème du voyageur de commerce (TSP) avec PuLP et contraintes MTZ.

Ce module expose uniquement des fonctions robustes pour :
- construire un modèle TSP
- résoudre ce modèle
- extraire le chemin optimal
- afficher la solution de manière lisible

Les tests et utilisations doivent être réalisés ailleurs.
"""

import pulp
import pandas as pd
from typing import List, Tuple
from utils.logger import logger

def create_model(villes: List[str], matrix: pd.DataFrame) -> Tuple[pulp.LpProblem, dict, dict]:
    """
    Construit un modèle TSP en formulation MTZ.

    Args:
        villes (List[str]): Liste ordonnée des villes.
        matrix (pd.DataFrame): Matrice des distances symétriques entre les villes.

    Returns:
        Tuple contenant :
            - modèle PuLP (pulp.LpProblem)
            - variables x[i,j] pour les trajets
            - variables u[i] pour l'ordre de passage
    """
    try:
        n = len(villes)
        model = pulp.LpProblem("TSP", pulp.LpMinimize)

        x = pulp.LpVariable.dicts("x", ((i, j) for i in villes for j in villes if i != j), cat="Binary")
        u = pulp.LpVariable.dicts("u", villes, lowBound=0, upBound=n-1, cat="Continuous")

        # Fonction objectif : minimiser la distance totale
        model += pulp.lpSum(matrix.loc[i, j] * x[i, j] for (i, j) in x)

        # Contraintes de départ et d'arrivée
        for i in villes:
            model += pulp.lpSum(x[i, j] for j in villes if i != j) == 1
            model += pulp.lpSum(x[j, i] for j in villes if j != i) == 1

        # Contraintes MTZ pour éliminer les sous-tours
        for i in villes:
            for j in villes:
                if i != j and i != villes[0] and j != villes[0]:
                    model += u[i] - u[j] + n * x[i, j] <= n - 1

        logger.info("Modèle TSP construit avec succès.")
        return model, x, u

    except Exception as e:
        logger.exception(f"Erreur lors de la construction du modèle : {e}")
        raise

def solve_model(model: pulp.LpProblem) -> None:
    """
    Résout un modèle PuLP avec CBC en désactivant les messages solveur.

    Args:
        model (pulp.LpProblem): Modèle à résoudre.

    Raises:
        ValueError: Si la résolution échoue.
    """
    try:
        solver = pulp.PULP_CBC_CMD(msg=False)
        model.solve(solver)

        if pulp.LpStatus[model.status] != "Optimal":
            raise ValueError(f"Résolution échouée avec statut : {pulp.LpStatus[model.status]}")

        logger.success("Résolution optimale obtenue.")

    except Exception as e:
        logger.exception(f"Erreur lors de la résolution du modèle : {e}")
        raise

def extract_solution(x: dict, villes: List[str]) -> Tuple[List[str], List[Tuple[str, str]]]:
    """
    Extrait le chemin optimal à partir des variables de décision.

    Args:
        x (dict): Variables de décision (x[i,j]).
        villes (List[str]): Liste ordonnée des villes.

    Returns:
        Tuple contenant :
            - Liste ordonnée du chemin optimal (List[str])
            - Liste des arêtes sélectionnées (List[Tuple[str, str]])
    """
    try:
        edges = [(i, j) for (i, j) in x if pulp.value(x[i, j]) > 0.5]
        logger.info(f"Arêtes actives sélectionnées : {edges}")

        path = []
        visited = set()
        current = villes[0]
        path.append(current)
        visited.add(current)

        iterations = 0
        max_iterations = len(villes) + 5

        while len(visited) < len(villes):
            found = False
            for (start, end) in edges:
                if start == current and end not in visited:
                    path.append(end)
                    visited.add(end)
                    current = end
                    logger.debug(f"Étape {iterations}: {start} -> {end}")
                    found = True
                    break
            if not found:
                raise RuntimeError(f"Chemin bloqué à {current}. Chemin actuel: {path}")
            iterations += 1
            if iterations > max_iterations:
                raise RuntimeError("Trop d'itérations, boucle infinie détectée.")

        path.append(path[0])  # Retour à la ville de départ
        return path, edges

    except Exception as e:
        logger.exception(f"Erreur lors de l'extraction de la solution : {e}")
        raise

def display_solution(path: List[str], total_distance: float) -> None:
    """
    Affiche joliment la solution optimale dans un bloc structuré.

    Args:
        path (List[str]): Liste ordonnée des villes visitées.
        total_distance (float): Distance totale du chemin.
    """
    try:
        solution_text = (
            "\n========= SOLUTION TSP =========\n"
            f"Ordre optimal : {' -> '.join(path)}\n"
            f"Distance totale estimée : {total_distance:.2f} km\n"
            "================================\n"
        )
        logger.success(solution_text)

    except Exception as e:
        logger.exception(f"Erreur lors de l'affichage de la solution : {e}")
        raise