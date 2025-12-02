"""
Helper script to download NLTK data manually.
Run this if you encounter NLTK download errors.
"""

import nltk
import sys

def download_nltk_data():
    """Download required NLTK data."""
    print("Downloading NLTK data...")
    
    try:
        print("Downloading punkt tokenizer...")
        nltk.download('punkt', quiet=False)
        print("✓ punkt downloaded successfully")
    except Exception as e:
        print(f"✗ Error downloading punkt: {e}")
        print("The app will use a fallback tokenization method.")
    
    try:
        print("\nDownloading stopwords...")
        nltk.download('stopwords', quiet=False)
        print("✓ stopwords downloaded successfully")
    except Exception as e:
        print(f"✗ Error downloading stopwords: {e}")
        print("The app will use a basic stopword list.")
    
    print("\nNLTK setup complete!")

if __name__ == "__main__":
    download_nltk_data()

