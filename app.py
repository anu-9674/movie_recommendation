
import requests
import streamlit as st
import pickle
import pandas as pd

from pathlib import Path
current_directory= Path(__file__).resolve().parent
movie_dict_path=current_directory/"movie_dict.pkl"
movies_dict = pickle.load(open(movie_dict_path, 'rb'))
movies=pd.DataFrame(movies_dict)

similarity_path=current_directory/"similarity.pkl"
similarity = pickle.load(open(similarity_path, 'rb'))

def fetch_poster(movie_id):
    # url = "https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id)
    # data = requests.get(url)
    # data = data.json()
    # poster_path = data['poster_path']
    # full_path = "https://image.tmdb.org/t/p/w500/" + poster_path
    # return full_path

    response=requests.get("https://api.themoviedb.org/3/movie/{}?api_key=8265bd1679663a7ea12ac168da84d2e8&language=en-US".format(movie_id))
    data=response.json()
    return "https://image.tmdb.org/t/p/w500/" + data['poster_path']
def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(list(enumerate(distances)), reverse=True, key=lambda x: x[1])[1:6]

    recommended_movies=[]
    recommended_movies_posters=[]

    for i in movies_list:
        movie_id=movies.iloc[i[0]].movie_id
        recommended_movies.append(movies.iloc[i[0]].title)
        recommended_movies_posters.append(fetch_poster(movie_id))

    return recommended_movies,recommended_movies_posters

def set_bg_hack_url():
    st.markdown(
        f"""
         <style>
         body {{
             background: url("https://c4.wallpaperflare.com/wallpaper/727/858/367/cartoons-wallpaper-preview.jpg");
             background-size: cover;
         }}
         .stApp {{
             background-color: rgba(255, 255, 255, 0.7); 
             position: absolute;
             top: 0;
             left: 0;
             width: 100%;
             height: 100%;
             z-index: -1; 
         }}
         </style>
         """,
        unsafe_allow_html=True
    )



set_bg_hack_url()

st.title('MOVIE RECOMMENDER')

selected_movie_name=st.selectbox('What movies would you like to be recommended ?',movies['title'].values)
if st.button('RECOMMEND'):
    names,posters=recommend(selected_movie_name)

    col1,col2,col3,col4,col5=st.columns(5)
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



