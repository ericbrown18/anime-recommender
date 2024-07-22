import streamlit as st
import pandas as pd
import pickle

animes_dict = pickle.load(open('model/animes_dict.pkl','rb'))
animes = pd.DataFrame(animes_dict)
@st.cache_resource()
def recommend(anime):
    similarity = pickle.load(open('model/similarity.pkl', 'rb'))

    index = animes[animes["Name"] == anime]["index"].values[0]
    distances = sorted(list(enumerate(similarity[index])), reverse=True, key=lambda x: x[1])
    recommended_anime_names = []
    recommended_anime_summery = []
    recommended_anime_tags = []
    #recommended_anime_posters = []
    for i in distances[1:6]:
        # fetch the anime poster
        #anime_id = animes.iloc[i[0]].anime_id
        #recommended_anime_posters.append((anime_id))
        recommended_anime_names.append(animes.iloc[i[0]].Name)
        recommended_anime_summery.append(animes.iloc[i[0]].Synopsis)
        recommended_anime_tags.append(animes.iloc[i[0]].Tags)

    return recommended_anime_names, recommended_anime_summery, recommended_anime_tags

from PIL import Image

# Load icon
icon_image = Image.open("icon.png")

# page configuration
st.set_page_config(
    page_title="Anime Recommender",
    page_icon=icon_image,
    layout="wide"
)


st.title('Anime Recommender')
selected_anime = st.selectbox(
'Which anime did you like?',
(animes['Name'].values))

if st.button('Recommend'):
    with st.spinner(text="Chill folk! your taste is awesome! I'm trynna find perfect match "):
         recommendations,summery,tags = recommend(selected_anime)
         st.success('Enjoy.. These anime are perfect 🤩')
         for i in range(5):
             st.write(f"{i+1})"+"Title  :  "+str(recommendations[i]))
             st.write("Summery  : "+str(summery[i]))
             st.write("Tags :  "+str(tags[i]))