"""
Enhanced Business Contract Relationship Extractor
Specifically designed to extract business relationships from e-contracts
"""

import re
from typing import List, Dict, Any, Tuple, Set, Optional
from collections import defaultdict
from itertools import combinations

class BusinessRelationshipExtractor:
    """Enhanced relationship extractor for business contracts"""
    
    def __init__(self):
        self.business_patterns = self._define_business_patterns()
        self.relationship_counter = 0
    
    def _define_business_patterns(self) -> Dict[str, List[Dict[str, Any]]]:
        """Define business-specific relationship patterns"""
        return {
            'payment_relationships': [
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+(?:pays?|shall\s+pay|will\s+pay|must\s+pay)\s+([^.]+?)\s+to\s+(\w+(?:\s+\w+)*)',
                    'relation': 'payment',
                    'source_group': 1,  # payer
                    'target_group': 3,  # payee
                    'amount_group': 2,  # payment amount
                    'confidence': 0.95
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+(?:receives?|shall\s+receive|will\s+receive)\s+([^.]+?)\s+from\s+(\w+(?:\s+\w+)*)',
                    'relation': 'payment',
                    'source_group': 3,  # payer
                    'target_group': 1,  # payee
                    'amount_group': 2,  # payment amount
                    'confidence': 0.95
                },
                {
                    'pattern': r'(?:monthly\s+)?(?:rent|payment)\s+of\s+([^.]+?)\s+(?:shall\s+be\s+)?(?:paid|due)',
                    'relation': 'payment_obligation',
                    'amount_group': 1,
                    'confidence': 0.85
                }
            ],
            'ownership_relationships': [
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+(?:owns?|owns?\s+and\s+operates?|has\s+title\s+to)\s+([^.]+)',
                    'relation': 'ownership',
                    'source_group': 1,  # owner
                    'target_group': 2,  # owned property
                    'confidence': 0.90
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+(?:is\s+the\s+owner\s+of|possesses)\s+([^.]+)',
                    'relation': 'ownership',
                    'source_group': 1,
                    'target_group': 2,
                    'confidence': 0.85
                },
                {
                    'pattern': r'([^.]+?)\s+(?:belongs?\s+to|is\s+(?:the\s+)?property\s+of)\s+(\w+(?:\s+\w+)*)',
                    'relation': 'ownership',
                    'source_group': 2,  # owner
                    'target_group': 1,  # owned property
                    'confidence': 0.90
                }
            ],
            'temporal_relationships': [
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+(?:starts?|begins?|commences?)\s+(?:on\s+)?([^.]+)',
                    'relation': 'starts_on',
                    'source_group': 1,  # event/contract
                    'target_group': 2,  # start date
                    'confidence': 0.85
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+(?:ends?|expires?|terminates?)\s+(?:on\s+)?([^.]+)',
                    'relation': 'ends_on',
                    'source_group': 1,  # event/contract
                    'target_group': 2,  # end date
                    'confidence': 0.85
                },
                {
                    'pattern': r'(?:lease|contract)\s+(?:duration|period|term)\s+(?:is\s+|of\s+)?([^.]+)',
                    'relation': 'has_duration',
                    'target_group': 1,  # duration
                    'confidence': 0.80
                }
            ],
            'obligation_relationships': [
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+(?:shall|must|will|agrees?\s+to|is\s+(?:required\s+to|obligated\s+to))\s+([^.]+)',
                    'relation': 'obligation',
                    'source_group': 1,  # obligated party
                    'target_group': 2,  # obligation
                    'confidence': 0.90
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+(?:is\s+)?(?:responsible\s+for|liable\s+for)\s+([^.]+)',
                    'relation': 'responsibility',
                    'source_group': 1,  # responsible party
                    'target_group': 2,  # responsibility
                    'confidence': 0.85
                }
            ],
            'condition_relationships': [
                {
                    'pattern': r'if\s+([^,]+),\s*(?:then\s+)?([^.]+)',
                    'relation': 'condition',
                    'source_group': 1,  # condition
                    'target_group': 2,  # consequence
                    'confidence': 0.80
                },
                {
                    'pattern': r'([^.]+?)\s+provided\s+that\s+([^.]+)',
                    'relation': 'conditional_on',
                    'source_group': 1,  # main clause
                    'target_group': 2,  # condition
                    'confidence': 0.80
                }
            ],
            'specification_relationships': [
                {
                    'pattern': r'(?:the\s+)?(\w+(?:\s+\w+)*)\s+(?:specifies?|defines?|states?|includes?)\s+([^.]+)',
                    'relation': 'specifies',
                    'source_group': 1,  # specifier (contract, clause)
                    'target_group': 2,  # specified item
                    'confidence': 0.75
                },
                {
                    'pattern': r'(\w+(?:\s+\w+)*)\s+(?:is|are)\s+([^.]+)',
                    'relation': 'is_defined_as',
                    'source_group': 1,  # term
                    'target_group': 2,  # definition
                    'confidence': 0.70
                }
            ]
        }
    
    def extract_business_relationships(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract business-specific relationships from contract text"""
        relationships = []
        
        # Split text into sentences for better relationship extraction
        sentences = self._split_into_sentences(text)
        
        for sentence in sentences:
            sentence = sentence.strip()
            if not sentence:
                continue
            
            # Extract relationships from each sentence with enhanced matching
            
            # Extract relationships from each sentence
            sentence_relationships = self._extract_from_sentence(sentence, entities)
            relationships.extend(sentence_relationships)
        
        # Add entity-based relationships
        entity_relationships = self._extract_entity_relationships(text, entities)
        relationships.extend(entity_relationships)
        
        # Remove duplicates and assign IDs
        unique_relationships = self._deduplicate_and_assign_ids(relationships)
        
        print(f"Extracted {len(unique_relationships)} business relationships")
        return unique_relationships
    
    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences for processing"""
        # Simple sentence splitting - can be enhanced with more sophisticated methods
        sentences = re.split(r'[.!?]+', text)
        return [s.strip() for s in sentences if s.strip()]
    
    def _extract_from_sentence(self, sentence: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract relationships from a single sentence"""
        relationships = []
        
        # Apply each pattern category
        for category, patterns in self.business_patterns.items():
            for pattern_info in patterns:
                matches = re.finditer(pattern_info['pattern'], sentence, re.IGNORECASE | re.DOTALL)
                
                for match in matches:
                    relationship = self._create_relationship_from_match(
                        match, pattern_info, sentence, entities
                    )
                    if relationship:
                        relationships.append(relationship)
        
        return relationships
    
    def _create_relationship_from_match(self, match: re.Match, pattern_info: Dict[str, Any], 
                                      sentence: str, entities: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Create relationship object from regex match"""
        try:
            source_text = None
            target_text = None
            
            # Extract source if specified
            if 'source_group' in pattern_info:
                source_text = match.group(pattern_info['source_group']).strip()
            
            # Extract target if specified
            if 'target_group' in pattern_info:
                target_text = match.group(pattern_info['target_group']).strip()
            
            # For patterns without explicit source/target, try to infer from entities
            if not source_text or not target_text:
                sentence_entities = self._find_entities_in_sentence(sentence, entities)
                if len(sentence_entities) >= 2:
                    if not source_text:
                        source_text = sentence_entities[0]['text']
                    if not target_text:
                        target_text = sentence_entities[1]['text']
            
            # Must have both source and target for a valid relationship
            if not source_text or not target_text:
                return None
            
            # Find matching entities
            source_entity = self._find_matching_entity(source_text, entities)
            target_entity = self._find_matching_entity(target_text, entities)
            
            # Create relationship
            relationship = {
                'id': f'business_rel_{self.relationship_counter}',
                'source': source_entity['id'] if source_entity else source_text,
                'target': target_entity['id'] if target_entity else target_text,
                'source_text': source_text,
                'target_text': target_text,
                'relation': pattern_info['relation'],
                'pattern': pattern_info['pattern'],
                'sentence': sentence,
                'confidence': pattern_info['confidence'],
                'source_type': source_entity['label'] if source_entity else 'UNKNOWN',
                'target_type': target_entity['label'] if target_entity else 'UNKNOWN',
                'extraction_method': 'business_pattern'
            }
            
            # Add additional context if available
            if 'amount_group' in pattern_info:
                try:
                    amount_text = match.group(pattern_info['amount_group']).strip()
                    relationship['amount'] = amount_text
                except (IndexError, AttributeError):
                    pass
            
            self.relationship_counter += 1
            return relationship
            
        except Exception as e:
            print(f"Error creating relationship from match: {e}")
            return None
    
    def _find_entities_in_sentence(self, sentence: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Find entities that appear in the given sentence"""
        sentence_lower = sentence.lower()
        sentence_entities = []
        
        for entity in entities:
            entity_text = entity.get('text', '').lower()
            if entity_text and entity_text in sentence_lower:
                sentence_entities.append(entity)
        
        # Sort by position in sentence for consistent ordering
        sentence_entities.sort(key=lambda e: sentence_lower.find(e.get('text', '').lower()))
        return sentence_entities
    
    def _find_matching_entity(self, text: str, entities: List[Dict[str, Any]]) -> Optional[Dict[str, Any]]:
        """Find entity that best matches the given text"""
        text_lower = text.lower().strip()
        
        # Try exact match first
        for entity in entities:
            entity_text = entity.get('text', '').lower().strip()
            if entity_text == text_lower:
                return entity
        
        # Try partial match
        for entity in entities:
            entity_text = entity.get('text', '').lower().strip()
            if entity_text and (entity_text in text_lower or text_lower in entity_text):
                return entity
        
        return None
    
    def _extract_entity_relationships(self, text: str, entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract relationships between co-occurring entities"""
        relationships = []
        sentences = self._split_into_sentences(text)
        
        for sentence in sentences:
            sentence_entities = self._find_entities_in_sentence(sentence, entities)
            
            # Create relationships between entities in the same sentence
            if len(sentence_entities) >= 2:
                for i, entity1 in enumerate(sentence_entities):
                    for entity2 in sentence_entities[i+1:]:
                        # Determine relationship type based on entity types and context
                        relation_type = self._infer_relationship_type(entity1, entity2, sentence)
                        
                        relationship = {
                            'id': f'entity_rel_{self.relationship_counter}',
                            'source': entity1['id'],
                            'target': entity2['id'],
                            'source_text': entity1['text'],
                            'target_text': entity2['text'],
                            'relation': relation_type,
                            'sentence': sentence,
                            'confidence': 0.6,
                            'source_type': entity1.get('label', 'UNKNOWN'),
                            'target_type': entity2.get('label', 'UNKNOWN'),
                            'extraction_method': 'entity_cooccurrence'
                        }
                        
                        relationships.append(relationship)
                        self.relationship_counter += 1
        
        return relationships
    
    def _infer_relationship_type(self, entity1: Dict[str, Any], entity2: Dict[str, Any], 
                               sentence: str) -> str:
        """Infer relationship type based on entity types and sentence context"""
        type1 = entity1.get('label', '').upper()
        type2 = entity2.get('label', '').upper()
        sentence_lower = sentence.lower()
        
        # Financial relationships
        if 'FINANCIAL' in [type1, type2] or 'MONEY' in [type1, type2]:
            if any(word in sentence_lower for word in ['pay', 'payment', 'rent', 'fee']):
                return 'financial_obligation'
        
        # Temporal relationships
        if 'TEMPORAL' in [type1, type2] or 'DATE' in [type1, type2]:
            if any(word in sentence_lower for word in ['start', 'begin', 'commence']):
                return 'temporal_start'
            elif any(word in sentence_lower for word in ['end', 'expire', 'terminate']):
                return 'temporal_end'
            else:
                return 'temporal_reference'
        
        # Party relationships
        if type1 in ['PERSON', 'ORG', 'ORGANIZATION'] and type2 in ['PERSON', 'ORG', 'ORGANIZATION']:
            return 'party_relationship'
        
        # Obligation relationships
        if 'OBLIGATIONS' in [type1, type2]:
            return 'obligation_assignment'
        
        # Location relationships
        if type1 in ['GPE', 'ADDRESS', 'FACILITY'] or type2 in ['GPE', 'ADDRESS', 'FACILITY']:
            return 'location_reference'
        
        # Default relationship
        return 'co_occurrence'
    
    def _deduplicate_and_assign_ids(self, relationships: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Remove duplicates and ensure proper ID assignment"""
        seen = set()
        unique_relationships = []
        
        for rel in relationships:
            # Create deduplication key
            source = rel.get('source', '')
            target = rel.get('target', '')
            relation = rel.get('relation', '')
            
            # Normalize the key for comparison
            key = (str(source).lower(), str(target).lower(), relation.lower())
            
            if key not in seen:
                seen.add(key)
                # Ensure relationship has proper ID
                if 'id' not in rel or not rel['id']:
                    rel['id'] = f'rel_{len(unique_relationships)}'
                unique_relationships.append(rel)
        
        return unique_relationships
    
    def get_relationship_statistics(self, relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Get statistics about extracted relationships"""
        if not relationships:
            return {
                'total_relationships': 0,
                'relation_types': {},
                'extraction_methods': {},
                'average_confidence': 0
            }
        
        # Count by relation type
        relation_counts = defaultdict(int)
        method_counts = defaultdict(int)
        confidences = []
        
        for rel in relationships:
            relation_counts[rel.get('relation', 'unknown')] += 1
            method_counts[rel.get('extraction_method', 'unknown')] += 1
            if 'confidence' in rel:
                confidences.append(rel['confidence'])
        
        return {
            'total_relationships': len(relationships),
            'relation_types': dict(relation_counts),
            'extraction_methods': dict(method_counts),
            'average_confidence': sum(confidences) / len(confidences) if confidences else 0,
            'unique_relation_types': len(relation_counts)
        }