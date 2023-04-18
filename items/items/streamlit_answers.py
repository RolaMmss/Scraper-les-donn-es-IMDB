
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
db = client.imdb
movies = db.movies
###########################################################################
#Répondre aux questions suivantes en utilisant uniquement pymongo (l’objectif est d’apprendre la syntaxe pour intéragir avec un BDD MongoDB) :
###########################################################################

# 1. Quel est le film le plus long ?

##########################################################
# 2. Quels sont les 5 films les mieux notés ?

top_movies = movies.find().sort([("imdb.score", pymongo.DESCENDING)]).limit(5)

# imprimer les titres des 5 films les mieux notés
st.title('Top 5 movies')
for movie in top_movies:
    st.write(movie["title"])
st.write("#######################")
##########################################################
# 3. Dans combien de films a joué Morgan Freeman ? Tom Cruise ?
# Count the number of movies in which Morgan Freeman has acted
morgan_freeman_movies = movies.count_documents({"actors": {"$in": ["Morgan Freeman"]}})
st.write("Morgan Freeman has acted in", morgan_freeman_movies, "movies.")


# Count the number of movies in which Tom Cruise has acted
tom_cruise_movies = movies.count_documents({"actors": {"$in": ["Tom Cruise"]}})
st.write("Tom Cruise has acted in", tom_cruise_movies, "movies.")
