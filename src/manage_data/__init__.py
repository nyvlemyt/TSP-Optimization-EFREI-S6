"""
Package manage_data.

Contient les modules pour préparer les données de base et visualiser les graphes.
Expose les principales fonctions de préparation et d'affichage.
"""

from .generate_data import generate_sample_distance_matrix
from .graph_plotter import build_graph, plot_graph

__all__ = [
    "generate_sample_distance_matrix",
    "build_graph",
    "plot_graph",
]