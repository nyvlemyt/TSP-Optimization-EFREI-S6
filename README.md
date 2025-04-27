# 🧭 TSP Optimization – EFREI S6

Projet réalisé dans le cadre du cours **"Optimisation et Complexité"** à l'EFREI (S6 - informatique).  
Notre groupe a choisi de travailler sur le **problème du voyageur de commerce** (TSP - Traveling Salesman Problem).

---

# 🧐 Sujet choisi

Le TSP consiste à trouver le plus court chemin permettant à un vendeur de visiter une série de villes une seule fois chacune, puis de revenir à son point de départ.  
Ce problème est emblématique en algorithmique combinatoire et en recherche opérationnelle.

---

# 📌 Objectifs

Notre projet vise à :

- Définir précisément le problème du TSP
- Réaliser une revue de littérature synthétique
- Formaliser le problème mathématiquement
- Résoudre des instances du TSP de complexité croissante
- Analyser les performances des solutions proposées
- Créer une visualisation interactive du chemin optimal

---

# 🛠️ Technologies utilisées

- **Python 3.12+**
- **PuLP** : bibliothèque principale de modélisation linéaire pour la **résolution du TSP**.
- **DOcplex** : bibliothèque IBM utilisée pour **construire** et **modéliser** un TSP sous forme mathématique (partie architecture et modélisation uniquement).
- **NetworkX** : création de graphes pour représenter les villes et les trajets.
- **Matplotlib** : visualisation dynamique, boutons interactifs pour afficher/cacher le chemin optimal.
- **Visual Studio Code** + **venv** pour l'environnement de développement.

> **Note :**  
> Initialement, le projet devait utiliser uniquement **Docplex** avec IBM CPLEX pour tout résoudre, mais **l'impossibilité d'installer CPLEX sur Mac** a forcé l'adaptation vers **PuLP** pour la résolution automatique.  
> **Docplex est conservé** dans un module spécifique pour montrer la maîtrise de la modélisation avancée.

---

# 📦 Installation du projet

## 🔄 Méthode automatique recommandée

```bash
# Clonez le projet
git clone https://github.com/nyvlemyt/TSP-Optimization-EFREI-S6.git
cd TSP-Optimization-EFREI-S6

# Lancez le setup automatique
python setup_and_run.py
```

Cela crée l'environnement, installe les dépendances et lance directement le projet.

## 👉 Alternative manuelle

1. **Créer et activer l'environnement virtuel**

### Linux / macOS
```bash
python3 -m venv .venv
source .venv/bin/activate
```

### Windows (cmd)
```bash
python -m venv .venv
.venv\Scripts\activate.bat
```

### Windows (PowerShell)
```bash
python -m venv .venv
.venv\Scripts\Activate.ps1
```

2. **Installer les dépendances**
```bash
pip install -r requirements.txt
```

3. **Lancer le projet**
```bash
python src/main.py
```

---

# 🏢 Fonctionnalités principales

- Génération de données (liaison et distance) aléatoire
- Résolution du TSP par modélisation linéaire (formulation MTZ)
- Visualisation dynamique du graphe des villes
- Possibilité d'afficher / cacher le chemin optimal en appuyant sur un bouton

---

# 📅 Comment personnaliser le projet ?

## Ajouter / Retirer des villes

Dans `src/main.py`, modifiez simplement la liste des villes :

```python
villes = ["Paris", "Lyon", "Marseille", "Toulouse", "Nantes", "Bordeaux", "Strasbourg", "Lille", "Nice", "Montpellier"]
```

Le graphe, les distances et la résolution s'ajusteront automatiquement.

## Modifier les distances

Les distances sont générées automatiquement de façon cohérente avec `manage_data/generate_data.py`.  
Vous pouvez surcharger manuellement certaines distances dans le fichier si besoin.

---

# 📅 Structure du projet

```
TSP-Optimization-EFREI-S6/
├── data/                 # (optionnel) Données JSON éventuelles
├── manage_data/          # Création et visualisation de données
│   ├── prepare_data.py
│   ├── graph_plotter.py
├── solver/               # Résolution du TSP (PuLP)
│   ├── tsp_solver.py
│   ├── tsp_model.py
├── utils/                # Outils
│   ├── logger.py
├── src/                  # Dossier principal exécutable
│   ├── main.py
│   └── __init__.py
├── setup_and_run.py       # Script automatique
├── requirements.txt       # Dépendances
└── README.md
```

---

# 📄 Rapport & Présentation

- 📚 [Rapport du projet (PDF)](https://github.com/nyvlemyt/TSP-Optimization-EFREI-S6/blob/main/Rapport.pdf) 
- 🎮 [Présentation orale (PDF)](https://github.com/nyvlemyt/TSP-Optimization-EFREI-S6/blob/main/Presentation.pdf)

---

# 👥 Membres du groupe

- Melvyn
- Pierre
- Madavan


