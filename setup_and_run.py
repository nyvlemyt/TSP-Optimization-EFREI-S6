
"""
Script pour configurer et exécuter automatiquement le projet TSP Optimization.
"""

import subprocess
import sys
import os

def create_virtualenv():
    """Crée un environnement virtuel si absent."""
    if not os.path.exists(".venv"):
        print("[INFO] Création de l'environnement virtuel...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"])
    else:
        print("[INFO] Environnement virtuel déjà présent.")

def install_dependencies():
    """Installe les dépendances nécessaires."""
    print("[INFO] Installation des dépendances...")
    subprocess.run([".venv/bin/pip", "install", "-r", "requirements.txt"])

def run_project():
    """Lance le projet."""
    print("[INFO] Lancement du projet...")
    subprocess.run([".venv/bin/python", "src/main.py"])

def main():
    """Orchestration de la mise en place."""
    create_virtualenv()
    install_dependencies()
    run_project()

if __name__ == "__main__":
    main()