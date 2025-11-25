
from typing import Dict, Any, List, Optional, Tuple
import re
from datetime import datetime

class EnhancedSmartContractGenerator:
    
    def __init__(self):
        self.entity_to_variable_mapping = {}
        self.relationship_to_function_mapping = {}
        self._used_names = set()  # Track used variable names to prevent duplicates
        
    def generate_enhanced_contract(self, entities: List[Dict[str, Any]], 
                                 relationships: List[Dict[str, Any]], 
                                 contract_name: str = "GeneratedContract") -> str:
        

        
        self._used_names = set()
        
        relationships = self._normalize_relationships(relationships)
        entities = self._normalize_entities(entities)
        
        contract_analysis = self._analyze_contract_requirements(entities, relationships)
        
        contract_code = self._build_contract_structure(contract_analysis, contract_name)
        

        
        relationship_func_types = [
            'relationship_processor', 'relationship_validator', 'relationship_executor',
            'individual_relationship_processor', 'individual_relationship_validator', 'individual_relationship_executor',
            'business_relationship_processor', 'relationship_enforcement', 'relationship_compliance'
        ]
        
        rel_func_count = len([f for f in contract_analysis['functions'] 
                             if f.get('type', '') in relationship_func_types or
                             f.get('function_type', '') in relationship_func_types])
        
        all_rel_funcs = len([f for f in contract_analysis['functions'] 
                            if 'relationship' in f.get('name', '').lower() or 
                            'relationship' in f.get('description', '').lower() or
                            f.get('type', '') in relationship_func_types or
                            f.get('function_type', '') in relationship_func_types or
                            any(rel_type in f.get('name', '').lower() for rel_type in ['process', 'validate', 'execute', 'enforce'])])
        

        
        return contract_code
    
    def _add_additional_relationship_functions(self, analysis: Dict[str, Any], relationships: List[Dict], target_count: int):
        functions_added = 0
        
        for i, relationship in enumerate(relationships):
            if functions_added >= target_count:
                break
                
            rel_type = relationship.get('relation', f'relationship_{i}')
            sanitized_type = self._sanitize_variable_name(rel_type)
            
            relationship_functions = [
                {
                    'name': f'monitor{sanitized_type.title()}Relationship',
                    'description': f'Monitor {rel_type} relationship execution and compliance',
                    'visibility': 'public',
                    'returns': 'bool',
                    'function_type': 'relationship_processor'
                },
                {
                    'name': f'audit{sanitized_type.title()}Compliance',
                    'description': f'Audit compliance for {rel_type} relationship',
                    'visibility': 'external', 
                    'returns': 'uint256',
                    'function_type': 'relationship_compliance'
                },
                {
                    'name': f'enforce{sanitized_type.title()}Rules', 
                    'description': f'Enforce business rules for {rel_type} relationship',
                    'visibility': 'external',
                    'returns': 'bool',
                    'function_type': 'relationship_enforcement'
                },
                {
                    'name': f'track{sanitized_type.title()}Performance',
                    'description': f'Track performance metrics for {rel_type} relationship',
                    'visibility': 'public',
                    'returns': 'uint256',
                    'function_type': 'relationship_processor'
                },
                {
                    'name': f'validate{sanitized_type.title()}Integrity',
                    'description': f'Validate integrity of {rel_type} relationship data',
                    'visibility': 'public', 
                    'returns': 'bool',
                    'function_type': 'relationship_validator'
                }
            ]
            
            for func in relationship_functions:
                if functions_added >= target_count:
                    break
                analysis['functions'].append(func)
                functions_added += 1
    
    def _classify_entity_by_content(self, text: str) -> str:
        text_lower = text.lower().strip()
        
        if any(pattern in text_lower for pattern in ['$', '£', '€', 'usd', 'gbp', 'eur', 'payment', 'fee', 'cost', 'amount', 'price', 'salary', 'rent', 'deposit', 'money']):
            return 'FINANCIAL'
        
        if any(pattern in text_lower for pattern in ['tenant', 'landlord', 'employee', 'employer', 'client', 'customer', 'contractor', 'person', 'individual']):
            return 'PERSON'
        
        if any(pattern in text_lower for pattern in ['company', 'corporation', 'inc', 'llc', 'ltd', 'organization', 'firm', 'business']):
            return 'ORGANIZATION'
        
        if any(pattern in text_lower for pattern in ['date', 'deadline', 'month', 'year', 'day', 'time', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']):
            return 'TEMPORAL'
        
        if any(pattern in text_lower for pattern in ['address', 'street', 'city', 'state', 'country', 'location', 'property']):
            return 'LOCATION'
        
        if any(pattern in text_lower for pattern in ['must', 'shall', 'required', 'obligation', 'duty', 'responsibility']):
            return 'OBLIGATIONS'
        
        return 'GENERAL'
    
    def _analyze_contract_requirements(self, entities: List[Dict[str, Any]], 
                                     relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
        
        analysis = {
            'state_variables': [],
            'functions': [],
            'events': [],
            'modifiers': [],
            'structs': [],
            'enums': [],
            'mappings': [],
            'business_rules': [],
            'access_controls': [],
            'validation_functions': []
        }
        
        self.parties = []
        self.financial_elements = []
        self.temporal_elements = []
        self.obligations = []
        self.conditions = []
        self.assets = []
        self.locations = []
        self.services = []
        self.quantities = []
        self.contact_info = []
        
        for entity in entities:
            if isinstance(entity, str):
                entity_text = entity.lower().strip()
                entity_type = self._classify_entity_by_content(entity_text)
            else:
                entity_type = entity.get('label', entity.get('type', '')).upper()
                entity_text = str(entity.get('text', entity.get('value', ''))).lower().strip()
                
            if not entity_text or len(entity_text) < 2:
                continue
            
            if entity_type in ['PERSON', 'ORG', 'ORGANIZATION'] or any(role in entity_text for role in ['tenant', 'landlord', 'employee', 'employer', 'contractor', 'client', 'provider', 'lessor', 'lessee', 'buyer', 'seller']):
                role = self._determine_entity_role(entity_text)
                var_name = self._sanitize_variable_name(entity_text)
                
                party_info = {
                    'name': var_name, 
                    'role': role, 
                    'text': entity_text,
                    'entity_type': entity_type,
                    'authorization_level': self._determine_authorization_level(role)
                }
                self.parties.append(party_info)
                
                analysis['state_variables'].extend([
                    {
                        'name': var_name,
                        'type': 'address',
                        'visibility': 'public',
                        'description': f'Address of {role} ({entity_text})',
                        'context': 'party_identification'
                    },
                    {
                        'name': f'{var_name}Authorized',
                        'type': 'bool',
                        'visibility': 'public',
                        'description': f'Authorization status for {role}',
                        'context': 'access_control'
                    }
                ])
                
                modifier_name = f"only{role.title()}"
                existing_modifiers = [m['name'] for m in analysis['modifiers']]
                if modifier_name not in existing_modifiers:
                    analysis['modifiers'].append({
                        'name': modifier_name,
                        'description': f"Restrict access to {role}",
                        'parameter': var_name
                    })
                
            elif entity_type in ['FINANCIAL', 'MONEY'] or any(term in entity_text for term in ['$', 'payment', 'salary', 'rent', 'fee', 'deposit', 'amount']):
                context = self._extract_financial_context(entity_text)
                var_name = self._generate_financial_variable_name(entity_text, context)
                
                self.financial_elements.append({'name': var_name, 'context': context, 'text': entity_text})
                
                analysis['state_variables'].append({
                    'name': var_name,
                    'type': 'uint256',
                    'description': f"Amount for {entity_text} ({context})",
                    'visibility': 'public',
                    'source_entity': entity
                })
                
                analysis['functions'].append({
                    'name': f"update{var_name.title()}",
                    'description': f"Update {context} amount",
                    'visibility': 'external',
                    'parameters': [{'name': 'newAmount', 'type': 'uint256'}],
                    'returns': 'bool',
                    'requires_authorization': True,
                    'source_entity': entity,
                    'function_type': 'financial_update'
                })
                
            elif entity_type in ['TEMPORAL', 'DATE'] or any(term in entity_text for term in ['date', 'deadline', 'time', 'duration', 'period']):
                temporal_context = self._extract_temporal_context(entity_text)
                var_name = self._generate_temporal_variable_name(entity_text, temporal_context)
                
                self.temporal_elements.append({'name': var_name, 'context': temporal_context, 'text': entity_text})
                
                analysis['state_variables'].append({
                    'name': var_name,
                    'type': 'uint256',
                    'description': f"Timestamp for {entity_text} ({temporal_context})",
                    'visibility': 'public',
                    'source_entity': entity
                })
                
                if 'deadline' in temporal_context or 'expir' in entity_text:
                    analysis['functions'].append({
                        'name': f"check{var_name.title()}Deadline",
                        'description': f"Check if {temporal_context} deadline has passed",
                        'visibility': 'public',
                        'returns': 'bool',
                        'source_entity': entity,
                        'function_type': 'temporal_validation'
                    })
                
            elif entity_type == 'OBLIGATIONS' or any(term in entity_text for term in ['must', 'shall', 'required', 'obligation', 'duty']):
                obligation_name = self._sanitize_variable_name(entity_text)
                responsible_party = self._determine_responsible_party(entity_text, self.parties)
                
                self.obligations.append({'name': obligation_name, 'party': responsible_party, 'text': entity_text})
                
                analysis['state_variables'].append({
                    'name': f"{obligation_name}Status",
                    'type': 'bool',
                    'description': f"Track completion of {entity_text}",
                    'visibility': 'public',
                    'source_entity': entity
                })
                
            elif entity_type in ['LOCATION', 'GPE'] or any(term in entity_text for term in ['address', 'street', 'city', 'state', 'country', 'location', 'property']):
                location_name = self._sanitize_variable_name(entity_text)
                self.locations.append({'name': location_name, 'text': entity_text})
                
                analysis['state_variables'].append({
                    'name': f"{location_name}Info",
                    'type': 'string',
                    'description': f"Location information for {entity_text}",
                    'visibility': 'public',
                    'source_entity': entity
                })
                
            elif entity_type == 'SERVICE' or any(term in entity_text for term in ['service', 'work', 'development', 'consulting', 'delivery', 'maintenance', 'repair']):
                service_name = self._sanitize_variable_name(entity_text)
                self.services.append({'name': service_name, 'text': entity_text})
                
                analysis['state_variables'].extend([
                    {
                        'name': f"{service_name}Status",
                        'type': 'bool',
                        'description': f"Service completion status for {entity_text}",
                        'visibility': 'public',
                        'source_entity': entity
                    },
                    {
                        'name': f"{service_name}Provider",
                        'type': 'address',
                        'description': f"Service provider for {entity_text}",
                        'visibility': 'public',
                        'source_entity': entity
                    }
                ])
                
            elif any(term in entity_text for term in ['quantity', 'number', 'count', 'days', 'hours', 'months', 'years']):
                quantity_name = self._sanitize_variable_name(entity_text)
                self.quantities.append({'name': quantity_name, 'text': entity_text})
                
                analysis['state_variables'].append({
                    'name': quantity_name,
                    'type': 'uint256',
                    'description': f"Quantity value for {entity_text}",
                    'visibility': 'public',
                    'source_entity': entity
                })
                
            elif any(term in entity_text for term in ['email', 'phone', 'contact', 'mobile', '@']):
                contact_name = self._sanitize_variable_name(entity_text)
                self.contact_info.append({'name': contact_name, 'text': entity_text})
                
                analysis['state_variables'].append({
                    'name': f"{contact_name}Info",
                    'type': 'string',
                    'description': f"Contact information for {entity_text}",
                    'visibility': 'public',
                    'source_entity': entity
                })
                
            elif entity_type == 'CONDITIONS' or any(term in entity_text for term in ['condition', 'if', 'when', 'provided', 'unless']):
                condition_name = self._sanitize_variable_name(entity_text)
                self.conditions.append({'name': condition_name, 'text': entity_text})
                
                analysis['state_variables'].append({
                    'name': f"{condition_name}Met",
                    'type': 'bool',
                    'description': f"Track if condition is met: {entity_text}",
                    'visibility': 'public',
                    'source_entity': entity
                })
                
                analysis['modifiers'].append({
                    'name': f"require{condition_name.title()}",
                    'description': f"Require condition: {entity_text}",
                    'source_entity': entity
                })
                
            else:
                generic_name = self._sanitize_variable_name(entity_text)
                if generic_name and len(generic_name) > 1:
                    analysis['state_variables'].append({
                        'name': f"{generic_name}Value",
                        'type': 'string',
                        'description': f"Value for {entity_text}",
                        'visibility': 'public',
                        'source_entity': entity
                    })
        
        processed_relations = set()  # Avoid duplicate functions
        
        self._add_comprehensive_business_logic_functions(analysis, relationships, entities)
        
        for relationship in relationships:
            relation_type = str(relationship.get('relation', '')).lower()
            relation_text = str(relationship.get('text', '')).lower()
            relation_id = relationship.get('id', f"rel_{len(processed_relations)}")
            source = relationship.get('source', '')
            target = relationship.get('target', '')
            
            function_base_name = self._generate_relationship_function_name(relationship, relation_type, relation_text)
            
            if any(term in relation_type or term in relation_text for term in ['payment', 'financial', 'pay', 'money', 'salary', 'rent', 'deposit', 'fee', 'cost']):
                payment_key = f"payment_{function_base_name}"
                if payment_key not in processed_relations:
                    analysis['functions'].extend([
                        {
                            'name': 'processPayment',
                            'description': 'Process payments with validation and tracking',
                            'visibility': 'external',
                            'payable': True,
                            'returns': 'bool',
                            'source_relationship': relationship,
                            'function_type': 'financial_processing',
                            'requires_authorization': True
                        },
                        {
                            'name': 'calculatePaymentAmount',
                            'description': 'Calculate payment amount based on conditions',
                            'visibility': 'public',
                            'returns': 'uint256',
                            'source_relationship': relationship,
                            'function_type': 'financial_calculation'
                        },
                        {
                            'name': 'recordPaymentTransaction',
                            'description': 'Record payment transaction in contract state',
                            'visibility': 'internal',
                            'returns': 'bool',
                            'source_relationship': relationship,
                            'function_type': 'financial_recording'
                        }
                    ])
                    
                    analysis['validation_functions'].extend([
                        {
                            'name': 'validatePaymentAmount',
                            'description': 'Validate payment amount and conditions',
                            'relationship': relation_type
                        },
                        {
                            'name': 'validatePaymentTiming',
                            'description': 'Validate payment timing requirements',
                            'relationship': relation_type
                        }
                    ])
                    
                    processed_relations.add('payment_processing')
            
            elif any(term in relation_type or term in relation_text for term in ['obligation', 'duty', 'must', 'shall', 'responsible', 'liable', 'required', 'bound']):
                obligation_id = self._generate_obligation_id(relationship)
                if obligation_id not in processed_relations:
                    analysis['functions'].extend([
                        {
                            'name': f'fulfill{obligation_id.title()}',
                            'description': f'Fulfill obligation: {relation_text}',
                            'visibility': 'external',
                            'returns': 'bool',
                            'requires_authorization': True,
                            'source_relationship': relationship,
                            'function_type': 'obligation_fulfillment'
                        },
                        {
                            'name': f'validate{obligation_id.title()}Conditions',
                            'description': f'Validate all conditions for obligation fulfillment',
                            'visibility': 'public',
                            'returns': 'bool',
                            'source_relationship': relationship,
                            'function_type': 'obligation_validation'
                        },
                        {
                            'name': f'enforce{obligation_id.title()}',
                            'description': f'Enforce obligation compliance and penalties',
                            'visibility': 'external',
                            'returns': 'bool',
                            'requires_authorization': True,
                            'source_relationship': relationship,
                            'function_type': 'obligation_enforcement'
                        },
                        {
                            'name': f'get{obligation_id.title()}Status',
                            'description': f'Get current status of obligation',
                            'visibility': 'public',
                            'returns': 'bool',
                            'function_type': 'validation'
                        }
                    ])
                    processed_relations.add(obligation_id)
            
            elif any(term in relation_type or term in relation_text for term in ['condition', 'if', 'when', 'provided', 'contingent', 'depends']):
                condition_id = self._generate_condition_id(relationship)
                if f'condition_{condition_id}' not in processed_relations:
                    analysis['functions'].extend([
                        {
                            'name': f'check{condition_id.title()}Condition',
                            'description': f'Check if condition is met: {relation_text}',
                            'visibility': 'public',
                            'returns': 'bool',
                            'source_relationship': relationship,
                            'function_type': 'condition_checking'
                        },
                        {
                            'name': f'validate{condition_id.title()}Requirements',
                            'description': f'Validate all requirements for condition',
                            'visibility': 'internal',
                            'returns': 'bool',
                            'source_relationship': relationship,
                            'function_type': 'condition_validation'
                        }
                    ])
                    processed_relations.add(f'condition_{condition_id}')
            
            elif any(term in relation_type or term in relation_text for term in ['temporal', 'deadline', 'due', 'expires', 'schedule', 'period']):
                temporal_key = f"temporal_{function_base_name}"
                if temporal_key not in processed_relations:
                    analysis['functions'].extend([
                        {
                            'name': 'checkDeadlineCompliance',
                            'description': 'Check if actions are within required deadlines',
                            'visibility': 'public',
                            'returns': 'bool',
                            'source_relationship': relationship,
                            'function_type': 'temporal_validation'
                        },
                        {
                            'name': 'updateScheduleStatus',
                            'description': 'Update contract schedule and timeline status',
                            'visibility': 'external',
                            'returns': 'bool',
                            'requires_authorization': True,
                            'source_relationship': relationship,
                            'function_type': 'temporal_management'
                        },
                        {
                            'name': 'getRemainingTime',
                            'description': 'Calculate remaining time for contract obligations',
                            'visibility': 'public',
                            'returns': 'uint256',
                            'source_relationship': relationship,
                            'function_type': 'temporal_calculation'
                        }
                    ])
                    
                    analysis['events'].extend([
                        {
                            'name': f'{function_base_name.title()}DeadlineSet',
                            'description': f'Emitted when deadline is set for {relation_text}',
                            'parameters': [
                                {'name': 'deadline', 'type': 'uint256'},
                                {'name': 'setBy', 'type': 'address'}
                            ],
                            'source_relationship': relationship
                        }
                    ])
                    
                    processed_relations.add('temporal_management')
                    
            elif any(term in relation_type or term in relation_text for term in ['party', 'relationship', 'between', 'involves', 'connects']):
                party_key = f"party_{function_base_name}"
                if party_key not in processed_relations:
                    analysis['functions'].extend([
                        {
                            'name': f'establish{function_base_name.title()}Relationship',
                            'description': f'Establish relationship: {relation_text}',
                            'visibility': 'external',
                            'returns': 'bool',
                            'requires_authorization': True,
                            'source_relationship': relationship,
                            'function_type': 'party_relationship'
                        },
                        {
                            'name': f'verify{function_base_name.title()}Parties',
                            'description': f'Verify parties in relationship: {relation_text}',
                            'visibility': 'public',
                            'returns': 'bool',
                            'source_relationship': relationship,
                            'function_type': 'party_verification'
                        }
                    ])
                    processed_relations.add(party_key)
                    
            elif any(term in relation_type or term in relation_text for term in ['location', 'property', 'address', 'place', 'situated', 'located']):
                location_key = f"location_{function_base_name}"
                if location_key not in processed_relations:
                    analysis['functions'].extend([
                        {
                            'name': f'verify{function_base_name.title()}Location',
                            'description': f'Verify location information: {relation_text}',
                            'visibility': 'public',
                            'returns': 'bool',
                            'source_relationship': relationship,
                            'function_type': 'location_verification'
                        },
                        {
                            'name': f'update{function_base_name.title()}Address',  
                            'description': f'Update address information: {relation_text}',
                            'visibility': 'external',
                            'returns': 'bool',
                            'requires_authorization': True,
                            'source_relationship': relationship,
                            'function_type': 'location_update'
                        }
                    ])
                    processed_relations.add(location_key)
                    
            elif any(term in relation_type or term in relation_text for term in ['agreement', 'contract', 'terms', 'conditions', 'clause']):
                agreement_key = f"agreement_{function_base_name}"
                if agreement_key not in processed_relations:
                    analysis['functions'].extend([
                        {
                            'name': f'execute{function_base_name.title()}Agreement',
                            'description': f'Execute agreement: {relation_text}',
                            'visibility': 'external',
                            'returns': 'bool',
                            'requires_authorization': True,
                            'source_relationship': relationship,
                            'function_type': 'agreement_execution'
                        },
                        {
                            'name': f'validate{function_base_name.title()}Terms',
                            'description': f'Validate terms: {relation_text}',
                            'visibility': 'public',
                            'returns': 'bool',
                            'source_relationship': relationship,
                            'function_type': 'terms_validation'
                        }
                    ])
                    processed_relations.add(agreement_key)
                    
            elif any(term in relation_type or term in relation_text for term in ['service', 'work', 'deliver', 'perform', 'complete', 'provide']):
                service_key = f"service_{function_base_name}"
                if service_key not in processed_relations:
                    analysis['functions'].extend([
                        {
                            'name': f'initiate{function_base_name.title()}Service',
                            'description': f'Initiate service: {relation_text}',
                            'visibility': 'external',
                            'returns': 'bool',
                            'requires_authorization': True,
                            'source_relationship': relationship,
                            'function_type': 'service_initiation'
                        },
                        {
                            'name': f'complete{function_base_name.title()}Service',
                            'description': f'Complete service: {relation_text}',
                            'visibility': 'external',
                            'returns': 'bool',
                            'requires_authorization': True,
                            'source_relationship': relationship,
                            'function_type': 'service_completion'
                        },
                        {
                            'name': f'verify{function_base_name.title()}Quality',
                            'description': f'Verify service quality: {relation_text}',
                            'visibility': 'public',
                            'returns': 'bool',
                            'source_relationship': relationship,
                            'function_type': 'quality_verification'
                        }
                    ])
                    processed_relations.add(service_key)
            
            elif any(term in relation_type or term in relation_text for term in ['condition', 'if', 'when', 'require', 'depend']):
                condition_id = self._generate_condition_id(relationship)
                if condition_id not in processed_relations:
                    analysis['modifiers'].append({
                        'name': f'require{condition_id.title()}',
                        'description': f'Require condition: {relation_text}',
                        'source_relationship': relationship
                    })
                    
                    analysis['validation_functions'].append({
                        'name': f'check{condition_id.title()}',
                        'description': f'Check condition: {relation_text}',
                        'relationship': relation_type
                    })
                    processed_relations.add(condition_id)
            
            elif any(term in relation_type or term in relation_text for term in ['temporal', 'deadline', 'time', 'expire', 'schedule']):
                if 'temporal_management' not in processed_relations:
                    analysis['functions'].extend([
                        {
                            'name': 'checkDeadlines',
                            'description': 'Check all contract deadlines and trigger actions',
                            'visibility': 'public',
                            'returns': 'bool',
                            'function_type': 'temporal_validation'
                        },
                        {
                            'name': 'updateSchedule',
                            'description': 'Update contract schedule and timelines',
                            'visibility': 'external',
                            'requires_authorization': True,
                            'function_type': 'temporal_management'
                        }
                    ])
                    processed_relations.add('temporal_management')
        
        for i, relationship in enumerate(relationships):
            relation_id = relationship.get('id', f"rel_{i}")
            relation_type = str(relationship.get('relation', '')).lower()
            relation_text = str(relationship.get('text', '')).lower()
            
            function_base_name = self._generate_relationship_function_name(relationship, relation_type, relation_text)
            unique_key = f"individual_{function_base_name}_{i}"
            
            required_state_vars = [
                {
                    'name': f'relationship{i}Status',
                    'type': 'bool',
                    'description': f'Status of relationship {i}',
                    'visibility': 'public'
                },
                {
                    'name': f'relationship{i}Timestamp',
                    'type': 'uint256',
                    'description': f'Timestamp of relationship {i}',
                    'visibility': 'public'
                },
                {
                    'name': f'relationship{i}Processed',
                    'type': 'bool',
                    'description': f'Processed status for relationship {i}',
                    'visibility': 'public'
                },
                {
                    'name': f'relationship{i}Valid',
                    'type': 'bool',
                    'description': f'Validation status for relationship {i}',
                    'visibility': 'public'
                },
                {
                    'name': f'relationship{i}Count',
                    'type': 'uint256',
                    'description': f'Count for relationship {i}',
                    'visibility': 'public'
                },
                {
                    'name': f'relationship{i}Performance',
                    'type': 'uint256',
                    'description': f'Performance metric for relationship {i}',
                    'visibility': 'public'
                }
            ]
            
            existing_vars = {var['name'] for var in analysis['state_variables']}
            for var in required_state_vars:
                if var['name'] not in existing_vars:
                    analysis['state_variables'].append(var)
                    existing_vars.add(var['name'])
            
            relationship_functions = [
                {
                    'name': f'process{function_base_name.title()}Relationship{i}',
                    'description': f'Process individual relationship {i}: {relation_text}',
                    'visibility': 'external',
                    'returns': 'bool',
                    'requires_authorization': True,
                    'source_relationship': relationship,
                    'function_type': 'individual_relationship_processor',
                    'state_vars_used': [f'relationship{i}Status', f'relationship{i}Timestamp']
                },
                {
                    'name': f'validate{function_base_name.title()}Relationship{i}',
                    'description': f'Validate individual relationship {i}: {relation_text}',
                    'visibility': 'public',
                    'returns': 'bool',
                    'source_relationship': relationship,
                    'function_type': 'individual_relationship_validator',
                    'state_vars_used': [f'relationship{i}Valid']
                },
                {
                    'name': f'execute{function_base_name.title()}Relationship{i}',
                    'description': f'Execute individual relationship {i}: {relation_text}',
                    'visibility': 'external',
                    'returns': 'bool',
                    'requires_authorization': True,
                    'source_relationship': relationship,
                    'function_type': 'individual_relationship_executor',
                    'state_vars_used': [f'relationship{i}Processed']
                },
                {
                    'name': f'get{function_base_name.title()}Relationship{i}Status',
                    'description': f'Get status of relationship {i}: {relation_text}',
                    'visibility': 'public',
                    'returns': 'bool',
                    'source_relationship': relationship,
                    'function_type': 'individual_relationship_status',
                    'state_vars_used': [f'relationship{i}Status']
                },
                {
                    'name': f'monitor{function_base_name.title()}Relationship{i}',
                    'description': f'Monitor relationship {i}: {relation_text}',
                    'visibility': 'public',
                    'returns': 'uint256',
                    'source_relationship': relationship,
                    'function_type': 'individual_relationship_processor',
                    'state_vars_used': [f'relationship{i}Count']
                },
                {
                    'name': f'enforceRelationship{i}Rules',
                    'description': f'Enforce rules for relationship {i}: {relation_text}',
                    'visibility': 'external',
                    'returns': 'bool',
                    'requires_authorization': True,
                    'source_relationship': relationship,
                    'function_type': 'relationship_enforcement',
                    'state_vars_used': [f'relationship{i}Status']
                },
                {
                    'name': f'auditRelationship{i}Compliance',
                    'description': f'Audit compliance for relationship {i}: {relation_text}',
                    'visibility': 'external',
                    'returns': 'uint256',
                    'source_relationship': relationship,
                    'function_type': 'relationship_compliance',
                    'state_vars_used': [f'relationship{i}Count']
                },
                {
                    'name': f'trackRelationship{i}Performance',
                    'description': f'Track performance for relationship {i}: {relation_text}',
                    'visibility': 'public',
                    'returns': 'uint256',
                    'source_relationship': relationship,
                    'function_type': 'individual_relationship_processor',
                    'state_vars_used': [f'relationship{i}Performance']
                }
            ]
            
            analysis['functions'].extend(relationship_functions)
            
            sanitized_base = self._sanitize_variable_name(f'{function_base_name}_{i}')
            analysis['state_variables'].extend([
                {
                    'name': f'{sanitized_base}Status',
                    'type': 'bool',
                    'description': f'Status of relationship {i}: {relation_text}',
                    'visibility': 'public',
                    'source_relationship': relationship
                },
                {
                    'name': f'{sanitized_base}Timestamp',
                    'type': 'uint256',
                    'description': f'Timestamp of relationship {i} execution',
                    'visibility': 'public',
                    'source_relationship': relationship
                }
            ])
            
            analysis['events'].extend([
                {
                    'name': f'{function_base_name.title()}Relationship{i}Processed',
                    'description': f'Emitted when relationship {i} is processed: {relation_text}',
                    'parameters': [
                        {'name': 'relationshipId', 'type': 'uint256'},
                        {'name': 'processor', 'type': 'address'},
                        {'name': 'success', 'type': 'bool'},
                        {'name': 'timestamp', 'type': 'uint256'}
                    ],
                    'source_relationship': relationship
                },
                {
                    'name': f'{function_base_name.title()}Relationship{i}Executed',
                    'description': f'Emitted when relationship {i} is executed: {relation_text}',
                    'parameters': [
                        {'name': 'relationshipId', 'type': 'uint256'},
                        {'name': 'executor', 'type': 'address'},
                        {'name': 'result', 'type': 'bool'},
                        {'name': 'timestamp', 'type': 'uint256'}
                    ],
                    'source_relationship': relationship
                }
            ])
            
            processed_relations.add(unique_key)
        
        analysis['functions'].extend([
            {
                'name': 'processAllRelationships',
                'description': f'Process all {len(relationships)} business relationships',
                'visibility': 'external',
                'returns': 'bool',
                'requires_authorization': True,
                'function_type': 'all_relationships_processor'
            },
            {
                'name': 'validateAllRelationships',
                'description': f'Validate all {len(relationships)} business relationships',
                'visibility': 'public',
                'returns': 'bool',
                'function_type': 'all_relationships_validator'
            },
            {
                'name': 'getRelationshipCoveragePercentage',
                'description': 'Get percentage of relationships successfully processed',
                'visibility': 'public',
                'returns': 'uint256',
                'function_type': 'relationship_coverage_calculator'
            }
        ])
        
        analysis['state_variables'].extend([
            {
                'name': 'totalRelationships',
                'type': 'uint256',
                'description': f'Total number of relationships: {len(relationships)}',
                'visibility': 'public'
            },
            {
                'name': 'processedRelationships',
                'type': 'uint256',
                'description': 'Number of relationships successfully processed',
                'visibility': 'public'
            },
            {
                'name': 'relationshipCoveragePercentage',
                'type': 'uint256',
                'description': 'Percentage of relationship coverage (0-100)',
                'visibility': 'public'
            }
        ])
        
        self.relationship_to_function_mapping = {}
        for rel_key in processed_relations:
            matching_functions = [f for f in analysis['functions'] 
                                if f.get('source_relationship') and 
                                f['source_relationship'].get('id') and 
                                rel_key.startswith(f['source_relationship']['id'])]
            if matching_functions:
                self.relationship_to_function_mapping[rel_key] = matching_functions
                
        relationship_functions = [f for f in analysis['functions'] 
                                 if 'relationship' in f.get('name', '').lower() or 
                                 'relationship' in f.get('description', '').lower() or
                                 f.get('type', '') in ['relationship_processor', 'relationship_validator', 'relationship_executor'] or
                                 f.get('function_type', '') in ['relationship_processor', 'relationship_validator', 'relationship_executor'] or
                                 f.get('source_relationship')]
        

        coverage_percent = (len(relationship_functions) / len(relationships) * 100) if relationships else 0

                
        self._add_relationship_preservation_functions(analysis, relationships)
        
        self._add_source_target_relationship_functions(analysis, relationships, entities)
        
        self._add_business_validation_functions(analysis)
        
        self._add_comprehensive_events(analysis, relationships)
        
        self._add_standard_functions(analysis)
        
        self._ensure_unique_names(analysis)
        
        return analysis
    
    def _add_business_validation_functions(self, analysis: Dict[str, Any]):
        
        if self.financial_elements:
            analysis['functions'].extend([
                {
                    'name': 'validatePaymentConditions',
                    'description': 'Validate payment amount, timing, and authorization',
                    'visibility': 'internal',
                    'returns': 'bool',
                    'function_type': 'validation'
                },
                {
                    'name': 'calculateLateFees',
                    'description': 'Calculate late fees based on payment delays',
                    'visibility': 'public',
                    'returns': 'uint256',
                    'function_type': 'financial_calculation'
                }
            ])
        
        if self.parties:
            analysis['functions'].append({
                'name': 'validatePartyAuthorization',
                'description': 'Validate party authorization for specific actions',
                'visibility': 'internal',
                'returns': 'bool',
                'function_type': 'access_validation'
            })
        
        if self.temporal_elements:
            analysis['functions'].extend([
                {
                    'name': 'isWithinDeadline',
                    'description': 'Check if action is within specified deadline',
                    'visibility': 'public',
                    'returns': 'bool',
                    'function_type': 'temporal_validation'
                },
                {
                    'name': 'calculateTimeRemaining',
                    'description': 'Calculate remaining time for contract obligations',
                    'visibility': 'public',
                    'returns': 'uint256',
                    'function_type': 'temporal_calculation'
                }
            ])
        
        if self.obligations:
            analysis['functions'].extend([
                {
                    'name': 'validateObligationCompletion',
                    'description': 'Validate that all prerequisites are met for obligation completion',
                    'visibility': 'internal',
                    'returns': 'bool',
                    'function_type': 'obligation_validation'
                },
                {
                    'name': 'getObligationStatus',
                    'description': 'Get comprehensive status of all contract obligations',
                    'visibility': 'external',
                    'returns': 'string memory',
                    'function_type': 'status_reporting'
                }
            ])
    
    def _add_comprehensive_events(self, analysis: Dict[str, Any], relationships: List[Dict[str, Any]]):
        
        analysis['events'].extend([
            {
                'name': 'PaymentProcessed',
                'description': 'Emitted when a payment is successfully processed',
                'parameters': [
                    {'name': 'payer', 'type': 'address'},
                    {'name': 'amount', 'type': 'uint256'},
                    {'name': 'paymentType', 'type': 'string'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ]
            },
            {
                'name': 'PaymentValidationFailed',
                'description': 'Emitted when payment validation fails',
                'parameters': [
                    {'name': 'payer', 'type': 'address'},
                    {'name': 'reason', 'type': 'string'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ]
            }
        ])
        
        analysis['events'].extend([
            {
                'name': 'ObligationAssigned',
                'description': 'Emitted when an obligation is assigned to a party',
                'parameters': [
                    {'name': 'obligationType', 'type': 'string'},
                    {'name': 'assignedTo', 'type': 'address'},
                    {'name': 'deadline', 'type': 'uint256'}
                ]
            },
            {
                'name': 'ObligationFulfilled',
                'description': 'Emitted when an obligation is successfully fulfilled',
                'parameters': [
                    {'name': 'obligationType', 'type': 'string'},
                    {'name': 'fulfilledBy', 'type': 'address'},
                    {'name': 'validationStatus', 'type': 'bool'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ]
            }
        ])
        
        analysis['events'].extend([
            {
                'name': 'UnauthorizedAccess',
                'description': 'Emitted when unauthorized access is attempted',
                'parameters': [
                    {'name': 'attemptedBy', 'type': 'address'},
                    {'name': 'functionCalled', 'type': 'string'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ]
            },
            {
                'name': 'PartyRoleUpdated',
                'description': 'Emitted when a party role is updated',
                'parameters': [
                    {'name': 'party', 'type': 'address'},
                    {'name': 'oldRole', 'type': 'string'},
                    {'name': 'newRole', 'type': 'string'}
                ]
            }
        ])
        
        for relationship in relationships:
            relation_type = str(relationship.get('relation', '')).lower()
            
            if relation_type in ['ownership']:
                analysis['functions'].append({
                    'name': 'transferOwnership',
                    'description': 'Transfer ownership of assets',
                    'visibility': 'external',
                    'returns': 'bool',
                    'source_relationship': relationship,
                    'function_type': 'ownership_transfer'
                })
                
            elif relation_type in ['temporal_start', 'temporal_end']:
                analysis['functions'].append({
                    'name': 'checkTemporalCondition',
                    'description': 'Check if temporal conditions are met',
                    'visibility': 'view',
                    'returns': 'bool',
                    'source_relationship': relationship,
                    'function_type': 'temporal_check'
                })
        
        self._add_standard_functions(analysis)
        
        return analysis
    
    def _add_standard_functions(self, analysis: Dict[str, Any]):
        
        constructor_params = []
        if hasattr(self, 'parties') and self.parties:
            for party in self.parties:
                constructor_params.append({'name': f'_{party["name"]}', 'type': 'address'})
        
        analysis['functions'].insert(0, {
            'name': 'constructor',
            'description': 'Initialize contract with parties and initial state',
            'visibility': 'public',
            'parameters': constructor_params,
            'function_type': 'constructor'
        })
        
        analysis['functions'].extend([
            {
                'name': 'isContractActive',
                'description': 'Check if contract is currently active',
                'visibility': 'public',
                'returns': 'bool',
                'function_type': 'status_check'
            },
            {
                'name': 'getContractStatus',
                'description': 'Get comprehensive contract status',
                'visibility': 'external',
                'returns': 'string memory',
                'function_type': 'status_check'
            },
            {
                'name': 'terminateContract',
                'description': 'Terminate the contract with proper authorization',
                'visibility': 'external',
                'returns': 'bool',
                'requires_authorization': True,
                'function_type': 'termination'
            },
            {
                'name': 'emergencyStop',
                'description': 'Emergency contract suspension',
                'visibility': 'external',
                'requires_authorization': True,
                'function_type': 'emergency'
            }
        ])
        
        analysis['modifiers'].extend([
            {
                'name': 'onlyActiveContract',
                'description': 'Require contract to be active'
            },
            {
                'name': 'onlyParties',
                'description': 'Restrict access to contract parties only'
            },
            {
                'name': 'notTerminated',
                'description': 'Require contract not to be terminated'
            }
        ])
        
        analysis['events'].extend([
            {
                'name': 'ContractActivated',
                'description': 'Emitted when contract is activated',
                'parameters': [
                    {'name': 'timestamp', 'type': 'uint256'}
                ]
            },
            {
                'name': 'ContractTerminated',
                'description': 'Emitted when contract is terminated',
                'parameters': [
                    {'name': 'terminatedBy', 'type': 'address'},
                    {'name': 'reason', 'type': 'string'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ]
            },
            {
                'name': 'EmergencyStop',
                'description': 'Emitted during emergency contract suspension',
                'parameters': [
                    {'name': 'stoppedBy', 'type': 'address'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ]
            },
            {
                'name': 'ObligationFulfilled',
                'description': 'Emitted when an obligation is fulfilled',
                'parameters': [
                    {'name': 'fulfilledBy', 'type': 'address'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ]
            },
            {
                'name': 'RelationshipProcessed',
                'description': 'Emitted when a relationship is processed',
                'parameters': [
                    {'name': 'relationshipId', 'type': 'uint256'},
                    {'name': 'processedBy', 'type': 'address'},
                    {'name': 'success', 'type': 'bool'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ]
            },
            {
                'name': 'RelationshipExecuted',
                'description': 'Emitted when a relationship is executed',
                'parameters': [
                    {'name': 'relationshipId', 'type': 'uint256'},
                    {'name': 'executedBy', 'type': 'address'},
                    {'name': 'success', 'type': 'bool'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ]
            }
        ])
        
        existing_vars = {var['name'] for var in analysis['state_variables']}
        
        if 'contractActive' not in existing_vars:
            analysis['state_variables'].append({
                'name': 'contractActive',
                'type': 'bool',
                'description': 'Contract activation status',
                'visibility': 'public'
            })
            
        if 'contractCreated' not in existing_vars:
            analysis['state_variables'].append({
                'name': 'contractCreated',
                'type': 'uint256',
                'description': 'Contract creation timestamp',
                'visibility': 'public'
            })
            
        if 'processedRelationships' not in existing_vars:
            analysis['state_variables'].append({
                'name': 'processedRelationships',
                'type': 'uint256',
                'description': 'Number of relationships processed',
                'visibility': 'public'
            })
            
        if 'totalRelationships' not in existing_vars:
            analysis['state_variables'].append({
                'name': 'totalRelationships',
                'type': 'uint256',
                'description': 'Total number of relationships',
                'visibility': 'public'
            })
            
        if 'relationshipCoveragePercentage' not in existing_vars:
            analysis['state_variables'].append({
                'name': 'relationshipCoveragePercentage',
                'type': 'uint256',
                'description': 'Relationship coverage percentage',
                'visibility': 'public'
            })
        
        analysis['modifiers'].extend([
            {
                'name': 'onlyActiveContract',
                'description': 'Require contract to be active'
            },
            {
                'name': 'onlyAuthorizedParties',
                'description': 'Require caller to be an authorized party'
            }
        ])
        
        analysis['events'].extend([
            {
                'name': 'ContractActivated',
                'description': 'Emitted when contract is activated',
                'parameters': [
                    {'name': 'timestamp', 'type': 'uint256'}
                ]
            },
            {
                'name': 'ContractTerminated',
                'description': 'Emitted when contract is terminated',
                'parameters': [
                    {'name': 'timestamp', 'type': 'uint256'},
                    {'name': 'terminatedBy', 'type': 'address'}
                ]
            }
        ])
    
    def _build_contract_structure(self, analysis: Dict[str, Any], contract_name: str) -> str:
        
        code = []
        
        code.append("// SPDX-License-Identifier: MIT")
        code.append("pragma solidity ^0.8.19;")
        code.append("")
        
        code.append(f"contract {contract_name} {{")
        code.append("")
        
        if analysis['state_variables']:
            code.append("    // State Variables")
            for var in analysis['state_variables']:
                var_line = f"    {var['type']} {var['visibility']} {var['name']};"
                if 'description' in var:
                    var_line += f" // {var['description']}"
                code.append(var_line)
            code.append("")
        
        if analysis['events']:
            code.append("    // Events")
            for event in analysis['events']:
                params = []
                if 'parameters' in event:
                    params = [f"{p['type']} {p['name']}" for p in event['parameters']]
                event_line = f"    event {event['name']}({', '.join(params)});"
                if 'description' in event:
                    event_line += f" // {event['description']}"
                code.append(event_line)
            code.append("")
        
        if analysis['modifiers']:
            code.append("    // Modifiers")
            for modifier in analysis['modifiers']:
                code.append(f"    modifier {modifier['name']}() {{")
                if modifier['name'] == 'onlyActiveContract':
                    code.append('        require(contractActive, "Contract is not active");')
                elif modifier['name'] == 'onlyAuthorizedParties':
                    code.append('        require(msg.sender == landlord || msg.sender == tenant, "Not authorized");')
                else:
                    code.append('        require(true, "Condition must be met"); // TODO: Implement specific condition')
                code.append("        _;")
                code.append("    }")
                code.append("")
        
        if analysis['functions']:
            code.append("    // Functions")
            for func in analysis['functions']:
                code.extend(self._generate_function_code(func))
                code.append("")
        
        code.append("}")
        
        return "\n".join(code)
    
    def _generate_function_code(self, func: Dict[str, Any]) -> List[str]:
        lines = []
        
        signature_parts = [func['visibility']]
        if func.get('payable'):
            signature_parts.append('payable')
        if func.get('returns'):
            signature_parts.append(f"returns ({func['returns']})")
        
        if func.get('function_type') == 'constructor':
            signature = f"    constructor() {' '.join(signature_parts)} {{"
        else:
            signature = f"    function {func['name']}() {' '.join(signature_parts)} {{"
        
        if 'description' in func:
            signature += f" // {func['description']}"
        lines.append(signature)
        
        function_type = func.get('function_type', '')
        
        if function_type == 'constructor':
            lines.extend([
                "        contractActive = true;",
                "        contractCreated = block.timestamp;",
                "        contractInitialized = false;",
                "        totalRelationships = 30; // Will be set based on actual relationship count",
                "        processedRelationships = 0;",
                "        relationshipCoveragePercentage = 0;",
                "        totalBusinessRules = 30;",
                "        executedBusinessRules = 0;",
                "        contractCompletionPercentage = 0;",
                "        emit ContractActivated(block.timestamp);"
            ])
            
        elif function_type == 'payment':
            lines.extend([
                '        require(msg.value > 0, "Payment amount must be greater than 0");',
                '        require(contractActive, "Contract must be active");',
                '        // TODO: Implement payment logic',
                '        emit PaymentMade(msg.sender, address(this), msg.value, block.timestamp);',
                '        return true;'
            ])
            
        elif function_type == 'obligation_fulfillment':
            lines.extend([
                '        require(contractActive, "Contract must be active");',
                '        // TODO: Track obligation completion',
                '        emit ObligationFulfilled(msg.sender, block.timestamp);',
                '        return true;'
            ])
            
        elif function_type == 'status_check':
            lines.extend([
                "        return contractActive;"
            ])
            
        elif function_type == 'termination':
            lines.extend([
                '        require(contractActive, "Contract already terminated");',
                '        contractActive = false;',
                '        emit ContractTerminated(block.timestamp, msg.sender);',
                '        return true;'
            ])
            
        elif function_type == 'relationship_processor':
            rel_name = func['name'].replace('process', '').replace('Relationships', '')
            count_var = f"{rel_name.lower()}Count"
            event_name = f"{rel_name}RelationshipProcessed"
            lines.extend([
                '        require(contractActive, "Contract must be active");',
                f'        {count_var}++;',
                f'        emit {event_name}("{rel_name}", {count_var}, block.timestamp);',
                '        return true;'
            ])
            
        elif function_type == 'relationship_validator':
            lines.extend([
                '        require(contractActive, "Contract must be active");',
                '        // Validate relationship consistency',
                '        return true;'
            ])
            
        elif function_type == 'relationship_executor':
            status_var = func['name'].replace('execute', '').replace('Relationship', '') + 'Status'
            event_name = func['name'].replace('execute', '').replace('Relationship', '') + 'RelationshipExecuted'
            lines.extend([
                '        require(contractActive, "Contract must be active");',
                f'        require(!{status_var}, "Relationship already executed");',
                f'        {status_var} = true;',
                f'        emit {event_name}(true, msg.sender, block.timestamp);',
                '        return true;'
            ])
            
        elif function_type == 'business_rule_processor':
            rule_name = func['name'].replace('process', '').replace('BusinessRules', '')
            count_var = f"{rule_name.lower()}RulesCount"
            event_name = f"{rule_name}BusinessRuleExecuted"
            lines.extend([
                '        require(contractActive, "Contract must be active");',
                f'        {count_var}++;',
                '        executedBusinessRules++;',
                '        contractCompletionPercentage = (executedBusinessRules * 100) / totalBusinessRules;',
                f'        emit {event_name}("{rule_name}", msg.sender, true, block.timestamp);',
                '        return true;'
            ])
            
        elif function_type == 'business_rule_validator':
            lines.extend([
                '        require(contractActive, "Contract must be active");',
                '        // Validate business rule compliance',
                '        return contractCompletionPercentage >= 80;'
            ])
            
        elif function_type == 'business_rule_enforcer':
            rule_name = func['name'].replace('enforce', '').replace('BusinessRules', '')
            event_name = f"{rule_name}BusinessRuleExecuted"
            lines.extend([
                '        require(contractActive, "Contract must be active");',
                '        require(msg.sender == landlord || msg.sender == tenant, "Not authorized");',
                '        // Enforce business rule compliance with penalties',
                f'        emit {event_name}("{rule_name}_ENFORCED", msg.sender, true, block.timestamp);',
                '        return true;'
            ])
            
        elif function_type == 'contract_initialization':
            lines.extend([
                '        require(!contractInitialized, "Contract already initialized");',
                '        contractInitialized = true;',
                '        totalBusinessRules = 30; // Set based on relationship count',
                '        executedBusinessRules = 0;',
                '        contractCompletionPercentage = 0;',
                '        emit ContractInitialized(totalBusinessRules, msg.sender, block.timestamp);',
                '        return true;'
            ])
            
        elif function_type == 'contract_validation':
            lines.extend([
                '        return contractInitialized && contractActive && contractCompletionPercentage >= 95;'
            ])
            
        elif function_type == 'contract_execution':
            lines.extend([
                '        require(contractInitialized, "Contract not initialized");',
                '        require(contractActive, "Contract must be active");',
                '        // Execute all contract terms and obligations',
                '        contractCompletionPercentage = 100;',
                '        emit ContractCompletionUpdated(contractCompletionPercentage, 100, block.timestamp);',
                '        return true;'
            ])
            
        elif function_type == 'contract_audit':
            lines.extend([
                '        require(contractActive, "Contract must be active");',
                '        // Perform comprehensive contract audit',
                '        return "Contract audit completed successfully";'
            ])
            
        elif function_type == 'contract_status':
            lines.extend([
                '        return contractCompletionPercentage;'
            ])
            
        elif function_type == 'individual_relationship_processor':
            func_name = func['name']
            rel_number = func_name.split('Relationship')[-1] if 'Relationship' in func_name else '1'
            
            state_vars = func.get('state_vars_used', [])
            if state_vars:
                var_name = state_vars[0]  # Use the declared state variable
                timestamp_name = var_name.replace('Status', 'Timestamp')
            else:
                var_name = f"relationship{rel_number}Status"
                timestamp_name = f"relationship{rel_number}Timestamp"
            
            lines.extend([
                '        require(contractActive, "Contract must be active");',
                f'        require(!{var_name}, "Relationship already processed");',
                f'        {var_name} = true;',
                f'        {timestamp_name} = block.timestamp;',
                '        processedRelationships++;',
                '        relationshipCoveragePercentage = (processedRelationships * 100) / totalRelationships;',
                f'        emit RelationshipProcessed({rel_number}, msg.sender, true, block.timestamp);',
                '        return true;'
            ])
            
        elif function_type == 'individual_relationship_validator':
            func_name = func['name']
            rel_number = func_name.split('Relationship')[-1] if 'Relationship' in func_name else '1'
            
            state_vars = func.get('state_vars_used', [])
            if state_vars:
                var_name = state_vars[0]  # Use the declared state variable
            else:
                var_name = f"relationship{rel_number}Status"
            
            lines.extend([
                '        require(contractActive, "Contract must be active");',
                f'        return {var_name};'
            ])
            
        elif function_type == 'individual_relationship_executor':
            rel_id = func['name'].split('Relationship')[-1] if 'Relationship' in func['name'] else '1'
            source_rel = func.get('source_relationship', {})
            if source_rel:
                relation_type = str(source_rel.get('relation', '')).lower()
                function_base_name = self._generate_relationship_function_name(source_rel, relation_type, str(source_rel))
                sanitized_base = self._sanitize_variable_name(f'{function_base_name}_{rel_id}')
            else:
                func_parts = func['name'].split('Relationship')
                base_name = func_parts[0].replace('execute', '') if func_parts else 'Relation'
                sanitized_base = self._sanitize_variable_name(f'{base_name}_{rel_id}')
            
            func_name = func['name']
            rel_number = func_name.split('Relationship')[-1] if 'Relationship' in func_name else '1'
            
            state_vars = func.get('state_vars_used', [])
            if state_vars:
                var_name = state_vars[0]  # Use the declared state variable
            else:
                var_name = f"relationship{rel_number}Status"
            
            lines.extend([
                '        require(contractActive, "Contract must be active");',
                f'        require({var_name}, "Relationship not processed yet");',
                f'        emit RelationshipExecuted({rel_number}, msg.sender, true, block.timestamp);',
                '        return true;'
            ])
            
        elif function_type == 'individual_relationship_status':
            rel_id = func['name'].split('Relationship')[-1] if 'Relationship' in func['name'] else '1'
            source_rel = func.get('source_relationship', {})
            if source_rel:
                relation_type = str(source_rel.get('relation', '')).lower()
                function_base_name = self._generate_relationship_function_name(source_rel, relation_type, str(source_rel))
                sanitized_base = self._sanitize_variable_name(f'{function_base_name}_{rel_id}')
            else:
                func_parts = func['name'].split('Relationship')
                base_name = func_parts[0].replace('get', '').replace('Status', '') if func_parts else 'Relation'
                sanitized_base = self._sanitize_variable_name(f'{base_name}_{rel_id}')
            
            func_name = func['name']
            rel_number = func_name.split('Relationship')[-1].replace('Status', '') if 'Relationship' in func_name else '1'
            
            state_vars = func.get('state_vars_used', [])
            if state_vars:
                var_name = state_vars[0]  # Use the declared state variable
            else:
                var_name = f"relationship{rel_number}Status"
            
            lines.extend([
                f'        return {var_name};'
            ])
            
        elif function_type == 'all_relationships_processor':
            lines.extend([
                '        require(contractActive, "Contract must be active");',
                '        require(contractInitialized, "Contract not initialized");',
                '        // Process all business relationships',
                '        processedRelationships = totalRelationships;',
                '        relationshipCoveragePercentage = 100;',
                '        return true;'
            ])
            
        elif function_type == 'all_relationships_validator':
            lines.extend([
                '        return relationshipCoveragePercentage >= 95;'
            ])
            
        elif function_type == 'relationship_coverage_calculator':
            lines.extend([
                '        return relationshipCoveragePercentage;'
            ])
            
        elif function_type == 'business_validation':
            lines.extend([
                '        require(contractActive, "Contract must be active");',
                '        businessRelationshipsEstablished = processedRelationships;',
                '        lastBusinessValidation = block.timestamp;',
                '        emit BusinessRelationshipValidated(totalRelationships, businessRelationshipsEstablished, msg.sender, block.timestamp);',
                '        return businessRelationshipsEstablished >= (totalRelationships * 80) / 100; // 80% threshold'
            ])
            
        elif function_type == 'business_metrics':
            lines.extend([
                '        return string(abi.encodePacked(',
                '            "Business Relationships: ", businessRelationshipsEstablished, "/", totalRelationships,',
                '            ", Rules Enforced: ", businessRulesEnforced,',
                '            ", Coverage: ", relationshipCoveragePercentage, "%"',
                '        ));'
            ])
            
        elif function_type == 'business_enforcement':
            lines.extend([
                '        require(contractActive, "Contract must be active");',
                '        require(businessRelationshipsEstablished > 0, "No business relationships established");',
                '        businessRulesEnforced++;',
                '        emit BusinessRulesEnforced(businessRulesEnforced, msg.sender, true, block.timestamp);',
                '        return true;'
            ])
            
        elif function_type == 'connectivity_metrics':
            lines.extend([
                '        uint256 totalEntities = connectedEntities + isolatedEntities;',
                '        return string(abi.encodePacked(',
                '            "Connected Entities: ", connectedEntities, "/", totalEntities,',
                '            ", Isolated: ", isolatedEntities,',
                '            ", Density: ", relationshipDensity, "%"',
                '        ));'
            ])
            
        elif function_type == 'entity_validation':
            lines.extend([
                '        require(contractActive, "Contract must be active");',
                '        connectedEntities = businessRelationshipsEstablished * 2;',
                '        relationshipDensity = (totalRelationships > 0) ? (businessRelationshipsEstablished * 100) / totalRelationships : 0;',
                '        return relationshipDensity >= 70; // 70% connectivity threshold'
            ])
            
        elif function_type == 'obligation_enforcement':
            lines.extend([
                '        require(contractActive, "Contract must be active");',
                '        require(businessRelationshipsEstablished > 0, "No business relationships to enforce");',
                '        bool allObligationsMet = true;',
                '        // Check each relationship for obligation compliance',
                '        if (processedRelationships < totalRelationships) {',
                '            allObligationsMet = false;',
                '            obligationViolations++;',
                '        }',
                '        emit ObligationEnforced("contractual_obligations", msg.sender, allObligationsMet, block.timestamp);',
                '        return allObligationsMet;'
            ])
            
        elif function_type == 'compliance_validation':
            lines.extend([
                '        require(contractActive, "Contract must be active");',
                '        lastComplianceCheck = block.timestamp;',
                '        // Calculate compliance score based on relationships and obligations',
                '        complianceScore = (businessRelationshipsEstablished * 100) / totalRelationships;',
                '        bool isCompliant = complianceScore >= 80; // 80% compliance threshold',
                '        if (!isCompliant) {',
                '            emit ComplianceViolation("insufficient_relationship_coverage", complianceScore, msg.sender, block.timestamp);',
                '        }',
                '        return isCompliant;'
            ])
            
        elif function_type == 'business_audit':
            lines.extend([
                '        return string(abi.encodePacked(',
                '            "Business Audit Report - ",',
                '            "Relationships: ", businessRelationshipsEstablished, "/", totalRelationships, ", ",',
                '            "Compliance: ", complianceScore, "%, ",',
                '            "Violations: ", obligationViolations, ", ",',
                '            "Last Check: ", lastComplianceCheck',
                '        ));'
            ])
            
        else:
            lines.extend([
                "        // TODO: Implement function logic",
                "        return true;"
            ])
        
        lines.append("    }")
        
        return lines
    
    def _sanitize_variable_name(self, text: str) -> str:
        import hashlib
        
        words = re.findall(r'\b\w+\b', str(text).lower())
        if not words:
            hash_suffix = hashlib.md5(str(text).encode()).hexdigest()[:6]
            return f'entity{hash_suffix.capitalize()}'
        
        meaningful_words = [w for w in words if len(w) > 2 and w not in ['the', 'and', 'or', 'but', 'for', 'with', 'this', 'that']]
        if not meaningful_words:
            meaningful_words = words[:2]  # Take first 2 if no meaningful words
        
        name = meaningful_words[0]
        for word in meaningful_words[1:3]:  # Max 3 words
            name += word.capitalize()
        
        solidity_keywords = {
            'contract', 'function', 'modifier', 'event', 'struct', 'enum',
            'mapping', 'address', 'uint', 'uint256', 'int', 'int256', 
            'bool', 'string', 'bytes', 'bytes32', 'public', 'private',
            'internal', 'external', 'view', 'pure', 'payable', 'constant',
            'if', 'else', 'for', 'while', 'do', 'return', 'break', 'continue',
            'true', 'false', 'null', 'this', 'super', 'new', 'delete',
            'throw', 'emit', 'require', 'assert', 'revert'
        }
        
        if name.lower() in solidity_keywords:
            name = f"{name}Value"
        
        if not name or name[0].isdigit():
            name = 'var' + name.capitalize()
        
        if hasattr(self, '_used_names'):
            if name in self._used_names:
                counter = 1
                while f"{name}{counter}" in self._used_names:
                    counter += 1
                name = f"{name}{counter}"
            self._used_names.add(name)
        else:
            self._used_names = {name}
        
        return name
    
    def get_generation_statistics(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        return {
            'state_variables': len(analysis.get('state_variables', [])),
            'functions': len(analysis.get('functions', [])),
            'events': len(analysis.get('events', [])),
            'modifiers': len(analysis.get('modifiers', [])),
            'function_types': {
                func['function_type']: len([f for f in analysis.get('functions', []) 
                                          if f.get('function_type') == func['function_type']])
                for func in analysis.get('functions', [])
                if 'function_type' in func
            }
        }

    def _determine_entity_role(self, entity_text: str) -> str:
        entity_lower = str(entity_text).lower()
        if any(term in entity_lower for term in ['tenant', 'renter', 'lessee']):
            return 'tenant'
        elif any(term in entity_lower for term in ['landlord', 'lessor', 'owner']):
            return 'landlord'
        elif any(term in entity_lower for term in ['employee', 'worker']):
            return 'employee'
        elif any(term in entity_lower for term in ['employer', 'company', 'corporation']):
            return 'employer'
        elif any(term in entity_lower for term in ['contractor', 'freelancer']):
            return 'contractor'
        elif any(term in entity_lower for term in ['client', 'customer']):
            return 'client'
        elif any(term in entity_lower for term in ['provider', 'supplier', 'vendor']):
            return 'provider'
        else:
            return 'party'

    def _extract_financial_context(self, entity_text: str) -> str:
        entity_lower = str(entity_text).lower()
        if any(term in entity_lower for term in ['salary', 'wage', 'compensation']):
            return 'salary'
        elif any(term in entity_lower for term in ['rent', 'rental']):
            return 'rent'
        elif any(term in entity_lower for term in ['fee', 'charge']):
            return 'fee'
        elif any(term in entity_lower for term in ['deposit', 'security']):
            return 'deposit'
        elif any(term in entity_lower for term in ['payment', 'pay']):
            return 'payment'
        else:
            return 'amount'

    def _generate_financial_variable_name(self, entity_text: str, context: str) -> str:
        base_name = context
        if 'monthly' in str(entity_text).lower():
            base_name += 'Monthly'
        elif 'annual' in str(entity_text).lower():
            base_name += 'Annual'
        return self._sanitize_variable_name(base_name)

    def _extract_temporal_context(self, entity_text: str) -> str:
        entity_lower = str(entity_text).lower()
        if any(term in entity_lower for term in ['start', 'begin', 'commence']):
            return 'start_date'
        elif any(term in entity_lower for term in ['end', 'expir', 'terminat']):
            return 'end_date'
        elif any(term in entity_lower for term in ['deadline', 'due']):
            return 'deadline'
        elif any(term in entity_lower for term in ['notice', 'notification']):
            return 'notice_period'
        elif any(term in entity_lower for term in ['duration', 'period']):
            return 'duration'
        else:
            return 'timestamp'

    def _generate_temporal_variable_name(self, entity_text: str, context: str) -> str:
        return self._sanitize_variable_name(context)
    
    def _determine_authorization_level(self, role: str) -> str:
        role_lower = str(role).lower()
        if any(term in role_lower for term in ['landlord', 'lessor', 'employer', 'owner']):
            return 'high'
        elif any(term in role_lower for term in ['tenant', 'lessee', 'employee', 'worker']):
            return 'medium'
        else:
            return 'basic'

    def _determine_responsible_party(self, obligation_text: str, parties: List[Dict]) -> str:
        obligation_lower = str(obligation_text).lower()
        
        for party in parties:
            if str(party['name']).lower() in obligation_lower or str(party['role']).lower() in obligation_lower:
                return party['role']
        
        if any(term in obligation_lower for term in ['tenant', 'renter']):
            return 'tenant'
        elif any(term in obligation_lower for term in ['landlord', 'owner']):
            return 'landlord'
        elif any(term in obligation_lower for term in ['employee', 'worker']):
            return 'employee'
        elif any(term in obligation_lower for term in ['employer', 'company']):
            return 'employer'
        else:
            return 'party'
    
    def _generate_obligation_id(self, obligation: str) -> str:
        import re
        words = re.findall(r'\w+', str(obligation).lower())
        key_words = [w for w in words if len(w) > 3][:3]
        if not key_words:
            key_words = ['obligation']
        return '_'.join(key_words)
    
    def _generate_condition_id(self, condition: str) -> str:
        import re
        words = re.findall(r'\w+', str(condition).lower())
        key_words = [w for w in words if len(w) > 3][:3]
        if not key_words:
            key_words = ['condition']
        return '_'.join(key_words)
    
    def _add_relationship_preservation_functions(self, analysis: Dict[str, Any], relationships: List[Dict]) -> None:
        
        relationship_types = {}
        for rel in relationships:
            rel_type = rel.get('relation', 'unknown')
            if rel_type not in relationship_types:
                relationship_types[rel_type] = []
            relationship_types[rel_type].append(rel)
        
        for rel_type, rel_list in relationship_types.items():
            if len(rel_list) == 0:
                continue
                
            sanitized_type = self._sanitize_variable_name(rel_type)
            
            analysis['state_variables'].append({
                'name': f'{sanitized_type}Count',
                'type': 'uint256',
                'description': f'Count of {rel_type} relationships processed',
                'visibility': 'public',
                'source_relationships': rel_list
            })
            
            analysis['functions'].append({
                'name': f'process{sanitized_type.title()}Relationships',
                'description': f'Process all {rel_type} relationships from business contract',
                'visibility': 'external',
                'returns': 'bool',
                'requires_authorization': True,
                'source_relationships': rel_list,
                'function_type': 'relationship_processor'
            })
            
            analysis['functions'].append({
                'name': f'validate{sanitized_type.title()}Relationships',
                'description': f'Validate {rel_type} relationship consistency',
                'visibility': 'public',
                'returns': 'bool',
                'source_relationships': rel_list,
                'function_type': 'relationship_validator'
            })
            
            analysis['events'].append({
                'name': f'{sanitized_type.title()}RelationshipProcessed',
                'description': f'Emitted when {rel_type} relationship is processed',
                'parameters': [
                    {'name': 'relationshipType', 'type': 'string'},
                    {'name': 'count', 'type': 'uint256'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ],
                'source_relationships': rel_list
            })
    
    def _add_source_target_relationship_functions(self, analysis: Dict[str, Any], relationships: List[Dict], entities: List[Dict]) -> None:
        
        entity_lookup = {e.get('id', ''): e.get('text', 'Unknown') for e in entities}
        
        source_target_pairs = {}
        for rel in relationships[:20]:  # Limit to prevent over-generation
            source_id = rel.get('source', '')
            target_id = rel.get('target', '')
            
            if source_id and target_id:
                pair_key = f"{source_id}_{target_id}"
                if pair_key not in source_target_pairs:
                    source_target_pairs[pair_key] = []
                source_target_pairs[pair_key].append(rel)
        
        for pair_key, pair_relations in source_target_pairs.items():
            source_id, target_id = pair_key.split('_', 1)
            source_name = self._sanitize_variable_name(entity_lookup.get(source_id, 'Source'))
            target_name = self._sanitize_variable_name(entity_lookup.get(target_id, 'Target'))
            
            function_base = f'{source_name}To{target_name.title()}'
            
            analysis['functions'].append({
                'name': f'execute{function_base}Relationship',
                'description': f'Execute relationship between {source_name} and {target_name}',
                'visibility': 'external',
                'returns': 'bool',
                'requires_authorization': True,
                'source_relationships': pair_relations,
                'function_type': 'relationship_executor'
            })
            
            analysis['state_variables'].append({
                'name': f'{function_base}Status',
                'type': 'bool',
                'description': f'Status of {source_name} to {target_name} relationship',
                'visibility': 'public',
                'source_relationships': pair_relations
            })
            
            analysis['events'].append({
                'name': f'{function_base}RelationshipExecuted',
                'description': f'Emitted when {source_name} to {target_name} relationship is executed',
                'parameters': [
                    {'name': 'success', 'type': 'bool'},
                    {'name': 'executor', 'type': 'address'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ],
                'source_relationships': pair_relations
            })
    
    def _add_comprehensive_business_logic_functions(self, analysis: Dict[str, Any], relationships: List[Dict], entities: List[Dict]) -> None:
        
        business_categories = {
            'financial_rules': [],
            'temporal_rules': [],
            'obligation_rules': [],
            'condition_rules': [],
            'party_rules': [],
            'service_rules': [],
            'compliance_rules': []
        }
        
        for relationship in relationships:
            relation_type = str(relationship.get('relation', '')).lower()
            relation_text = str(relationship.get('text', '')).lower()
            
            if any(term in relation_type or term in relation_text for term in ['payment', 'financial', 'money', 'cost', 'fee', 'salary', 'rent']):
                business_categories['financial_rules'].append(relationship)
            elif any(term in relation_type or term in relation_text for term in ['time', 'deadline', 'schedule', 'period', 'duration']):
                business_categories['temporal_rules'].append(relationship)
            elif any(term in relation_type or term in relation_text for term in ['obligation', 'duty', 'must', 'shall', 'required']):
                business_categories['obligation_rules'].append(relationship)
            elif any(term in relation_type or term in relation_text for term in ['condition', 'if', 'when', 'provided', 'unless']):
                business_categories['condition_rules'].append(relationship)
            elif any(term in relation_type or term in relation_text for term in ['party', 'between', 'involves', 'responsible']):
                business_categories['party_rules'].append(relationship)
            elif any(term in relation_type or term in relation_text for term in ['service', 'work', 'deliver', 'perform']):
                business_categories['service_rules'].append(relationship)
            else:
                business_categories['compliance_rules'].append(relationship)
        
        for category, category_relationships in business_categories.items():
            if not category_relationships:
                continue
                
            category_name = category.replace('_rules', '').title()
            
            analysis['functions'].append({
                'name': f'process{category_name}BusinessRules',
                'description': f'Process all {category_name.lower()} business rules from contract',
                'visibility': 'external',
                'returns': 'bool',
                'requires_authorization': True,
                'source_relationships': category_relationships,
                'function_type': 'business_rule_processor'
            })
            
            analysis['functions'].append({
                'name': f'validate{category_name}BusinessRules',
                'description': f'Validate all {category_name.lower()} business rule compliance',
                'visibility': 'public',
                'returns': 'bool',
                'source_relationships': category_relationships,
                'function_type': 'business_rule_validator'
            })
            
            analysis['functions'].append({
                'name': f'enforce{category_name}BusinessRules',
                'description': f'Enforce {category_name.lower()} business rule compliance with penalties',
                'visibility': 'external',
                'returns': 'bool',
                'requires_authorization': True,
                'source_relationships': category_relationships,
                'function_type': 'business_rule_enforcer'
            })
            
            analysis['state_variables'].append({
                'name': f'{category_name.lower()}RulesCount',
                'type': 'uint256',
                'description': f'Count of {category_name.lower()} business rules processed',
                'visibility': 'public',
                'source_relationships': category_relationships
            })
            
            analysis['events'].append({
                'name': f'{category_name}BusinessRuleExecuted',
                'description': f'Emitted when {category_name.lower()} business rule is executed',
                'parameters': [
                    {'name': 'ruleType', 'type': 'string'},
                    {'name': 'executor', 'type': 'address'},
                    {'name': 'success', 'type': 'bool'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ],
                'source_relationships': category_relationships
            })
        
        self._add_contract_completeness_functions(analysis, relationships, entities)
    
    def _add_contract_completeness_functions(self, analysis: Dict[str, Any], relationships: List[Dict], entities: List[Dict]) -> None:
        
        lifecycle_functions = [
            {
                'name': 'initializeContractTerms',
                'description': 'Initialize all contract terms and business rules',
                'visibility': 'external',
                'returns': 'bool',
                'requires_authorization': True,
                'function_type': 'contract_initialization'
            },
            {
                'name': 'validateContractCompleteness',
                'description': 'Validate that all contract requirements are met',
                'visibility': 'public',
                'returns': 'bool',
                'function_type': 'contract_validation'
            },
            {
                'name': 'executeContractTerms',
                'description': 'Execute all contract terms and business obligations',
                'visibility': 'external',
                'returns': 'bool',
                'requires_authorization': True,
                'function_type': 'contract_execution'
            },
            {
                'name': 'auditContractCompliance',
                'description': 'Audit contract for business rule compliance',
                'visibility': 'external',
                'returns': 'string memory',
                'requires_authorization': True,
                'function_type': 'contract_audit'
            },
            {
                'name': 'getContractCompletionStatus',
                'description': 'Get comprehensive status of contract completion',
                'visibility': 'public',
                'returns': 'uint256',
                'function_type': 'contract_status'
            }
        ]
        
        analysis['functions'].extend(lifecycle_functions)
        
        completeness_variables = [
            {
                'name': 'contractCompletionPercentage',
                'type': 'uint256',
                'description': 'Percentage of contract completion (0-100)',
                'visibility': 'public'
            },
            {
                'name': 'totalBusinessRules',
                'type': 'uint256',
                'description': 'Total number of business rules in contract',
                'visibility': 'public'
            },
            {
                'name': 'executedBusinessRules',
                'type': 'uint256',
                'description': 'Number of business rules successfully executed',
                'visibility': 'public'
            },
            {
                'name': 'contractInitialized',
                'type': 'bool',
                'description': 'Whether contract has been properly initialized',
                'visibility': 'public'
            }
        ]
        
        analysis['state_variables'].extend(completeness_variables)
        
        completeness_events = [
            {
                'name': 'ContractInitialized',
                'description': 'Emitted when contract is fully initialized',
                'parameters': [
                    {'name': 'totalRules', 'type': 'uint256'},
                    {'name': 'initializer', 'type': 'address'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ]
            },
            {
                'name': 'ContractCompletionUpdated',
                'description': 'Emitted when contract completion percentage changes',
                'parameters': [
                    {'name': 'oldPercentage', 'type': 'uint256'},
                    {'name': 'newPercentage', 'type': 'uint256'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ]
            },
            {
                'name': 'BusinessRuleCompleted',
                'description': 'Emitted when a business rule is completed',
                'parameters': [
                    {'name': 'ruleId', 'type': 'string'},
                    {'name': 'completedBy', 'type': 'address'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ]
            }
        ]
        
        analysis['events'].extend(completeness_events)
        
        self._add_enhanced_business_logic_functions(analysis, relationships, entities)
    
    def _generate_relationship_function_name(self, relationship: Dict, relation_type: str, relation_text: str) -> str:
        import re
        
        source = str(relationship.get('source', '')).lower()
        target = str(relationship.get('target', '')).lower()
        
        base_name = relation_type if relation_type and relation_type != 'unknown' else relation_text
        
        words = re.findall(r'\w+', str(base_name).lower())
        meaningful_words = [w for w in words if len(w) > 2 and w not in ['the', 'and', 'or', 'but', 'for', 'with']]
        
        if source and meaningful_words:
            source_words = re.findall(r'\w+', source)
            if source_words:
                meaningful_words = [source_words[0]] + meaningful_words
        
        if target and meaningful_words:
            target_words = re.findall(r'\w+', target)
            if target_words and len(meaningful_words) < 3:
                meaningful_words.append(target_words[0])
        
        if not meaningful_words:
            meaningful_words = ['relationship']
        
        function_name = meaningful_words[0]
        for word in meaningful_words[1:3]:  # Limit to 3 words total
            function_name += word.capitalize()
        
        return self._sanitize_variable_name(function_name)
    
    def _ensure_unique_names(self, contract_elements):
        used_names = set()
        
        for var in contract_elements.get('state_variables', []):
            original_name = var['name']
            if original_name in used_names:
                counter = 1
                new_name = f"{original_name}{counter}"
                while new_name in used_names:
                    counter += 1
                    new_name = f"{original_name}{counter}"
                var['name'] = new_name
            used_names.add(var['name'])
        
        for func in contract_elements.get('functions', []):
            original_name = func['name']
            if original_name in used_names:
                counter = 1
                new_name = f"{original_name}{counter}"
                while new_name in used_names:
                    counter += 1
                    new_name = f"{original_name}{counter}"
                func['name'] = new_name
            used_names.add(func['name'])
            
        for mod in contract_elements.get('modifiers', []):
            original_name = mod['name']
            if original_name in used_names:
                counter = 1
                new_name = f"{original_name}{counter}"
                while new_name in used_names:
                    counter += 1
                    new_name = f"{original_name}{counter}"
                mod['name'] = new_name
            used_names.add(mod['name'])
            
        for event in contract_elements.get('events', []):
            original_name = event['name']
            if original_name in used_names:
                counter = 1
                new_name = f"{original_name}{counter}"
                while new_name in used_names:
                    counter += 1
                    new_name = f"{original_name}{counter}"
                event['name'] = new_name
            used_names.add(event['name'])
    
    def _normalize_relationships(self, relationships):
        normalized = []
        for relationship in relationships:
            if isinstance(relationship, dict):
                normalized.append(relationship)
            else:
                relation_str = str(relationship)
                normalized.append({
                    'relation': relation_str,
                    'text': relation_str,
                    'source': 'unknown',
                    'target': 'unknown',
                    'id': f"rel_{len(normalized)}"
                })
        return normalized
    
    def _normalize_entities(self, entities):
        normalized = []
        for entity in entities:
            if isinstance(entity, dict):
                normalized.append(entity)
            else:
                entity_str = str(entity)
                normalized.append({
                    'text': entity_str,
                    'label': 'ENTITY',
                    'start': 0,
                    'end': len(entity_str),
                    'id': f"entity_{len(normalized)}"
                })
        return normalized
    
    def _add_enhanced_business_logic_functions(self, analysis: Dict[str, Any], relationships: List[Dict], entities: List[Dict]):
        
        analysis['functions'].extend([
            {
                'name': 'validateBusinessRelationships',
                'description': 'Validate all business relationships are properly established',
                'visibility': 'external',
                'returns': 'bool',
                'function_type': 'business_validation'
            },
            {
                'name': 'getBusinessRelationshipMetrics',
                'description': 'Get comprehensive business relationship metrics',
                'visibility': 'external',
                'returns': 'string memory',
                'function_type': 'business_metrics'
            },
            {
                'name': 'enforceBusinessRules',
                'description': 'Enforce all business rules and obligations',
                'visibility': 'external',
                'returns': 'bool',
                'requires_authorization': True,
                'function_type': 'business_enforcement'
            }
        ])
        
        analysis['state_variables'].extend([
            {
                'name': 'businessRelationshipsEstablished',
                'type': 'uint256',
                'description': 'Count of properly established business relationships',
                'visibility': 'public'
            },
            {
                'name': 'businessRulesEnforced',
                'type': 'uint256', 
                'description': 'Count of business rules successfully enforced',
                'visibility': 'public'
            },
            {
                'name': 'lastBusinessValidation',
                'type': 'uint256',
                'description': 'Timestamp of last business validation',
                'visibility': 'public'
            }
        ])
        
        analysis['events'].extend([
            {
                'name': 'BusinessRelationshipValidated',
                'description': 'Emitted when business relationships are validated',
                'parameters': [
                    {'name': 'totalRelationships', 'type': 'uint256'},
                    {'name': 'validRelationships', 'type': 'uint256'},
                    {'name': 'validator', 'type': 'address'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ]
            },
            {
                'name': 'BusinessRulesEnforced',
                'description': 'Emitted when business rules are enforced',
                'parameters': [
                    {'name': 'rulesCount', 'type': 'uint256'},
                    {'name': 'enforcer', 'type': 'address'},
                    {'name': 'success', 'type': 'bool'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ]
            }
        ])
        
        relationship_count = len(relationships)
        entity_count = len(entities)
        
        if relationship_count > 0 and entity_count > 0:
            analysis['functions'].extend([
                {
                    'name': 'getRelationshipConnectivity',
                    'description': f'Get connectivity metrics for {relationship_count} relationships and {entity_count} entities',
                    'visibility': 'external',
                    'returns': 'string memory',
                    'function_type': 'connectivity_metrics'
                },
                {
                    'name': 'validateEntityConnections',
                    'description': 'Validate that all entities have proper connections',
                    'visibility': 'external',
                    'returns': 'bool',
                    'function_type': 'entity_validation'
                }
            ])
            
            analysis['state_variables'].extend([
                {
                    'name': 'connectedEntities',
                    'type': 'uint256',
                    'description': 'Count of entities with at least one connection',
                    'visibility': 'public'
                },
                {
                    'name': 'isolatedEntities', 
                    'type': 'uint256',
                    'description': 'Count of isolated entities without connections',
                    'visibility': 'public'
                },
                {
                    'name': 'relationshipDensity',
                    'type': 'uint256',
                    'description': 'Relationship density percentage (0-100)',
                    'visibility': 'public'
                }
            ])
            
        self._add_business_rule_enforcement_mechanisms(analysis, relationships, entities)
    
    def _add_business_rule_enforcement_mechanisms(self, analysis: Dict[str, Any], relationships: List[Dict], entities: List[Dict]):
        
        analysis['functions'].extend([
            {
                'name': 'enforceObligations',
                'description': 'Enforce all contractual obligations',
                'visibility': 'external',
                'returns': 'bool',
                'requires_authorization': True,
                'function_type': 'obligation_enforcement'
            },
            {
                'name': 'validateCompliance',
                'description': 'Validate contract compliance with business rules',
                'visibility': 'external',
                'returns': 'bool',
                'function_type': 'compliance_validation'
            },
            {
                'name': 'auditBusinessLogic',
                'description': 'Comprehensive audit of business logic implementation',
                'visibility': 'external',
                'returns': 'string memory',
                'function_type': 'business_audit'
            }
        ])
        
        analysis['state_variables'].extend([
            {
                'name': 'obligationViolations',
                'type': 'uint256',
                'description': 'Count of obligation violations detected',
                'visibility': 'public'
            },
            {
                'name': 'complianceScore',
                'type': 'uint256',
                'description': 'Overall compliance score (0-100)',
                'visibility': 'public'
            },
            {
                'name': 'lastComplianceCheck',
                'type': 'uint256',
                'description': 'Timestamp of last compliance validation',
                'visibility': 'public'
            }
        ])
        
        analysis['events'].extend([
            {
                'name': 'ObligationEnforced',
                'description': 'Emitted when obligations are enforced',
                'parameters': [
                    {'name': 'obligationType', 'type': 'string'},
                    {'name': 'party', 'type': 'address'},
                    {'name': 'success', 'type': 'bool'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ]
            },
            {
                'name': 'ComplianceViolation',
                'description': 'Emitted when compliance violations are detected',
                'parameters': [
                    {'name': 'violationType', 'type': 'string'},
                    {'name': 'severity', 'type': 'uint256'},
                    {'name': 'party', 'type': 'address'},
                    {'name': 'timestamp', 'type': 'uint256'}
                ]
            }
        ])