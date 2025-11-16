"""
Text preprocessing module for e-contract analysis
"""

import re
import string
from typing import List, Dict, Any
import nltk
from nltk.tokenize import word_tokenize, sent_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer
from nltk.tag import pos_tag
import spacy
from ..utils.config import Config

class TextPreprocessor:
    """Handles text preprocessing for e-contract analysis"""
    
    def __init__(self):
        self.nlp = None
        self.lemmatizer = WordNetLemmatizer()
        self.stop_words = set(stopwords.words('english'))
        self.stop_words.update(Config.STOPWORDS)
        self._load_models()
    
    def _load_models(self):
        """Load required NLP models"""
        try:
            self.nlp = spacy.load(Config.NLP_MODEL)
        except OSError:
            print(f"Spacy model {Config.NLP_MODEL} not found. Please install it using:")
            print(f"python -m spacy download {Config.NLP_MODEL}")
            self.nlp = None
        
        # Download required NLTK data
        try:
            nltk.data.find('tokenizers/punkt')
        except LookupError:
            nltk.download('punkt')
        
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            nltk.download('stopwords')
        
        try:
            nltk.data.find('corpora/wordnet')
        except LookupError:
            nltk.download('wordnet')
        
        try:
            nltk.data.find('taggers/averaged_perceptron_tagger')
        except LookupError:
            nltk.download('averaged_perceptron_tagger')
    
    def clean_text(self, text: str) -> str:
        """
        Clean text by removing noise, special characters, and unwanted symbols
        
        Args:
            text: Raw input text
            
        Returns:
            Cleaned text string
        """
        if not text:
            return ""
        
        # Remove extra whitespace and line breaks
        text = re.sub(r'\s+', ' ', text)
        
        # Remove special characters but keep important punctuation
        text = re.sub(r'[^\w\s.,;:!?()-]', '', text)
        
        # Remove multiple consecutive punctuation marks
        text = re.sub(r'[.,;:!?]{2,}', '.', text)
        
        # Remove extra spaces around punctuation
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)
        text = re.sub(r'([.,;:!?])\s+', r'\1 ', text)
        
        # Remove leading/trailing whitespace
        text = text.strip()
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        """
        Tokenize text into words
        
        Args:
            text: Input text to tokenize
            
        Returns:
            List of tokens
        """
        if not text:
            return []
        
        # Use NLTK tokenizer
        tokens = word_tokenize(text.lower())
        
        # Filter out punctuation and very short words
        tokens = [token for token in tokens 
                 if token not in string.punctuation and len(token) > 1]
        
        return tokens
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        """
        Remove stopwords from token list
        
        Args:
            tokens: List of tokens
            
        Returns:
            Filtered token list
        """
        return [token for token in tokens if token.lower() not in self.stop_words]
    
    def lemmatize(self, tokens: List[str]) -> List[str]:
        """
        Lemmatize tokens to their root forms
        
        Args:
            tokens: List of tokens to lemmatize
            
        Returns:
            List of lemmatized tokens
        """
        return [self.lemmatizer.lemmatize(token) for token in tokens]
    
    def pos_tagging(self, tokens: List[str]) -> List[tuple]:
        """
        Perform part-of-speech tagging on tokens
        
        Args:
            tokens: List of tokens
            
        Returns:
            List of (token, pos_tag) tuples
        """
        return pos_tag(tokens)
    
    def sentence_segmentation(self, text: str) -> List[str]:
        """
        Segment text into sentences
        
        Args:
            text: Input text
            
        Returns:
            List of sentences
        """
        if not text:
            return []
        
        sentences = sent_tokenize(text)
        # Clean each sentence
        sentences = [self.clean_text(sentence) for sentence in sentences]
        # Filter out very short sentences
        sentences = [sentence for sentence in sentences if len(sentence) > 10]
        
        return sentences
    
    def extract_contract_sections(self, text: str) -> Dict[str, str]:
        """
        Extract common contract sections using pattern matching
        
        Args:
            text: Contract text
            
        Returns:
            Dictionary with section names and content
        """
        sections = {}
        
        # Common contract section patterns
        section_patterns = {
            'parties': r'(?i)(parties?|party\s+names?|contracting\s+parties?)[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)',
            'recitals': r'(?i)(recitals?|whereas)[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)',
            'terms': r'(?i)(terms?\s+and\s+conditions?|agreement\s+terms?)[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)',
            'obligations': r'(?i)(obligations?|duties|responsibilities)[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)',
            'payment': r'(?i)(payment|compensation|remuneration)[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)',
            'termination': r'(?i)(termination|expir|end\s+of\s+contract)[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)',
            'governing_law': r'(?i)(governing\s+law|jurisdiction|applicable\s+law)[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)',
            'signatures': r'(?i)(signature|executed|signed)[:\s]*(.*?)(?=\n\n|\n[A-Z]|$)'
        }
        
        for section_name, pattern in section_patterns.items():
            matches = re.findall(pattern, text, re.DOTALL)
            if matches:
                # Take the first match and clean it
                content = matches[0][1] if isinstance(matches[0], tuple) else matches[0]
                sections[section_name] = self.clean_text(content)
        
        return sections
    
    def preprocess_contract(self, text: str) -> Dict[str, Any]:
        """
        Complete preprocessing pipeline for contract text
        
        Args:
            text: Raw contract text
            
        Returns:
            Dictionary containing processed text components
        """
        # Clean the text
        cleaned_text = self.clean_text(text)
        
        # Segment into sentences
        sentences = self.sentence_segmentation(cleaned_text)
        
        # Tokenize
        tokens = self.tokenize(cleaned_text)
        
        # Remove stopwords
        filtered_tokens = self.remove_stopwords(tokens)
        
        # Lemmatize
        lemmatized_tokens = self.lemmatize(filtered_tokens)
        
        # POS tagging
        pos_tags = self.pos_tagging(filtered_tokens)
        
        # Extract contract sections
        sections = self.extract_contract_sections(text)
        
        return {
            'original_text': text,
            'cleaned_text': cleaned_text,
            'sentences': sentences,
            'tokens': tokens,
            'filtered_tokens': filtered_tokens,
            'lemmatized_tokens': lemmatized_tokens,
            'pos_tags': pos_tags,
            'sections': sections,
            'word_count': len(tokens),
            'sentence_count': len(sentences),
            'section_count': len(sections)
        }
    
    def normalize_text(self, text: str) -> str:
        """
        Normalize text for comparison purposes
        
        Args:
            text: Input text
            
        Returns:
            Normalized text
        """
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = re.sub(r'\s+', ' ', text)
        
        # Remove punctuation
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        return text.strip()
    
    def extract_key_phrases(self, text: str, max_phrases: int = 20) -> List[str]:
        """
        Extract key phrases from text using NLP techniques
        
        Args:
            text: Input text
            max_phrases: Maximum number of phrases to extract
            
        Returns:
            List of key phrases
        """
        if not self.nlp or not text:
            return []
        
        doc = self.nlp(text)
        
        # Extract noun phrases
        noun_phrases = [chunk.text.strip() for chunk in doc.noun_chunks 
                       if len(chunk.text.strip()) > 3 and len(chunk.text.split()) <= 4]
        
        # Extract named entities
        entities = [ent.text.strip() for ent in doc.ents 
                   if ent.label_ in Config.ENTITY_TYPES]
        
        # Combine and deduplicate
        key_phrases = list(set(noun_phrases + entities))
        
        # Filter and clean
        key_phrases = [phrase for phrase in key_phrases 
                      if len(phrase) > 3 and not phrase.isdigit()]
        
        # Sort by length (longer phrases first) and limit
        key_phrases.sort(key=len, reverse=True)
        
        return key_phrases[:max_phrases]