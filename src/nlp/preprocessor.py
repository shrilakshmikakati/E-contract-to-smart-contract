
import re
import string
from typing import List, Dict, Any
import re
import string
from typing import List, Dict, Any
try:
    import nltk
    from nltk.tokenize import word_tokenize, sent_tokenize
    from nltk.corpus import stopwords
    from nltk.stem import WordNetLemmatizer
    from nltk.tag import pos_tag
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    print("NLTK not available, using basic preprocessing")

try:
    import spacy
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    print("spaCy not available, using basic preprocessing")

try:
    from ..utils.config import Config
except ImportError:
    from utils.config import Config

class TextPreprocessor:
    
    def __init__(self):
        self.nlp = None
        self.lemmatizer = None
        self.stop_words = set()
        self.nltk_available = NLTK_AVAILABLE
        self.spacy_available = SPACY_AVAILABLE
        self._load_models()
    
    def _load_models(self):
        
        if self.spacy_available:
            try:
                self.nlp = spacy.load(Config.NLP_MODEL)
                print(f"✓ Loaded spaCy model: {Config.NLP_MODEL}")
            except OSError:
                if not hasattr(TextPreprocessor, '_spacy_warning_shown'):
                    print(f"⚠️  spaCy model {Config.NLP_MODEL} not found. Using fallback processing.")
                    TextPreprocessor._spacy_warning_shown = True
                self.nlp = None
        else:
            if not hasattr(TextPreprocessor, '_spacy_unavailable_shown'):
                print("⚠️  spaCy not available. Using fallback processing.")
                TextPreprocessor._spacy_unavailable_shown = True
        
        if self.nltk_available:
            try:
                self._setup_nltk_data()
                
                self.lemmatizer = WordNetLemmatizer()
                
                try:
                    self.stop_words = set(stopwords.words('english'))
                    self.stop_words.update(Config.STOPWORDS)
                    print("✓ Loaded NLTK stopwords")
                except Exception as e:
                    print(f"Error loading stopwords: {e}. Using basic stopwords.")
                    self.stop_words = self._get_basic_stopwords()
                    
            except Exception as e:
                print(f"Error setting up NLTK: {e}. Using basic preprocessing.")
                self.nltk_available = False
                self._setup_fallback_processing()
        else:
            self._setup_fallback_processing()
    
    def _setup_nltk_data(self):
        required_data = [
            ('tokenizers/punkt', 'punkt'),
            ('tokenizers/punkt_tab', 'punkt_tab'), 
            ('corpora/stopwords', 'stopwords'),
            ('corpora/wordnet', 'wordnet'),
            ('taggers/averaged_perceptron_tagger', 'averaged_perceptron_tagger'),
            ('taggers/averaged_perceptron_tagger_eng', 'averaged_perceptron_tagger_eng'),
            ('chunkers/maxent_ne_chunker', 'maxent_ne_chunker'),
            ('chunkers/maxent_ne_chunker_tab', 'maxent_ne_chunker_tab'),
            ('corpora/words', 'words')
        ]
        
        for data_path, package_name in required_data:
            try:
                nltk.data.find(data_path)
            except LookupError:
                try:
                    print(f"Downloading NLTK {package_name}...")
                    nltk.download(package_name, quiet=True)
                except Exception as e:
                    print(f"Warning: Could not download {package_name}: {e}")
    
    def _setup_fallback_processing(self):
        self.lemmatizer = None
        self.stop_words = self._get_basic_stopwords()
        print("✓ Setup fallback text processing")
    
    def _get_basic_stopwords(self):
        return set([
            'the', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 
            'by', 'from', 'up', 'about', 'into', 'through', 'during', 'before', 
            'after', 'above', 'below', 'between', 'among', 'within', 'without', 
            'across', 'a', 'an', 'as', 'are', 'was', 'were', 'been', 'be', 'have', 
            'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could', 'should', 
            'may', 'might', 'must', 'can', 'this', 'that', 'these', 'those', 'i', 
            'you', 'he', 'she', 'it', 'we', 'they', 'me', 'him', 'her', 'us', 'them'
        ])
    
    def clean_text(self, text: str) -> str:
        if not text:
            return ""
        
        text = re.sub(r'\s+', ' ', text)
        
        text = re.sub(r'[^\w\s.,;:!?()-]', '', text)
        
        text = re.sub(r'[.,;:!?]{2,}', '.', text)
        
        text = re.sub(r'\s+([.,;:!?])', r'\1', text)
        text = re.sub(r'([.,;:!?])\s+', r'\1 ', text)
        
        text = text.strip()
        
        return text
    
    def tokenize(self, text: str) -> List[str]:
        if not text:
            return []
        
        if self.nltk_available:
            try:
                tokens = word_tokenize(text.lower())
            except Exception as e:
                print(f"NLTK tokenization failed: {e}. Using fallback tokenization.")
                tokens = self._fallback_tokenize(text)
        else:
            tokens = self._fallback_tokenize(text)
        
        tokens = [token for token in tokens 
                 if token not in string.punctuation and len(token) > 1]
        
        return tokens
    
    def _fallback_tokenize(self, text: str) -> List[str]:
        import string
        text = text.lower()
        for char in string.punctuation:
            text = text.replace(char, ' ')
        tokens = [token.strip() for token in text.split() if token.strip()]
        return tokens
    
    def remove_stopwords(self, tokens: List[str]) -> List[str]:
        return [token for token in tokens if token.lower() not in self.stop_words]
    
    def lemmatize(self, tokens: List[str]) -> List[str]:
        if self.lemmatizer:
            try:
                return [self.lemmatizer.lemmatize(token) for token in tokens]
            except Exception as e:
                print(f"Lemmatization failed: {e}. Returning original tokens.")
                return tokens
        else:
            return [self._simple_lemmatize(token) for token in tokens]
    
    def _simple_lemmatize(self, word: str) -> str:
        suffixes = ['ing', 'ed', 'er', 'est', 'ly', 's']
        word = word.lower()
        for suffix in suffixes:
            if word.endswith(suffix) and len(word) > len(suffix) + 2:
                return word[:-len(suffix)]
        return word
    
    def pos_tagging(self, tokens: List[str]) -> List[tuple]:
        if self.nltk_available:
            try:
                return pos_tag(tokens)
            except Exception as e:
                print(f"POS tagging failed: {e}. Using basic tagging.")
                return self._basic_pos_tag(tokens)
        else:
            return self._basic_pos_tag(tokens)
    
    def _basic_pos_tag(self, tokens: List[str]) -> List[tuple]:
        tagged = []
        for token in tokens:
            if token.endswith('ing') or token.endswith('ed'):
                tag = 'VB'  # Verb
            elif token.endswith('ly'):
                tag = 'RB'  # Adverb  
            elif token.endswith('er') or token.endswith('est'):
                tag = 'JJ'  # Adjective
            elif token.endswith('s') and len(token) > 3:
                tag = 'NNS'  # Plural noun
            else:
                tag = 'NN'  # Default to noun
            tagged.append((token, tag))
        return tagged
    
    def sentence_segmentation(self, text: str) -> List[str]:
        if not text:
            return []
        
        if self.nltk_available:
            try:
                sentences = sent_tokenize(text)
            except Exception as e:
                print(f"NLTK sentence tokenization failed: {e}. Using fallback.")
                sentences = self._fallback_sentence_tokenize(text)
        else:
            sentences = self._fallback_sentence_tokenize(text)
        
        sentences = [self.clean_text(sentence) for sentence in sentences]
        sentences = [sentence for sentence in sentences if len(sentence) > 10]
        
        return sentences
    
    def _fallback_sentence_tokenize(self, text: str) -> List[str]:
        import re
        sentence_endings = re.compile(r'(?<=[.!?])\s+(?=[A-Z])')
        sentences = sentence_endings.split(text)
        all_sentences = []
        for sentence in sentences:
            paragraphs = sentence.split('\n\n')
            for paragraph in paragraphs:
                lines = re.split(r'\n(?=[A-Z])', paragraph)
                all_sentences.extend(lines)
        
        return [s.strip() for s in all_sentences if s.strip()]
    
    def extract_contract_sections(self, text: str) -> Dict[str, str]:
        sections = {}
        
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
                content = matches[0][1] if isinstance(matches[0], tuple) else matches[0]
                sections[section_name] = self.clean_text(content)
        
        return sections
    
    def preprocess_contract(self, text: str) -> Dict[str, Any]:
        cleaned_text = self.clean_text(text)
        
        sentences = self.sentence_segmentation(cleaned_text)
        
        tokens = self.tokenize(cleaned_text)
        
        filtered_tokens = self.remove_stopwords(tokens)
        
        lemmatized_tokens = self.lemmatize(filtered_tokens)
        
        pos_tags = self.pos_tagging(filtered_tokens)
        
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
        text = text.lower()
        
        text = re.sub(r'\s+', ' ', text)
        
        text = text.translate(str.maketrans('', '', string.punctuation))
        
        return text.strip()
    
    def extract_key_phrases(self, text: str, max_phrases: int = 20) -> List[str]:
        if not self.nlp or not text:
            return []
        
        doc = self.nlp(text)
        
        noun_phrases = [chunk.text.strip() for chunk in doc.noun_chunks 
                       if len(chunk.text.strip()) > 3 and len(chunk.text.split()) <= 4]
        
        entities = [ent.text.strip() for ent in doc.ents 
                   if ent.label_ in Config.ENTITY_TYPES]
        
        key_phrases = list(set(noun_phrases + entities))
        
        key_phrases = [phrase for phrase in key_phrases 
                      if len(phrase) > 3 and not phrase.isdigit()]
        
        key_phrases.sort(key=len, reverse=True)
        
        return key_phrases[:max_phrases]