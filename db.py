from pymongo import MongoClient, errors

def connect_db():
    try:
        client = MongoClient("mongodb://localhost:27017/")
        db = client["web_scraping_db"]
        print("Connexion à la base de données MongoDB réussie.")
        return db
    except errors.ConnectionError as e:
        print(f"Erreur de connexion à MongoDB : {e}")
        return None

def format_date(date_string):
    try:
        months = {
            "janvier": "01", "février": "02", "mars": "03", "avril": "04",
            "mai": "05", "juin": "06", "juillet": "07", "août": "08",
            "septembre": "09", "octobre": "10", "novembre": "11", "décembre": "12"
        }
        parts = date_string.split()
        day = parts[0]
        month = months[parts[1].lower()]
        year = parts[2]
        return f"{year}-{month}-{day.zfill(2)}"
    except Exception as e:
        print(f"Erreur lors de la conversion de la date : {e}")
        return None

def store_articles_in_mongo(articles):
    print("Insertion des articles dans MongoDB...")
    try:
        db = connect_db()
        if db is None:
            return
        collection = db["articles"]

        collection.create_index("url", unique=True)

        for article in articles:
            try:
                article['date'] = format_date(article['date'])
                collection.insert_one(article)
                print(f"Article inséré : {article['title']}")
            except errors.DuplicateKeyError:
                print(f"Article déjà existant : {article['url']}")
    except Exception as e:
        print(f"Erreur lors de l'insertion dans MongoDB : {e}")