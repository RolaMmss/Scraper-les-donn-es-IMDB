# Scraper-les-donn-es-IMDB
Vous êtes cinéphile et vous souhaitez vous créer une base de données personnelle pour rechercher vos films et séries préférés. 

#Description du projet

Le but de ce projet est de créer une base de données personnelle pour rechercher et stocker vos films et séries préférés en utilisant le framework Scrapy pour extraire les données disponibles en ligne sur des sites comme IMDb.com, puis stocker ces données dans une base de données NoSQL MongoDB. Enfin, vous pourrez créer une application avec Streamlit pour afficher vos résultats.

#Prérequis

    Python 3.9 ou supérieur
    Connaissance de base en Python et en HTML
    Installation de Scrapy, MongoDB et Streamlit

#Installation

    Cloner ce dépôt sur votre machine locale
    Installer les dépendances en exécutant pip install -r requirements.txt
    Installer MongoDB sur votre machine locale
    Configurer votre base de données MongoDB
    Exécuter le script Scrapy pour extraire les données en utilisant la commande scrapy crawl <nom_du_spider>
    Exécuter le script Python pour stocker les données dans MongoDB en utilisant la commande python store_data.py
    Exécuter l'application Streamlit pour afficher vos résultats en utilisant la commande streamlit run app.py

#Utilisation

    Pour extraire les données, vous pouvez modifier le spider Scrapy selon vos besoins
    Pour stocker les données, vous pouvez modifier le script Python selon vos besoins
    Pour afficher les résultats, vous pouvez modifier l'application Streamlit selon vos besoins
