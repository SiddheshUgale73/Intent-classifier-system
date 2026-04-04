import re

def extract_amount(text: str):
    """
    Extracts numerical amounts from text.
    Supports integers and decimals.
    """
    # Regex to find numbers (e.g., 500, 1200.50, 1,000)
    # Removing commas for processing
    clean_text = text.replace(',', '')
    matches = re.findall(r'\b\d+(?:\.\d{1,2})?\b', clean_text)
    
    if matches:
        # Return the first found amount as a float
        try:
            return float(matches[0])
        except ValueError:
            return None
    return None

def extract_receiver(text: str):
    """
    Extracts the receiver's name from text using rule-based logic.
    Focuses on words following common keywords like 'to', 'transfer to', 'send to'.
    """
    # Common patterns for banking transfers
    patterns = [
        r'\bto\s+([A-Z][a-z]+)\b',          # "to John"
        r'\bsend\s+money\s+to\s+([A-Z][a-z]+)\b', # "send money to John"
        r'\btransfer\s+to\s+([A-Z][a-z]+)\b',   # "transfer to John"
        r'\bpay\s+([A-Z][a-z]+)\b'           # "pay John"
    ]
    
    for pattern in patterns:
        match = re.search(pattern, text)
        if match:
            return match.group(1)
            
    # Fallback: look for any capitalized word that isn't at the start 
    # and follows common prepositions (if not already matched)
    tokens = text.split()
    for i in range(1, len(tokens)):
        if tokens[i-1].lower() in ['to', 'for'] and tokens[i][0].isupper():
            return tokens[i].rstrip('.,!?')
            
    return None

def extract_entities(text: str):
    """
    Main entry point for entity extraction.
    Returns a dictionary of found entities.
    """
    return {
        "amount": extract_amount(text),
        "receiver": extract_receiver(text)
    }

if __name__ == "__main__":
    # Test cases
    test_inputs = [
        "Transfer 500 to John",
        "Send 1200.50 to Sarah please",
        "I want to pay Mike 50 bucks",
        "Can you send money to Dave?",
        "Check my balance"
    ]
    
    for inp in test_inputs:
        print(f"Input: '{inp}'")
        print(f"Output: {extract_entities(inp)}\n")
