import os
import ast
import json
import pandas as pd
import numpy as np
import faiss
from sentence_transformers import SentenceTransformer

def safe_literal_eval(val):
    try:
        return ast.literal_eval(val)
    except (ValueError, SyntaxError):
        return []

class RecipeRAG:
    def __init__(self):
        self.recipes_csv_path = r"C:\Users\Vijyot\Downloads\recipe\RAW_recipes.csv"
        self.index_path = "data/recipe_index.faiss"
        self.metadata_path = "data/recipe_metadata.json"
        
        print("Loading Sentence Transformer embedding model...")
        self.embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
        self.index = None
        self.recipes_data = []
        
        self._initialize_rag()
        
    def _initialize_rag(self):
        os.makedirs("data", exist_ok=True)
        
        if os.path.exists(self.index_path) and os.path.exists(self.metadata_path):
            print("Cached FAISS index found! Loading from disk to save time...")
            self.index = faiss.read_index(self.index_path)
            with open(self.metadata_path, 'r', encoding='utf-8') as f:
                self.recipes_data = json.load(f)
            print(f"Loaded {len(self.recipes_data)} recipes from cache.")
        else:
            print("FAISS index not found. Building from scratch...")
            self._build_index()

    def _build_index(self):
        # We parse the full dataset up to a safe limit or full depending on the user requirements.
        # "Build FAISS index from all recipes"
        if not os.path.exists(self.recipes_csv_path):
            print(f"ERROR: Recipe dataset not found at {self.recipes_csv_path}")
            print("Please ensure the CSV file is downloaded and placed correctly.")
            # Gracefully build an empty index
            dimension = self.embedding_model.get_sentence_embedding_dimension()
            self.index = faiss.IndexFlatL2(dimension)
            return

        print(f"Loading and processing recipes from {self.recipes_csv_path}...")
        try:
            df = pd.read_csv(self.recipes_csv_path)
            # Drop empty names
            df = df.dropna(subset=['name'])
            
            for _, row in df.iterrows():
                try:
                    ingreds = safe_literal_eval(row['ingredients'])
                    steps = safe_literal_eval(row['steps'])
                    if len(ingreds) > 0 and len(steps) > 0:
                        self.recipes_data.append({
                            "name": row['name'],
                            "ingredients": ingreds,
                            "steps": steps
                        })
                except Exception:
                    pass
                    
            print(f"Successfully processed {len(self.recipes_data)} recipes.")
        except Exception as e:
            print(f"Failed to read dataset: {e}")
            return
            
        print("Computing semantic embeddings for all recipes... (This may take several minutes)")
        docs = [str(r['name']) for r in self.recipes_data]
        
        # We can encode in batches for better RAM efficiency
        embeddings = self.embedding_model.encode(
            docs, 
            batch_size=128, 
            show_progress_bar=True, 
            convert_to_numpy=True
        )
        
        dimension = embeddings.shape[1]
        self.index = faiss.IndexFlatL2(dimension)
        self.index.add(embeddings)
        
        print(f"Saving FAISS index to {self.index_path}...")
        faiss.write_index(self.index, self.index_path)
        
        print(f"Saving recipe metadata to {self.metadata_path}...")
        with open(self.metadata_path, 'w', encoding='utf-8') as f:
            json.dump(self.recipes_data, f)
            
        print("FAISS Index build complete and cached locally!")

    def search(self, query, threshold=1.2):
        if not self.index or len(self.recipes_data) == 0:
            return None
        
        query_vector = self.embedding_model.encode([query], convert_to_numpy=True)
        distances, indices = self.index.search(query_vector, 1)
        
        best_distance = distances[0][0]
        best_idx = indices[0][0]
        
        if best_idx != -1 and best_distance < threshold:
            recipe = self.recipes_data[best_idx]
            return {
                "name": recipe['name'],
                "ingredients": recipe['ingredients'],
                "steps": recipe['steps'],
                "distance": float(best_distance)
            }
            
        return None

if __name__ == "__main__":
    rag = RecipeRAG()
    test_q = "How to make a simple roti"
    print(f"\nTesting search query: '{test_q}'")
    res = rag.search(test_q)
    if res:
        print(f"Found match: {res['name']} (Distance: {res['distance']:.3f})")
    else:
        print("No matches found within the threshold barrier!")
