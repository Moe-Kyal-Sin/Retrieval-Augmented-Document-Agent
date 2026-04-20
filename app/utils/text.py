import re

STOP_WORDS = {
    "the", "is", "a", "an", "and", "or", "but", "if", "then", "else",
    "what", "which", "who", "whom", "this", "that", "these", "those",
    "am", "is", "are", "was", "were", "be", "been", "being",
    "have", "has", "had", "do", "does", "did",
    "of", "in", "on", "at", "to", "for", "with", "about", "from",
    "by", "as", "into", "through", "after", "before", "between",
    "it", "its", "he", "she", "they", "them", "their", "you", "your",
    "we", "our", "i", "me", "my",
    "can", "could", "should", "would", "may", "might", "will",
    "not", "no", "yes"
}


def clean_text(text:str) -> str:
    '''
    normalize newline character for windows and others.
    multiple space into one space
    newline character max 2
    '''
    text = text.replace("\r\n", "\n")
    text = re.sub(r"[ \t]", " ", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text
    
def chunk_text(text:str, chunk_size:int = 500, overlap:int = 100) -> list[str]:
    '''
    Split the original string into a list of strings of length chunk_size with overlap
    '''
    if chunk_size <= 0:
        raise ValueError('Chunk Size cannot be less than or equal to zero')
    if overlap <0:
        raise ValueError('Overlap cannot be negative value')
    if chunk_size < overlap:
        raise ValueError('Overlap cannot be greater than chunk size')
    
    chunks = []
    text_length = len(text)
    start = 0
    while start < text_length:
        end = start + chunk_size
        chunk = text[start:end]

        if chunk.strip():
            chunks.append(chunk)
        start += chunk_size - overlap
    return chunks

def normalize_text(text:str) -> str:
    ''' For keyword searching make everyting
    lowercase
    remove puncuation and special characters
    no more than one space between each text'''
    
    text = text.lower()
    text = re.sub(r"[^a-z0-9\s]", "", text)
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def extract_keywords(text:str) -> list[str]:
    'Given the text, try to extract keywords.'
    'Keywords = words that are not Stopwords'
    text = normalize_text(text)
    keywords = [ word for word in text.split() if word not in STOP_WORDS]
    return keywords
    