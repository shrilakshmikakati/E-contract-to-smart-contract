"""
Enhanced Comparator with Business-to-Technical Entity Mapping
Fixed version without embedded newline literals
"""

from typing import Dict, Any, List, Tuple, Optional, Set
import difflib
from datetime import datetime
from collections import defaultdict
import numpy as np

try:
    from .knowledge_graph import KnowledgeGraph
    from .econtract_processor import EContractProcessor
    from .smartcontract_processor import SmartContractProcessor
    from ..utils.file_handler import FileHandler
except ImportError:
    from core.knowledge_graph import KnowledgeGraph
    from core.econtract_processor import EContractProcessor
    from core.smartcontract_processor import SmartContractProcessor
    from utils.file_handler import FileHandler

class KnowledgeGraphComparator:
    """
    Enhanced comparator with business-to-technical entity mapping
    """
    
    def __init__(self):
        self.econtract_processor = EContractProcessor()
        self.smartcontract_processor = SmartContractProcessor()
        self.comparison_results = {}
    
    def compare_knowledge_graphs(self, g_e: KnowledgeGraph, g_s: KnowledgeGraph, 
                                comparison_id: str = None) -> Dict[str, Any]:
        """Enhanced knowledge graph comparison with business-to-technical mapping"""
        if comparison_id is None:
            comparison_id = f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"Comparing: E-contract has {len(g_e.entities)} entities, Smart contract has {len(g_s.entities)} entities")
        print(f"E-contract sample entities: {list(g_e.entities.keys())[:5]}")
        print(f"Smart contract sample entities: {list(g_s.entities.keys())[:5]}")
        
        # Step 1: Enhanced entity matching
        entity_matches = self._match_entities(g_e.entities, g_s.entities)
        print(f"Found {len(entity_matches)} entity matches")
        
        # Step 2: Enhanced relationship matching  
        relation_matches = self._match_relations(g_e.relationships, g_s.relationships)
        print(f"Found {len(relation_matches)} relationship matches")
        
        # Step 3: Calculate preservation metrics
        entity_preservation = self._calculate_entity_preservation(g_e.entities, g_s.entities, entity_matches)
        relation_preservation = self._calculate_relation_preservation(g_e.relationships, g_s.relationships, relation_matches)
        
        # Step 4: Generate detailed comparison report
        overall_similarity = (entity_preservation + relation_preservation) / 2
        
        comparison_report = {
            'comparison_id': comparison_id,
            'entity_matches': entity_matches,
            'relationship_matches': relation_matches,
            'entity_preservation_percentage': entity_preservation,
            'relationship_preservation_percentage': relation_preservation,
            'overall_similarity_score': overall_similarity,
            'timestamp': datetime.now().isoformat(),
            
            # GUI expects these structures
            'summary': {
                'overall_similarity_score': overall_similarity,
                'total_entity_matches': len(entity_matches),
                'total_relation_matches': len(relation_matches),
                'entity_coverage_econtract': entity_preservation * 100,  # Convert to percentage for display
                'entity_coverage_smartcontract': (len(entity_matches) / len(g_s.entities) * 100) if g_s.entities else 0,
                'relation_coverage_econtract': relation_preservation * 100,  # Convert to percentage for display
                'relation_coverage_smartcontract': (len(relation_matches) / len(g_s.relationships) * 100) if g_s.relationships else 0
            },
            
            'entity_analysis': {
                'matches': entity_matches,
                'match_quality_distribution': self._analyze_match_quality(entity_matches)
            },
            
            'compliance_assessment': {
                'overall_compliance_score': overall_similarity,
                'compliance_level': 'High' if overall_similarity > 0.8 else 'Medium' if overall_similarity > 0.5 else 'Low',
                'is_compliant': overall_similarity > 0.6,
                'compliance_issues': [] if overall_similarity > 0.6 else ['Low similarity between contracts']
            },
            
            'recommendations': self._generate_recommendations(overall_similarity, len(entity_matches), len(relation_matches))
        }
        
        return comparison_report
    
    def _analyze_match_quality(self, entity_matches: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze the quality distribution of entity matches"""
        quality_dist = {'high_quality': 0, 'medium_quality': 0, 'low_quality': 0}
        
        for match in entity_matches:
            score = match.get('similarity_score', 0)
            if score > 0.7:
                quality_dist['high_quality'] += 1
            elif score > 0.4:
                quality_dist['medium_quality'] += 1
            else:
                quality_dist['low_quality'] += 1
        
        return quality_dist
    
    def _generate_recommendations(self, similarity: float, entity_matches: int, relation_matches: int) -> List[str]:
        """Generate recommendations based on comparison results"""
        recommendations = []
        
        if similarity < 0.3:
            recommendations.append("Consider redesigning the smart contract to better reflect business logic")
        if entity_matches < 10:
            recommendations.append("Add more business entities mapping to smart contract variables")
        if relation_matches < 20:
            recommendations.append("Improve relationship modeling between contract parties and functions")
        if similarity > 0.7:
            recommendations.append("Good alignment between e-contract and smart contract")
        
        return recommendations
    
    def _match_entities(self, entities_e: Dict[str, Any], entities_s: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Enhanced entity matching with business-to-technical mapping"""
        matches = []
        
        e_entities = [{'id': eid, **data} for eid, data in entities_e.items()]
        s_entities = [{'id': sid, **data} for sid, data in entities_s.items()]
        
        for e_entity in e_entities:
            best_match = None
            best_score = 0
            
            for s_entity in s_entities:
                similarity_score = self._calculate_entity_similarity(e_entity, s_entity)
                
                if similarity_score > best_score and similarity_score > 0.1:  # Much lower threshold for better matching
                    best_score = similarity_score
                    best_match = s_entity
            
            if best_match:
                matches.append({
                    'econtract_entity': e_entity,
                    'smartcontract_entity': best_match,
                    'similarity_score': best_score,
                    'match_type': self._classify_match_type(e_entity, best_match)
                })
        
        return matches
    
    def _calculate_entity_similarity(self, e_entity: Dict[str, Any], s_entity: Dict[str, Any]) -> float:
        """Enhanced entity similarity with business-to-technical mapping"""
        score = 0.0
        
        text_e = e_entity.get('text', '').lower().strip()
        text_s = s_entity.get('text', '').lower().strip()
        type_e = e_entity.get('type', '').upper()
        type_s = s_entity.get('type', '').upper()
        
        # 1. Business-to-Technical Mapping (Primary Factor - 50%)
        business_mapping_score = self._get_business_to_technical_mapping(e_entity, s_entity)
        if business_mapping_score > 0:
            score += business_mapping_score * 0.5
        
        # 2. Type Compatibility (30%)
        if self._are_compatible_types(type_e, type_s):
            score += 0.3
        elif self._are_related_entity_domains(type_e, type_s):
            score += 0.2
        
        # 3. Text Similarity (15%)
        if text_e and text_s:
            text_similarity = difflib.SequenceMatcher(None, text_e, text_s).ratio()
            substring_match = max(
                len(text_e) / len(text_s) if text_e in text_s else 0,
                len(text_s) / len(text_e) if text_s in text_e else 0
            )
            best_text_score = max(text_similarity, substring_match)
            score += best_text_score * 0.15
        
        # 4. Semantic Context (25%)
        semantic_score = self._calculate_enhanced_semantic_similarity(e_entity, s_entity)
        score += semantic_score * 0.25
        
        return min(score, 1.0)
    
    def _get_business_to_technical_mapping(self, e_entity: Dict[str, Any], s_entity: Dict[str, Any]) -> float:
        """Map business entities to smart contract technical elements"""
        e_text = e_entity.get('text', '').lower().strip()
        e_type = e_entity.get('type', '').upper()
        s_text = s_entity.get('text', '').lower().strip()
        s_type = s_entity.get('type', '').upper()
        
        # Business entity patterns to smart contract mappings
        business_mappings = {
            'party_mappings': {
                'patterns': ['corporation', 'company', 'inc', 'llc', 'ltd', 'party a', 'party b', 'client', 'provider', 'contractor', 'landlord', 'tenant', 'employee', 'employer', 'person', 'organization'],
                'smart_contract_vars': ['client', 'provider', 'party', 'owner', 'contractor', 'payee', 'payer', 'address', 'account']
            },
            'financial_mappings': {
                'patterns': ['$', 'usd', 'payment', 'fee', 'cost', 'amount', 'price', 'salary', 'wage', 'rent', 'money', 'gbp'],
                'smart_contract_vars': ['amount', 'price', 'fee', 'payment', 'balance', 'value', 'cost', 'uint256']
            },
            'contract_mappings': {
                'patterns': ['contract', 'agreement', 'lease', 'rental', 'employment', 'service'],
                'smart_contract_vars': ['contract', 'agreement', 'active', 'created', 'activated']
            },
            'action_mappings': {
                'patterns': ['pay', 'receive', 'send', 'transfer', 'activate', 'terminate', 'create', 'obligation'],
                'smart_contract_vars': ['function', 'event', 'activate', 'terminate', 'payment', 'transfer']
            },
            'temporal_mappings': {
                'patterns': ['month', 'day', 'year', 'deadline', 'duration', 'start', 'end', 'january', 'february'],
                'smart_contract_vars': ['deadline', 'timestamp', 'duration', 'starttime', 'endtime', 'expiry']
            },
            'service_mappings': {
                'patterns': ['service', 'work', 'development', 'consulting', 'delivery', 'obligation'],
                'smart_contract_vars': ['complete', 'deliver', 'execute', 'perform', 'fulfill', 'finish']
            },
            'status_mappings': {
                'patterns': ['completed', 'finished', 'approved', 'signed', 'agreed'],
                'smart_contract_vars': ['completed', 'approved', 'signed', 'active', 'finished', 'executed']
            }
        }
        
        max_mapping_score = 0.0
        
        for mapping_type, mapping_data in business_mappings.items():
            e_matches_pattern = any(pattern in e_text for pattern in mapping_data['patterns'])
            s_matches_var = any(var in s_text for var in mapping_data['smart_contract_vars'])
            
            if e_matches_pattern and s_matches_var:
                max_mapping_score = max(max_mapping_score, 0.9)  # Strong mapping
            elif e_matches_pattern and s_type in ['VARIABLE', 'FUNCTION', 'STATE_VARIABLE']:
                max_mapping_score = max(max_mapping_score, 0.6)  # Moderate mapping
            elif (e_type in ['MONEY', 'FINANCIAL'] and s_type in ['VARIABLE'] and 
                  any(word in s_text for word in ['amount', 'price', 'payment', 'fee'])):
                max_mapping_score = max(max_mapping_score, 0.8)  # Financial mapping
            elif (e_type in ['PERSON', 'ORG'] and s_type in ['VARIABLE'] and 
                  any(word in s_text for word in ['client', 'provider', 'owner', 'party'])):
                max_mapping_score = max(max_mapping_score, 0.8)  # Party mapping
        
        return max_mapping_score
    
    def _are_compatible_types(self, type1: str, type2: str) -> bool:
        """Enhanced entity type compatibility"""
        compatibility_mappings = {
            'PERSON': ['PARTY', 'ORGANIZATION', 'CONTRACT_PARTY', 'VARIABLE', 'STATE_VARIABLE'],
            'ORG': ['ORGANIZATION', 'PARTY', 'CONTRACT_PARTY', 'VARIABLE', 'STATE_VARIABLE'],
            'PARTY': ['PERSON', 'ORG', 'ORGANIZATION', 'VARIABLE', 'STATE_VARIABLE'],
            'MONEY': ['FINANCIAL', 'MONETARY_AMOUNT', 'CURRENCY', 'VARIABLE', 'STATE_VARIABLE'],
            'FINANCIAL': ['MONEY', 'MONETARY_AMOUNT', 'CURRENCY', 'VARIABLE', 'STATE_VARIABLE'],
            'DATE': ['TEMPORAL', 'DATE_TERMS', 'TIME', 'VARIABLE', 'STATE_VARIABLE'],
            'TIME': ['TEMPORAL', 'DATE', 'DATE_TERMS', 'VARIABLE', 'STATE_VARIABLE'],
            'FUNCTION': ['SMART_CONTRACT_FUNCTION', 'FUNCTION_DEFINITION', 'OBLIGATIONS', 'CONDITIONS'],
            'OBLIGATIONS': ['LEGAL_OBLIGATION', 'FUNCTION', 'SMART_CONTRACT_FUNCTION', 'CONDITIONS'],
            'VARIABLE': ['STATE_VARIABLE', 'SMART_CONTRACT_VARIABLE', 'PERSON', 'ORG', 'MONEY', 'DATE'],
            'STATE_VARIABLE': ['VARIABLE', 'SMART_CONTRACT_VARIABLE', 'PERSON', 'ORG', 'MONEY', 'DATE'],
        }
        
        for key, compatible_types in compatibility_mappings.items():
            if (type1 == key and type2 in compatible_types) or (type2 == key and type1 in compatible_types):
                return True
        
        return False
    
    def _are_related_entity_domains(self, type1: str, type2: str) -> bool:
        """Check if entity types are from related domains"""
        domain_groups = [
            ['PERSON', 'ORG', 'ORGANIZATION', 'PARTY', 'CONTRACT_PARTY', 'VARIABLE'],
            ['MONEY', 'FINANCIAL', 'MONETARY_AMOUNT', 'CURRENCY', 'VARIABLE', 'STATE_VARIABLE'],
            ['DATE', 'TEMPORAL', 'TIME', 'DURATION', 'VARIABLE', 'STATE_VARIABLE'],
            ['FUNCTION', 'SMART_CONTRACT_FUNCTION', 'OBLIGATIONS', 'CONDITIONS'],
            ['CONTRACT', 'SMART_CONTRACT', 'AGREEMENT', 'CONTRACT_DEFINITION']
        ]
        
        for group in domain_groups:
            if type1 in group and type2 in group:
                return True
        return False
    
    def _calculate_enhanced_semantic_similarity(self, e_entity: Dict[str, Any], s_entity: Dict[str, Any]) -> float:
        """Enhanced semantic similarity calculation"""
        e_text = e_entity.get('text', '').lower()
        s_text = s_entity.get('text', '').lower()
        e_properties = str(e_entity.get('properties', {})).lower()
        s_properties = str(s_entity.get('properties', {})).lower()
        
        semantic_groups = {
            'financial': ['payment', 'money', 'amount', 'fee', 'cost', 'price', 'salary', 'wage', 'balance', 'value', '$'],
            'temporal': ['date', 'time', 'deadline', 'duration', 'month', 'day', 'year', 'start', 'end', 'timestamp'],
            'party': ['party', 'client', 'provider', 'contractor', 'organization', 'company', 'person', 'owner'],
            'contract': ['contract', 'agreement', 'obligation', 'condition', 'term', 'clause', 'provision'],
            'action': ['function', 'method', 'procedure', 'operation', 'complete', 'execute', 'perform', 'deliver'],
            'storage': ['variable', 'storage', 'state', 'data', 'property', 'attribute', 'field'],
            'status': ['completed', 'active', 'finished', 'approved', 'signed', 'executed', 'pending']
        }
        
        e_semantic_groups = set()
        s_semantic_groups = set()
        
        for group_name, keywords in semantic_groups.items():
            if any(keyword in e_text or keyword in e_properties for keyword in keywords):
                e_semantic_groups.add(group_name)
            if any(keyword in s_text or keyword in s_properties for keyword in keywords):
                s_semantic_groups.add(group_name)
        
        if not e_semantic_groups and not s_semantic_groups:
            return 0.0
        
        intersection = len(e_semantic_groups & s_semantic_groups)
        union = len(e_semantic_groups | s_semantic_groups)
        
        return intersection / union if union > 0 else 0.0
    
    def _match_relations(self, relations_e: Dict[str, Any], relations_s: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Enhanced relationship matching"""
        matches = []
        
        e_relations = [{'id': rid, **data} for rid, data in relations_e.items()]
        s_relations = [{'id': rid, **data} for rid, data in relations_s.items()]
        
        for e_relation in e_relations:
            best_match = None
            best_score = 0
            
            for s_relation in s_relations:
                similarity_score = self._calculate_relation_similarity(e_relation, s_relation)
                
                if similarity_score > best_score and similarity_score > 0.2:  # Reduced threshold
                    best_score = similarity_score
                    best_match = s_relation
            
            if best_match:
                matches.append({
                    'econtract_relation': e_relation,
                    'smartcontract_relation': best_match,
                    'similarity_score': best_score
                })
        
        return matches
    
    def _calculate_relation_similarity(self, e_relation: Dict[str, Any], s_relation: Dict[str, Any]) -> float:
        """Enhanced relationship similarity calculation"""
        score = 0.0
        
        relation_e = e_relation.get('relation', '').lower()
        relation_s = s_relation.get('relation', '').lower()
        
        # 1. Business-to-Technical Relationship Mapping (40%)
        business_relation_mapping = self._get_business_to_technical_relation_mapping(e_relation, s_relation)
        if business_relation_mapping > 0:
            score += business_relation_mapping * 0.4
        
        # 2. Direct Relation Type Similarity (30%)
        if relation_e == relation_s:
            score += 0.3
        elif self._are_compatible_relations(relation_e, relation_s):
            score += 0.2
        
        # 3. Source and Target Compatibility (20%)
        source_type_e = e_relation.get('source_type', '').upper()
        target_type_e = e_relation.get('target_type', '').upper()
        source_type_s = s_relation.get('source_type', '').upper()
        target_type_s = s_relation.get('target_type', '').upper()
        
        if source_type_e == source_type_s:
            score += 0.1
        elif self._are_compatible_types(source_type_e, source_type_s):
            score += 0.06
        
        if target_type_e == target_type_s:
            score += 0.1
        elif self._are_compatible_types(target_type_e, target_type_s):
            score += 0.06
        
        # 4. Semantic Context (10%)
        semantic_relation_score = self._calculate_semantic_relation_similarity(e_relation, s_relation)
        score += semantic_relation_score * 0.1
        
        return min(score, 1.0)
    
    def _get_business_to_technical_relation_mapping(self, e_relation: Dict[str, Any], s_relation: Dict[str, Any]) -> float:
        """Map business relationships to technical smart contract relationships"""
        e_rel = e_relation.get('relation', '').lower()
        s_rel = s_relation.get('relation', '').lower()
        
        business_relation_mappings = {
            'obligation_mappings': {
                'business_relations': ['obligation', 'must_do', 'shall_perform', 'required_to'],
                'technical_relations': ['has_parameter', 'contains', 'calls', 'requires', 'modifies']
            },
            'financial_mappings': {
                'business_relations': ['payment', 'pays', 'financial', 'monetary', 'cost'],
                'technical_relations': ['has_member', 'contains', 'stores', 'transfers', 'updates']
            },
            'temporal_mappings': {
                'business_relations': ['temporal', 'deadline', 'duration', 'schedule'],
                'technical_relations': ['contains', 'inherits_from', 'depends_on', 'triggers']
            },
            'conditional_mappings': {
                'business_relations': ['condition', 'if_then', 'requires', 'depends_on'],
                'technical_relations': ['has_parameter', 'contains', 'controls', 'validates']
            }
        }
        
        max_mapping_score = 0.0
        
        for mapping_type, mapping_data in business_relation_mappings.items():
            e_matches_business = any(pattern in e_rel for pattern in mapping_data['business_relations'])
            s_matches_technical = any(pattern in s_rel for pattern in mapping_data['technical_relations'])
            
            if e_matches_business and s_matches_technical:
                max_mapping_score = max(max_mapping_score, 0.8)
            elif e_matches_business and s_rel in ['contains', 'has_member', 'has_parameter']:
                max_mapping_score = max(max_mapping_score, 0.6)
        
        return max_mapping_score
    
    def _calculate_semantic_relation_similarity(self, e_relation: Dict[str, Any], s_relation: Dict[str, Any]) -> float:
        """Calculate semantic similarity for relationships"""
        e_context = (e_relation.get('relation', '') + ' ' + 
                    str(e_relation.get('properties', {}))).lower()
        s_context = (s_relation.get('relation', '') + ' ' + 
                    str(s_relation.get('properties', {}))).lower()
        
        relation_semantic_groups = {
            'control': ['obligation', 'condition', 'requires', 'controls', 'validates', 'modifies'],
            'data': ['contains', 'has_member', 'stores', 'references', 'includes'],
            'temporal': ['temporal', 'deadline', 'triggers', 'depends_on', 'schedule'],
            'financial': ['payment', 'financial', 'transfers', 'updates', 'monetary'],
            'structural': ['has_parameter', 'inherits_from', 'calls', 'part_of']
        }
        
        e_groups = set()
        s_groups = set()
        
        for group_name, keywords in relation_semantic_groups.items():
            if any(keyword in e_context for keyword in keywords):
                e_groups.add(group_name)
            if any(keyword in s_context for keyword in keywords):
                s_groups.add(group_name)
        
        if not e_groups and not s_groups:
            return 0.0
        
        intersection = len(e_groups & s_groups)
        union = len(e_groups | s_groups)
        
        return intersection / union if union > 0 else 0.0
    
    def _are_compatible_relations(self, rel1: str, rel2: str) -> bool:
        """Enhanced relation compatibility check"""
        relation_mappings = {
            'obligation': ['contains', 'has_parameter', 'requires', 'controls'],
            'financial': ['contains', 'has_member', 'stores', 'transfers'],
            'temporal': ['contains', 'inherits_from', 'depends_on', 'triggers'],
            'condition': ['contains', 'has_parameter', 'validates', 'controls'],
            'co_occurrence': ['contains', 'has_member', 'references', 'includes']
        }
        
        for key, compatible_rels in relation_mappings.items():
            if (rel1 == key and rel2 in compatible_rels) or (rel2 == key and rel1 in compatible_rels):
                return True
        
        return False
    
    def _classify_match_type(self, e_entity: Dict[str, Any], s_entity: Dict[str, Any]) -> str:
        """Classify the type of match between entities"""
        e_text = e_entity.get('text', '').lower()
        s_text = s_entity.get('text', '').lower()
        
        if e_text == s_text:
            return 'exact_match'
        elif e_text in s_text or s_text in e_text:
            return 'partial_match'
        elif self._are_compatible_types(e_entity.get('type', ''), s_entity.get('type', '')):
            return 'semantic_match'
        else:
            return 'weak_match'
    
    def _calculate_entity_preservation(self, entities_e: Dict[str, Any], entities_s: Dict[str, Any], 
                                     entity_matches: List[Dict[str, Any]]) -> float:
        """Calculate entity preservation score (0-1)"""
        if not entities_e:
            return 1.0 if not entities_s else 0.0
        
        return len(entity_matches) / len(entities_e)
    
    def _calculate_relation_preservation(self, relations_e: Dict[str, Any], relations_s: Dict[str, Any],
                                       relation_matches: List[Dict[str, Any]]) -> float:
        """Calculate relationship preservation score (0-1)"""
        if not relations_e:
            return 1.0 if not relations_s else 0.0
        
        return len(relation_matches) / len(relations_e)


# Legacy alias for backwards compatibility
ContractComparator = KnowledgeGraphComparator