"""Text embeddings utility for ticket classification."""
from sentence_transformers import SentenceTransformer
import numpy as np


class EmbeddingGenerator:
    """Generates embeddings for text using sentence transformers."""
    
    def __init__(self, model_name: str = 'all-MiniLM-L6-v2'):
        """Initialize embedding generator.
        
        Args:
            model_name: Name of the sentence transformer model
        """
        self.model = SentenceTransformer(model_name)
    
    def encode(self, texts):
        """Generate embeddings for texts.
        
        Args:
            texts: Single text string or list of text strings
            
        Returns:
            Numpy array of embeddings
        """
        if isinstance(texts, str):
            texts = [texts]
        return self.model.encode(texts)
    
    def encode_batch(self, texts, batch_size: int = 32):
        """Generate embeddings for a batch of texts.
        
        Args:
            texts: List of text strings
            batch_size: Batch size for encoding
            
        Returns:
            Numpy array of embeddings
        """
        return self.model.encode(texts, batch_size=batch_size, show_progress_bar=True)
    
    def compute_similarity(self, text1, text2):
        """Compute cosine similarity between two texts.
        
        Args:
            text1: First text string
            text2: Second text string
            
        Returns:
            Similarity score between 0 and 1
        """
        emb1 = self.encode(text1)
        emb2 = self.encode(text2)
        
        # Compute cosine similarity
        similarity = np.dot(emb1[0], emb2[0]) / (np.linalg.norm(emb1[0]) * np.linalg.norm(emb2[0]))
        return float(similarity)
