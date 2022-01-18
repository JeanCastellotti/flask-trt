# Guide

## Documentation technique
Vous trouverez la documentation technique à la racine du dépôt Github. 

## Manuel d'utilisation
Vous trouverez le manuel d'utilisation à la racine du dépôt Github.

## Déploiement en local
Avant tout, il faut que Python (3.9+) et PostgreSQL soient installés. Si ce n'est pas déjà fait, vous pouvez les installer sur macOS via [Homebrew](https://formulae.brew.sh) ou directement depuis les sites officiels respectifs.

Cloner le projet :

```bash
git clone https://github.com/JeanDevFR/flask-trt
```

Se rendre dans le répertoire du projet :

```bash
cd flask-trt
```

Créer un environnement virtuel :

```bash
# macOS
python3 -m venv venv

# Windows
py -3 -m venv venv
```

Activer l'environnement virtuel :

```bash
# macOS
. venv/bin/activate

# Windows
venv/Scripts/activate
```

Installer les packages :

```bash
pip install -r requirements.txt
```

Créer un fichier .env avec les informations suivantes :

```bash
SECRET_KEY = "secret"
DATABASE_URL = "postgresql://<username>:<password>@localhost:5432/<db-name>"
```

Modifier les informations suivantes dans le fichier config.py en fonction du serveur smtp que vous utilisez :

```python
# ...
MAIL_SERVER = 'smtp.gmail.com'
MAIL_PORT = 465 # Ou 587 par exemple
# ...
MAIL_USE_TLS = False
MAIL_USE_SSL = True
```

Créer la base de données :

```bash
CREATE DATABASE <db-name>;
```

Créer les tables :

```bash
cd flask-trt
flask db upgrade
```

Lancer l'application :
```bash
flask run
```

Créer un administrateur :
```bash
# Un seul administrateur peut être créé. Conservez-bien son mot de passe.
http://localhost:5000/admin/create/administrator
```