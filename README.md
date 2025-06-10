# Web Scraping avec BeautifulSoup et MongoDB

## Description
Ce projet permet de scraper les articles du site [Blog du Modérateur](https://www.blogdumoderateur.com) en utilisant **BeautifulSoup** et de sauvegarder les données dans une base de données **MongoDB**. Une API Flask est également mise en place pour interagir avec les données, et un front-end simple permet de rechercher des articles selon différents critères.

---

## Fonctionnalités
1. **Scraping des articles** :
   - Titre de l'article
   - Image miniature principale
   - Catégorie
   - Résumé (extrait ou chapô)
   - Date de publication
   - Auteur de l'article
   - Contenu de l’article
   - Dictionnaire des images présentes dans l'article (URL et légende)

2. **Sauvegarde dans MongoDB** :
   - Les articles sont sauvegardés dans une collection appelée `articles`.
   - Les doublons sont évités grâce à un index unique sur le champ `url`.

3. **API Flask** :
   - Permet de rechercher des articles selon les critères suivants :
     - Catégorie
     - Auteur
     - Date de publication (début/fin)
     - Sous-chaîne dans le titre

4. **Front-end** :
   - Interface utilisateur simple en HTML et JavaScript.
   - Recherche dynamique des articles via l'API Flask.
   - Affichage des résultats sous forme de cartes Bootstrap.

---

## Prérequis
- **Python** (version 3.8 ou supérieure)
- **Docker** et **Docker Compose**
- **MongoDB** (via Docker)

---

## Installation

1. Clonez le dépôt :
   ```bash
   git clone https://github.com/noahrd0/bs4.git web-scraping-mongodb
   cd web-scraping-mongodb
   ```

2. Créez votre venv python :
   ```bash
   python3 -m venv venv_name
   source venv_name/bin/activate
   ```

3. Installez les dépendances :
   ```bash
   pip install -r requirements.txt
   ```

4. Lancez MongoDB avec Docker Compose :
   ```bash
   docker compose up -d
   ```

5. Exécutez le script de scraping pour récupérer les articles :
   ```bash
   python scrap.py
   python api.py
   ```

6. Accédez au front-end via votre navigateur :
   ```bash
   URL : http://127.0.0.1:5000
   ```

## Structure du projet
    web-scraping-mongodb/
    ├── scrap.py          # Script de scraping
    ├── api.py            # API Flask
    ├── db.py             # Gestion de la base MongoDB
    ├── index.html        # Front-end HTML
    ├── static/           # Dossier pour les fichiers statiques (JS, CSS)
    ├── docker-compose.yml # Configuration Docker Compose pour MongoDB
    ├── requirements.txt  # Dépendances Python
    ├── README.md         # Documentation du projet