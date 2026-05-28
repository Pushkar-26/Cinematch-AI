import os
import pickle
import streamlit as st
import gdown

# ==========================================
# DOWNLOAD SIMILARITY FILE (sirf pehli baar)
# ==========================================

if not os.path.exists('similarity.pkl'):
    FILE_ID = "1IcLNpZ6YChsQTcCSzkcSFVpSxgyZusXw"
    gdown.download(f"https://drive.google.com/uc?id={FILE_ID}", 'similarity.pkl', quiet=False)

# ==========================================
# PAGE CONFIG
# ==========================================

st.set_page_config(
    page_title="CineMatch AI",
    page_icon="🎬",
    layout="wide"
)

# ==========================================
# LOAD DATA (cached — ek baar hi load hoga)
# ==========================================

@st.cache_resource
def load_data():
    with open('movie_list.pkl', 'rb') as f:
        movies = pickle.load(f)
    with open('similarity.pkl', 'rb') as f:
        similarity = pickle.load(f)
    return movies, similarity

movies, similarity = load_data()

# ==========================================
# RECOMMEND FUNCTION
# ==========================================

def recommend(movie):
    movie_index = movies[movies['title'] == movie].index[0]
    distances = similarity[movie_index]
    movies_list = sorted(
        list(enumerate(distances)),
        reverse=True,
        key=lambda x: x[1]
    )[1:6]
    recommended_movies = []
    for i in movies_list:
        recommended_movies.append(movies.iloc[i[0]].title)
    return recommended_movies

# ==========================================
# CUSTOM CSS
# ==========================================

st.markdown("""
<style>
#MainMenu { visibility: hidden; }
footer { visibility: hidden; }
header { visibility: hidden; }
.main { background: linear-gradient(to bottom right, #050816, #0b1023); color: white; }
.block-container { padding-top: 2rem; padding-left: 4rem; padding-right: 4rem; }
.hero { text-align: center; padding-top: 20px; padding-bottom: 50px; }
.hero-title { font-size: 80px; font-weight: 800; background: linear-gradient(90deg, #ff4b4b, #ff416c, #ff4b2b); -webkit-background-clip: text; -webkit-text-fill-color: transparent; }
.hero-subtitle { color: #cfcfcf; font-size: 24px; margin-top: -15px; }
.stSelectbox label { color: white !important; font-size: 20px; font-weight: 600; }
.stButton > button { width: 100%; height: 60px; border: none; border-radius: 18px; background: linear-gradient(135deg, #ff416c, #ff4b2b); color: white; font-size: 22px; font-weight: 700; transition: 0.3s ease; }
.stButton > button:hover { transform: translateY(-5px) scale(1.02); box-shadow: 0px 15px 35px rgba(255,75,75,0.5); color: white; }
.section-heading { font-size: 50px; font-weight: 800; margin-top: 40px; margin-bottom: 30px; color: white; }
.custom-card { background: rgba(255,255,255,0.05); border-radius: 24px; padding: 35px 20px; text-align: center; min-height: 240px; display: flex; flex-direction: column; justify-content: center; align-items: center; border: 1px solid rgba(255,255,255,0.08); transition: 0.35s ease; cursor: pointer; }
.custom-card:hover { transform: translateY(-10px) scale(1.03); box-shadow: 0px 15px 35px rgba(255,75,75,0.4); background: rgba(255,255,255,0.08); }
.movie-emoji { font-size: 60px; margin-bottom: 20px; }
.movie-name { font-size: 22px; font-weight: 700; color: white; line-height: 1.5; }
.footer { text-align: center; color: #9e9e9e; padding-top: 30px; padding-bottom: 10px; font-size: 16px; }
hr { border: 1px solid rgba(255,255,255,0.1); }
</style>
""", unsafe_allow_html=True)

# ==========================================
# HERO SECTION
# ==========================================

st.markdown("""
<div class="hero">
<div class="hero-title">🎬 CineMatch AI</div>
<div class="hero-subtitle">Discover movies you'll actually love</div>
</div>
""", unsafe_allow_html=True)

# ==========================================
# SELECT MOVIE
# ==========================================

selected_movie_name = st.selectbox(
    "Choose your movie",
    movies['title'].values
)

# ==========================================
# BUTTON
# ==========================================

if st.button("✨ Recommend Movies"):
    with st.spinner("Finding perfect recommendations for you..."):
        recommendations = recommend(selected_movie_name)

        st.markdown('<div class="section-heading">🍿 Recommended For You</div>', unsafe_allow_html=True)

        col1, col2, col3, col4, col5 = st.columns(5)
        cols = [col1, col2, col3, col4, col5]
        icons = ["🎥", "🍿", "🎬", "⭐", "🎞️"]

        for idx, movie in enumerate(recommendations):
            with cols[idx]:
                st.markdown(f'<div class="custom-card"><div class="movie-emoji">{icons[idx]}</div><div class="movie-name">{movie}</div></div>', unsafe_allow_html=True)

# ==========================================
# FOOTER
# ==========================================

st.markdown("""
<br><br><hr>
<div class="footer">Made with ❤️ using Streamlit & Machine Learning</div>
""", unsafe_allow_html=True)