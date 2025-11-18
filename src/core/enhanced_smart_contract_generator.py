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
    
    def _analyze_contract_requirements(self, entities: List[Dict[str, Any]], 
                                     relationships: List[Dict[str, Any]]) -> Dict[str, Any]:
        """Analyze entities and relationships to determine contract requirements"""
        
        analysis = {
            'state_variables': [],
            'functions': [],
            'events': [],
            'modifiers': [],
            'structs': [],
            'enums': [],
            'mappings': []
        }
        
        # Process entities to create state variables
        for entity in entities:
            entity_type = entity.get('label', '').upper()
            entity_text = entity.get('text', '')
            
            if entity_type in ['PERSON', 'ORG', 'ORGANIZATION']:
                # Party entities become address variables
                var_name = self._sanitize_variable_name(entity_text)
                analysis['state_variables'].append({
                    'name': var_name,
                    'type': 'address',
                    'description': f"Address of {entity_text}",
                    'visibility': 'public',
                    'source_entity': entity
                })
                
            elif entity_type in ['FINANCIAL', 'MONEY']:
                # Financial entities become uint variables
                var_name = self._sanitize_variable_name(entity_text)
                analysis['state_variables'].append({
                    'name': var_name,
                    'type': 'uint256',
                    'description': f"Amount for {entity_text}",
                    'visibility': 'public',
                    'source_entity': entity
                })
                
            elif entity_type in ['TEMPORAL', 'DATE']:
                # Temporal entities become timestamp variables
                var_name = self._sanitize_variable_name(entity_text)
                analysis['state_variables'].append({
                    'name': var_name,
                    'type': 'uint256',
                    'description': f"Timestamp for {entity_text}",
                    'visibility': 'public',
                    'source_entity': entity
                })
                
            elif entity_type == 'OBLIGATIONS':
                # Obligations become functions and state tracking variables
                obligation_name = self._sanitize_variable_name(entity_text)
                
                # Add completion tracking variable
                analysis['state_variables'].append({
                    'name': f"{obligation_name}Completed",
                    'type': 'bool',
                    'description': f"Track completion of {entity_text}",
                    'visibility': 'public',
                    'source_entity': entity
                })
                
                # Add function to fulfill obligation
                analysis['functions'].append({
                    'name': f"fulfill{obligation_name.title()}",
                    'description': f"Fulfill obligation: {entity_text}",
                    'visibility': 'external',
                    'returns': 'bool',
                    'source_entity': entity,
                    'function_type': 'obligation_fulfillment'
                })
                
                # Add completion event
                analysis['events'].append({
                    'name': f"{obligation_name.title()}Completed",
                    'description': f"Emitted when {entity_text} is completed",
                    'parameters': [
                        {'name': 'timestamp', 'type': 'uint256'},
                        {'name': 'completedBy', 'type': 'address'}
                    ],
                    'source_entity': entity
                })
                
            elif entity_type == 'CONDITIONS':
                # Conditions become modifiers
                condition_name = self._sanitize_variable_name(entity_text)
                analysis['modifiers'].append({
                    'name': f"require{condition_name.title()}",
                    'description': f"Require condition: {entity_text}",
                    'source_entity': entity
                })
        
        # Process relationships to create functions
        for relationship in relationships:
            relation_type = relationship.get('relation', '')
            
            if relation_type in ['payment', 'financial_obligation']:
                # Payment relationships become payment functions
                analysis['functions'].append({
                    'name': 'makePayment',
                    'description': 'Process payment between parties',
                    'visibility': 'external',
                    'payable': True,
                    'returns': 'bool',
                    'source_relationship': relationship,
                    'function_type': 'payment'
                })
                
                # Add payment event
                analysis['events'].append({
                    'name': 'PaymentMade',
                    'description': 'Emitted when a payment is made',
                    'parameters': [
                        {'name': 'from', 'type': 'address'},
                        {'name': 'to', 'type': 'address'},
                        {'name': 'amount', 'type': 'uint256'},
                        {'name': 'timestamp', 'type': 'uint256'}
                    ],
                    'source_relationship': relationship
                })
                
            elif relation_type in ['ownership']:
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
        """Add standard contract management functions"""
        
        # Constructor
        analysis['functions'].insert(0, {
            'name': 'constructor',
            'description': 'Initialize contract with required parameters',
            'visibility': 'public',
            'function_type': 'constructor'
        })
        
        # Contract status checking
        analysis['functions'].append({
            'name': 'isContractActive',
            'description': 'Check if contract is currently active',
            'visibility': 'view',
            'returns': 'bool',
            'function_type': 'status_check'
        })
        
        # Contract termination
        analysis['functions'].append({
            'name': 'terminateContract',
            'description': 'Terminate the contract',
            'visibility': 'external',
            'returns': 'bool',
            'function_type': 'termination'
        })
        
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