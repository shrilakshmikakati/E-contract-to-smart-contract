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
        
        # Step 4: Calculate accuracy metrics
        accuracy_data = self._calculate_accuracy_score(g_e, g_s, {
            'entity_matches': entity_matches, 
            'relationship_matches': relation_matches
        })
        
        # Step 5: Generate detailed comparison report  
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
                'compliance_level': self._determine_compliance_level(overall_similarity, accuracy_data),
                'is_compliant': self._assess_deployment_readiness(overall_similarity, accuracy_data),
                'compliance_issues': self._identify_compliance_issues(overall_similarity, accuracy_data)
            },
            
            'recommendations': self._generate_enhanced_recommendations(overall_similarity, accuracy_data, len(entity_matches), len(relation_matches)),
            
            # Enhanced accuracy and deployment readiness
            'accuracy_analysis': accuracy_data
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

    def _generate_enhanced_recommendations(self, similarity: float, accuracy_data: Dict[str, Any], 
                                         entity_matches: int, relation_matches: int) -> List[str]:
        """Generate enhanced recommendations based on comprehensive analysis"""
        recommendations = []
        
        # Accuracy-based recommendations
        accuracy_score = accuracy_data.get('accuracy_score', 0)
        if accuracy_score < 0.3:
            recommendations.append("🔴 CRITICAL: Smart contract requires major redesign - business logic poorly represented")
            recommendations.append("🔧 Add missing state variables for key business entities (parties, amounts, dates)")
        elif accuracy_score < 0.6:
            recommendations.append("🟡 MODERATE: Enhance smart contract with better business logic mapping")
            recommendations.append("📈 Add validation functions for business rules and constraints")
        elif accuracy_score > 0.8:
            recommendations.append("✅ EXCELLENT: Smart contract accurately represents business logic")
        
        # Entity coverage recommendations
        entity_coverage = accuracy_data.get('entity_coverage', 0)
        if entity_coverage < 0.5:
            recommendations.append("🎯 Add missing business entities: parties, financial amounts, temporal constraints")
        elif entity_coverage < 0.8:
            recommendations.append("📊 Improve entity representation with more comprehensive variable mapping")
        
        # Relationship preservation recommendations
        relation_coverage = accuracy_data.get('relation_coverage', 0)
        if relation_coverage < 0.3:
            recommendations.append("🔗 PRIORITY: Model business relationships as smart contract functions")
            recommendations.append("⚖️ Add enforcement mechanisms for obligations and conditions")
        elif relation_coverage < 0.6:
            recommendations.append("🔧 Enhance function interactions to better reflect business workflows")
        
        # Business logic recommendations
        business_logic_score = accuracy_data.get('business_logic_score', 0)
        if business_logic_score < 0.4:
            recommendations.append("💼 Add business rule validation (payment conditions, termination clauses)")
            recommendations.append("🛡️ Implement access controls for different contract parties")
        
        # Completeness recommendations
        completeness_score = accuracy_data.get('completeness_score', 0)
        if completeness_score < 0.5:
            recommendations.append("🏗️ Add missing contract elements: constructor, events, modifiers")
            recommendations.append("📝 Include comprehensive state management functions")
        
        # Deployment readiness
        if not accuracy_data.get('deployment_ready', False):
            recommendations.append("⚠️ CONTRACT NOT DEPLOYMENT-READY: Address above issues before deployment")
            recommendations.append("🧪 Implement thorough testing for all business scenarios")
        else:
            recommendations.append("🚀 CONTRACT READY: Suitable for deployment after security audit")
        
        # Similarity-based recommendations (enhanced)
        if similarity < 0.4:
            recommendations.append("🎨 Consider using contract templates that better match your business domain")
        elif similarity > 0.7:
            recommendations.append("🎉 Strong alignment achieved between business and technical requirements")
        
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
                
                if similarity_score > best_score and similarity_score > 0.15:  # Further reduced threshold for better matching
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
        """Enhanced relationship similarity calculation with comprehensive business logic"""
        score = 0.0
        
        relation_e = e_relation.get('relation', '').lower()
        relation_s = s_relation.get('relation', '').lower()
        
        # 1. Enhanced Business-to-Technical Relationship Mapping (45%)
        business_relation_mapping = self._get_enhanced_business_relation_mapping(e_relation, s_relation)
        if business_relation_mapping > 0:
            score += business_relation_mapping * 0.45
        
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
        """Enhanced mapping of business relationships to technical smart contract relationships"""
        e_rel = e_relation.get('relation', '').lower()
        s_rel = s_relation.get('relation', '').lower()
        
        # Enhanced business relation mappings with more patterns
        enhanced_relation_mappings = {
            'obligation_mappings': {
                'business_relations': ['obligation', 'must_do', 'shall_perform', 'required_to', 'responsible_for', 
                                     'duty', 'bound_to', 'commit_to', 'agree_to', 'undertake'],
                'technical_relations': ['has_parameter', 'contains', 'calls', 'requires', 'modifies', 'validates', 
                                      'controls', 'enforces', 'executes']
            },
            'financial_mappings': {
                'business_relations': ['payment', 'pays', 'financial', 'monetary', 'cost', 'fee', 'salary', 
                                     'rent', 'deposit', 'transfer', 'compensation'],
                'technical_relations': ['has_member', 'contains', 'stores', 'transfers', 'updates', 'modifies',
                                      'references', 'tracks', 'calculates']
            },
            'temporal_mappings': {
                'business_relations': ['temporal', 'deadline', 'duration', 'schedule', 'time', 'date', 
                                     'period', 'expires', 'starts', 'ends'],
                'technical_relations': ['contains', 'inherits_from', 'depends_on', 'triggers', 'schedules',
                                      'timestamps', 'tracks', 'monitors']
            },
            'conditional_mappings': {
                'business_relations': ['condition', 'if_then', 'requires', 'depends_on', 'contingent', 
                                     'subject_to', 'provided_that', 'unless', 'when'],
                'technical_relations': ['has_parameter', 'contains', 'controls', 'validates', 'checks',
                                      'verifies', 'enforces', 'triggers']
            },
            'party_mappings': {
                'business_relations': ['party_to', 'involves', 'between', 'signatory', 'participant',
                                     'contractor', 'client', 'provider', 'owner'],
                'technical_relations': ['has_member', 'contains', 'references', 'stores', 'manages',
                                      'owns', 'accesses', 'controls']
            },
            'status_mappings': {
                'business_relations': ['status', 'state', 'active', 'terminated', 'completed', 'pending',
                                     'approved', 'signed', 'executed'],
                'technical_relations': ['contains', 'stores', 'tracks', 'manages', 'updates', 'modifies',
                                      'references', 'controls']
            }
        }
        
        max_mapping_score = 0.0
        
        # Direct pattern matching with confidence scoring
        for mapping_type, mapping_data in enhanced_relation_mappings.items():
            e_matches_business = any(pattern in e_rel for pattern in mapping_data['business_relations'])
            s_matches_technical = any(pattern in s_rel for pattern in mapping_data['technical_relations'])
            
            if e_matches_business and s_matches_technical:
                # High confidence mapping
                max_mapping_score = max(max_mapping_score, 0.9)
            elif e_matches_business and s_rel in ['contains', 'has_member', 'has_parameter', 'stores']:
                # Medium confidence mapping to common technical relations
                max_mapping_score = max(max_mapping_score, 0.7)
            elif any(word in e_rel for word in ['co_occurrence', 'part_of', 'includes']) and s_rel in ['contains', 'has_member']:
                # Generic structural mapping
                max_mapping_score = max(max_mapping_score, 0.5)
        
        # Semantic similarity fallback for broader matching
        if max_mapping_score == 0.0:
            semantic_score = self._calculate_semantic_relation_similarity(e_relation, s_relation)
            if semantic_score > 0.3:
                max_mapping_score = semantic_score * 0.6  # Lower confidence for semantic-only matches
        
        return max_mapping_score

    def _get_enhanced_business_relation_mapping(self, e_relation: Dict[str, Any], s_relation: Dict[str, Any]) -> float:
        """Enhanced business-to-technical relationship mapping with comprehensive patterns"""
        e_rel = e_relation.get('relation', '').lower()
        s_rel = s_relation.get('relation', '').lower()
        e_props = str(e_relation.get('properties', {})).lower()
        s_props = str(s_relation.get('properties', {})).lower()
        
        # Comprehensive business relationship mappings
        enhanced_relation_mappings = {
            # Obligation and enforcement mappings
            'obligation_mappings': {
                'business_patterns': ['obligation', 'must_do', 'shall_perform', 'required_to', 'duty', 'responsibility', 'liable'],
                'technical_patterns': ['has_parameter', 'contains', 'calls', 'requires', 'modifies', 'validates', 'enforces'],
                'score': 0.90
            },
            # Financial transaction mappings
            'financial_mappings': {
                'business_patterns': ['payment', 'pays', 'financial', 'monetary', 'cost', 'fee', 'salary', 'rent'],
                'technical_patterns': ['has_member', 'contains', 'stores', 'transfers', 'updates', 'balances'],
                'score': 0.85
            },
            # Temporal constraint mappings
            'temporal_mappings': {
                'business_patterns': ['temporal', 'deadline', 'duration', 'schedule', 'expires', 'due_date'],
                'technical_patterns': ['contains', 'inherits_from', 'depends_on', 'triggers', 'timestamps'],
                'score': 0.80
            },
            # Conditional logic mappings
            'conditional_mappings': {
                'business_patterns': ['condition', 'if_then', 'requires', 'depends_on', 'contingent', 'provided'],
                'technical_patterns': ['has_parameter', 'contains', 'controls', 'validates', 'checks'],
                'score': 0.85
            },
            # Access control mappings
            'access_mappings': {
                'business_patterns': ['authorized', 'permitted', 'allowed', 'restricted', 'exclusive'],
                'technical_patterns': ['modifies', 'requires', 'controls', 'validates', 'restricts'],
                'score': 0.88
            },
            # State management mappings
            'state_mappings': {
                'business_patterns': ['status', 'state', 'active', 'inactive', 'completed', 'pending'],
                'technical_patterns': ['stores', 'contains', 'updates', 'modifies', 'tracks'],
                'score': 0.75
            }
        }
        
        max_score = 0.0
        context_text = f"{e_rel} {e_props}"
        tech_text = f"{s_rel} {s_props}"
        
        for mapping_type, mapping_data in enhanced_relation_mappings.items():
            business_match = any(pattern in context_text for pattern in mapping_data['business_patterns'])
            tech_match = any(pattern in tech_text for pattern in mapping_data['technical_patterns'])
            
            if business_match and tech_match:
                max_score = max(max_score, mapping_data['score'])
            elif business_match and any(generic in s_rel for generic in ['contains', 'has_member', 'has_parameter']):
                max_score = max(max_score, mapping_data['score'] * 0.7)  # Partial match
        
        return max_score
    
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

    def _extract_business_context(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Extract business context from entity"""
        text = entity.get('text', '').lower()
        entity_type = entity.get('type', '').lower()
        
        context = {
            'is_financial': any(term in text for term in ['$', 'payment', 'money', 'cost', 'fee', 'salary', 'rent', 'gbp', 'usd']),
            'is_party': any(term in text for term in ['company', 'person', 'tenant', 'landlord', 'employee', 'contractor']),
            'is_temporal': any(term in text for term in ['date', 'time', 'deadline', 'month', 'year', 'day']),
            'is_obligation': any(term in text for term in ['must', 'shall', 'required', 'obligation', 'responsible']),
            'is_asset': any(term in text for term in ['property', 'equipment', 'asset', 'resource', 'item']),
            'domain': self._identify_business_domain(text)
        }
        return context

    def _extract_technical_context(self, entity: Dict[str, Any]) -> Dict[str, Any]:
        """Extract technical context from smart contract entity"""
        text = entity.get('text', '').lower()
        entity_type = entity.get('type', '').lower()
        
        context = {
            'is_variable': 'variable' in entity_type or any(term in text for term in ['uint', 'bool', 'address', 'string']),
            'is_function': 'function' in entity_type or text.endswith('()'),
            'is_event': 'event' in entity_type,
            'is_modifier': 'modifier' in entity_type,
            'is_storage': any(term in text for term in ['mapping', 'array', 'struct']),
            'data_type': self._identify_solidity_type(text)
        }
        return context

    def _identify_business_domain(self, text: str) -> str:
        """Identify the business domain of an entity"""
        domains = {
            'employment': ['employee', 'employer', 'job', 'work', 'salary', 'wage'],
            'rental': ['tenant', 'landlord', 'rent', 'lease', 'property'],
            'financial': ['payment', 'money', 'cost', 'fee', 'deposit'],
            'legal': ['contract', 'agreement', 'obligation', 'clause'],
            'temporal': ['date', 'time', 'deadline', 'duration']
        }
        
        for domain, keywords in domains.items():
            if any(keyword in text for keyword in keywords):
                return domain
        return 'general'

    def _identify_solidity_type(self, text: str) -> str:
        """Identify Solidity data type from text"""
        if any(t in text for t in ['uint', 'int']):
            return 'numeric'
        elif 'address' in text:
            return 'address'
        elif 'bool' in text:
            return 'boolean'
        elif 'string' in text:
            return 'string'
        elif 'mapping' in text:
            return 'mapping'
        else:
            return 'unknown'

    def _calculate_contextual_similarity(self, e_context: Dict[str, Any], s_context: Dict[str, Any]) -> float:
        """Calculate contextual similarity between business and technical contexts"""
        score = 0.0
        
        # Business-to-technical context mapping
        if e_context.get('is_financial') and s_context.get('data_type') == 'numeric':
            score += 0.8
        if e_context.get('is_party') and s_context.get('data_type') == 'address':
            score += 0.9
        if e_context.get('is_temporal') and s_context.get('data_type') in ['numeric', 'string']:
            score += 0.7
        if e_context.get('is_obligation') and s_context.get('is_function'):
            score += 0.8
        
        return min(score, 1.0)

    def _calculate_advanced_text_similarity(self, text1: str, text2: str) -> float:
        """Advanced text similarity using multiple algorithms"""
        # Jaccard similarity
        words1 = set(text1.split())
        words2 = set(text2.split())
        jaccard = len(words1 & words2) / len(words1 | words2) if words1 or words2 else 0
        
        # Sequence similarity
        sequence = difflib.SequenceMatcher(None, text1, text2).ratio()
        
        # Substring similarity
        substring = max(
            len(text1) / len(text2) if text1 in text2 else 0,
            len(text2) / len(text1) if text2 in text1 else 0
        )
        
        return max(jaccard, sequence, substring)

    def _get_enhanced_business_mapping(self, e_entity: Dict[str, Any], s_entity: Dict[str, Any]) -> float:
        """Enhanced business-to-technical mapping with comprehensive pattern matching"""
        e_text = e_entity.get('text', '').lower()
        s_text = s_entity.get('text', '').lower()
        
        # Comprehensive enhanced mapping patterns
        enhanced_mappings = {
            # Party mappings with variations
            ('tenant', 'address'): 0.95, ('renter', 'address'): 0.95, ('lessee', 'address'): 0.95,
            ('landlord', 'address'): 0.95, ('lessor', 'address'): 0.95, ('owner', 'address'): 0.90,
            ('employee', 'address'): 0.95, ('worker', 'address'): 0.90, ('staff', 'address'): 0.85,
            ('employer', 'address'): 0.95, ('company', 'address'): 0.90, ('corporation', 'address'): 0.90,
            ('contractor', 'address'): 0.90, ('freelancer', 'address'): 0.85, ('consultant', 'address'): 0.85,
            ('client', 'address'): 0.90, ('customer', 'address'): 0.85, ('buyer', 'address'): 0.85,
            
            # Financial mappings with context
            ('rent', 'amount'): 0.95, ('rental', 'amount'): 0.90, ('lease', 'amount'): 0.85,
            ('salary', 'amount'): 0.95, ('wage', 'amount'): 0.90, ('compensation', 'amount'): 0.90,
            ('payment', 'amount'): 0.90, ('pay', 'amount'): 0.85, ('remuneration', 'amount'): 0.85,
            ('fee', 'amount'): 0.90, ('charge', 'amount'): 0.85, ('cost', 'amount'): 0.80,
            ('deposit', 'amount'): 0.90, ('security', 'amount'): 0.85, ('bond', 'amount'): 0.80,
            ('fine', 'amount'): 0.85, ('penalty', 'amount'): 0.85, ('late', 'amount'): 0.80,
            
            # Contract state and function mappings
            ('contract', 'active'): 0.85, ('agreement', 'active'): 0.85, ('deal', 'active'): 0.80,
            ('terminated', 'terminate'): 0.95, ('ended', 'terminate'): 0.90, ('cancelled', 'terminate'): 0.85,
            ('signed', 'active'): 0.80, ('executed', 'active'): 0.75, ('valid', 'active'): 0.70,
            ('breach', 'terminate'): 0.85, ('violation', 'terminate'): 0.80, ('default', 'terminate'): 0.80,
            
            # Temporal mappings with enhanced context
            ('deadline', 'timestamp'): 0.90, ('due', 'timestamp'): 0.85, ('expiry', 'timestamp'): 0.85,
            ('date', 'timestamp'): 0.85, ('time', 'timestamp'): 0.80, ('period', 'timestamp'): 0.75,
            ('start', 'timestamp'): 0.85, ('begin', 'timestamp'): 0.80, ('commence', 'timestamp'): 0.80,
            ('end', 'timestamp'): 0.85, ('finish', 'timestamp'): 0.80, ('complete', 'timestamp'): 0.75,
            
            # Obligation and condition mappings
            ('obligation', 'function'): 0.90, ('duty', 'function'): 0.85, ('responsibility', 'function'): 0.85,
            ('condition', 'modifier'): 0.85, ('requirement', 'modifier'): 0.80, ('clause', 'modifier'): 0.75,
            ('rule', 'modifier'): 0.80, ('policy', 'modifier'): 0.75, ('standard', 'modifier'): 0.70,
        }
        
        # Check for direct matches with enhanced scoring
        best_score = 0.0
        for (business_term, tech_term), score in enhanced_mappings.items():
            if business_term in e_text and tech_term in s_text:
                best_score = max(best_score, score)
        
        # Additional pattern matching for complex business rules
        if best_score == 0.0:
            best_score = self._match_business_rule_patterns(e_text, s_text)
        
        # Fallback to original mapping if still no match
        if best_score == 0.0:
            best_score = self._get_business_to_technical_mapping(e_entity, s_entity)
            
        return best_score

    def _match_business_rule_patterns(self, e_text: str, s_text: str) -> float:
        """Match complex business rule patterns to technical implementations"""
        score = 0.0
        
        # Payment validation patterns
        if any(term in e_text for term in ['pay', 'payment', 'money']) and \
           any(term in s_text for term in ['require', 'validate', 'check', 'verify']):
            score = max(score, 0.75)
            
        # Access control patterns  
        if any(term in e_text for term in ['only', 'authorized', 'permitted']) and \
           any(term in s_text for term in ['modifier', 'require', 'msg.sender']):
            score = max(score, 0.80)
            
        # Time-based validation patterns
        if any(term in e_text for term in ['deadline', 'expire', 'time']) and \
           any(term in s_text for term in ['timestamp', 'block.timestamp', 'now']):
            score = max(score, 0.70)
            
        # State management patterns
        if any(term in e_text for term in ['status', 'state', 'condition']) and \
           any(term in s_text for term in ['bool', 'enum', 'mapping']):
            score = max(score, 0.65)
            
        return score

    def _calculate_accuracy_score(self, e_kg, s_kg, matches: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate comprehensive accuracy score for smart contract generation"""
        
        # Entity coverage analysis
        entity_coverage = len(matches['entity_matches']) / len(e_kg.entities) if e_kg.entities else 0
        
        # Relationship preservation analysis
        relation_coverage = len(matches['relationship_matches']) / len(e_kg.relationships) if e_kg.relationships else 0
        
        # Business logic preservation
        business_logic_score = self._analyze_business_logic_preservation(e_kg, s_kg)
        
        # Contract completeness
        completeness_score = self._analyze_contract_completeness(s_kg)
        
        # Calculate weighted accuracy
        accuracy_weights = {
            'entity_coverage': 0.3,
            'relation_coverage': 0.25,
            'business_logic': 0.3,
            'completeness': 0.15
        }
        
        weighted_accuracy = (
            entity_coverage * accuracy_weights['entity_coverage'] +
            relation_coverage * accuracy_weights['relation_coverage'] +
            business_logic_score * accuracy_weights['business_logic'] +
            completeness_score * accuracy_weights['completeness']
        )
        
        return {
            'accuracy_score': weighted_accuracy,
            'deployment_ready': weighted_accuracy > 0.7 and completeness_score > 0.6,
            'entity_coverage': entity_coverage,
            'relation_coverage': relation_coverage,
            'business_logic_score': business_logic_score,
            'completeness_score': completeness_score
        }

    def _analyze_business_logic_preservation(self, e_kg, s_kg) -> float:
        """Comprehensive analysis of business logic preservation in smart contract"""
        score = 0.0
        
        # Enhanced business concept detection with scoring weights
        business_concepts = {
            # Core business entities (high importance)
            'parties': ['party', 'tenant', 'landlord', 'employee', 'employer', 'client', 'provider'],
            'financial': ['payment', 'salary', 'rent', 'fee', 'cost', 'amount', 'money'],
            'obligations': ['obligation', 'duty', 'responsibility', 'must', 'shall', 'required'],
            'conditions': ['condition', 'if', 'when', 'provided', 'subject', 'contingent'],
            'temporal': ['date', 'time', 'deadline', 'duration', 'period', 'schedule'],
            # Contract management (medium importance)
            'termination': ['terminate', 'end', 'cancel', 'expire', 'breach'],
            'validation': ['validate', 'verify', 'check', 'confirm', 'approve'],
            'access_control': ['authorized', 'permitted', 'restricted', 'allowed'],
        }
        
        e_entities_text = ' '.join([e.get('text', '') for e in e_kg.entities.values()]).lower()
        s_entities_text = ' '.join([e.get('text', '') for e in s_kg.entities.values()]).lower()
        
        # Add relationships text for broader context
        e_relations_text = ' '.join([r.get('relation', '') for r in e_kg.relationships.values()]).lower()
        s_relations_text = ' '.join([r.get('relation', '') for r in s_kg.relationships.values()]).lower()
        
        e_full_text = f"{e_entities_text} {e_relations_text}"
        s_full_text = f"{s_entities_text} {s_relations_text}"
        
        concept_weights = {
            'parties': 0.20, 'financial': 0.18, 'obligations': 0.16, 'conditions': 0.14, 
            'temporal': 0.12, 'termination': 0.08, 'validation': 0.07, 'access_control': 0.05
        }
        
        preserved_score = 0.0
        for concept_group, keywords in business_concepts.items():
            e_has_concept = any(keyword in e_full_text for keyword in keywords)
            s_has_concept = any(keyword in s_full_text for keyword in keywords)
            
            if e_has_concept and s_has_concept:
                preserved_score += concept_weights[concept_group]
            elif e_has_concept:  # Concept in e-contract but missing in smart contract
                preserved_score += concept_weights[concept_group] * 0.3  # Partial credit for awareness
        
        # Business rule structure preservation (relationships to functions)
        relationship_score = 0.0
        if len(e_kg.relationships) > 0:
            relationship_ratio = min(len(s_kg.relationships) / len(e_kg.relationships), 1.0)
            # Enhanced scoring for relationship complexity
            if relationship_ratio > 0.7:
                relationship_score = 0.30  # Excellent preservation
            elif relationship_ratio > 0.5:
                relationship_score = 0.25  # Good preservation
            elif relationship_ratio > 0.3:
                relationship_score = 0.20  # Fair preservation
            else:
                relationship_score = relationship_ratio * 0.15  # Poor preservation
        
        # Smart contract completeness bonus
        completeness_bonus = 0.0
        if 'function' in s_full_text and 'constructor' in s_full_text:
            completeness_bonus += 0.05
        if any(term in s_full_text for term in ['event', 'modifier', 'require']):
            completeness_bonus += 0.05
        
        total_score = preserved_score + relationship_score + completeness_bonus
        return min(total_score, 1.0)

    def _analyze_contract_completeness(self, s_kg) -> float:
        """Comprehensive analysis of generated smart contract completeness"""
        score = 0.0
        
        entities_text = ' '.join([e.get('text', '') for e in s_kg.entities.values()]).lower()
        relations_text = ' '.join([r.get('relation', '') for r in s_kg.relationships.values()]).lower()
        full_text = f"{entities_text} {relations_text}"
        
        # Enhanced essential smart contract elements with detailed scoring
        essential_elements = {
            # Core structural elements
            'constructor_elements': {
                'patterns': ['constructor', 'initialize', 'init'],
                'weight': 0.15,
                'bonus_patterns': ['parameter', 'address', 'party']  # Constructor with proper params
            },
            'state_variables': {
                'patterns': ['uint256', 'address', 'bool', 'mapping', 'variable'],
                'weight': 0.20,
                'bonus_patterns': ['public', 'private', 'internal']  # Proper visibility
            },
            'functions': {
                'patterns': ['function', 'external', 'public', 'internal'],
                'weight': 0.25,
                'bonus_patterns': ['payable', 'view', 'pure', 'returns']  # Function modifiers
            },
            # Business logic elements
            'events': {
                'patterns': ['event', 'emit', 'log'],
                'weight': 0.10,
                'bonus_patterns': ['indexed', 'timestamp', 'address']  # Proper event params
            },
            'modifiers': {
                'patterns': ['modifier', 'require', 'only'],
                'weight': 0.10,
                'bonus_patterns': ['msg.sender', 'authorized', 'active']  # Access control
            },
            # Advanced elements
            'error_handling': {
                'patterns': ['require', 'revert', 'assert'],
                'weight': 0.08,
                'bonus_patterns': ['error', 'message', 'condition']
            },
            'business_validation': {
                'patterns': ['validate', 'check', 'verify'],
                'weight': 0.07,
                'bonus_patterns': ['payment', 'deadline', 'condition']
            },
            'state_management': {
                'patterns': ['active', 'status', 'completed'],
                'weight': 0.05,
                'bonus_patterns': ['enum', 'mapping', 'tracking']
            }
        }
        
        for element_group, element_data in essential_elements.items():
            element_found = any(pattern in full_text for pattern in element_data['patterns'])
            if element_found:
                base_score = element_data['weight']
                # Bonus for advanced implementation
                bonus_found = any(bonus in full_text for bonus in element_data.get('bonus_patterns', []))
                if bonus_found:
                    base_score *= 1.2  # 20% bonus for advanced implementation
                score += base_score
        
        # Additional completeness checks
        completeness_bonuses = {
            'comprehensive_access_control': {
                'check': lambda text: all(term in text for term in ['modifier', 'require', 'msg.sender']),
                'bonus': 0.05
            },
            'proper_event_system': {
                'check': lambda text: 'event' in text and 'emit' in text,
                'bonus': 0.03
            },
            'business_rule_enforcement': {
                'check': lambda text: any(term in text for term in ['validate', 'enforce', 'check']) and 'require' in text,
                'bonus': 0.04
            },
            'temporal_handling': {
                'check': lambda text: any(term in text for term in ['timestamp', 'deadline', 'block.timestamp']),
                'bonus': 0.03
            }
        }
        
        for bonus_name, bonus_data in completeness_bonuses.items():
            if bonus_data['check'](full_text):
                score += bonus_data['bonus']
        
        return min(score, 1.0)

    def _determine_compliance_level(self, similarity: float, accuracy_data: Dict[str, Any]) -> str:
        """Determine compliance level based on multiple factors"""
        business_logic_score = accuracy_data.get('business_logic_score', 0)
        completeness_score = accuracy_data.get('completeness_score', 0)
        
        # Weighted compliance scoring
        weighted_score = (similarity * 0.4 + business_logic_score * 0.35 + completeness_score * 0.25)
        
        if weighted_score >= 0.80:
            return 'High'
        elif weighted_score >= 0.65:
            return 'Medium-High'
        elif weighted_score >= 0.50:
            return 'Medium'
        elif weighted_score >= 0.35:
            return 'Medium-Low'
        else:
            return 'Low'
    
    def _assess_deployment_readiness(self, similarity: float, accuracy_data: Dict[str, Any]) -> bool:
        """Comprehensive deployment readiness assessment"""
        # Multiple criteria for deployment readiness
        criteria = {
            'similarity_threshold': similarity >= 0.60,
            'business_logic_preserved': accuracy_data.get('business_logic_score', 0) >= 0.50,
            'contract_complete': accuracy_data.get('completeness_score', 0) >= 0.60,
            'entity_coverage': accuracy_data.get('entity_coverage', 0) >= 0.70
        }
        
        # Require at least 3 out of 4 criteria to be met
        met_criteria = sum(criteria.values())
        return met_criteria >= 3
    
    def _identify_compliance_issues(self, similarity: float, accuracy_data: Dict[str, Any]) -> List[str]:
        """Identify specific compliance issues for targeted improvement"""
        issues = []
        
        if similarity < 0.60:
            issues.append(f"Overall similarity too low ({similarity:.1%} < 60%)")
        
        business_logic_score = accuracy_data.get('business_logic_score', 0)
        if business_logic_score < 0.50:
            issues.append(f"Insufficient business logic preservation ({business_logic_score:.1%} < 50%)")
        
        completeness_score = accuracy_data.get('completeness_score', 0)
        if completeness_score < 0.60:
            issues.append(f"Contract elements incomplete ({completeness_score:.1%} < 60%)")
        
        entity_coverage = accuracy_data.get('entity_coverage', 0)
        if entity_coverage < 0.70:
            issues.append(f"Low entity coverage ({entity_coverage:.1%} < 70%)")
        
        relation_coverage = accuracy_data.get('relation_coverage', 0)
        if relation_coverage < 0.40:
            issues.append(f"Poor relationship modeling ({relation_coverage:.1%} < 40%)")
        
        if not issues:
            issues.append("All compliance criteria met - ready for deployment")
            
        return issues


# Legacy alias for backwards compatibility
ContractComparator = KnowledgeGraphComparator