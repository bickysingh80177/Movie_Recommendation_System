import pandas as pd
import streamlit as st
import pickle
import requests

st.set_page_config(layout="wide")


def fetch_data(movie_id):
    response = requests.get('https://api.themoviedb.org/3/movie/{}'
                            '?api_key=ccd561cd0c15519550ed0aa41f5591f9&language=en-US'.format(movie_id))

    data = response.json()
    return data


def recommend(movie):
    """ return 5 similar movies """
    # fetching the index of the movie
    movie_index = movies[movies['original_title'] == movie].index[0]
    distances = similarity[movie_index]  # finding the distances
    movie_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])
    recommended_movies = []
    recommended_movies_posters = []
    movie_overview = []
    movie_ratings = []
    for i in movie_list[1:6]:
        movie_id = movies.iloc[i[0]].id
        recommended_movies.append(movies.iloc[i[0]].original_title)
        data = fetch_data(movie_id)
        # fetch poster from api
        poster_path = "https://image.tmdb.org/t/p/w500" + data['poster_path']
        # recommended_movies_posters.append(fetch_posters(movie_id))
        recommended_movies_posters.append(poster_path)
        movie_overview.append(data['overview'])
        movie_ratings.append(data['vote_average'])
    return recommended_movies, recommended_movies_posters, movie_overview, movie_ratings


movies_dict = pickle.load(open('movies_dict.plk', 'rb'))
movies = pd.DataFrame(movies_dict)


similarity = pickle.load(open('similarity.pkl', 'rb'))

st.title("Movie Recommender System")

question = '<p style="font-family:Courier; colo:Blue; font-size: 20px;">Select Movie from the list</p>'
selected_movie_name = st.selectbox(
    'Select Movie from list -',
    movies['original_title'].values,
)

if st.button('Recommend Movies'):
    names, posters, overview, rating = recommend(selected_movie_name)
    for i in range(5):
        st.markdown("""<div style="margin-bottom:1rem"><div style="display:flex;gap:3rem;flex-direction:row">
                    <div><img src={} alt={} style="width:auto;height:250px"/></div>
                    <div><h2>{}</h2>
                    <p>{}</p>
                    <p>Average Ratings: <span style="color:#f59842; font-weight:bold">{}</span></p>
                    </div>
                    </div></div>""".format(posters[i], names[i], names[i], overview[i], rating[i]),
                    unsafe_allow_html=True)
