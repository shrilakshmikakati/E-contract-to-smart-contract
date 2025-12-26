
import re
from typing import List, Dict, Any, Tuple
from collections import defaultdict, Counter
try:
    import spacy
    from spacy.matcher import Matcher
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False
    print("Spacy not available. Install with: pip install spacy")

try:
    import nltk
    from nltk.chunk import ne_chunk
    from nltk.tag import pos_tag
    from nltk.tokenize import word_tokenize
    NLTK_AVAILABLE = True
except ImportError:
    NLTK_AVAILABLE = False
    print("NLTK not available. Install with: pip install nltk")

try:
    from ..utils.config import Config
except ImportError:
    from utils.config import Config

class EntityExtractor:
    
    def __init__(self):
        self.nlp = None
        self.matcher = None
        self._load_models()
        self._setup_patterns()
    
    def _load_models(self):
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load(Config.NLP_MODEL)
                self.matcher = Matcher(self.nlp.vocab)
            except OSError:
                self.nlp = None
    
    def _setup_patterns(self):
        if not self.matcher:
            return
        
        patterns = {
            "CONTRACT_PARTY": [
                [{"LOWER": {"IN": ["party", "parties", "contractor", "client", "vendor"]}},
                 {"IS_ALPHA": True, "OP": "+"}],
                [{"LOWER": "between"}, {"IS_ALPHA": True, "OP": "+"}, {"LOWER": "and"}, {"IS_ALPHA": True, "OP": "+"}]
            ],
            "MONETARY_AMOUNT": [
                [{"LIKE_NUM": True}, {"LOWER": {"IN": ["dollars", "usd", "eur", "euro", "pounds", "gbp"]}}],
                [{"TEXT": {"REGEX": r"^\$\d+"}}, {"OP": "?"}],
                [{"LOWER": {"IN": ["payment", "fee", "cost", "price", "amount"]}}, {"LIKE_NUM": True}]
            ],
            "DATE_TERMS": [
                [{"LOWER": {"IN": ["by", "before", "after", "on", "within"]}}, 
                 {"LIKE_NUM": True}, {"LOWER": {"IN": ["days", "months", "years", "weeks"]}}],
                [{"SHAPE": "dd/dd/dddd"}],
                [{"SHAPE": "dd-dd-dddd"}]
            ],
            "OBLIGATIONS": [
                [{"LOWER": {"IN": ["shall", "must", "will", "agrees", "undertakes"]}}, 
                 {"POS": "VERB", "OP": "+"}],
                [{"LOWER": {"IN": ["responsible", "liable", "obligated"]}}, {"LOWER": "for"}]
            ],
            "LEGAL_TERMS": [
                [{"LOWER": {"IN": ["whereas", "therefore", "notwithstanding", "pursuant"]}},
                 {"OP": "*"}],
                [{"LOWER": "governing"}, {"LOWER": "law"}],
                [{"LOWER": {"IN": ["jurisdiction", "venue", "arbitration", "mediation"]}}]
            ]
        }
        
        for pattern_name, pattern_list in patterns.items():
            self.matcher.add(pattern_name, pattern_list)
    
    def extract_named_entities_spacy(self, text: str) -> List[Dict[str, Any]]:
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        entities = []
        
        for ent in doc.ents:
            if ent.label_ in Config.ENTITY_TYPES:
                entities.append({
                    'text': ent.text.strip(),
                    'label': ent.label_,
                    'start': ent.start_char,
                    'end': ent.end_char,
                    'confidence': ent._.get('confidence', 1.0) if hasattr(ent._, 'confidence') else 1.0
                })
        
        return entities
    
    def extract_named_entities_nltk(self, text: str) -> List[Dict[str, Any]]:
        if not NLTK_AVAILABLE:
            return []
        
        try:
            tokens = word_tokenize(text)
            pos_tags = pos_tag(tokens)
            chunks = ne_chunk(pos_tags)
            
            entities = []
            for chunk in chunks:
                if hasattr(chunk, 'label'):
                    entity_text = ' '.join([token for token, pos in chunk])
                    entities.append({
                        'text': entity_text,
                        'label': chunk.label(),
                        'start': -1,  # NLTK doesn't provide character positions
                        'end': -1,
                        'confidence': 0.8  # Default confidence for NLTK
                    })
        except Exception as e:
            print(f"NLTK entity extraction failed: {e}. Using regex fallback.")
            return self.extract_regex_entities(text)
        
        return entities
    
    def extract_contract_patterns(self, text: str) -> List[Dict[str, Any]]:
        if not self.matcher:
            return []
        
        doc = self.nlp(text)
        matches = self.matcher(doc)
        
        pattern_entities = []
        for match_id, start, end in matches:
            span = doc[start:end]
            label = self.nlp.vocab.strings[match_id]
            
            pattern_entities.append({
                'text': span.text,
                'label': label,
                'start': span.start_char,
                'end': span.end_char,
                'confidence': 0.9,
                'type': 'pattern'
            })
        
        return pattern_entities
    
    def extract_regex_entities(self, text: str) -> List[Dict[str, Any]]:
        regex_patterns = {
            'EMAIL': r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            'PHONE': r'\b(?:\+?1[-.\s]?)?\(?[0-9]{3}\)?[-.\s]?[0-9]{3}[-.\s]?[0-9]{4}\b',
            'DATE': r'\b\d{1,2}[/-]\d{1,2}[/-]\d{2,4}\b|\b\d{4}[/-]\d{1,2}[/-]\d{1,2}\b',
            'CURRENCY': r'\$\d+(?:,\d{3})*(?:\.\d{2})?|\b\d+(?:,\d{3})*(?:\.\d{2})?\s*(?:dollars?|USD|euros?|EUR|pounds?|GBP)\b',
            'PERCENTAGE': r'\b\d+(?:\.\d+)?%\b',
            'CONTRACT_REF': r'\b(?:contract|agreement|clause|section|paragraph)\s+(?:no\.?\s*)?\d+(?:\.\d+)*\b',
            'ADDRESS': r'\b\d+\s+[A-Za-z\s,]+(?:Street|St|Avenue|Ave|Road|Rd|Boulevard|Blvd|Lane|Ln|Drive|Dr|Court|Ct|Place|Pl)\b'
        }
        
        entities = []
        for label, pattern in regex_patterns.items():
            matches = re.finditer(pattern, text, re.IGNORECASE)
            for match in matches:
                entities.append({
                    'text': match.group(),
                    'label': label,
                    'start': match.start(),
                    'end': match.end(),
                    'confidence': 0.85,
                    'type': 'regex'
                })
        
        return entities
    
    def extract_domain_entities(self, text: str) -> List[Dict[str, Any]]:
        domain_keywords = {
            'PARTIES': [
                'plaintiff', 'defendant', 'contractor', 'subcontractor', 'client',
                'vendor', 'supplier', 'buyer', 'seller', 'lessor', 'lessee',
                'licensor', 'licensee', 'employer', 'employee', 'principal', 'agent'
            ],
            'OBLIGATIONS': [
                'shall provide', 'agrees to', 'undertakes to', 'commits to',
                'responsible for', 'liable for', 'duty to', 'obligation to',
                'required to', 'bound to', 'covenant to'
            ],
            'CONDITIONS': [
                'subject to', 'provided that', 'on condition that', 'if and when',
                'in the event', 'unless otherwise', 'except as', 'save for'
            ],
            'TEMPORAL': [
                'effective date', 'commencement date', 'expiration date', 'due date',
                'within days', 'no later than', 'prior to', 'following'
            ],
            'FINANCIAL': [
                'payment terms', 'invoice', 'remuneration', 'compensation',
                'fee structure', 'interest rate', 'penalty', 'damages'
            ]
        }
        
        entities = []
        text_lower = text.lower()
        
        for category, keywords in domain_keywords.items():
            for keyword in keywords:
                pattern = r'\b' + re.escape(keyword) + r'\b'
                matches = re.finditer(pattern, text_lower)
                for match in matches:
                    original_text = text[match.start():match.end()]
                    entities.append({
                        'text': original_text,
                        'label': category,
                        'start': match.start(),
                        'end': match.end(),
                        'confidence': 0.75,
                        'type': 'domain'
                    })
        
        return entities
    
    def merge_overlapping_entities(self, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not entities:
            return []
        
        sorted_entities = sorted(entities, key=lambda x: (x['start'], -x['confidence']))
        merged = []
        
        for entity in sorted_entities:
            overlap_found = False
            for i, merged_entity in enumerate(merged):
                if (entity['start'] < merged_entity['end'] and 
                    entity['end'] > merged_entity['start']):
                    if entity['confidence'] > merged_entity['confidence']:
                        merged[i] = entity
                    overlap_found = True
                    break
            
            if not overlap_found:
                merged.append(entity)
        
        return merged
    
    def extract_all_entities(self, text: str) -> List[Dict[str, Any]]:
        all_entities = []
        
        if self.nlp:
            all_entities.extend(self.extract_named_entities_spacy(text))
            all_entities.extend(self.extract_contract_patterns(text))
        else:
            all_entities.extend(self.extract_named_entities_nltk(text))
        
        all_entities.extend(self.extract_regex_entities(text))
        all_entities.extend(self.extract_domain_entities(text))
        
        merged_entities = self.merge_overlapping_entities(all_entities)
        
        filtered_entities = [e for e in merged_entities if e['confidence'] >= 0.5]
        
        for i, entity in enumerate(filtered_entities):
            entity['id'] = f"entity_{i}"
        
        return filtered_entities
    
    def categorize_entities(self, entities: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        categorized = defaultdict(list)
        
        for entity in entities:
            category = entity['label']
            categorized[category].append(entity)
        
        return dict(categorized)
    
    def get_entity_statistics(self, entities: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not entities:
            return {}
        
        labels = [e['label'] for e in entities]
        label_counts = Counter(labels)
        
        return {
            'total_entities': len(entities),
            'unique_labels': len(label_counts),
            'label_distribution': dict(label_counts),
            'average_confidence': sum(e['confidence'] for e in entities) / len(entities),
            'confidence_range': {
                'min': min(e['confidence'] for e in entities),
                'max': max(e['confidence'] for e in entities)
            }
        }