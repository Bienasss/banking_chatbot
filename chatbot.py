"""
Banking FAQ Chatbot using Word2Vec/fastText embeddings for semantic similarity.
"""

import json
import numpy as np
from typing import List, Tuple, Optional
from gensim.models import Word2Vec, FastText
import nltk
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from sklearn.metrics.pairwise import cosine_similarity

# Download required NLTK data
try:
    nltk.data.find('tokenizers/punkt')
except LookupError:
    nltk.download('punkt', quiet=True)

try:
    nltk.data.find('corpora/stopwords')
except LookupError:
    nltk.download('stopwords', quiet=True)


class BankingChatbot:
    """Banking FAQ Chatbot using Word2Vec/fastText for semantic similarity."""
    
    def __init__(self, faq_file: str = "faq_data.json", use_fasttext: bool = False):
        """
        Initialize the chatbot.
        
        Args:
            faq_file: Path to JSON file with FAQ data
            use_fasttext: If True, use FastText, otherwise use Word2Vec
        """
        self.use_fasttext = use_fasttext
        self.faq_data = self._load_faq_data(faq_file)
        self.questions = [item["question"] for item in self.faq_data]
        self.answers = [item["answer"] for item in self.faq_data]
        
        # Lithuanian stopwords
        try:
            self.stop_words = set(stopwords.words('lithuanian'))
        except LookupError:
            nltk.download('stopwords', quiet=True)
            try:
                self.stop_words = set(stopwords.words('lithuanian'))
            except LookupError:
                # Fallback to English if Lithuanian not available
                self.stop_words = set(stopwords.words('english'))
        
        # Add common Lithuanian stopwords manually if needed
        self.stop_words.update(['ir', 'bei', 'arba', 'taip', 'ne', 'kad', 'kur', 'kaip', 'kokie', 'kokia'])
        
        # Preprocess questions
        self.processed_questions = [self._preprocess_text(q) for q in self.questions]
        
        # Train or load embeddings
        self.model = self._train_embeddings()
        
        # Precompute question embeddings
        self.question_embeddings = self._compute_embeddings(self.processed_questions)
    
    def _load_faq_data(self, faq_file: str) -> List[dict]:
        """Load FAQ data from JSON file."""
        with open(faq_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    
    def _preprocess_text(self, text: str) -> List[str]:
        """
        Preprocess text: lowercase, tokenize, remove stopwords and punctuation.
        
        Args:
            text: Input text
            
        Returns:
            List of processed tokens
        """
        # Convert to lowercase
        text = text.lower()
        
        # Tokenize
        tokens = word_tokenize(text)
        
        # Remove stopwords and non-alphabetic tokens
        tokens = [
            token for token in tokens 
            if token.isalpha() and token not in self.stop_words and len(token) > 2
        ]
        
        return tokens
    
    def _train_embeddings(self):
        """
        Train Word2Vec or FastText model on FAQ questions.
        
        Returns:
            Trained embedding model
        """
        # Combine all processed questions for training
        sentences = self.processed_questions
        
        # Train model
        if self.use_fasttext:
            model = FastText(
                sentences=sentences,
                vector_size=100,
                window=5,
                min_count=1,
                workers=4,
                sg=1  # Skip-gram
            )
        else:
            model = Word2Vec(
                sentences=sentences,
                vector_size=100,
                window=5,
                min_count=1,
                workers=4,
                sg=1  # Skip-gram
            )
        
        return model
    
    def _get_sentence_embedding(self, tokens: List[str]) -> np.ndarray:
        """
        Get embedding for a sentence by averaging word embeddings.
        
        Args:
            tokens: List of tokens
            
        Returns:
            Sentence embedding vector
        """
        if not tokens:
            return np.zeros(self.model.vector_size)
        
        embeddings = []
        for token in tokens:
            if token in self.model.wv:
                embeddings.append(self.model.wv[token])
            elif self.use_fasttext:
                # FastText can handle out-of-vocabulary words
                embeddings.append(self.model.wv[token])
        
        if not embeddings:
            return np.zeros(self.model.vector_size)
        
        return np.mean(embeddings, axis=0)
    
    def _compute_embeddings(self, processed_texts: List[List[str]]) -> np.ndarray:
        """
        Compute embeddings for all processed texts.
        
        Args:
            processed_texts: List of processed text tokens
            
        Returns:
            Array of embeddings
        """
        embeddings = []
        for tokens in processed_texts:
            embedding = self._get_sentence_embedding(tokens)
            embeddings.append(embedding)
        
        return np.array(embeddings)
    
    def find_best_match(self, user_input: str, threshold: float = 0.3) -> Tuple[Optional[str], float]:
        """
        Find the best matching FAQ answer for user input.
        
        Args:
            user_input: User's question
            threshold: Minimum similarity threshold
            
        Returns:
            Tuple of (answer, similarity_score) or (None, 0.0) if no match found
        """
        # Preprocess user input
        processed_input = self._preprocess_text(user_input)
        
        if not processed_input:
            return None, 0.0
        
        # Get embedding for user input
        user_embedding = self._get_sentence_embedding(processed_input)
        user_embedding = user_embedding.reshape(1, -1)
        
        # Calculate cosine similarity with all questions
        similarities = cosine_similarity(user_embedding, self.question_embeddings)[0]
        
        # Find best match
        best_idx = np.argmax(similarities)
        best_similarity = similarities[best_idx]
        
        if best_similarity >= threshold:
            return self.answers[best_idx], best_similarity
        
        return None, best_similarity
    
    def get_response(self, user_input: str) -> str:
        """
        Get chatbot response for user input.
        
        Args:
            user_input: User's question
            
        Returns:
            Chatbot response
        """
        answer, similarity = self.find_best_match(user_input)
        
        if answer:
            return answer
        else:
            return "Atsiprašau, bet negaliu rasti tinkamo atsakymo į jūsų klausimą. Prašome kreiptis į klientų aptarnavimo centrą telefonu 1888 arba atvykti į filialą."


if __name__ == "__main__":
    # Example usage
    chatbot = BankingChatbot(use_fasttext=False)
    
    test_questions = [
        "Kaip atidaryti sąskaitą?",
        "Kokie mokesčiai už sąskaitą?",
        "Kaip gauti internetinio banko prieigą?",
        "Kiek kainuoja pavedimas?",
        "Kaip pakeisti PIN kodą?"
    ]
    
    print("Banking Chatbot - Test Run\n")
    print("=" * 50)
    
    for question in test_questions:
        response = chatbot.get_response(question)
        print(f"\nKlausimas: {question}")
        print(f"Atsakymas: {response}")
        print("-" * 50)

