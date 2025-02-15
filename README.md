# Network Scanner

Un scanner réseau avec interface TUI (Terminal User Interface) permettant de :
- Scanner les appareils sur le réseau
- Afficher les détails des appareils (IP, MAC, Vendor)
- Trier les résultats
- Naviguer dans les résultats avec les flèches

## Installation

```bash
# Cloner le dépôt
git clone https://github.com/votre-username/network_scanner.git
cd network_scanner

# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/Mac
# ou
.\venv\Scripts\activate  # Windows

# Installer les dépendances
pip install -r requirements.txt
```

## Utilisation

```bash
sudo python src/main.py -i <interface>
```

### Commandes disponibles
- `ctrl+r` : Rafraîchir le scan
- `ctrl+s` : Trier les résultats
- `↑` et `↓` : Naviguer dans les résultats
- `ctrl+t` : Changer le thème

## Dépendances
- textual
- netifaces