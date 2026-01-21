import streamlit as st
import pickle
import pandas as pd
import requests
import numpy as np

# --- 1. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="Cinema AI",
    layout="wide",
    initial_sidebar_state="expanded",
    page_icon="🎬"
)

# --- 2. MODERN UI CSS (Glassmorphism & Gradient) ---
st.markdown("""
    <style>
    /* MAIN BACKGROUND (Dark Modern Gradient) */
    .stApp {
        background: radial-gradient(circle at top left, #1a0b0b, #000000, #0f0c29);
        color: #ffffff;
    }
    
    /* SIDEBAR GLASS EFFECT */
    section[data-testid="stSidebar"] {
        background-color: rgba(0, 0, 0, 0.5);
        backdrop-filter: blur(10px);
        border-right: 1px solid rgba(255, 255, 255, 0.1);
    }
    
    /* MOVIE CARD STYLING */
    .movie-card {
        background: rgba(255, 255, 255, 0.05);
        border: 1px solid rgba(255, 255, 255, 0.1);
        border-radius: 12px;
        padding: 15px;
        transition: transform 0.3s ease;
    }
    .movie-card:hover {
        transform: translateY(-5px);
        border-color: #e50914; /* Netflix Red */
        box-shadow: 0 10px 20px rgba(0,0,0,0.5);
    }
    
    /* TEXT STYLING */
    h1, h2, h3 { color: #fff !important; font-family: sans-serif; }
    p { color: #ccc; }
    
    /* BUTTON STYLING */
    .trailer-btn {
        display: block;
        background: linear-gradient(45deg, #e50914, #b20710);
        color: white !important;
        text-decoration: none;
        padding: 8px 0;
        border-radius: 6px;
        text-align: center;
        font-weight: bold;
        margin-top: 10px;
    }
    .trailer-btn:hover {
        transform: scale(1.02);
        box-shadow: 0 5px 15px rgba(229, 9, 20, 0.4);
    }
    
    /* MATCH BADGE */
    .match-badge {
        background-color: #46d369;
        color: black;
        font-weight: bold;
        padding: 2px 8px;
        border-radius: 10px;
        font-size: 12px;
        float: right;
    }
    
    /* HIDE DEFAULT MENU */
    #MainMenu {visibility: hidden;}
    footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

# --- 3. DATA LOADING (OPTIMIZED & CACHED) ---
@st.cache_resource(show_spinner="Initializing Cinema AI Database...")
def load_data():
    """
    Loads data ONCE and keeps it in memory. 
    It stitches the 10 split files automatically.
    """
    try:
        # 1. Load Movie List
        movie_dict = pickle.load(open('artifacts/movie_list.pkl', 'rb'))
        
        # 2. Load and Stitch Similarity Matrix
        parts = []
        # We expect files sim_0.pkl to sim_9.pkl
        for i in range(10):
            try:
                part = pickle.load(open(f'artifacts/sim_{i}.pkl', 'rb'))
                parts.append(part)
            except FileNotFoundError:
                # Fallback: If local and you have the BIG file, use that instead
                try:
                    return movie_dict, pickle.load(open('artifacts/similarity.pkl', 'rb'))
                except:
                    st.error(f"❌ Critical Error: Missing file 'artifacts/sim_{i}.pkl'. Please run split_data.py again.")
                    return None, None
        
        # Stitch them together
        similarity_matrix = np.concatenate(parts, axis=0)
        return movie_dict, similarity_matrix
            
    except Exception as e:
        st.error(f"Error loading data: {e}")
        return None, None

# Run the loader
movies_dict, similarity = load_data()

# Stop if data failed
if movies_dict is None:
    st.stop()

movies = pd.DataFrame(movies_dict)

# --- 4. HELPER FUNCTIONS ---

def fetch_movie_details(movie_title):
    """Fetches details (Poster, Plot, Rating) with robust fallback."""
    default_data = {
        "Poster": "https://images.unsplash.com/photo-1536440136628-849c177e76a1?w=500&q=80",
        "Plot": "Plot details unavailable.",
        "imdbRating": "N/A", "Runtime": "--", "Director": "Unknown", "Year": "----"
    }
    try:
        # Timeout prevents freezing
        url = f"https://www.omdbapi.com/?t={movie_title}&apikey=bdeb32eb"
        response = requests.get(url, timeout=1.5)
        data = response.json()
        
        if data.get('Response') == 'True':
            if data.get('Poster') == 'N/A': data['Poster'] = default_data['Poster']
            return data
        return default_data
    except:
        return default_data

def get_star_rating(rating_value):
    try:
        return "⭐" * int(float(rating_value) / 2)
    except:
        return "⭐"

def recommend(movie, movies_df, similarity_matrix):
    try:
        # Find index
        idx = movies_df[movies_df['title'] == movie].index[0]
        
        # Calculate scores
        scores = list(enumerate(similarity_matrix[idx]))
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:6]
        
        results = []
        for i in sorted_scores:
            title = movies_df.iloc[i[0]].title
            details = fetch_movie_details(title)
            
            results.append({
                "title": title,
                "poster": details['Poster'],
                "match_score": int(i[1] * 100)
            })
        return results
    except Exception as e:
        st.error(f"Error in recommendation: {e}")
        return []

# --- 5. UI LAYOUT ---

# --- SIDEBAR ---
with st.sidebar:
    st.title("🍿 Cinema AI")
    st.markdown("Your personal movie curator.")
    st.markdown("---")
    
    # SEARCH INPUT
    selected_movie_name = st.selectbox(
        "🔍 Select a Movie:",
        movies['title'].values,
        index=None,
        placeholder="Type here..."
    )
    
    # Button
    if st.button('🚀 Find Matches', type="primary"):
        if selected_movie_name:
            st.session_state['show_rec'] = True
            st.session_state['selected_movie'] = selected_movie_name
        else:
            st.warning("⚠️ Please select a movie first!")

    st.markdown("---")
    st.caption("v2.1 | Fast Stitching Engine")

# --- MAIN CONTENT ---
if 'show_rec' in st.session_state and st.session_state['show_rec']:
    
    current_movie = st.session_state['selected_movie']
    
    # Show loading spinner while fetching info
    with st.spinner(f"Analyzing {current_movie}..."):
        details = fetch_movie_details(current_movie)
    
    # HERO SECTION
    col1, col2 = st.columns([1, 2.5], gap="large")
    
    with col1:
        st.image(details['Poster'], use_container_width=True)
        
    with col2:
        st.markdown(f"# {details.get('Title', current_movie)}")
        st.markdown(f"### {details['Year']} • {details['Runtime']}")
        
        st.markdown(f"#### {get_star_rating(details['imdbRating'])} ({details['imdbRating']})")
        st.info(details['Plot'])
        st.write(f"**Director:** {details['Director']}")

    st.markdown("---")
    st.subheader(f"✨ Top Recommendations")
    
    # RECOMMENDATION GRID
    recs = recommend(current_movie, movies, similarity)
    
    if recs:
        cols = st.columns(5)
        for idx, col in enumerate(cols):
            m = recs[idx]
            with col:
                st.markdown(f"""
                <div class="movie-card">
                    <img src="{m['poster']}" style="width:100%; border-radius:8px;">
                    <div style="padding-top:10px;">
                        <span class="match-badge">{m['match_score']}%</span>
                        <div style="font-weight:bold; font-size:14px; margin-top:5px; white-space:nowrap; overflow:hidden; text-overflow:ellipsis;">
                            {m['title']}
                        </div>
                    </div>
                </div>
                """, unsafe_allow_html=True)
                
                # Trailer Link
                url = f"https://www.youtube.com/results?search_query={m['title']}+trailer"
                st.markdown(f"<a href='{url}' target='_blank' class='trailer-btn'>▶ Watch Trailer</a>", unsafe_allow_html=True)
    else:
        st.warning("No recommendations found.")
        
else:
    # WELCOME SCREEN
    st.markdown("<br><br><br>", unsafe_allow_html=True)
    st.markdown("<h1 style='text-align: center; font-size: 5rem;'>Cinema AI</h1>", unsafe_allow_html=True)
    st.markdown("<p style='text-align: center; font-size: 1.2rem; color: #888;'>Select a movie from the sidebar to begin.</p>", unsafe_allow_html=True)