import re
import nltk
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

# Ensure NLTK resources are available
try:
    nltk.data.find('corpora/stopwords')
    nltk.data.find('corpora/wordnet')
except LookupError:
    nltk.download('stopwords')
    nltk.download('wordnet')
    nltk.download('omw-1.4')

def clean_text(text: str) -> str:
    """
    Core cleaning function:
    - Lowercase
    - Remove special characters
    - Remove extra spaces
    """
    if not isinstance(text, str):
        return ""
    
    # 1. Lowercase
    text = text.lower()
    
    # 2. Remove special characters (keep alphanumeric and spaces)
    text = re.sub(r'[^a-zA-Z0-9\s]', ' ', text)
    
    # 3. Remove extra spaces
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def preprocess_pipeline(text: str) -> str:
    """
    Full preprocessing pipeline:
    - Initial cleaning
    - Stopword removal
    - Lemmatization (reusable and production-ready NLP pipeline)
    """
    # Step 1: Basic cleaning
    text = clean_text(text)
    
    # Step 2: Advanced NLP (Lemmatization & Stopwords)
    lemmatizer = WordNetLemmatizer()
    stop_words = set(stopwords.words('english'))
    
    tokens = text.split()
    tokens = [lemmatizer.lemmatize(word) for word in tokens if word not in stop_words]
    
    return " ".join(tokens)

if __name__ == "__main__":
    test_input = "  Hello! This is a TEST with special characters: @#$%^&* and extra    spaces!!  "
    
    print(f"Original: '{test_input}'")
    print(f"Cleaned : '{clean_text(test_input)}'")
    print(f"Pipeline: '{preprocess_pipeline(test_input)}'")
