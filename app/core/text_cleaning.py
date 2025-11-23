import re
import unicodedata

def clean_text(text):
    if not isinstance(text, str):
        return ""

    # 1. Unicode Normalization (NFKC)
    # This converts "fancy" characters to their standard equivalents.
    # Example: It turns the special hyphen '‐' (U+2010) into a standard '-' (U+002D).
    text = unicodedata.normalize('NFKC', text)

    # 2. Remove non-printable control characters (if any exist)
    # This creates a translation table to map control characters to None
    text = "".join(ch for ch in text if unicodedata.category(ch)[0] != "C")

    # 3. Collapse Whitespace
    # Replaces newlines, tabs, and multiple spaces with a single space.
    text = re.sub(r'\s+', ' ', text)

    # 4. Remove single and double quotes
    text = re.sub(r'["\']', '', text)

    return text.strip()
