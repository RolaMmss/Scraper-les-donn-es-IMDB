import pymongo
from pymongo import MongoClient
import streamlit as st
from dotenv import load_dotenv
import os
import pandas as pd

load_dotenv()

ATLAS_KEY=os.getenv('ATLAS_KEY')
# Create a MongoClient instance
client = MongoClient(ATLAS_KEY)

# Connect to the "imdb" database and "movies" collection
# db = client.imdb
# movies = db.movies

db = client.imdb
collection = db.movies

# Fonction pour chercher les films selon le titre
def search_by_title(title):
    results = collection.find({"title": {"$regex": title, "$options": "i"}})
    return list(results)

# Fonction pour chercher les films selon les acteurs
def search_by_actors(actors):
    results = collection.find({"actors": {"$in": actors}})
    return list(results)

# Fonction pour chercher les films selon le genre
def search_by_genre(genre):
    results = collection.find({"genre": {"$regex": genre, "$options": "i"}})
    return list(results)

# Fonction pour chercher les films selon la durée
def search_by_duration(duration):
    results = collection.find({"duration": {"$lt": duration}})
    return list(results)

# Fonction pour chercher les films selon le score
def search_by_score(score):
    results = collection.find({"score": {"$gte": score}})
    return list(results)

# Interface Streamlit pour chercher des films
st.title("Recherche de films")

# Recherche par titre
title = st.text_input("Titre du film")
if title:
    results = search_by_title(title)
    df = pd.DataFrame(results)
    st.dataframe(df)

# Recherche par acteurs
actors = st.multiselect("Acteurs", collection.distinct("actors"))
if actors:
    results = search_by_actors(actors)
    df = pd.DataFrame(results)
    st.dataframe(df)

# Recherche par genre
genre = st.text_input("Genre")
if genre:
    results = search_by_genre(genre)
    df = pd.DataFrame(results)
    st.dataframe(df)

# Recherche par durée
duration = st.number_input("Durée maximale (minutes)", value=120)
if duration:
    results = search_by_duration(duration)
    df = pd.DataFrame(results)
    st.dataframe(df)

# Recherche par score
score = st.slider("Note minimale", 0.0, 10.0, 5.0, 0.1)
if score:
    results = search_by_score(score)
    df = pd.DataFrame(results)
    st.dataframe(df)
