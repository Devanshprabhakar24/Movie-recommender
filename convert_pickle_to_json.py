import pickle
import json

# Load movies_dict
with open('movies_dict.pkl', 'rb') as f:
    movies = pickle.load(f)

# Save to movies.json
with open('backend/movies.json', 'w') as f:
    json.dump(movies, f)

# Load similarity matrix
with open('similarity.pkl', 'rb') as f:
    similarity = pickle.load(f)

# Save to similarity.json
with open('backend/similarity.json', 'w') as f:
    json.dump(similarity.tolist(), f)
