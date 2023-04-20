import pymongo
from pymongo import MongoClient
import streamlit as st
from dotenv import load_dotenv
import os
# import pandas as pd

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
st.title("Best movies of all time")

# créer un formulaire de recherche par nom
st.sidebar.header("Search a movie by")
nom_title = st.sidebar.text_input("Title")
###################################################
# créer un formulaire de recherche par actor
# st.sidebar.header("Search by actors")
nom_actor = st.sidebar.text_input("Actors name")
#############################################
# créer un formulaire de recherche par genre
# st.sidebar.header("Search by gendre")
genres = collection.distinct("genre")
genre_selectionne = st.sidebar.selectbox("Gendre", genres)

# effectuer une requête sur la base de données pour trouver les films correspondants
results_genre = collection.find({"genre": genre_selectionne})
#############################################
# Get unique ratings from MongoDB
ratings = collection.distinct("score")

# Create menu list for rating selection
selected_rating = st.sidebar.selectbox("Rating", ratings)

# Query database for films with selected rating
results_rating = collection.find({"rating": selected_rating})
###################################################
def rechercher_par_duree(duree_max):
    resultats = collection.find({"duree": {"$lt": duree_max}})
    return resultats
# # def rechercher_par_note(note_min):
# #     resultats = collection.find({"note": {"$gte": note_min}})
# #     return resultats
# # st.title("Recherche de films")

# Recherche par durée
duree_max = st.sidebar.slider("Maximum duration(minutes)", min_value=0, max_value=300, step=30)
resultats_duree = rechercher_par_duree(duree_max)
# st.write("Résultats de la recherche par durée :")
for resultat in resultats_duree:
    st.write(resultat["title"])

# # Recherche par note
# note_min = st.slider("Note minimale", min_value=0.0, max_value=10.0, step=0.1)
# resultats_note = rechercher_par_note(note_min)
# st.write("Résultats de la recherche par note :")
# for resultat in resultats_note:
#     st.write(resultat["titre"])
#########################################################

# effectuer une requête sur la base de données pour trouver les films correspondants
# if nom_title is not None:
resultats_title = collection.find({"title": {"$regex": nom_title, "$options": "i"}})
# afficher les résultats de recherche
for resultat in resultats_title:
    st.write(f"Titre: {resultat['title']}")
    st.write(f"Acteurs: {resultat['actors']}")
    st.write(f"Genre: {resultat['genre']}")
    st.write(f"Durée: {resultat['duration']}")
    st.write(f"Note: {resultat['score']}")
    # st.image(resultat['miniature'])
    # st.write(f"Lien vers la bande annonce: {resultat['lien_youtube']}")
#########################################################
# # effectuer une requête sur la base de données pour trouver les films correspondants
# resultats_actor = collection.find({"actor": {"$regex": nom_actor, "$options": "i"}})

# # afficher les résultats de recherche
# for resultat in resultats_actor:
#     st.write(f"Titre: {resultat['title']}")
#     st.write(f"Acteurs: {resultat['actors']}")
#     st.write(f"Genre: {resultat['genre']}")
#     st.write(f"Durée: {resultat['duration']}")
#     st.write(f"Note: {resultat['score']}")
#     # st.image(resultat['miniature'])
    # st.write(f"Lien vers la bande annonce: {resultat['lien_youtube']}")
#     #########################################################
# # effectuer une requête sur la base de données pour trouver les films correspondants
# resultats_genre = collection.find({"genre": {"$regex": genre_selectionne, "$options": "i"}})

# # afficher les résultats de recherche
# for resultat in resultats_genre:
#     st.write(f"Titre: {resultat['title']}")
#     st.write(f"Acteurs: {resultat['actors']}")
#     st.write(f"Genre: {resultat['genre']}")
#     st.write(f"Durée: {resultat['duration']}")
#     st.write(f"Note: {resultat['score']}")
#     # st.image(resultat['miniature'])
#     # st.write(f"Lien vers la bande annonce: {resultat['lien_youtube']}")
# #########################################################################################################
# # effectuer une requête sur la base de données pour trouver les films correspondants
# resultats_score = collection.find({"score": {"$regex": selected_rating, "$options": "i"}})

# # afficher les résultats de recherche
# for resultat in resultats_score:
#     st.write(f"Titre: {resultat['title']}")
#     st.write(f"Acteurs: {resultat['actors']}")
#     st.write(f"Genre: {resultat['genre']}")
#     st.write(f"Durée: {resultat['duration']}")
#     st.write(f"Note: {resultat['score']}")
#     # st.image(resultat['miniature'])
#     # st.write(f"Lien vers la bande annonce: {resultat['lien_youtube']}")
# #########################################################################################################
# Recherche par acteurs
# # actors = st.multiselect("Acteurs", collection.distinct("actors"))
# actors = st.sidebar.text_input("Actors name")

# if actors:
#     # results = search_by_actors(actors)
#     results = collection.find({"actors": {"$in": actors}})
#     df = pd.DataFrame(results)
#     st.dataframe(df)
######################################################################
# # 1. Quel est le film le plus long ?
st.title('Longest movie')
dict_duration = {}
for document in collection.find():
    duration = document["duration"]
    title = document["title"]
    if duration is not None:
        if len(duration.split()) == 2:
            x = int(duration.split()[0][0]) * 60 + int(duration.split()[1][0 : len(duration.split()[1])-1])
        elif duration.split()[0][-1] == 'h':
            x = int(duration.split('h')[0]) * 60
        elif duration.split()[0][-1] == 'm':
            x = int(duration.split('m')[0])
        dict_duration[x] = title
