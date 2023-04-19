import pymongo
from pymongo import MongoClient
import streamlit as st
from dotenv import load_dotenv
import os

load_dotenv()

ATLAS_KEY=os.getenv('ATLAS_KEY')
# Create a MongoClient instance
client = MongoClient(ATLAS_KEY)

# Connect to the "imdb" database and "movies" collection
# db = client.imdb
# movies = db.movies

db = client.imdb
collection = db.movies
##################################################################
# st.title("")


# créer un formulaire de recherche par nom
st.sidebar.header("Search a movie by")
nom = st.sidebar.text_input("Title")
#############################################
# créer un formulaire de recherche par genre
# st.sidebar.header("Search by gendre")
genres = collection.distinct("genre")
genre_selectionne = st.sidebar.selectbox("Gendre", genres)

# effectuer une requête sur la base de données pour trouver les films correspondants
resultats = collection.find({"genre": genre_selectionne})
#############################################
# Get unique ratings from MongoDB
ratings = collection.distinct("score")

# Create menu list for rating selection
selected_rating = st.sidebar.selectbox("Rating", ratings)

# Query database for films with selected rating
results = collection.find({"rating": selected_rating})
###################################################
# créer un formulaire de recherche par actor
# st.sidebar.header("Search by actors")
nom = st.sidebar.text_input("Actors name")
###################################################
# Define Streamlit app
def app():
    # Get user input for duration threshold
    max_duration = st.slider("Select maximum duration (minutes)", min_value=0, max_value=300, step=5)

    # Query MongoDB for films with duration less than max_duration
    pipeline = [
        {"$match": {"duration": {"$lt": max_duration}}},
        {"$project": {"_id": 0, "title": 1, "duration": 1}}
    ]
    results = collection.aggregate(pipeline)

    # Display results
    st.write(f"Films with duration less than {max_duration} minutes:")
    for film in results:
        st.write(f"- {film['title']} ({film['duration']} minutes)")
#########################################################

# effectuer une requête sur la base de données pour trouver les films correspondants
resultats = collection.find({"nom": {"$regex": nom, "$options": "i"}})

# afficher les résultats de recherche
for resultat in resultats:
    st.write(f"Titre: {resultat['nom']}")
    st.write(f"Acteurs: {resultat['acteurs']}")
    st.write(f"Genre: {resultat['genre']}")
    st.write(f"Durée: {resultat['duree']}")
    st.write(f"Note: {resultat['note']}")
    st.image(resultat['miniature'])
    st.write(f"Lien vers la bande annonce: {resultat['lien_youtube']}")
