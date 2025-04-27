"""
Script d'exécution pour résoudre un TSP avec PuLP sur un jeu de données personnalisé et visualiser le graphe.
"""

import pulp
from solver import create_model, solve_model, extract_solution, display_solution
from manage_data import generate_sample_distance_matrix, build_graph, plot_graph
from utils.logger import logger

def main() -> None:
    """Point d'entrée principal du script."""
    try:
        villes = [
            "Paris",
            "Lyon",
            "Marseille",
            "Toulouse",
            "Nantes",
            "Bordeaux",
            "Strasbourg",
            "Lille",
            "Nice",
            "Rennes",
            "Grenoble",
            "Montpellier",
            "Le Havre",
            "Nancy",
            "Dijon",
            #"Saint-Étienne",
            #"Angers",
            #"Nîmes",
            #"Villeurbanne",
            #"Saint-Denis",
            #"Aix-en-Provence",
            #"Clermont-Ferrand",
            #"La Rochelle",
            #"Saint-Paul",
            #"Saint-Pierre",
            #"Antibes",
            #"Brest",
            #"Limoges",
            #"Tours",
            #"Amiens",
            #"Perpignan",
            #"Metz",
            #"Besançon",
            #"Orléans",
            #"Rouen"
        ]
        matrix = generate_sample_distance_matrix(villes)

        # Construction et affichage du graphe initial
        G = build_graph(matrix)
        #plot_graph(G)

        model, x, u = create_model(villes, matrix)
        logger.info("Modèle construit, résolution en cours...")

        solve_model(model)

        if pulp.LpStatus[model.status] != "Optimal":
            logger.error(f"La résolution a échoué avec le statut : {pulp.LpStatus[model.status]}")
            return

        path, edges = extract_solution(x, villes)
        total_distance = pulp.value(model.objective)

        display_solution(path, total_distance)

        # Affichage du graphe avec le chemin optimal en rouge
        plot_graph(G, path=path, total_distance=total_distance)

    except Exception as e:
        logger.exception(f"Erreur lors de l'exécution du TSP : {e}")
        raise

if __name__ == "__main__":
    main()
