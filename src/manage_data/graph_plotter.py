import pandas as pd
import networkx as nx
import matplotlib.pyplot as plt
from matplotlib.widgets import Button
from typing import List
import textwrap

from utils.logger import logger

def build_graph(distance_matrix: pd.DataFrame) -> nx.Graph:
    """
    Construit un graphe NetworkX à partir d'une matrice de distances.

    Args:
        distance_matrix (pd.DataFrame): Matrice des distances entre les villes.

    Returns:
        nx.Graph: Graphe NetworkX avec les villes en nœuds et les distances comme poids.
    """
    try:
        G = nx.Graph()

        for i in distance_matrix.index:
            for j in distance_matrix.columns:
                if i != j and distance_matrix.loc[i, j] != float('inf'):
                    G.add_edge(i, j, weight=distance_matrix.loc[i, j])

        logger.success(f"Graphe construit avec {G.number_of_nodes()} nœuds et {G.number_of_edges()} arêtes.")
        return G

    except Exception as e:
        logger.exception(f"Erreur lors de la construction du graphe : {e}")
        raise

def plot_graph(G: nx.Graph, path: List[str] = None, total_distance: float = None) -> None:
    """
    Affiche un graphe NetworkX, avec possibilité d'afficher/masquer le chemin optimal via un bouton.

    Caractéristiques :
    - Arêtes du graphe : gris clair avec les distances affichées.
    - Chemin optimal : arêtes rouges pointillées avec flèches directionnelles.
    - Description textuelle du chemin wrap automatique en haut du bouton.

    Args:
        G (nx.Graph): Graphe NetworkX représentant les villes et distances.
        path (List[str], optional): Liste ordonnée des villes formant le chemin optimal.
        total_distance (float, optional): Distance totale du chemin optimal.
    """
    try:
        pos = nx.spring_layout(G, seed=42)
        weights = nx.get_edge_attributes(G, 'weight')

        fig, ax = plt.subplots(figsize=(15, 10))
        plt.subplots_adjust(bottom=0.3)  # Plus de place pour plusieurs lignes

        # --- Dessiner le graphe initial ---
        nx.draw(
            G, pos, ax=ax,
            with_labels=True,
            node_size=700,
            node_color="skyblue",
            font_size=10,
            font_weight="bold",
            edge_color="gray",
            arrows=False
        )
        nx.draw_networkx_edge_labels(
            G, pos, ax=ax,
            edge_labels={k: f"{v:.0f}" for k, v in weights.items()},
            font_size=8
        )

        ax.set_title("Visualisation du réseau de villes", fontsize=14)
        ax.axis("off")

        # --- Gestion de l'affichage du chemin optimal ---
        if path:
            ax_button = plt.axes([0.4, 0.05, 0.2, 0.075])
            button = Button(ax_button, "Afficher / Cacher Chemin", color='lightgray', hovercolor='gray')

            displayed = {"value": False}
            drawn_edges = {"edges": None}
            text_annotation = {"text": None}

            def on_click(event):
                if not displayed["value"]:
                    # --- Afficher le chemin optimal ---
                    G_path = nx.DiGraph()
                    path_edges = [(path[i], path[i + 1]) for i in range(len(path) - 1)]
                    G_path.add_edges_from(path_edges)

                    drawn_edges["edges"] = nx.draw_networkx_edges(
                        G_path, pos, ax=ax,
                        edgelist=path_edges,
                        edge_color="red",
                        style="dashed",
                        width=3,
                        arrows=True,
                        arrowsize=20,
                        connectionstyle="arc3,rad=0.2"
                    )

                    # --- Afficher la description du chemin avec retour à la ligne ---
                    path_str = " -> ".join(path)
                    full_text = f"Chemin optimal : {path_str} (Distance totale : {total_distance:.0f} km)"

                    wrapped_text = "\n".join(textwrap.wrap(full_text, width=100))

                    text_annotation["text"] = fig.text(
                        0.5, 0.15,  # Placement plus haut pour éviter de gêner
                        wrapped_text,
                        ha='center', fontsize=12, color='red'
                    )

                    displayed["value"] = True

                else:
                    # --- Supprimer le chemin optimal et la description ---
                    if drawn_edges["edges"]:
                        for artist in drawn_edges["edges"]:
                            artist.remove()
                        drawn_edges["edges"] = None

                    if text_annotation["text"]:
                        text_annotation["text"].remove()
                        text_annotation["text"] = None

                    displayed["value"] = False

                plt.draw()

            button.on_clicked(on_click)

        plt.show()

    except Exception as e:
        logger.exception(f"Erreur lors de l'affichage du graphe : {e}")
        raise