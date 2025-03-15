import streamlit as st
import pickle
import pandas as pd
from PIL import Image
import base64
import os

# Load model and data
similarity_path = "similarity.pkl"
movies_path = "tmdb_5000_movies.csv"
logo_path = "innomatics-footer-logo.png"
background_path = "background.jpg"  # Optional background image

def load_data():
    with open(similarity_path, 'rb') as file:
        similarity = pickle.load(file)
    movies_df = pd.read_csv(movies_path)
    return movies_df, similarity

movies_df, similarity = load_data()

# Streamlit App Configuration
st.set_page_config(page_title="🎬 Movie Recommendation System", page_icon="🍿", layout="wide")

# Custom CSS for Background & Centering Content
def set_background():
    if os.path.exists(background_path):  # Check if background image exists
        with open(background_path, "rb") as file:
            encoded_string = base64.b64encode(file.read()).decode()
        bg_style = f"""
        <style>
            .stApp {{
                background: url(data:image/jpeg;base64,{encoded_string});
                background-size: cover;
                background-position: center;
            }}
        </style>
        """
    else:  # Use gradient background if no image is found
        bg_style = """
        <style>
            .stApp {
                background: linear-gradient(135deg, #1f1c2c, #928DAB);
                color: white;
                text-align: center;
            }
            h1, h2, h3, h4 {
                color: #FFC107;
                text-align: center;
            }
            .stSelectbox, .stButton > button {
                background-color: #FFC107 !important;
                color: black !important;
                border-radius: 10px;
                display: flex;
                justify-content: center;
                margin: auto;
            }
            .center-content {
                background-color: #FFF;
                color: black;
                text-align: center;
                display: flex;
                justify-content: center;
                margin: auto;
                padding: 20px;
                width: 500px;
                border-radius: 12px;
                box-shadow: 2px 2px 20px rgba(0,0,0,0.2);
                font-size: 18px;
                line-height: 1.6;
            }
            .stSelectbox, .stButton > button {
                display: flex;
                margin: 10px;
            }
            .center-logo {
                display: flex;
                justify-content: center;
                align-items: center;
                padding: 20px;
                margin:10px;
            }
            .center-logo img {
                max-width: 1000px;
                height: auto;
            }
            .movie-list {
                text-align: center;
                font-size: 18px;
                font-weight: bold;
            }
        </style>
        """
    
    st.markdown(bg_style, unsafe_allow_html=True)

set_background()

# Header Section (Larger Centered Logo)
logo = Image.open(logo_path)
st.markdown('<div class="center-logo"><img src="data:image/png;base64,' + 
            base64.b64encode(open(logo_path, "rb").read()).decode() + 
            '"/></div>', unsafe_allow_html=True)

st.title("🍿 Movie Recommender 🎥")
st.markdown('<div class="center-content">🔍 Discover Your Next Favorite Movie! 🌟</div>', unsafe_allow_html=True)

# About the Project
st.subheader("📌 About the Project 🎬")
st.markdown('<div class="center-content">🤖 This project develops a content-based movie recommendation system that utilizes a dataset containing a variety of movie features. By analyzing attributes like genres, directors, cast, and plot descriptions, the system provides personalized movie recommendations based on user preferences. The objective is to suggest movies that align with user tastes and explore the relationships between different features for improved recommendations ! 🎞️💡</div>', unsafe_allow_html=True)

# Business Problem
st.subheader("💡 Business Problem ❓")
st.markdown('<div class="center-content">📺 With thousands of movies available across streaming platforms, finding the right movie to watch can be overwhelming! This system helps users discover movies they are most likely to enjoy based on their preferences. 🧐🎥</div>', unsafe_allow_html=True)

# Business Objective
st.subheader("🎯 Business Objective 🏆")
st.markdown('<div class="center-content">🎯 The goal is to enhance user experience by recommending relevant movies based on past preferences, boosting user engagement, and ensuring an exciting movie-watching journey! 🍿🔥</div>', unsafe_allow_html=True)

# Business Constraints
st.subheader("⚠ Business Constraints 🚧")
st.markdown("""
<div class="center-content">
- ⚡ Fast and real-time recommendations 🕒  
- 📈 Scalability to handle large movie datasets 📊  
- 🎞️ Accurate and up-to-date movie information 🎬  
</div>
""", unsafe_allow_html=True)

# Select Movie (Centered Dropdown)
movie_list = movies_df['title'].values
title = st.selectbox("🎬 Choose a Movie to Get Recommendations:", movie_list, key="movie_select")

# Recommendation Function
def recommend(movie):
    index = movies_df[movies_df['title'] == movie].index[0]
    distances = similarity[index]
    movie_indices = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = [(movies_df.iloc[i[0]].title, movies_df.iloc[i[0]].vote_average, movies_df.iloc[i[0]].vote_count) for i in movie_indices]
    return recommended_movies

# Display Recommendations (Centered)
if st.button("🍿 Get Movie Recommendations! 🎥"):
    recommendations = recommend(title)
    st.subheader("📌 Recommended Movies Just for You! 🎞️✨")
    st.markdown('<div class="center-content">', unsafe_allow_html=True)
    for i, (movie, rating, votes) in enumerate(recommendations, 1):
        st.markdown(f"<div class='movie-list'>{i}. 🎬 {movie} (⭐ {rating}/10, {votes} votes) 🍿</div>", unsafe_allow_html=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Footer (Centered)
st.markdown("---")
st.markdown('<div class="center-content">© 2025 Movie Recommender | 🎥 Your Personalized Movie Guide! 🍿</div>', unsafe_allow_html=True)  
