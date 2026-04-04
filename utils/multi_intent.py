import re
import os
import sys
import json
from datetime import datetime

# Add parent directory to sys.path for local imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from model.predict import predict_intent

# Path to the knowledge base
KNOWLEDGE_BASE_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "intent_knowledge.json")

def load_intent_knowledge():
    """
    Loads intent descriptions and approaches from the JSON file.
    """
    if not os.path.exists(KNOWLEDGE_BASE_PATH):
        return {}
    try:
        with open(KNOWLEDGE_BASE_PATH, 'r') as f:
            return json.load(f)
    except Exception as e:
        print(f"Error loading intent knowledge: {e}")
        return {}

# Shared state to avoid reloading knowledge on every request
_intent_kb = load_intent_knowledge()

def detect_multi_intent(text: str):
    """
    Splits the user input into sub-sentences based on conjunctions and processes each for intent and entities.
    Returns: A dictionary formatted for the multi-intent response.
    """
    # 1. Splitting logic
    # Using regex to split on 'and', 'then', 'also', and commas (,) while preserving some structure
    delimiters = r'\band\b|\bthen\b|\balso\b|,'
    raw_fragments = re.split(delimiters, text, flags=re.IGNORECASE)
    
    # Clean fragments: strip whitespace and filter out trivial ones (e.g., " ")
    fragments = [f.strip() for f in raw_fragments if len(f.strip()) > 3]
    
    # Fallback: if no valid fragments, treat the whole text as one
    if not fragments:
        fragments = [text.strip()]
        
    results = []
    
    for fragment in fragments:
        # 2. Process each fragment
        try:
            # Reusing the existing predict_intent (which also handles entity extraction for that string)
            prediction = predict_intent(fragment)
            intent_name = prediction["intent"]
            
            # 3. Enrich with Knowledge Base
            kb_info = _intent_kb.get(intent_name, _intent_kb.get("UNCERTAIN", {}))
            
            # 4. Construct fragment object
            intent_obj = {
                "intent": intent_name,
                "confidence": prediction["confidence"],
                "entities": prediction["entities"],
                "description": kb_info.get("description", "No description available."),
                "common_approaches": kb_info.get("approaches", [])
            }
            results.append(intent_obj)
            
        except Exception as e:
            print(f"Error processing fragment '{fragment}': {e}")
            continue

    # 5. Final Response Structure
    return {
        "status": "success",
        "input": text,
        "intents": results,
        "timestamp": datetime.now().isoformat()
    }

if __name__ == "__main__":
    # Test block
    test_text = "Transfer 500 dollars to Rahul, also check my balance and then block my card"
    print(f"Testing multi-intent for: '{test_text}'")
    result = detect_multi_intent(test_text)
    print(json.dumps(result, indent=2))
