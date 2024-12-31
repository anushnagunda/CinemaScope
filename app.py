import streamlit as st
import pandas as pd
import requests
import pickle

# Load the processed data and similarity matrix
with open('movie_data.pkl', 'rb') as file:
    movies, cosine_sim = pickle.load(file)

# Function to get movie recommendations
def get_recommendations(title, cosine_sim=cosine_sim):
    idx = movies[movies['title'] == title].index[0]
    sim_scores = list(enumerate(cosine_sim[idx]))
    sim_scores = sorted(sim_scores, key=lambda x: x[1], reverse=True)
    sim_scores = sim_scores[1:11]  # Get top 10 similar movies
    movie_indices = [i[0] for i in sim_scores]
    return movies[['title', 'movie_id']].iloc[movie_indices]

# Fetch movie poster from TMDB API
def fetch_poster(movie_id):
    api_key = '7b995d3c6fd91a2284b4ad8cb390c7b8'  # Replace with your TMDB API key
    url = f'https://api.themoviedb.org/3/movie/{movie_id}?api_key={api_key}'
    response = requests.get(url)
    data = response.json()
    poster_path = data.get('poster_path', None)
    if poster_path:
        full_path = f"https://image.tmdb.org/t/p/w500{poster_path}"
        return full_path
    return None  # Return None if no poster is found

# CSS Styling
st.markdown(
    """
    <style>
    .stApp {
        background-image: url("https://clipart-library.com/img/1148111.jpg");
        background-size: cover;
        background-position: center;
        background-repeat: no-repeat;
        color: white;
    }
    #cinema-scope {
        display: flex;
        justify-content: center;
        align-items: center;
        position: fixed;
        top: 7%;
        left: 0;
        width: 100%;
        background-color: rgba(0, 0, 0, 0.8);
        color: white;
        padding: 20px 0;
        font-size: 3em;
        font-weight: bold;
        border-bottom: 5px solid gold;
        text-align: center;
        z-index: 10;
        box-shadow: 0px 5px 10px rgba(0, 0, 0, 0.5);
    }
    .content {
        margin-top: 150px; /* Adds spacing to prevent overlap with the header */
        text-align: center;
    }
    .subtitle {
        font-size: 1.5em;
        font-weight: 400;
        margin-top: 5px;
        margin-bottom: 30px;
        color: lightgoldenrodyellow;
        text-align: center;
    }
    .select-box-container {
        margin-top: 20px; /* Adds space above the dropdown */
        margin-bottom: 10px; /* Adds space below the dropdown */
    }
    .recommend-button-container {
        margin-top: 10px; /* Adds space above the button */
    }
    </style>
    <div id="cinema-scope">Cinema Scope</div>
    """,
    unsafe_allow_html=True
)

# UI Subtitle
st.markdown(
    """
    <div class="content">
        <div class="subtitle">
            Your ultimate movie recommendation platform! Select a film you love, and let Cinema Scope curate the perfect list of movies just for you.
        </div>
    </div>
    """,
    unsafe_allow_html=True
)

# Streamlit UI
st.title("Cinema Scope")

# Add a container for the select box
st.markdown('<div class="select-box-container">', unsafe_allow_html=True)
selected_movie = st.selectbox("Select a movie:", movies['title'].values)
st.markdown('</div>', unsafe_allow_html=True)

# Add a container for the button
st.markdown('<div class="recommend-button-container">', unsafe_allow_html=True)
if st.button('Recommend'):
    recommendations = get_recommendations(selected_movie)
    st.write("Top 10 recommended movies:")

    # Create a 2x5 grid layout
    for i in range(0, 10, 5):  # Loop over rows (2 rows, 5 movies each)
        cols = st.columns(5)  # Create 5 columns for each row
        for col, j in zip(cols, range(i, i+5)):
            if j < len(recommendations):
                movie_title = recommendations.iloc[j]['title']
                movie_id = recommendations.iloc[j]['movie_id']
                poster_url = fetch_poster(movie_id)
                with col:
                    if poster_url:
                        st.image(poster_url, width=130)
                    st.write(movie_title)
st.markdown('</div>', unsafe_allow_html=True)
                    
