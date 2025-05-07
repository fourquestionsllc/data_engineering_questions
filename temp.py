import re

def insert_space_around_symbols(text: str) -> str:
    # Step 1: Protect decimals and comma numbers
    text = re.sub(r'(\d+)\.(\d+)', r'\1DOTDOTDOT\2', text)
    text = re.sub(r'(\d+),(\d+)', r'\1COMMACOMMACOMMA\2', text)

    # Step 2: Add spaces around substrings of non-alphanumeric characters (excluding whitespace)
    text = re.sub(r'([^a-zA-Z0-9\s]+)', r' \1 ', text)

    # Step 3: Normalize multiple spaces
    text = re.sub(r'\s+', ' ', text).strip()

    # Step 4: Restore protected decimal and comma patterns
    text = text.replace('DOTDOTDOT', '.').replace('COMMACOMMACOMMA', ',')

    return text
