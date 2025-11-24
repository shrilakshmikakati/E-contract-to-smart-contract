"""
Enhanced Smart Contract Generator
Generates comprehensive Solidity contracts with functions, events, modifiers, and business logic
"""

from typing import Dict, Any, List, Optional, Tuple
import re
from datetime import datetime

class EnhancedSmartContractGenerator:
    """Generates comprehensive smart contracts from business requirements"""
    
    def __init__(self):
        self.entity_to_variable_mapping = {}
        self.relationship_to_function_mapping = {}
        
    def generate_enhanced_contract(self, entities: List[Dict[str, Any]], 
                                 relationships: List[Dict[str, Any]], 
                                 contract_name: str = "GeneratedContract") -> str:
        """Generate a comprehensive Solidity contract"""
        
        print(f"Generating enhanced smart contract: {contract_name}")
        
        # Analyze entities and relationships
        contract_analysis = self._analyze_contract_requirements(entities, relationships)
        
        # Generate contract components
        contract_code = self._build_contract_structure(contract_analysis, contract_name)
        
        print(f"Generated contract with {len(contract_analysis['state_variables'])} state variables, "
              f"{len(contract_analysis['functions'])} functions, and {len(contract_analysis['events'])} events")
        
        return contract_code
    
    def _classify_entity_by_content(self, text: str) -> str:
        """Classify entity type based on content analysis"""
        text_lower = text.lower().strip()
        
        # Financial entities
        if any(pattern in text_lower for pattern in ['$', '£', '€', 'usd', 'gbp', 'eur', 'payment', 'fee', 'cost', 'amount', 'price', 'salary', 'rent', 'deposit', 'money']):
            return 'FINANCIAL'
        
        # Person entities
        if any(pattern in text_lower for pattern in ['tenant', 'landlord', 'employee', 'employer', 'client', 'customer', 'contractor', 'person', 'individual']):
            return 'PERSON'
        
        # Organization entities
        if any(pattern in text_lower for pattern in ['company', 'corporation', 'inc', 'llc', 'ltd', 'organization', 'firm', 'business']):
            return 'ORGANIZATION'
        
        # Temporal entities
        if any(pattern in text_lower for pattern in ['date', 'deadline', 'month', 'year', 'day', 'time', 'january', 'february', 'march', 'april', 'may', 'june', 'july', 'august', 'september', 'october', 'november', 'december']):
            return 'TEMPORAL'
        
        # Location entities
        if any(pattern in text_lower for pattern in ['address', 'street', 'city', 'state', 'country', 'location', 'property']):
            return 'LOCATION'
        
        # Obligation entities
        if any(pattern in text_lower for pattern in ['must', 'shall', 'required', 'obligation', 'duty', 'responsibility']):
            return 'OBLIGATIONS'
        
        return 'GENERAL'
    
    def _analyze_contract_requirements(self, entities: List[Dict[str, Any]], 
                                     relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Enhanced analysis of entities and relationships to determine comprehensive contract requirements"""
        
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
        
        # Enhanced business entity categorization with expanded recognition
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
        
        # Enhanced entity processing with comprehensive business logic mapping and expanded recognition
        for entity in entities:
            # Handle different entity formats
            if isinstance(entity, str):
                entity_text = entity.lower().strip()
                entity_type = self._classify_entity_by_content(entity_text)
            else:
                entity_type = entity.get('label', entity.get('type', '')).upper()
                entity_text = str(entity.get('text', entity.get('value', ''))).lower().strip()
                
            # Skip empty or very short entities
            if not entity_text or len(entity_text) < 2:
                continue
            
            # Enhanced party detection with comprehensive role mapping
            if entity_type in ['PERSON', 'ORG', 'ORGANIZATION'] or any(role in entity_text for role in ['tenant', 'landlord', 'employee', 'employer', 'contractor', 'client', 'provider', 'lessor', 'lessee', 'buyer', 'seller']):
                # Enhanced party handling with role-based access control
                role = self._determine_entity_role(entity_text)
                var_name = self._sanitize_variable_name(entity_text)
                
                # More descriptive party information
                party_info = {
                    'name': var_name, 
                    'role': role, 
                    'text': entity_text,
                    'entity_type': entity_type,
                    'authorization_level': self._determine_authorization_level(role)
                }
                self.parties.append(party_info)
                
                # Add comprehensive party state variables
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
                
                # Add party role validation modifier
                analysis['modifiers'].append({
                    'name': f"only{role.title()}",
                    'description': f"Restrict access to {role}",
                    'parameter': var_name
                })
                
            elif entity_type in ['FINANCIAL', 'MONEY'] or any(term in entity_text for term in ['$', 'payment', 'salary', 'rent', 'fee', 'deposit', 'amount']):
                # Enhanced financial handling with context-aware variables
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
                
                # Add payment function for financial elements
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
                # Enhanced temporal handling with deadlines and validation
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
                
                # Add deadline validation function if it's a deadline
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
                # Enhanced obligation handling with enforcement mechanisms
                obligation_name = self._sanitize_variable_name(entity_text)
                responsible_party = self._determine_responsible_party(entity_text, self.parties)
                
                self.obligations.append({'name': obligation_name, 'party': responsible_party, 'text': entity_text})
                
                # Add completion tracking with party responsibility
                analysis['state_variables'].append({
                    'name': f"{obligation_name}Status",
                    'type': 'bool',
                    'description': f"Track completion of {entity_text}",
                    'visibility': 'public',
                    'source_entity': entity
                })
                
            elif entity_type in ['LOCATION', 'GPE'] or any(term in entity_text for term in ['address', 'street', 'city', 'state', 'country', 'location', 'property']):
                # Enhanced location handling
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
                # Enhanced service handling
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
                # Enhanced quantity and numeric handling
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
                # Enhanced contact information handling
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
                # Enhanced condition handling with validation mechanisms
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
                # Generic entity handling - ensure no entity is missed
                generic_name = self._sanitize_variable_name(entity_text)
                if generic_name and len(generic_name) > 1:
                    analysis['state_variables'].append({
                        'name': f"{generic_name}Value",
                        'type': 'string',
                        'description': f"Value for {entity_text}",
                        'visibility': 'public',
                        'source_entity': entity
                    })
        
        # Enhanced relationship processing to create comprehensive functions
        processed_relations = set()  # Avoid duplicate functions
        
        for relationship in relationships:
            relation_type = str(relationship.get('relation', '')).lower()
            relation_text = str(relationship.get('text', '')).lower()
            
            # Enhanced payment and financial processing with comprehensive function mapping
            if any(term in relation_type or term in relation_text for term in ['payment', 'financial', 'pay', 'money', 'salary', 'rent', 'deposit', 'fee', 'cost']):
                if 'payment_processing' not in processed_relations:
                    # Main payment processing function
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
                    
                    # Enhanced payment validation functions
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
            
            # Enhanced obligation processing with comprehensive enforcement
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
            
            # Enhanced condition processing with comprehensive validation
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
            
            # Enhanced temporal processing with deadline management
            elif any(term in relation_type or term in relation_text for term in ['temporal', 'deadline', 'due', 'expires', 'schedule', 'period']):
                if 'temporal_management' not in processed_relations:
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
                    processed_relations.add('temporal_management')
            
            # Enhanced access control processing  
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
            
            # Enhanced temporal processing
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
                
        # Add comprehensive business rule functions
        self._add_business_validation_functions(analysis)
        
        # Add enhanced event system
        self._add_comprehensive_events(analysis, relationships)
        
        # Add standard functions with enhancements
        self._add_standard_functions(analysis)
        
        return analysis
    
    def _add_business_validation_functions(self, analysis: Dict[str, Any]):
        """Add comprehensive business rule validation functions"""
        
        # Payment validation functions
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
        
        # Access control validation
        if self.parties:
            analysis['functions'].append({
                'name': 'validatePartyAuthorization',
                'description': 'Validate party authorization for specific actions',
                'visibility': 'internal',
                'returns': 'bool',
                'function_type': 'access_validation'
            })
        
        # Temporal validation functions
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
        
        # Obligation validation
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
                    'returns': 'string',
                    'function_type': 'status_reporting'
                }
            ])
    
    def _add_comprehensive_events(self, analysis: Dict[str, Any], relationships: List[Dict[str, Any]]):
        """Add comprehensive event system for contract transparency"""
        
        # Financial events
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
        
        # Obligation events
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
        
        # Access control events
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
        
        # Add additional relationship processing for ownership transfers
        for relationship in relationships:
            relation_type = str(relationship.get('relation', '')).lower()
            
            if relation_type in ['ownership']:
                # Ownership relationships become transfer functions
                analysis['functions'].append({
                    'name': 'transferOwnership',
                    'description': 'Transfer ownership of assets',
                    'visibility': 'external',
                    'returns': 'bool',
                    'source_relationship': relationship,
                    'function_type': 'ownership_transfer'
                })
                
            elif relation_type in ['temporal_start', 'temporal_end']:
                # Temporal relationships become time-based functions
                analysis['functions'].append({
                    'name': 'checkTemporalCondition',
                    'description': 'Check if temporal conditions are met',
                    'visibility': 'view',
                    'returns': 'bool',
                    'source_relationship': relationship,
                    'function_type': 'temporal_check'
                })
        
        # Add common contract management functions
        self._add_standard_functions(analysis)
        
        return analysis
    
    def _add_standard_functions(self, analysis: Dict[str, Any]):
        """Add comprehensive standard contract management functions and elements"""
        
        # Enhanced Constructor with party initialization
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
        
        # Enhanced contract status and management functions
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
                'returns': 'string',
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
        
        # Add essential modifiers for access control
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
        
        # Add comprehensive events for transparency
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
            }
        ])
        
        # Add contract status variables
        analysis['state_variables'].extend([
            {
                'name': 'contractActive',
                'type': 'bool',
                'description': 'Contract activation status',
                'visibility': 'public'
            },
            {
                'name': 'contractCreated',
                'type': 'uint256',
                'description': 'Contract creation timestamp',
                'visibility': 'public'
            }
        ])
        
        # Add standard modifiers
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
        
        # Add standard events
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
        """Build the complete Solidity contract code"""
        
        code = []
        
        # SPDX License and Pragma
        code.append("// SPDX-License-Identifier: MIT")
        code.append("pragma solidity ^0.8.19;")
        code.append("")
        
        # Contract declaration
        code.append(f"contract {contract_name} {{")
        code.append("")
        
        # State variables
        if analysis['state_variables']:
            code.append("    // State Variables")
            for var in analysis['state_variables']:
                var_line = f"    {var['type']} {var['visibility']} {var['name']};"
                if 'description' in var:
                    var_line += f" // {var['description']}"
                code.append(var_line)
            code.append("")
        
        # Events
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
        
        # Modifiers
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
        
        # Functions
        if analysis['functions']:
            code.append("    // Functions")
            for func in analysis['functions']:
                code.extend(self._generate_function_code(func))
                code.append("")
        
        # Close contract
        code.append("}")
        
        return "\n".join(code)
    
    def _generate_function_code(self, func: Dict[str, Any]) -> List[str]:
        """Generate code for a specific function"""
        lines = []
        
        # Function signature
        signature_parts = [func['visibility']]
        if func.get('payable'):
            signature_parts.append('payable')
        if func.get('returns'):
            signature_parts.append(f"returns ({func['returns']})")
        
        # Special handling for constructor
        if func.get('function_type') == 'constructor':
            signature = f"    constructor() {' '.join(signature_parts)} {{"
        else:
            signature = f"    function {func['name']}() {' '.join(signature_parts)} {{"
        
        if 'description' in func:
            signature += f" // {func['description']}"
        lines.append(signature)
        
        # Function body based on type
        function_type = func.get('function_type', '')
        
        if function_type == 'constructor':
            lines.extend([
                "        contractActive = true;",
                "        contractCreated = block.timestamp;",
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
            obligation_var = func['name'].replace('fulfill', '').lower() + 'Completed'
            event_name = func['name'].replace('fulfill', '') + 'Completed'
            lines.extend([
                '        require(contractActive, "Contract must be active");',
                f'        require(!{obligation_var}, "Obligation already completed");',
                f'        {obligation_var} = true;',
                f'        emit {event_name}(block.timestamp, msg.sender);',
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
            
        else:
            lines.extend([
                "        // TODO: Implement function logic",
                "        return true;"
            ])
        
        lines.append("    }")
        
        return lines
    
    def _sanitize_variable_name(self, text: str) -> str:
        """Convert entity text to valid Solidity variable name"""
        # Remove non-alphanumeric characters and convert to camelCase
        words = re.findall(r'\\b\\w+\\b', text.lower())
        if not words:
            return 'unknownVariable'
        
        # First word lowercase, rest title case
        name = words[0]
        for word in words[1:]:
            name += word.capitalize()
        
        # Ensure it's a valid identifier
        if not name or name[0].isdigit():
            name = 'var' + name
        
        return name
    
    def get_generation_statistics(self, analysis: Dict[str, Any]) -> Dict[str, Any]:
        """Get statistics about the generated contract"""
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
        """Determine the role of a party entity"""
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
        """Extract financial context from entity text"""
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
        """Generate appropriate variable name for financial elements"""
        base_name = context
        if 'monthly' in str(entity_text).lower():
            base_name += 'Monthly'
        elif 'annual' in str(entity_text).lower():
            base_name += 'Annual'
        return self._sanitize_variable_name(base_name)

    def _extract_temporal_context(self, entity_text: str) -> str:
        """Extract temporal context from entity text"""
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
        """Generate appropriate variable name for temporal elements"""
        return self._sanitize_variable_name(context)
    
    def _determine_authorization_level(self, role: str) -> str:
        """Determine authorization level based on party role"""
        role_lower = str(role).lower()
        if any(term in role_lower for term in ['landlord', 'lessor', 'employer', 'owner']):
            return 'high'
        elif any(term in role_lower for term in ['tenant', 'lessee', 'employee', 'worker']):
            return 'medium'
        else:
            return 'basic'

    def _determine_responsible_party(self, obligation_text: str, parties: List[Dict]) -> str:
        """Determine which party is responsible for an obligation"""
        obligation_lower = str(obligation_text).lower()
        
        # Check if obligation text mentions specific parties
        for party in parties:
            if str(party['name']).lower() in obligation_lower or str(party['role']).lower() in obligation_lower:
                return party['role']
        
        # Default responsibility based on common patterns
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
        """Generate a unique identifier for an obligation"""
        import re
        # Extract key words from obligation
        words = re.findall(r'\w+', str(obligation).lower())
        # Take first few significant words
        key_words = [w for w in words if len(w) > 3][:3]
        if not key_words:
            key_words = ['obligation']
        return '_'.join(key_words)
    
    def _generate_condition_id(self, condition: str) -> str:
        """Generate a unique identifier for a condition"""
        import re
        # Extract key words from condition
        words = re.findall(r'\w+', str(condition).lower())
        # Take first few significant words
        key_words = [w for w in words if len(w) > 3][:3]
        if not key_words:
            key_words = ['condition']
        return '_'.join(key_words)