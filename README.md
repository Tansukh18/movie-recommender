# 🎬 Cinema AI: Intelligent Movie Recommender

![Cinema AI Screenshot](assets/cinema-ai.png)


**Cinema AI** is a next-generation movie recommendation engine featuring a stunning **Glassmorphism UI**. It uses **Content-Based Filtering** to suggest movies based on plot, genre, and cast similarity, while fetching real-time data (posters, ratings, runtime) via the **OMDb API**.

🚀 **Live Demo:** https://movie-recommender-afrhxfgn66sagczr9sephb.streamlit.app/

Start the Streamlit server(Project Root Folder) :  streamlit run app.py


---

## ✨ Key Features

- **🧠 Advanced AI Logic:** Uses Cosine Similarity on a dataset of 5,000+ movies to find perfect matches.
- **🎨 Glassmorphism UI:** A modern, premium interface with translucent sidebars, hover effects, and a dynamic abstract background.
- **⚡ Smart Data Loading:** Implements a custom **"Split & Stitch"** algorithm to handle large Machine Learning models (180MB+) on GitHub by splitting them into 30 tiny chunks and stitching them instantly in memory.
- **📡 Real-Time Metadata:** Fetches live movie posters, IMDb ratings, plot summaries, and director info using the OMDb API.
- **📱 Fully Responsive:** Optimized for both desktop and mobile screens.

---

## 🛠️ Tech Stack

- **Frontend:** Streamlit (Custom CSS for Glassmorphism)
- **Backend:** Python 3.x
- **Machine Learning:** Scikit-Learn (Cosine Similarity), NumPy, Pandas
- **API:** OMDb API (Open Movie Database)
- **Data Serialization:** Pickle

---

## ▶️ Run Locally

1. Clone the repository and move into the project folder.
2. Install dependencies:
   ```bash
   pip install -r requirements.txt

│
└── artifacts/              # 💾 Data Folder
    ├── movie_list.pkl      # Dictionary of movie titles & IDs
    ├── sim_0.pkl           # 🧩 Similarity Matrix Chunk 0
    ├── sim_1.pkl           # 🧩 Similarity Matrix Chunk 1
    ├── ...                 # ... (Chunks 2-28)
    └── sim_29.pkl          # 🧩 Similarity Matrix Chunk 29



