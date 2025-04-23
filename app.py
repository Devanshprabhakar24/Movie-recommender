import streamlit as st
import pandas as pd
import pickle
import requests

# ------------------ Load Data ------------------
movies_dict = pickle.load(open('movies_dict.pkl', 'rb'))
movies = pd.DataFrame(movies_dict)
similarity = pickle.load(open('similarity.pkl', 'rb'))

# ------------------ Fetch Poster ------------------
def fetch_poster(movie_id):
    url = f"https://api.themoviedb.org/3/movie/{movie_id}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US"
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path', '')
    full_path = "https://image.tmdb.org/t/p/w500/" + poster_path if poster_path else ""
    return full_path

# ------------------ Recommend Movies ------------------
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]
    recommended_movies = []
    recommended_posters = []
    for i in movie_list:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_posters.append(fetch_poster(movie_id))
    return recommended_movies, recommended_posters

# ------------------ Streamlit App ------------------
st.set_page_config(page_title="Movie Recommender", layout="wide")
st.title('🎬 Movie Recommender System')

# Initialize session state for Hollywood and Bollywood buttons
if "show_hollywood" not in st.session_state:
    st.session_state.show_hollywood = False

if "show_bollywood" not in st.session_state:
    st.session_state.show_bollywood = False

# Handle Hollywood Button Click
if st.button("🍿 Hollywood"):
    st.session_state.show_hollywood = True  # Set session state to show Hollywood movies
    st.session_state.show_bollywood = False  # Reset Bollywood state

# Handle Bollywood Button Click
if st.button("🎥 Bollywood"):
    st.session_state.show_bollywood = True  # Set session state to show Bollywood message
    st.session_state.show_hollywood = False  # Reset Hollywood state
    st.warning("Bollywood recommendations are coming soon!")  # Popup message

# Show Hollywood movie selection and recommendations if button was clicked
if st.session_state.show_hollywood:
    Selected_movie_name = st.selectbox(
        'Choose a Hollywood movie:',
        movies['title'].values
    )

    if st.button('Show Recommendation'):
        names, posters = recommend(Selected_movie_name)

        # Display recommendations in columns
        col1, col2, col3, col4, col5 = st.columns(5)
        with col1:
            st.text(names[0])
            st.image(posters[0])
        with col2:
            st.text(names[1])
            st.image(posters[1])
        with col3:
            st.text(names[2])
            st.image(posters[2])
        with col4:
            st.text(names[3])
            st.image(posters[3])
        with col5:
            st.text(names[4])
            st.image(posters[4])

# Show Bollywood message if Bollywood button was clicked
if st.session_state.show_bollywood:
    # Display a placeholder message for Bollywood recommendations
    st.info("Stay tuned for Bollywood movie recommendations!")
