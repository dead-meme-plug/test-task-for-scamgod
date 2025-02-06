import spacy
from typing import List, Dict
from collections import Counter

class TextAnalyzer:
    
    def __init__(self, language_model: str = "ru_core_news_sm"):
        self.nlp = spacy.load(language_model)
        
    def extract_keywords(self, text: str, top_n: int = 10) -> List[str]:
        doc = self.nlp(text)
        keywords = [
            token.lemma_.lower() for token in doc 
            if not token.is_stop and not token.is_punct and not token.is_space
        ]
        return [word for word, _ in Counter(keywords).most_common(top_n)]
    
    def analyze_sentiment(self, text: str) -> float:
        doc = self.nlp(text)
        sentiment = 0
        for token in doc:
            if token.sentiment != 0:
                sentiment += token.sentiment
        return sentiment / len(doc) if len(doc) > 0 else 0
    
    def get_word_frequencies(self, text: str) -> Dict[str, int]:
        doc = self.nlp(text)
        words = [
            token.lemma_.lower() for token in doc 
            if not token.is_punct and not token.is_stop
        ]
        return dict(Counter(words))
    
    def lemmatize_text(self, text: str) -> str:
        doc = self.nlp(text)
        return " ".join([token.lemma_ for token in doc])
    
    def analyze_article(self, text: str) -> dict:
        return {
            "keywords": self.extract_keywords(text),
            "sentiment": self.analyze_sentiment(text),
            "word_frequencies": self.get_word_frequencies(text),
            "lemmatized_text": self.lemmatize_text(text)
        }
    
    def extract_topics(self, text: str, top_n: int = 3) -> List[str]:
        doc = self.nlp(text)
        nouns = [token.lemma_.lower() for token in doc if token.pos_ == "NOUN"]
        return [word for word, _ in Counter(nouns).most_common(top_n)]