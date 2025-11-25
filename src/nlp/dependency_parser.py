
import re
from typing import List, Dict, Any, Tuple, Set
from collections import defaultdict
from itertools import combinations

try:
    import spacy
    from spacy.tokens import Token
    SPACY_AVAILABLE = True
except ImportError:
    SPACY_AVAILABLE = False

try:
    from ..utils.config import Config
except ImportError:
    from utils.config import Config

class DependencyParser:
    
    def __init__(self):
        self.nlp = None
        self._load_models()
        self.relationship_patterns = self._define_relationship_patterns()
    
    def _load_models(self):
        if SPACY_AVAILABLE:
            try:
                self.nlp = spacy.load(Config.NLP_MODEL)
            except OSError:
                print(f"Spacy model {Config.NLP_MODEL} not found")
                self.nlp = None
    
    def _define_relationship_patterns(self) -> Dict[str, List[str]]:
        return {
            'obligation': [
                'shall', 'must', 'will', 'agrees to', 'undertakes to',
                'commits to', 'is required to', 'is obligated to'
            ],
            'permission': [
                'may', 'can', 'is permitted to', 'has the right to',
                'is authorized to', 'is allowed to'
            ],
            'prohibition': [
                'shall not', 'must not', 'cannot', 'is prohibited from',
                'is forbidden to', 'may not'
            ],
            'condition': [
                'if', 'unless', 'provided that', 'subject to',
                'on condition that', 'in the event that'
            ],
            'temporal': [
                'before', 'after', 'during', 'within', 'by',
                'no later than', 'prior to', 'following'
            ],
            'financial': [
                'pays', 'receives', 'owes', 'is liable for',
                'compensates', 'reimburses', 'charges'
            ],
            'ownership': [
                'owns', 'belongs to', 'is property of',
                'has title to', 'possesses'
            ],
            'agency': [
                'represents', 'acts on behalf of', 'is agent of',
                'has authority to', 'is authorized by'
            ]
        }
    
    def extract_dependencies_spacy(self, text: str) -> List[Dict[str, Any]]:
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        dependencies = []
        
        for sent in doc.sents:
            for token in sent:
                if token.dep_ != 'ROOT':
                    dependency = {
                        'head': token.head.text,
                        'head_pos': token.head.pos_,
                        'dependent': token.text,
                        'dependent_pos': token.pos_,
                        'relation': token.dep_,
                        'sentence': sent.text,
                        'confidence': 0.9
                    }
                    dependencies.append(dependency)
        
        return dependencies
    
    def extract_entity_relationships(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        relationships = []
        
        entity_spans = {}
        for entity in entities:
            start, end = entity.get('start', -1), entity.get('end', -1)
            if start >= 0 and end >= 0:
                entity_spans[(start, end)] = entity
        
        for sent in doc.sents:
            sent_entities = []
            for start, end in entity_spans.keys():
                if start >= sent.start_char and end <= sent.end_char:
                    sent_entities.append(entity_spans[(start, end)])
            
            if len(sent_entities) >= 2:
                for entity1, entity2 in combinations(sent_entities, 2):
                    relationship = self._find_relationship_in_sentence(
                        sent.text, entity1, entity2
                    )
                    if relationship:
                        relationships.append(relationship)
        
        return relationships
    
    def _find_relationship_in_sentence(self, sentence: str, entity1: Dict[str, Any], 
                                     entity2: Dict[str, Any]) -> Dict[str, Any]:
        sentence_lower = sentence.lower()
        entity1_text = entity1['text'].lower()
        entity2_text = entity2['text'].lower()
        
        entity1_pos = sentence_lower.find(entity1_text)
        entity2_pos = sentence_lower.find(entity2_text)
        
        if entity1_pos == -1 or entity2_pos == -1:
            return None
        
        start_pos = min(entity1_pos, entity2_pos)
        end_pos = max(entity1_pos + len(entity1_text), entity2_pos + len(entity2_text))
        between_text = sentence_lower[start_pos:end_pos]
        
        for relation_type, patterns in self.relationship_patterns.items():
            for pattern in patterns:
                if pattern in between_text:
                    return {
                        'source': entity1['text'],
                        'target': entity2['text'],
                        'relation': relation_type,
                        'pattern': pattern,
                        'sentence': sentence,
                        'confidence': 0.8,
                        'source_type': entity1.get('label', 'UNKNOWN'),
                        'target_type': entity2.get('label', 'UNKNOWN')
                    }
        
        return {
            'source': entity1['text'],
            'target': entity2['text'],
            'relation': 'co_occurrence',
            'pattern': 'same_sentence',
            'sentence': sentence,
            'confidence': 0.5,
            'source_type': entity1.get('label', 'UNKNOWN'),
            'target_type': entity2.get('label', 'UNKNOWN')
        }
    
    def extract_grammatical_relationships(self, text: str) -> List[Dict[str, Any]]:
        if not self.nlp:
            return []
        
        doc = self.nlp(text)
        relationships = []
        
        important_relations = [
            'nsubj',    # nominal subject
            'dobj',     # direct object
            'prep',     # prepositional modifier
            'agent',    # agent of passive
            'poss',     # possession modifier
            'compound', # compound modifier
            'amod',     # adjectival modifier
            'appos',    # appositional modifier
        ]
        
        for sent in doc.sents:
            for token in sent:
                if token.dep_ in important_relations:
                    relationship = {
                        'head': token.head.text,
                        'dependent': token.text,
                        'relation': token.dep_,
                        'head_lemma': token.head.lemma_,
                        'dependent_lemma': token.lemma_,
                        'sentence': sent.text,
                        'confidence': 0.85
                    }
                    relationships.append(relationship)
        
        return relationships
    
    def extract_semantic_relationships(self, text: str) -> List[Dict[str, Any]]:
        relationships = []
        sentences = text.split('.')
        
        patterns = {
            'causation': [
                r'(\w+(?:\s+\w+)*)\s+(?:causes?|results?\s+in|leads?\s+to)\s+(\w+(?:\s+\w+)*)',
                r'(?:due\s+to|because\s+of)\s+(\w+(?:\s+\w+)*),\s*(\w+(?:\s+\w+)*)'
            ],
            'temporal_sequence': [
                r'(\w+(?:\s+\w+)*)\s+(?:before|prior\s+to)\s+(\w+(?:\s+\w+)*)',
                r'(\w+(?:\s+\w+)*)\s+(?:after|following)\s+(\w+(?:\s+\w+)*)'
            ],
            'conditional': [
                r'if\s+(\w+(?:\s+\w+)*),?\s+(?:then\s+)?(\w+(?:\s+\w+)*)',
                r'(\w+(?:\s+\w+)*)\s+provided\s+that\s+(\w+(?:\s+\w+)*)'
            ],
            'equivalence': [
                r'(\w+(?:\s+\w+)*)\s+(?:equals?|is\s+equivalent\s+to|means)\s+(\w+(?:\s+\w+)*)',
                r'(\w+(?:\s+\w+)*)\s+(?:shall\s+be\s+deemed|is\s+defined\s+as)\s+(\w+(?:\s+\w+)*)'
            ]
        }
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            for relation_type, pattern_list in patterns.items():
                for pattern in pattern_list:
                    matches = re.finditer(pattern, sentence, re.IGNORECASE)
                    for match in matches:
                        if len(match.groups()) >= 2:
                            relationships.append({
                                'source': match.group(1).strip(),
                                'target': match.group(2).strip(),
                                'relation': relation_type,
                                'pattern': pattern,
                                'sentence': sentence,
                                'confidence': 0.75
                            })
        
        return relationships
    
    def extract_all_relationships(self, text: str, entities: List[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        all_relationships = []
        
        if self.nlp:
            all_relationships.extend(self.extract_dependencies_spacy(text))
            all_relationships.extend(self.extract_grammatical_relationships(text))
        
        all_relationships.extend(self.extract_semantic_relationships(text))
        
        if entities:
            all_relationships.extend(self.extract_entity_relationships(text, entities))
        
        unique_relationships = self._deduplicate_relationships(all_relationships)
        
        for i, rel in enumerate(unique_relationships):
            rel['id'] = f"rel_{i}"
        
        return unique_relationships
    
    def _deduplicate_relationships(self, relationships: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        seen = set()
        unique_rels = []
        
        for rel in relationships:
            key = (
                rel.get('source', rel.get('head', '')).lower(),
                rel.get('target', rel.get('dependent', '')).lower(),
                rel.get('relation', '').lower()
            )
            
            if key not in seen:
                seen.add(key)
                unique_rels.append(rel)
        
        return unique_rels
    
    def categorize_relationships(self, relationships: List[Dict[str, Any]]) -> Dict[str, List[Dict[str, Any]]]:
        categorized = defaultdict(list)
        
        for rel in relationships:
            relation_type = rel.get('relation', 'unknown')
            categorized[relation_type].append(rel)
        
        return dict(categorized)
    
    def get_relationship_statistics(self, relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
        if not relationships:
            return {}
        
        relation_types = [r.get('relation', 'unknown') for r in relationships]
        type_counts = {}
        for rel_type in relation_types:
            type_counts[rel_type] = type_counts.get(rel_type, 0) + 1
        
        confidences = [r.get('confidence', 0) for r in relationships if 'confidence' in r]
        
        stats = {
            'total_relationships': len(relationships),
            'unique_relation_types': len(type_counts),
            'relation_type_distribution': type_counts,
        }
        
        if confidences:
            stats.update({
                'average_confidence': sum(confidences) / len(confidences),
                'confidence_range': {
                    'min': min(confidences),
                    'max': max(confidences)
                }
            })
        
        return stats