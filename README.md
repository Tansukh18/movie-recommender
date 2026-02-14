# 🎬 Cinema AI: Intelligent Movie Recommender

**Cinema AI** is a next-generation movie recommendation engine featuring a stunning **Glassmorphism UI**. It uses **Content-Based Filtering** to suggest movies based on plot, genre, and cast similarity, while fetching real-time data (posters, ratings, runtime) via the **OMDb API**.

🚀 **Live Demo:** [https://movie-recommender-afrhxfgn66sagczr9sephb.streamlit.app/]

---

## ✨ Key Features

- **🧠 Advanced AI Logic:** Uses Cosine Similarity on a dataset of 5,000+ movies to find perfect matches.
- **🎨 Glassmorphism UI:** A modern, premium interface with translucent sidebars, hover effects, and a dynamic abstract background.
- **⚡ Smart Data Loading:** Implements a custom **"Split & Stitch"** algorithm to handle large Machine Learning models (180MB+) on GitHub by splitting them into 30 tiny chunks and stitching them instantly in memory.
- **📡 Real-Time Metadata:** Fetches live movie posters, IMDb ratings, plot summaries, and director info using the OMDb API.
- **📱 Fully Responsive:** Optimized for both desktop and mobile screens.

---

## 🛠️ Tech Stack

- **Frontend:** [Streamlit](https://streamlit.io/) (Custom CSS for Glassmorphism)
- **Backend:** Python 3.x
- **Machine Learning:** Scikit-Learn (Cosine Similarity), NumPy, Pandas
- **API:** OMDb API (Open Movie Database)
- **Data Serialization:** Pickle

---

## 📂 Project Structure

```bash
movie-recommender/
│
├── app.py                  # 🚀 Main application (UI + Logic + Stitching)
├── split_data.py           # 🛠️ Utility script to split large models for GitHub
├── requirements.txt        # 📦 List of python dependencies
├── README.md               # 📄 Project documentation
│
└── artifacts/              # 💾 Data Folder
    ├── movie_list.pkl      # Dictionary of movie titles & IDs
    ├── sim_0.pkl           # 🧩 Similarity Matrix Chunk 0
    ├── sim_1.pkl           # 🧩 Similarity Matrix Chunk 1
    ├── ...                 # ... (Chunks 2-28)
    └── sim_29.pkl          # 🧩 Similarity Matrix Chunk 29