st.write(f"The longest movie is {dict_duration[list(dict(sorted(dict_duration.items())).keys())[-1]]} with a duration of {list(dict(sorted(dict_duration.items())).keys())[-1]} minutes.")
##########################################################
# 2. Quels sont les 5 films les mieux notés ?

top_movies = collection.find().sort([("imdb.score", pymongo.DESCENDING)]).limit(5)

# imprimer les titres des 5 films les mieux notés
st.title('Top 5 highest-rated movies')
for movie in top_movies:
    st.write(movie["title"])
##########################################################
# 3. Dans combien de films a joué Morgan Freeman ? Tom Cruise ?
st.title('Movies Morgan Freeman has acted in')

# Count the number of movies in which Morgan Freeman has acted
morgan_freeman_movies = collection.count_documents({"actors": {"$in": ["Morgan Freeman"]}})
# display the movies Morgan Freeman has acted in with Streamlit

st.write("Morgan Freeman has acted in", morgan_freeman_movies, "movies.")

st.title('Movies Tom Cruise has acted in')

# Count the number of movies in which Tom Cruise has acted
tom_cruise_movies = collection.count_documents({"actors": {"$in": ["Tom Cruise"]}})
st.write("Tom Cruise has acted in", tom_cruise_movies, "movies.")
#########################################################
# 4. Quels sont les 3 meilleurs films d’horreur ? Dramatique ? Comique ?
# query for the top 3 horror movies based on rating
horror_movies = collection.find({"genre": "Horror"}).sort("score", pymongo.DESCENDING).limit(3)
st.title("Top 3 Horror Movies:")
for movie in horror_movies:
    st.write(movie["title"])

# query for the top 3 drama movies based on rating
drama_movies = collection.find({"genre": "Drama"}).sort("score", pymongo.DESCENDING).limit(3)
st.title("Top 3 Drama Movies:")
for movie in drama_movies:
    st.write(movie["title"])

# query for the top 3 comedy movies based on rating
comedy_movies = collection.find({"genre": "Comedy"}).sort("score", pymongo.DESCENDING).limit(3)
st.title("Top 3 Comedy Movies:")
for movie in comedy_movies:
    st.write(movie["title"])
#########################################################
# 5. Parmi les 100 films les mieux notés, quel pourcentage sont américains ? Français ?
# trouver les 100 films les mieux notés
st.title("What percentage of the top 100 rated films are American? French?")
top_rated = collection.find().sort("score", -1).limit(100)# st.write(top_films)
# count the number of American movies in the top 100
american_count = 0
for movie in top_rated:
    if movie["country"] == "United States":
        american_count += 1

# calculate the percentage of American movies in the top 100
american_percentage = american_count

st.write(f"{american_percentage:.2f}% of the top 100 movies are American.")

# count the number of French movies in the top 100
french_count = 0
for movie in top_rated:
    if movie["country"] == "France":
        french_count += 1

# calculate the percentage of French movies in the top 100
french_percentage = french_count

st.write(f"{french_percentage:.2f}% of the top 100 movies are French.")
###################################################################

# # 6. Quel est la durée moyenne d’un film en fonction du genre ?
# st.title("What is the average duration of a movie based on its genre?")

# # # aggregate movies by genre and calculate average duration for each genre
# # pipeline = [
# #     {"$group": {"_id": "$genre", "avg_duration": {"$avg": "$duration"}}}
# # ]

# # result = db.movies.aggregate(pipeline)

# # # print the result
# # for genre in result:
# #     st.write(f"The average duration of a movie in the {genre['_id']} genre is {genre['avg_duration']} minutes.")

# # aggregate the data to find the average duration of a film by genre
# # pipeline = [
# #     {
# #         "$group": {
# #             "_id": "$genre",
# #             "avg_duration": { "$avg": { "$sum": [ { "$multiply": [ { "$toInt": { "$arrayElemAt": [ { "$split": ["$duration", "h "] }, 0 ] } }, 60 ] }, { "$toInt": { "$arrayElemAt": [ { "$split": ["$duration", "h "] }, 1 ] } } ] } }
# #         }
# #     }
# # ]

# # result = db.films.aggregate(pipeline)

# # # print the average duration of a film by genre
# # if duration is not None:
# #     for doc in result:
# #         st.write(f"The average duration of a film in the '{doc['_id']}' genre is {doc['avg_duration']} minutes.")


# def tranform_to_minutes(duration):
#     if duration is not None:
#         if len(duration.split()) == 2:
#             x = int(duration.split()[0][0]) * 60 + int(duration.split()[1][0 : len(duration.split()[1])-1])
#         elif duration.split()[0][-1] == 'h':
#             x = int(duration.split('h')[0]) * 60
#         elif duration.split()[0][-1] == 'm':
#             x = int(duration.split('m')[0])
#     return x
# # # effectuer l'opération de groupement
# # pipeline = [
# #     {"$group": {"_id": "$genre", "duree_moyenne": {"$avg": "$duration"}}}
# # ]

# # resultats = list(collection.aggregate(pipeline))

# # # afficher les résultats
# # for resultat in resultats:
# #     st.write(f"Genre : {resultat['_id']}, Durée moyenne : {resultat['duree_moyenne']}")



# # effectuer l'opération de groupement
# pipeline = [
#     {"$addFields": {"duration_minutes": {"$function": {"body": f"{tranform_to_minutes}", "args": ["$duration"], "lang": "js"}}}},
#     {"$group": {"_id": "$genre", "duree_moyenne": {"$avg": "$duration_minutes"}}}
# ]

# resultats = list(collection.aggregate(pipeline))

# # afficher les résultats
# for resultat in resultats:
#     st.write(f"Genre : {resultat['_id']}, Durée moyenne : {resultat['duree_moyenne']}")


