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
    # 1. Use regex for patterns (case-insensitive for the name part now)
    patterns = [
        r'\bto\s+([A-Za-z]+)\b',          
        r'\bsend\s+money\s+to\s+([A-Za-z]+)\b', 
        r'\btransfer\s+to\s+([A-Za-z]+)\b',   
        r'\bpay\s+([A-Za-z]+)\b'           
    ]
    
    for pattern in patterns:
        # Use re.IGNORECASE for the match
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            name = match.group(1)
            # Ensure the "name" isn't actually the amount or a small stopword
            if not name.isdigit() and len(name) > 2:
                return name.capitalize() # Normalize for the UI
            
    # 2. Token-based fallback: look for words after 'to' or 'for'
    tokens = text.split()
    for i in range(1, len(tokens)):
        prev = tokens[i-1].lower()
        curr = tokens[i].strip('.,!?')
        
        if prev in ['to', 'for']:
            # If current word is mostly alphabetic and not a small functional word
            if curr.isalpha() and len(curr) > 2 and curr.lower() not in ['this', 'that', 'them']:
                return curr.capitalize()
            
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
