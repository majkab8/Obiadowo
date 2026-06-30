import re

def clean_recipe_text(raw_text):
    """Cleaning text from unnecessary HTML tags."""

    text = raw_text.replace('[ więcej ]', '').replace('[więcej]', '')
    text = re.sub(r'---.*?---', '', text)
    text = text.replace('Składniki:', '')
    lines = [line.strip() for line in text.split('\n') if line.strip()]
    return '\n'.join(lines)