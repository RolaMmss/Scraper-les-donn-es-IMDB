
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
###########################################################################
#Répondre aux questions suivantes en utilisant uniquement pymongo (l’objectif est d’apprendre la syntaxe pour intéragir avec un BDD MongoDB) :
###########################################################################

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
    # st.write(x,title)
    # st.write(dict_duration)
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
horror_movies = collection.find({"genre": "Horror"}).sort("rating", pymongo.DESCENDING).limit(3)
st.title("Top 3 Horror Movies:")
for movie in horror_movies:
    st.write(movie["title"])

# query for the top 3 drama movies based on rating
drama_movies = collection.find({"genre": "Drama"}).sort("rating", pymongo.DESCENDING).limit(3)
st.title("Top 3 Drama Movies:")
for movie in drama_movies:
    st.write(movie["title"])

# query for the top 3 comedy movies based on rating
comedy_movies = collection.find({"genre": "Comedy"}).sort("rating", pymongo.DESCENDING).limit(3)
st.title("Top 3 Comedy Movies:")
for movie in comedy_movies:
    st.write(movie["title"])
#########################################################
# 5. Parmi les 100 films les mieux notés, quel pourcentage sont américains ? Français ?
# trouver les 100 films les mieux notés
st.title("Parmi les 100 films les mieux notés, quel pourcentage sont américains ? Français")
top_rated = collection.find().sort("rating", -1).limit(100)# st.write(top_films)
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

# 6. Quel est la durée moyenne d’un film en fonction du genre ?

# # aggregate movies by genre and calculate average duration for each genre
# pipeline = [
#     {"$group": {"_id": "$genre", "avg_duration": {"$avg": "$duration"}}}
# ]

# result = db.movies.aggregate(pipeline)

# # print the result
# for genre in result:
#     st.write(f"The average duration of a movie in the {genre['_id']} genre is {genre['avg_duration']} minutes.")

# aggregate the data to find the average duration of a film by genre
# pipeline = [
#     {
#         "$group": {
#             "_id": "$genre",
#             "avg_duration": { "$avg": { "$sum": [ { "$multiply": [ { "$toInt": { "$arrayElemAt": [ { "$split": ["$duration", "h "] }, 0 ] } }, 60 ] }, { "$toInt": { "$arrayElemAt": [ { "$split": ["$duration", "h "] }, 1 ] } } ] } }
#         }
#     }
# ]

# result = db.films.aggregate(pipeline)

# # print the average duration of a film by genre
# if duration is not None:
#     for doc in result:
#         st.write(f"The average duration of a film in the '{doc['_id']}' genre is {doc['avg_duration']} minutes.")


def tranform_to_minutes(duration):
    if duration is not None:
        if len(duration.split()) == 2:
            x = int(duration.split()[0][0]) * 60 + int(duration.split()[1][0 : len(duration.split()[1])-1])
        elif duration.split()[0][-1] == 'h':
            x = int(duration.split('h')[0]) * 60
        elif duration.split()[0][-1] == 'm':
            x = int(duration.split('m')[0])
    return x
# # effectuer l'opération de groupement
# pipeline = [
#     {"$group": {"_id": "$genre", "duree_moyenne": {"$avg": "$duration"}}}
# ]

# resultats = list(collection.aggregate(pipeline))

# # afficher les résultats
# for resultat in resultats:
#     st.write(f"Genre : {resultat['_id']}, Durée moyenne : {resultat['duree_moyenne']}")



# effectuer l'opération de groupement
pipeline = [
    {"$addFields": {"duration_minutes": {"$function": {"body": f"{tranform_to_minutes}", "args": ["$duration"], "lang": "js"}}}},
    {"$group": {"_id": "$genre", "duree_moyenne": {"$avg": "$duration_minutes"}}}
]

resultats = list(collection.aggregate(pipeline))

# afficher les résultats
for resultat in resultats:
    st.write(f"Genre : {resultat['_id']}, Durée moyenne : {resultat['duree_moyenne']}")

