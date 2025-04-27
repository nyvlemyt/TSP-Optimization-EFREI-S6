"""
Script pour configurer et exécuter automatiquement le projet TSP Optimization sur Windows, macOS et Linux.
"""

import subprocess
import sys
import os
import platform

def create_virtualenv():
    """Crée un environnement virtuel s'il n'existe pas."""
    if not os.path.exists(".venv"):
        print("[INFO] Création de l'environnement virtuel...")
        subprocess.run([sys.executable, "-m", "venv", ".venv"], check=True)
    else:
        print("[INFO] Environnement virtuel déjà existant.")

def install_dependencies(pip_path: str):
    """Installe les dépendances du projet."""
    print("[INFO] Installation des dépendances...")
    subprocess.run([pip_path, "install", "-r", "requirements.txt"], check=True)

def run_project(python_path: str):
    """Exécute le projet principal."""
    print("[INFO] Lancement du projet...")
    subprocess.run([python_path, "src/main.py"], check=True)

def main():
    """Orchestre toute la mise en place et l'exécution."""
    # Détecte l'OS pour choisir les bons chemins
    os_type = platform.system()

    if os_type == "Windows":
        pip_path = os.path.join(".venv", "Scripts", "pip.exe")
        python_path = os.path.join(".venv", "Scripts", "python.exe")
    else:  # Linux ou Darwin (macOS)
        pip_path = os.path.join(".venv", "bin", "pip")
        python_path = os.path.join(".venv", "bin", "python")

    create_virtualenv()
    install_dependencies(pip_path)
    run_project(python_path)

if __name__ == "__main__":
    main()