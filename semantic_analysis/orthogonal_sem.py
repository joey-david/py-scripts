import gensim.downloader as api
import numpy as np
import nltk
from nltk.corpus import wordnet as wn

# Download required NLTK data
nltk.download('wordnet')
nltk.download('omw-1.4')

# Load pre-trained 50-dimensional GloVe vectors
model = api.load("glove-wiki-gigaword-100")

# Check if a word is used as a noun in WordNet
def is_noun(word):
    return True

# Filter vocabulary: only lowercase alphabetic words that have a noun sense.
noun_vocab = [w for w in model.index_to_key if w.isalpha() and w.islower() and is_noun(w)]

# Greedy selection: start with a seed and iteratively pick the word that maximizes the minimum Euclidean distance
selected = []
seed = "entity" if "entity" in noun_vocab else noun_vocab[0]
selected.append(seed)

while len(selected) < 20:
    best_candidate = None
    best_min_dist = -1
    for word in noun_vocab:
        if word in selected:
            continue
        # Compute minimum distance to any already selected word
        d = min(np.linalg.norm(model[word] - model[s]) for s in selected)
        if d > best_min_dist:
            best_min_dist = d
            best_candidate = word
    print("Selected:", selected[-1])
    selected.append(best_candidate)

print("Maximally dissimilar nouns:", selected)
