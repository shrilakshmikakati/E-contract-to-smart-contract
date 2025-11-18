"""
Comparator implementing Algorithm 3 & 4: Compare Knowledge Graphs and Integrated Contract Analysis
"""

from typing import Dict, Any, List, Tuple, Optional, Set
import difflib
from datetime import datetime
from collections import defaultdict
import numpy as np

from .knowledge_graph import KnowledgeGraph
from .econtract_processor import EContractProcessor
from .smartcontract_processor import SmartContractProcessor
from ..utils.file_handler import FileHandler

class ContractComparator:
    """
    Compares knowledge graphs from e-contracts and smart contracts
    Implements Algorithms 3 & 4 from the research paper
    """
    
    def __init__(self):
        self.econtract_processor = EContractProcessor()
        self.smartcontract_processor = SmartContractProcessor()
        self.comparison_results = {}
    
    def compare_knowledge_graphs(self, g_e: KnowledgeGraph, g_s: KnowledgeGraph, 
                                comparison_id: str = None) -> Dict[str, Any]:
        """
        Algorithm 3: Compare Knowledge Graphs
        
        Args:
            g_e: E-contract knowledge graph G_e = (V_e, E_e)
            g_s: Smart contract knowledge graph G_s = (V_s, E_s)
            comparison_id: Optional identifier for this comparison
            
        Returns:
            Discrepancy report Δ = (Δ_V, Δ_E)
        """
        if comparison_id is None:
            comparison_id = f"comparison_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"Comparing knowledge graphs: {comparison_id}")
        
        # Step 1: Match entities (M_V ← MatchEntities(V_e, V_s))
        print("Step 1: Matching entities...")
        entity_matches = self._match_entities(g_e.entities, g_s.entities)
        
        # Step 2: Match relations (M_E ← MatchRelations(E_e, E_s))
        print("Step 2: Matching relationships...")
        relation_matches = self._match_relations(g_e.relationships, g_s.relationships)
        
        # Step 3: Calculate entity discrepancies (Δ_V ← V_e ∪ V_s \ M_V)
        print("Step 3: Calculating entity discrepancies...")
        entity_discrepancies = self._calculate_entity_discrepancies(
            g_e.entities, g_s.entities, entity_matches
        )
        
        # Step 4: Calculate relation discrepancies (Δ_E ← E_e ∪ E_s \ M_E)
        print("Step 4: Calculating relationship discrepancies...")
        relation_discrepancies = self._calculate_relation_discrepancies(
            g_e.relationships, g_s.relationships, relation_matches
        )
        
        # Step 5: Generate comprehensive discrepancy report (Δ ← (Δ_V, Δ_E))
        print("Step 5: Generating discrepancy report...")
        discrepancy_report = self._generate_discrepancy_report(
            entity_matches, relation_matches, entity_discrepancies, 
            relation_discrepancies, g_e, g_s
        )
        
        # Store comparison results
        self.comparison_results[comparison_id] = {
            'econtract_graph': g_e,
            'smartcontract_graph': g_s,
            'entity_matches': entity_matches,
            'relation_matches': relation_matches,
            'entity_discrepancies': entity_discrepancies,
            'relation_discrepancies': relation_discrepancies,
            'discrepancy_report': discrepancy_report,
            'comparison_time': datetime.now().isoformat()
        }
        
        print(f"Knowledge graph comparison completed: {comparison_id}")
        
        return discrepancy_report
    
    def integrated_contract_analysis(self, econtract_text: str, smartcontract_code: str,
                                   analysis_id: str = None) -> Dict[str, Any]:
        """
        Algorithm 4: Integrated Contract Analysis and Comparison
        
        Args:
            econtract_text: E-contract text T_e
            smartcontract_code: Smart contract code S
            analysis_id: Optional identifier for this analysis
            
        Returns:
            Validation report Δ
        """
        if analysis_id is None:
            analysis_id = f"analysis_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"Starting integrated contract analysis: {analysis_id}")
        
        # Step 1: Generate e-contract knowledge graph (G_e ← E-ContractKnowledgeGraphConstruction(T_e))
        print("Step 1: Processing e-contract...")
        g_e = self.econtract_processor.process_contract(econtract_text, f"{analysis_id}_econtract")
        
        # Step 2: Generate smart contract knowledge graph (G_s ← SmartContractKnowledgeGraphConstruction(S))
        print("Step 2: Processing smart contract...")
        g_s = self.smartcontract_processor.process_contract(smartcontract_code, f"{analysis_id}_smartcontract")
        
        # Step 3: Compare knowledge graphs (Δ ← CompareKnowledgeGraphs(G_e, G_s))
        print("Step 3: Comparing knowledge graphs...")
        validation_report = self.compare_knowledge_graphs(g_e, g_s, analysis_id)
        
        # Enhance validation report with additional analysis
        enhanced_report = self._enhance_validation_report(validation_report, g_e, g_s, analysis_id)
        
        print(f"Integrated contract analysis completed: {analysis_id}")
        
        return enhanced_report
    
    def _match_entities(self, entities_e: Dict[str, Any], entities_s: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Match entities between e-contract and smart contract graphs"""
        matches = []
        
        # Convert entities to lists for easier processing
        e_entities = [{'id': eid, **data} for eid, data in entities_e.items()]
        s_entities = [{'id': sid, **data} for sid, data in entities_s.items()]
        
        # Match entities based on enhanced similarity algorithm
        for e_entity in e_entities:
            best_match = None
            best_score = 0
            
            for s_entity in s_entities:
                similarity_score = self._calculate_entity_similarity(e_entity, s_entity)
                
                if similarity_score > best_score and similarity_score > 0.25:  # Reduced threshold from 0.5 to 0.25
                    best_score = similarity_score
                    best_match = s_entity
            
            if best_match:
                matches.append({
                    'econtract_entity': e_entity,
                    'smartcontract_entity': best_match,
                    'similarity_score': best_score,
                    'match_type': self._classify_match_type(e_entity, best_match),
                    'confidence': self._calculate_match_confidence(e_entity, best_match, best_score)
                })
        return matches
    
    def _match_relations(self, relations_e: Dict[str, Any], relations_s: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Match relationships between e-contract and smart contract graphs"""
        matches = []
        
        # Convert relations to lists
        e_relations = [{'id': rid, **data} for rid, data in relations_e.items()]
        s_relations = [{'id': rid, **data} for rid, data in relations_s.items()]
        
        # Match relations based on type and connected entities
        for e_relation in e_relations:
            best_match = None
            best_score = 0
            
            for s_relation in s_relations:
                similarity_score = self._calculate_relation_similarity(e_relation, s_relation)
                
                if similarity_score > best_score and similarity_score > 0.2:  # Reduced threshold from 0.4 to 0.2
                    best_score = similarity_score
                    best_match = s_relation
            
            if best_match:
                matches.append({
                    'econtract_relation': e_relation,
                    'smartcontract_relation': best_match,
                    'similarity_score': best_score,
                    'match_type': self._classify_relation_match_type(e_relation, best_match),
                    'confidence': self._calculate_relation_match_confidence(e_relation, best_match, best_score)
                })
        
        return matches
    
    def _calculate_entity_similarity(self, e_entity: Dict[str, Any], s_entity: Dict[str, Any]) -> float:
        """Calculate similarity score between two entities with business-to-technical mapping"""
        score = 0.0
        
        text_e = e_entity.get('text', '').lower().strip()
        text_s = s_entity.get('text', '').lower().strip()
        type_e = e_entity.get('type', '').upper()
        type_s = s_entity.get('type', '').upper()
        
        # 1. BUSINESS-TO-TECHNICAL ENTITY MAPPING (New - Primary Factor)
        business_to_tech_mapping = self._get_business_to_technical_mapping(e_entity, s_entity)
        if business_to_tech_mapping > 0:
            score += business_to_tech_mapping * 0.5  # High weight for business mappings
        
        # 2. SEMANTIC TYPE COMPATIBILITY (Enhanced)
        if self._are_compatible_types(type_e, type_s):
            score += 0.3  # Strong compatibility bonus
        elif self._are_related_entity_domains(type_e, type_s):
            score += 0.2  # Related domain bonus
        
        # 3. TEXT SIMILARITY (Reduced weight, more flexible)
        if text_e and text_s:
            # Direct text match
            text_similarity = difflib.SequenceMatcher(None, text_e, text_s).ratio()
            # Substring matching for partial matches
            substring_match = max(
                len(text_e) / len(text_s) if text_e in text_s else 0,
                len(text_s) / len(text_e) if text_s in text_e else 0
            )
            best_text_score = max(text_similarity, substring_match)
            score += best_text_score * 0.15  # Reduced from 0.4 to 0.15
        
        # 4. SEMANTIC CONTEXT SIMILARITY (Enhanced)
        semantic_score = self._calculate_enhanced_semantic_similarity(e_entity, s_entity)
        score += semantic_score * 0.25  # Increased from 0.1 to 0.25
        
        # 5. CATEGORY AND LABEL MATCHING
        label_e = e_entity.get('label', '').upper()
        label_s = s_entity.get('label', '').upper()
        category_e = e_entity.get('category', '').upper()
        category_s = s_entity.get('category', '').upper()
        
        if label_e == label_s:
            score += 0.1
        elif self._are_compatible_categories(category_e, category_s):
            score += 0.05
        
        return min(score, 1.0)  # Cap at 1.0
    
    def _calculate_relation_similarity(self, e_relation: Dict[str, Any], s_relation: Dict[str, Any]) -> float:
        """Enhanced relationship similarity calculation"""
        score = 0.0
        
        relation_e = e_relation.get('relation', '').lower()
        relation_s = s_relation.get('relation', '').lower()
        
        # 1. BUSINESS-TO-TECHNICAL RELATIONSHIP MAPPING
        business_relation_mapping = self._get_business_to_technical_relation_mapping(e_relation, s_relation)
        if business_relation_mapping > 0:
            score += business_relation_mapping * 0.4
        
        # 2. DIRECT RELATION TYPE SIMILARITY
        if relation_e == relation_s:
            score += 0.3  # Reduced from 0.5
        elif self._are_compatible_relations(relation_e, relation_s):
            score += 0.2   # Reduced from 0.25
        
        # 3. ENHANCED SOURCE AND TARGET COMPATIBILITY
        source_type_e = e_relation.get('source_type', '').upper()
        target_type_e = e_relation.get('target_type', '').upper()
        source_type_s = s_relation.get('source_type', '').upper()
        target_type_s = s_relation.get('target_type', '').upper()
        
        # Source compatibility (enhanced)
        if source_type_e == source_type_s:
            score += 0.1
        elif self._are_compatible_types(source_type_e, source_type_s):
            score += 0.06
        elif self._are_related_entity_domains(source_type_e, source_type_s):
            score += 0.03
        
        # Target compatibility (enhanced)
        if target_type_e == target_type_s:
            score += 0.1
        elif self._are_compatible_types(target_type_e, target_type_s):
            score += 0.06
        elif self._are_related_entity_domains(target_type_e, target_type_s):
            score += 0.03
        
        # 4. SEMANTIC RELATIONSHIP CONTEXT
        semantic_relation_score = self._calculate_semantic_relation_similarity(e_relation, s_relation)
        score += semantic_relation_score * 0.15
        
        # 5. CONFIDENCE AND QUALITY FACTORS
        conf_e = e_relation.get('confidence', 0.5)
        conf_s = s_relation.get('confidence', 0.5)
        score += min(conf_e, conf_s) * 0.05  # Reduced weight
        
        return min(score, 1.0)
    
    def _are_compatible_types(self, type1: str, type2: str) -> bool:
        """Enhanced entity type compatibility check"""
        # Expanded compatibility mappings for better business-to-technical matching
        compatibility_mappings = {
            # Party/Organization mappings (expanded)
            'PERSON': ['PARTY', 'ORGANIZATION', 'CONTRACT_PARTY', 'VARIABLE', 'STATE_VARIABLE'],
            'ORG': ['ORGANIZATION', 'PARTY', 'CONTRACT_PARTY', 'VARIABLE', 'STATE_VARIABLE'],
            'PARTY': ['PERSON', 'ORG', 'ORGANIZATION', 'VARIABLE', 'STATE_VARIABLE'],
            
            # Financial mappings (expanded)
            'MONEY': ['FINANCIAL', 'MONETARY_AMOUNT', 'CURRENCY', 'VARIABLE', 'STATE_VARIABLE'],
            'FINANCIAL': ['MONEY', 'MONETARY_AMOUNT', 'CURRENCY', 'VARIABLE', 'STATE_VARIABLE'],
            'CURRENCY': ['MONEY', 'FINANCIAL', 'VARIABLE', 'STATE_VARIABLE'],
            
            # Temporal mappings (expanded)
            'DATE': ['TEMPORAL', 'DATE_TERMS', 'TIME', 'VARIABLE', 'STATE_VARIABLE'],
            'TIME': ['TEMPORAL', 'DATE', 'DATE_TERMS', 'VARIABLE', 'STATE_VARIABLE'],
            'TEMPORAL': ['DATE', 'TIME', 'VARIABLE', 'STATE_VARIABLE'],
            
            # Function/Action mappings (expanded)
            'FUNCTION': ['SMART_CONTRACT_FUNCTION', 'FUNCTION_DEFINITION', 'OBLIGATIONS', 'CONDITIONS'],
            'OBLIGATIONS': ['LEGAL_OBLIGATION', 'FUNCTION', 'SMART_CONTRACT_FUNCTION', 'CONDITIONS'],
            'CONDITIONS': ['CONDITION', 'MODIFIER', 'FUNCTION', 'OBLIGATIONS'],
            
            # Smart Contract specific mappings
            'VARIABLE': ['STATE_VARIABLE', 'SMART_CONTRACT_VARIABLE', 'PERSON', 'ORG', 'MONEY', 'DATE'],
            'STATE_VARIABLE': ['VARIABLE', 'SMART_CONTRACT_VARIABLE', 'PERSON', 'ORG', 'MONEY', 'DATE'],
            'SMART_CONTRACT_FUNCTION': ['FUNCTION', 'FUNCTION_DEFINITION', 'OBLIGATIONS', 'CONDITIONS'],
            'CONTRACT': ['SMART_CONTRACT', 'CONTRACT_DEFINITION', 'AGREEMENT'],
            'SMART_CONTRACT': ['CONTRACT', 'CONTRACT_DEFINITION', 'AGREEMENT']
        }
        
        # Check direct compatibility
        for key, compatible_types in compatibility_mappings.items():
            if (type1 == key and type2 in compatible_types) or (type2 == key and type1 in compatible_types):
                return True
        
        return False
    
    def _are_compatible_categories(self, cat1: str, cat2: str) -> bool:
        """Enhanced entity category compatibility check"""
        # Expanded category mappings for better business-to-technical matching
        category_mappings = {
            # Business entity categories to smart contract categories
            'PARTY': ['CONTRACT_DEFINITION', 'ORGANIZATION', 'STATE_STORAGE', 'FUNCTION_COMPONENT'],
            'FINANCIAL': ['STATE_STORAGE', 'FUNCTION_COMPONENT', 'DATA_COMPONENT', 'VARIABLE_STORAGE'],
            'TEMPORAL': ['FUNCTION_COMPONENT', 'DATA_COMPONENT', 'STATE_STORAGE', 'VARIABLE_STORAGE'],
            'LEGAL_OBLIGATION': ['FUNCTION_DEFINITION', 'ACCESS_CONTROL', 'FUNCTION_COMPONENT', 'CONTRACT_LOGIC'],
            'LEGAL_PROVISION': ['CONTRACT_DEFINITION', 'ACCESS_CONTROL', 'FUNCTION_DEFINITION', 'CONTRACT_LOGIC'],
            
            # Smart contract categories to business categories
            'CONTRACT_DEFINITION': ['PARTY', 'LEGAL_PROVISION', 'ORGANIZATION'],
            'STATE_STORAGE': ['FINANCIAL', 'TEMPORAL', 'PARTY', 'DATA_ELEMENT'],
            'FUNCTION_COMPONENT': ['FINANCIAL', 'TEMPORAL', 'LEGAL_OBLIGATION', 'SERVICE_ELEMENT'],
            'FUNCTION_DEFINITION': ['LEGAL_OBLIGATION', 'LEGAL_PROVISION', 'SERVICE_ELEMENT'],
            'ACCESS_CONTROL': ['LEGAL_OBLIGATION', 'LEGAL_PROVISION', 'SECURITY_ELEMENT'],
            'DATA_COMPONENT': ['FINANCIAL', 'TEMPORAL', 'DATA_ELEMENT'],
            
            # Cross-domain mappings
            'ORGANIZATION': ['PARTY', 'CONTRACT_DEFINITION'],
            'SERVICE_ELEMENT': ['LEGAL_OBLIGATION', 'FUNCTION_COMPONENT', 'FUNCTION_DEFINITION'],
            'DATA_ELEMENT': ['FINANCIAL', 'TEMPORAL', 'STATE_STORAGE', 'DATA_COMPONENT']
        }
        
        for key, compatible_cats in category_mappings.items():
            if (cat1 == key and cat2 in compatible_cats) or (cat2 == key and cat1 in compatible_cats):
                return True
        
        return False
    
    def _get_business_to_technical_relation_mapping(self, e_relation: Dict[str, Any], s_relation: Dict[str, Any]) -> float:
        """Map business relationships to technical smart contract relationships"""
        e_rel = e_relation.get('relation', '').lower()
        s_rel = s_relation.get('relation', '').lower()
        
        # Business relationship to smart contract relationship mappings
        business_relation_mappings = {
            # Contract obligations -> Function calls/parameters
            'obligation_mappings': {
                'business_relations': ['obligation', 'must_do', 'shall_perform', 'required_to'],
                'technical_relations': ['has_parameter', 'contains', 'calls', 'requires', 'modifies']
            },
            # Financial relationships -> Value transfers/storage
            'financial_mappings': {
                'business_relations': ['payment', 'pays', 'financial', 'monetary', 'cost'],
                'technical_relations': ['has_member', 'contains', 'stores', 'transfers', 'updates']
            },
            # Temporal relationships -> State changes/timing
            'temporal_mappings': {
                'business_relations': ['temporal', 'deadline', 'duration', 'schedule'],
                'technical_relations': ['contains', 'inherits_from', 'depends_on', 'triggers']
            },
            # Conditional relationships -> Logic/control flow
            'conditional_mappings': {
                'business_relations': ['condition', 'if_then', 'requires', 'depends_on'],
                'technical_relations': ['has_parameter', 'contains', 'controls', 'validates']
            },
            # Co-occurrence -> Data relationships
            'co_occurrence_mappings': {
                'business_relations': ['co_occurrence', 'associated_with', 'related_to'],
                'technical_relations': ['has_member', 'contains', 'references', 'includes']
            }
        }
        
        max_mapping_score = 0.0
        
        for mapping_type, mapping_data in business_relation_mappings.items():
            e_matches_business = any(pattern in e_rel for pattern in mapping_data['business_relations'])
            s_matches_technical = any(pattern in s_rel for pattern in mapping_data['technical_relations'])
            
            if e_matches_business and s_matches_technical:
                max_mapping_score = max(max_mapping_score, 0.8)  # Strong mapping
            elif e_matches_business and s_rel in ['contains', 'has_member', 'has_parameter']:
                max_mapping_score = max(max_mapping_score, 0.6)  # Moderate mapping
        
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
        # Original mappings (expanded)
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
    
    def _get_business_to_technical_mapping(self, e_entity: Dict[str, Any], s_entity: Dict[str, Any]) -> float:
        """Map business entities to technical smart contract elements"""
        e_text = e_entity.get('text', '').lower().strip()
        e_type = e_entity.get('type', '').upper()
        s_text = s_entity.get('text', '').lower().strip()
        s_type = s_entity.get('type', '').upper()
        
        # Business entity to smart contract mappings
        business_mappings = {
            # Party/Organization mappings
            'party_mappings': {
                'patterns': ['corporation', 'company', 'inc', 'llc', 'ltd', 'party a', 'party b', 'client', 'provider', 'contractor'],
                'smart_contract_vars': ['client', 'provider', 'party', 'owner', 'contractor', 'payee', 'payer']
            },
            # Financial mappings
            'financial_mappings': {
                'patterns': ['$', 'usd', 'payment', 'fee', 'cost', 'amount', 'price', 'salary', 'wage'],
                'smart_contract_vars': ['amount', 'price', 'fee', 'payment', 'balance', 'value', 'cost']
            },
            # Temporal mappings
            'temporal_mappings': {
                'patterns': ['month', 'day', 'year', 'deadline', 'duration', 'start', 'end', 'january', 'february'],
                'smart_contract_vars': ['deadline', 'timestamp', 'duration', 'starttime', 'endtime', 'expiry']
            },
            # Service/Function mappings
            'service_mappings': {
                'patterns': ['service', 'work', 'development', 'consulting', 'delivery', 'obligation'],
                'smart_contract_vars': ['complete', 'deliver', 'execute', 'perform', 'fulfill', 'finish']
            },
            # Status/Condition mappings
            'status_mappings': {
                'patterns': ['completed', 'finished', 'approved', 'signed', 'agreed'],
                'smart_contract_vars': ['completed', 'approved', 'signed', 'active', 'finished', 'executed']
            }
        }\n        \n        max_mapping_score = 0.0\n        \n        for mapping_type, mapping_data in business_mappings.items():\n            e_matches_pattern = any(pattern in e_text for pattern in mapping_data['patterns'])\n            s_matches_var = any(var in s_text for var in mapping_data['smart_contract_vars'])\n            \n            if e_matches_pattern and s_matches_var:\n                # Strong mapping if both match the pattern\n                max_mapping_score = max(max_mapping_score, 0.9)\n            elif e_matches_pattern and s_type in ['VARIABLE', 'FUNCTION', 'STATE_VARIABLE']:\n                # Moderate mapping if e-entity matches pattern and s-entity is a smart contract element\n                max_mapping_score = max(max_mapping_score, 0.6)\n            elif (e_type in ['MONEY', 'FINANCIAL'] and s_type in ['VARIABLE'] and \n                  any(word in s_text for word in ['amount', 'price', 'payment', 'fee'])):\n                # Financial entity to financial variable\n                max_mapping_score = max(max_mapping_score, 0.8)\n            elif (e_type in ['PERSON', 'ORG'] and s_type in ['VARIABLE'] and \n                  any(word in s_text for word in ['client', 'provider', 'owner', 'party'])):\n                # Party entity to party variable\n                max_mapping_score = max(max_mapping_score, 0.8)\n        \n        return max_mapping_score\n    \n    def _are_related_entity_domains(self, type1: str, type2: str) -> bool:\n        \"\"\"Check if entity types are from related domains\"\"\"\n        domain_groups = [\n            ['PERSON', 'ORG', 'ORGANIZATION', 'PARTY', 'CONTRACT_PARTY', 'VARIABLE'],\n            ['MONEY', 'FINANCIAL', 'MONETARY_AMOUNT', 'CURRENCY', 'VARIABLE', 'STATE_VARIABLE'],\n            ['DATE', 'TEMPORAL', 'TIME', 'DURATION', 'VARIABLE', 'STATE_VARIABLE'],\n            ['FUNCTION', 'SMART_CONTRACT_FUNCTION', 'OBLIGATIONS', 'CONDITIONS'],\n            ['CONTRACT', 'SMART_CONTRACT', 'AGREEMENT', 'CONTRACT_DEFINITION']\n        ]\n        \n        for group in domain_groups:\n            if type1 in group and type2 in group:\n                return True\n        return False\n    \n    def _calculate_enhanced_semantic_similarity(self, e_entity: Dict[str, Any], s_entity: Dict[str, Any]) -> float:\n        \"\"\"Enhanced semantic similarity calculation\"\"\"\n        e_text = e_entity.get('text', '').lower()\n        s_text = s_entity.get('text', '').lower()\n        e_properties = str(e_entity.get('properties', {})).lower()\n        s_properties = str(s_entity.get('properties', {})).lower()\n        \n        # Expanded semantic keyword groups\n        semantic_groups = {\n            'financial': ['payment', 'money', 'amount', 'fee', 'cost', 'price', 'salary', 'wage', 'balance', 'value', '$'],\n            'temporal': ['date', 'time', 'deadline', 'duration', 'month', 'day', 'year', 'start', 'end', 'timestamp'],\n            'party': ['party', 'client', 'provider', 'contractor', 'organization', 'company', 'person', 'owner'],\n            'contract': ['contract', 'agreement', 'obligation', 'condition', 'term', 'clause', 'provision'],\n            'action': ['function', 'method', 'procedure', 'operation', 'complete', 'execute', 'perform', 'deliver'],\n            'storage': ['variable', 'storage', 'state', 'data', 'property', 'attribute', 'field'],\n            'status': ['completed', 'active', 'finished', 'approved', 'signed', 'executed', 'pending']\n        }\n        \n        e_semantic_groups = set()\n        s_semantic_groups = set()\n        \n        for group_name, keywords in semantic_groups.items():\n            if any(keyword in e_text or keyword in e_properties for keyword in keywords):\n                e_semantic_groups.add(group_name)\n            if any(keyword in s_text or keyword in s_properties for keyword in keywords):\n                s_semantic_groups.add(group_name)\n        \n        if not e_semantic_groups and not s_semantic_groups:\n            return 0.0\n        \n        intersection = len(e_semantic_groups & s_semantic_groups)\n        union = len(e_semantic_groups | s_semantic_groups)\n        \n        return intersection / union if union > 0 else 0.0\n    \n    def _calculate_semantic_similarity(self, e_entity: Dict[str, Any], s_entity: Dict[str, Any]) -> float:\n        \"\"\"Legacy method - redirects to enhanced version\"\"\"\n        return self._calculate_enhanced_semantic_similarity(e_entity, s_entity)
    
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
    
    def _classify_relation_match_type(self, e_relation: Dict[str, Any], s_relation: Dict[str, Any]) -> str:
        """Classify the type of match between relationships"""
        e_rel = e_relation.get('relation', '')
        s_rel = s_relation.get('relation', '')
        
        if e_rel == s_rel:
            return 'exact_match'
        elif self._are_compatible_relations(e_rel, s_rel):
            return 'semantic_match'
        else:
            return 'weak_match'
    
    def _calculate_match_confidence(self, e_entity: Dict[str, Any], s_entity: Dict[str, Any], similarity_score: float) -> float:
        """Calculate confidence in entity match"""
        base_confidence = similarity_score
        
        # Boost confidence for high-quality entities
        e_confidence = e_entity.get('confidence', 0.5)
        s_confidence = s_entity.get('confidence', 0.5)
        
        avg_entity_confidence = (e_confidence + s_confidence) / 2
        
        # Weighted combination
        final_confidence = (base_confidence * 0.7) + (avg_entity_confidence * 0.3)
        
        return min(final_confidence, 1.0)
    
    def _calculate_relation_match_confidence(self, e_relation: Dict[str, Any], s_relation: Dict[str, Any], similarity_score: float) -> float:
        """Calculate confidence in relationship match"""
        base_confidence = similarity_score
        
        # Factor in relation confidence
        e_confidence = e_relation.get('confidence', 0.5)
        s_confidence = s_relation.get('confidence', 0.5)
        
        avg_relation_confidence = (e_confidence + s_confidence) / 2
        
        final_confidence = (base_confidence * 0.8) + (avg_relation_confidence * 0.2)
        
        return min(final_confidence, 1.0)
    
    def _calculate_entity_discrepancies(self, entities_e: Dict[str, Any], entities_s: Dict[str, Any], 
                                      entity_matches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate entity discrepancies (Δ_V)"""
        
        # Get matched entity IDs
        matched_e_ids = set()
        matched_s_ids = set()
        
        for match in entity_matches:
            matched_e_ids.add(match['econtract_entity']['id'])
            matched_s_ids.add(match['smartcontract_entity']['id'])
        
        # Find unmatched entities
        unmatched_e = {eid: data for eid, data in entities_e.items() if eid not in matched_e_ids}
        unmatched_s = {sid: data for sid, data in entities_s.items() if sid not in matched_s_ids}
        
        return {
            'unmatched_econtract_entities': unmatched_e,
            'unmatched_smartcontract_entities': unmatched_s,
            'total_econtract_entities': len(entities_e),
            'total_smartcontract_entities': len(entities_s),
            'matched_entities': len(entity_matches),
            'unmatched_econtract_count': len(unmatched_e),
            'unmatched_smartcontract_count': len(unmatched_s),
            'coverage_ratio_econtract': len(matched_e_ids) / max(len(entities_e), 1),
            'coverage_ratio_smartcontract': len(matched_s_ids) / max(len(entities_s), 1)
        }
    
    def _calculate_relation_discrepancies(self, relations_e: Dict[str, Any], relations_s: Dict[str, Any],
                                        relation_matches: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Calculate relationship discrepancies (Δ_E)"""
        
        # Get matched relation IDs
        matched_e_ids = set()
        matched_s_ids = set()
        
        for match in relation_matches:
            matched_e_ids.add(match['econtract_relation']['id'])
            matched_s_ids.add(match['smartcontract_relation']['id'])
        
        # Find unmatched relations
        unmatched_e = {rid: data for rid, data in relations_e.items() if rid not in matched_e_ids}
        unmatched_s = {rid: data for rid, data in relations_s.items() if rid not in matched_s_ids}
        
        return {
            'unmatched_econtract_relations': unmatched_e,
            'unmatched_smartcontract_relations': unmatched_s,
            'total_econtract_relations': len(relations_e),
            'total_smartcontract_relations': len(relations_s),
            'matched_relations': len(relation_matches),
            'unmatched_econtract_count': len(unmatched_e),
            'unmatched_smartcontract_count': len(unmatched_s),
            'coverage_ratio_econtract': len(matched_e_ids) / max(len(relations_e), 1),
            'coverage_ratio_smartcontract': len(matched_s_ids) / max(len(relations_s), 1)
        }
    
    def _generate_discrepancy_report(self, entity_matches: List[Dict[str, Any]], 
                                   relation_matches: List[Dict[str, Any]],
                                   entity_discrepancies: Dict[str, Any],
                                   relation_discrepancies: Dict[str, Any],
                                   g_e: KnowledgeGraph, g_s: KnowledgeGraph) -> Dict[str, Any]:
        """Generate comprehensive discrepancy report"""
        
        report = {
            'summary': {
                'total_entity_matches': len(entity_matches),
                'total_relation_matches': len(relation_matches),
                'entity_coverage_econtract': entity_discrepancies['coverage_ratio_econtract'],
                'entity_coverage_smartcontract': entity_discrepancies['coverage_ratio_smartcontract'],
                'relation_coverage_econtract': relation_discrepancies['coverage_ratio_econtract'],
                'relation_coverage_smartcontract': relation_discrepancies['coverage_ratio_smartcontract'],
                'overall_similarity_score': self._calculate_overall_similarity(
                    entity_matches, relation_matches, entity_discrepancies, relation_discrepancies
                )
            },
            'entity_analysis': {
                'matches': entity_matches,
                'discrepancies': entity_discrepancies,
                'match_quality_distribution': self._analyze_match_quality(entity_matches),
                'unmatched_entity_analysis': self._analyze_unmatched_entities(entity_discrepancies)
            },
            'relationship_analysis': {
                'matches': relation_matches,
                'discrepancies': relation_discrepancies,
                'match_quality_distribution': self._analyze_relation_match_quality(relation_matches),
                'unmatched_relation_analysis': self._analyze_unmatched_relations(relation_discrepancies)
            },
            'compliance_assessment': self._assess_compliance(
                entity_matches, relation_matches, entity_discrepancies, relation_discrepancies
            ),
            'recommendations': self._generate_recommendations(
                entity_matches, relation_matches, entity_discrepancies, relation_discrepancies
            )
        }
        
        return report
    
    def _calculate_overall_similarity(self, entity_matches: List[Dict[str, Any]], 
                                    relation_matches: List[Dict[str, Any]],
                                    entity_discrepancies: Dict[str, Any],
                                    relation_discrepancies: Dict[str, Any]) -> float:
        """Calculate overall similarity score between the contracts"""
        
        # Entity similarity component
        entity_similarity = 0
        if entity_matches:
            entity_similarity = sum(match['similarity_score'] for match in entity_matches) / len(entity_matches)
        
        # Relation similarity component
        relation_similarity = 0
        if relation_matches:
            relation_similarity = sum(match['similarity_score'] for match in relation_matches) / len(relation_matches)
        
        # Coverage component
        entity_coverage = (entity_discrepancies['coverage_ratio_econtract'] + 
                          entity_discrepancies['coverage_ratio_smartcontract']) / 2
        
        relation_coverage = (relation_discrepancies['coverage_ratio_econtract'] + 
                           relation_discrepancies['coverage_ratio_smartcontract']) / 2
        
        # Weighted overall similarity
        overall_similarity = (
            entity_similarity * 0.3 +
            relation_similarity * 0.2 +
            entity_coverage * 0.3 +
            relation_coverage * 0.2
        )
        
        return round(overall_similarity, 3)
    
    def _analyze_match_quality(self, entity_matches: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze the quality distribution of entity matches"""
        quality_distribution = {'exact_match': 0, 'partial_match': 0, 'semantic_match': 0, 'weak_match': 0}
        
        for match in entity_matches:
            match_type = match.get('match_type', 'weak_match')
            quality_distribution[match_type] = quality_distribution.get(match_type, 0) + 1
        
        return quality_distribution
    
    def _analyze_relation_match_quality(self, relation_matches: List[Dict[str, Any]]) -> Dict[str, int]:
        """Analyze the quality distribution of relationship matches"""
        quality_distribution = {'exact_match': 0, 'semantic_match': 0, 'weak_match': 0}
        
        for match in relation_matches:
            match_type = match.get('match_type', 'weak_match')
            quality_distribution[match_type] = quality_distribution.get(match_type, 0) + 1
        
        return quality_distribution
    
    def _analyze_unmatched_entities(self, entity_discrepancies: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze unmatched entities to identify patterns"""
        unmatched_e = entity_discrepancies['unmatched_econtract_entities']
        unmatched_s = entity_discrepancies['unmatched_smartcontract_entities']
        
        # Categorize unmatched entities
        e_categories = defaultdict(int)
        s_categories = defaultdict(int)
        
        for entity_data in unmatched_e.values():
            category = entity_data.get('category', 'OTHER')
            e_categories[category] += 1
        
        for entity_data in unmatched_s.values():
            category = entity_data.get('category', 'OTHER')
            s_categories[category] += 1
        
        return {
            'econtract_unmatched_categories': dict(e_categories),
            'smartcontract_unmatched_categories': dict(s_categories),
            'critical_missing_econtract': self._identify_critical_missing_entities(unmatched_e, 'econtract'),
            'critical_missing_smartcontract': self._identify_critical_missing_entities(unmatched_s, 'smartcontract')
        }
    
    def _analyze_unmatched_relations(self, relation_discrepancies: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze unmatched relationships"""
        unmatched_e = relation_discrepancies['unmatched_econtract_relations']
        unmatched_s = relation_discrepancies['unmatched_smartcontract_relations']
        
        # Categorize unmatched relations by type
        e_types = defaultdict(int)
        s_types = defaultdict(int)
        
        for relation_data in unmatched_e.values():
            rel_type = relation_data.get('relation', 'unknown')
            e_types[rel_type] += 1
        
        for relation_data in unmatched_s.values():
            rel_type = relation_data.get('relation', 'unknown')
            s_types[rel_type] += 1
        
        return {
            'econtract_unmatched_relation_types': dict(e_types),
            'smartcontract_unmatched_relation_types': dict(s_types)
        }
    
    def _identify_critical_missing_entities(self, unmatched_entities: Dict[str, Any], contract_type: str) -> List[Dict[str, Any]]:
        """Identify critically important missing entities"""
        critical_categories = {
            'econtract': ['PARTY', 'FINANCIAL', 'LEGAL_OBLIGATION', 'TEMPORAL'],
            'smartcontract': ['CONTRACT_DEFINITION', 'FUNCTION_DEFINITION', 'STATE_STORAGE', 'ACCESS_CONTROL']
        }
        
        critical_missing = []
        target_categories = critical_categories.get(contract_type, [])
        
        for entity_id, entity_data in unmatched_entities.items():
            if entity_data.get('category') in target_categories:
                critical_missing.append({
                    'entity_id': entity_id,
                    'entity_data': entity_data,
                    'criticality_reason': f"Missing {entity_data.get('category')} entity in {contract_type}"
                })
        
        return critical_missing
    
    def _assess_compliance(self, entity_matches: List[Dict[str, Any]], relation_matches: List[Dict[str, Any]],
                          entity_discrepancies: Dict[str, Any], relation_discrepancies: Dict[str, Any]) -> Dict[str, Any]:
        """Assess compliance between e-contract and smart contract"""
        
        # Calculate compliance metrics
        entity_compliance = entity_discrepancies['coverage_ratio_econtract']
        relation_compliance = relation_discrepancies['coverage_ratio_econtract']
        
        # Overall compliance score
        overall_compliance = (entity_compliance + relation_compliance) / 2
        
        # Determine compliance level
        if overall_compliance >= 0.9:
            compliance_level = 'Excellent'
        elif overall_compliance >= 0.7:
            compliance_level = 'Good'
        elif overall_compliance >= 0.5:
            compliance_level = 'Fair'
        else:
            compliance_level = 'Poor'
        
        # Identify compliance issues
        compliance_issues = []
        
        if entity_discrepancies['unmatched_econtract_count'] > 0:
            compliance_issues.append(f"Missing {entity_discrepancies['unmatched_econtract_count']} e-contract entities in smart contract")
        
        if relation_discrepancies['unmatched_econtract_count'] > 0:
            compliance_issues.append(f"Missing {relation_discrepancies['unmatched_econtract_count']} e-contract relationships in smart contract")
        
        return {
            'overall_compliance_score': round(overall_compliance, 3),
            'compliance_level': compliance_level,
            'entity_compliance_score': round(entity_compliance, 3),
            'relation_compliance_score': round(relation_compliance, 3),
            'compliance_issues': compliance_issues,
            'is_compliant': overall_compliance >= 0.7
        }
    
    def _generate_recommendations(self, entity_matches: List[Dict[str, Any]], relation_matches: List[Dict[str, Any]],
                                entity_discrepancies: Dict[str, Any], relation_discrepancies: Dict[str, Any]) -> List[str]:
        """Generate recommendations for improving compliance"""
        recommendations = []
        
        # Entity-based recommendations
        if entity_discrepancies['unmatched_econtract_count'] > 0:
            critical_missing = entity_discrepancies.get('unmatched_entity_analysis', {}).get('critical_missing_econtract', [])
            if critical_missing:
                recommendations.append(f"Implement {len(critical_missing)} critical missing entities in smart contract")
        
        if entity_discrepancies['coverage_ratio_econtract'] < 0.5:
            recommendations.append("Significant entity gaps detected - review smart contract implementation completeness")
        
        # Relationship-based recommendations
        if relation_discrepancies['unmatched_econtract_count'] > 0:
            recommendations.append("Add missing relationship implementations to ensure functional equivalence")
        
        # Quality-based recommendations
        low_quality_matches = sum(1 for match in entity_matches if match.get('confidence', 0) < 0.6)
        if low_quality_matches > 0:
            recommendations.append(f"Improve implementation of {low_quality_matches} entities with low confidence matches")
        
        # General recommendations
        overall_similarity = self._calculate_overall_similarity(entity_matches, relation_matches, entity_discrepancies, relation_discrepancies)
        if overall_similarity < 0.7:
            recommendations.append("Consider comprehensive review of smart contract to improve alignment with e-contract")
        
        if not recommendations:
            recommendations.append("Smart contract shows good alignment with e-contract")
        
        return recommendations
    
    def _enhance_validation_report(self, validation_report: Dict[str, Any], 
                                 g_e: KnowledgeGraph, g_s: KnowledgeGraph,
                                 analysis_id: str) -> Dict[str, Any]:
        """Enhance validation report with additional analysis"""
        
        enhanced_report = validation_report.copy()
        
        # Add graph statistics
        enhanced_report['graph_statistics'] = {
            'econtract_stats': g_e.get_statistics(),
            'smartcontract_stats': g_s.get_statistics()
        }
        
        # Add analysis metadata
        enhanced_report['analysis_metadata'] = {
            'analysis_id': analysis_id,
            'analysis_time': datetime.now().isoformat(),
            'econtract_graph_type': g_e.graph_type,
            'smartcontract_graph_type': g_s.graph_type
        }
        
        # Add detailed comparison insights
        enhanced_report['detailed_insights'] = self._generate_detailed_insights(validation_report, g_e, g_s)
        
        return enhanced_report
    
    def _generate_detailed_insights(self, validation_report: Dict[str, Any], 
                                  g_e: KnowledgeGraph, g_s: KnowledgeGraph) -> Dict[str, Any]:
        """Generate detailed insights from the comparison"""
        
        insights = {
            'structural_analysis': {
                'econtract_complexity': self._assess_graph_complexity(g_e),
                'smartcontract_complexity': self._assess_graph_complexity(g_s),
                'complexity_alignment': 'aligned' if abs(self._assess_graph_complexity(g_e) - self._assess_graph_complexity(g_s)) < 0.3 else 'misaligned'
            },
            'semantic_gaps': self._identify_semantic_gaps(validation_report),
            'implementation_completeness': self._assess_implementation_completeness(validation_report),
            'risk_assessment': self._assess_implementation_risks(validation_report)
        }
        
        return insights
    
    def _assess_graph_complexity(self, graph: KnowledgeGraph) -> float:
        """Assess the complexity of a knowledge graph"""
        stats = graph.get_statistics()
        
        # Normalize metrics
        entity_count = stats['basic_metrics']['total_entities']
        relation_count = stats['basic_metrics']['total_relationships']
        density = stats['basic_metrics'].get('graph_density', 0)
        
        # Calculate complexity score
        complexity = (entity_count * 0.3 + relation_count * 0.4 + density * 0.3) / 100
        
        return min(complexity, 1.0)
    
    def _identify_semantic_gaps(self, validation_report: Dict[str, Any]) -> List[str]:
        """Identify semantic gaps between contracts"""
        gaps = []
        
        compliance = validation_report.get('compliance_assessment', {})
        if compliance.get('entity_compliance_score', 1) < 0.7:
            gaps.append("Significant entity representation gaps")
        
        if compliance.get('relation_compliance_score', 1) < 0.7:
            gaps.append("Missing relationship implementations")
        
        unmatched_analysis = validation_report.get('entity_analysis', {}).get('unmatched_entity_analysis', {})
        critical_missing = unmatched_analysis.get('critical_missing_econtract', [])
        if critical_missing:
            gaps.append(f"Critical entities missing: {len(critical_missing)}")
        
        return gaps
    
    def _assess_implementation_completeness(self, validation_report: Dict[str, Any]) -> Dict[str, Any]:
        """Assess completeness of smart contract implementation"""
        
        compliance = validation_report.get('compliance_assessment', {})
        summary = validation_report.get('summary', {})
        
        completeness_score = summary.get('overall_similarity_score', 0)
        
        if completeness_score >= 0.9:
            completeness_level = 'Complete'
        elif completeness_score >= 0.7:
            completeness_level = 'Mostly Complete'
        elif completeness_score >= 0.5:
            completeness_level = 'Partially Complete'
        else:
            completeness_level = 'Incomplete'
        
        return {
            'completeness_score': completeness_score,
            'completeness_level': completeness_level,
            'is_production_ready': completeness_score >= 0.8 and compliance.get('is_compliant', False)
        }
    
    def _assess_implementation_risks(self, validation_report: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Assess risks in the smart contract implementation"""
        risks = []
        
        # High-risk missing entities
        unmatched_analysis = validation_report.get('entity_analysis', {}).get('unmatched_entity_analysis', {})
        critical_missing = unmatched_analysis.get('critical_missing_econtract', [])
        
        for missing in critical_missing:
            if missing['entity_data'].get('category') in ['PARTY', 'FINANCIAL', 'LEGAL_OBLIGATION']:
                risks.append({
                    'type': 'Critical Missing Entity',
                    'description': missing['criticality_reason'],
                    'severity': 'High',
                    'entity': missing['entity_data'].get('text', 'Unknown')
                })
        
        # Low compliance risks
        compliance = validation_report.get('compliance_assessment', {})
        if not compliance.get('is_compliant', False):
            risks.append({
                'type': 'Compliance Risk',
                'description': 'Smart contract does not adequately implement e-contract requirements',
                'severity': 'High' if compliance.get('overall_compliance_score', 0) < 0.5 else 'Medium',
                'score': compliance.get('overall_compliance_score', 0)
            })
        
        # Match quality risks
        entity_analysis = validation_report.get('entity_analysis', {})
        match_quality = entity_analysis.get('match_quality_distribution', {})
        weak_matches = match_quality.get('weak_match', 0)
        
        if weak_matches > 0:
            risks.append({
                'type': 'Implementation Quality Risk',
                'description': f'{weak_matches} entities have weak implementation matches',
                'severity': 'Medium' if weak_matches < 5 else 'High',
                'count': weak_matches
            })
        
        return risks
    
    def export_comparison_results(self, comparison_id: str, output_dir: str) -> Dict[str, str]:
        """Export comparison results to files"""
        if comparison_id not in self.comparison_results:
            return {}
        
        import os
        os.makedirs(output_dir, exist_ok=True)
        output_paths = {}
        
        comparison_data = self.comparison_results[comparison_id]
        
        try:
            # Export main comparison report
            report_path = os.path.join(output_dir, f"{comparison_id}_comparison_report.json")
            if FileHandler.write_json_file(report_path, comparison_data['discrepancy_report']):
                output_paths['comparison_report'] = report_path
            
            # Export detailed analysis
            detailed_path = os.path.join(output_dir, f"{comparison_id}_detailed_analysis.json")
            detailed_data = {
                'entity_matches': comparison_data['entity_matches'],
                'relation_matches': comparison_data['relation_matches'],
                'entity_discrepancies': comparison_data['entity_discrepancies'],
                'relation_discrepancies': comparison_data['relation_discrepancies']
            }
            if FileHandler.write_json_file(detailed_path, detailed_data):
                output_paths['detailed_analysis'] = detailed_path
            
            return output_paths
            
        except Exception as e:
            print(f"Error exporting comparison results for {comparison_id}: {e}")
            return output_paths