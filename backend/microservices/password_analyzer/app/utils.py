import re
import math
import secrets
import string

def calculate_entropy(password):
    """
    Calculate password entropy (measure of randomness)
    """
    # Define character set sizes
    char_sets = {
        'lowercase': string.ascii_lowercase,
        'uppercase': string.ascii_uppercase,
        'digits': string.digits,
        'symbols': string.punctuation
    }
    
    # Determine which character sets are used
    used_chars = set()
    for char_set_name, char_set in char_sets.items():
        if any(char in char_set for char in password):
            used_chars.update(char_set)
    
    # Calculate entropy
    charset_size = len(used_chars)
    password_length = len(password)
    entropy = password_length * math.log2(charset_size)
    
    return entropy

def analyze_password_strength(password):
    """
    Comprehensive password strength analysis
    """
    # Length check
    length = len(password)
    length_score = min(length / 16, 1.0)  # Normalized score, max at 16 chars
    # Entropy calculation
    entropy = calculate_entropy(password)
    entropy_score = min(entropy / 60, 1.0)  # Normalized score, max at 60 bits
    # Complexity checks
    has_lowercase = bool(re.search(r'[a-z]', password))
    has_uppercase = bool(re.search(r'[A-Z]', password))
    has_digit = bool(re.search(r'\d', password))
    has_symbol = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
 
    complexity_score = sum([
        has_lowercase,
        has_uppercase,
        has_digit,
        has_symbol
    ]) / 4.0 
    
    # Overall strength calculation
    overall_strength = (length_score + entropy_score ) / 2    
    # Categorize strength
    if overall_strength < 0.3:
        strength = "Very Weak"
    elif overall_strength < 0.5:
        strength = "Weak"
    elif overall_strength < 0.7:
        strength = "Moderate"
    elif overall_strength < 1 and complexity_score >=0.25:
        strength = "Strong"
    elif overall_strength == 1 and complexity_score == 1:
        strength = "Very Strong"
    else:
        strength = "Moderate"  # Valeur par défaut

    
    return {
        "strength": strength,
        "score": overall_strength,
        "details": {
            "length": length,
            "entropy": round(entropy, 2),
            "has_lowercase": has_lowercase,
            "has_uppercase": has_uppercase,
            "has_digit": has_digit,
            "has_symbol": has_symbol
        }
    }

def generate_strong_password(base_password=None, length=16):
    """
    Generate a strong password, optionally based on input password
    """
    # Character sets
    lowercase = string.ascii_lowercase
    uppercase = string.ascii_uppercase
    digits = string.digits
    symbols = string.punctuation
    
    # Initialize password_chars with base_password if provided
    password_chars = base_password if base_password else ''
    
    # Ensure mix of character types
    if not any(c in lowercase for c in password_chars):
        password_chars += secrets.choice(lowercase)
    if not any(c in uppercase for c in password_chars):
        password_chars += secrets.choice(uppercase)
    if not any(c in digits for c in password_chars):
        password_chars += secrets.choice(digits)
    if not any(c in symbols for c in password_chars):
        password_chars += secrets.choice(symbols)
    
    # Fill rest with random characters if length is less than required
    remaining_length = length - len(password_chars)
    all_chars = lowercase + uppercase + digits + symbols 
    return password_chars