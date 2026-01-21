import pickle
import numpy as np
import os

def split_similarity():
    print("Loading similarity matrix...")
    try:
        # Load the big file
        similarity = pickle.load(open('artifacts/similarity.pkl', 'rb'))
    except FileNotFoundError:
        print("❌ Error: Could not find 'artifacts/similarity.pkl'")
        return

    # 1. SPLIT into 10 PARTS (To ensure each part is < 25MB)
    print(f"Original shape: {similarity.shape}")
    print("Splitting into 10 small parts...")

    parts = np.array_split(similarity, 10)
    
    # Save 10 files: sim_0.pkl to sim_9.pkl
    for i, part in enumerate(parts):
        filename = f'artifacts/sim_{i}.pkl'
        pickle.dump(part, open(filename, 'wb'))
        print(f"   Saved {filename} ({os.path.getsize(filename)/1024/1024:.2f} MB)")
    
    print("\n✅ Success! You now have 10 small files.")
    print("👉 Upload these sim_0.pkl ... sim_9.pkl files to GitHub.")

if __name__ == "__main__":
    split_similarity()