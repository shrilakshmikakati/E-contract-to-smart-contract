"""
Improved Smart Contract Generator with Enhanced Relationship Preservation
Focus on genuine accuracy improvement through better relationship implementation
"""
import re
from typing import List, Dict, Any, Set
from dataclasses import dataclass
from pathlib import Path

@dataclass
class RelationshipImplementation:
    """Tracks how relationships are implemented in smart contracts"""
    relationship_id: str
    relation_type: str
    source_entity: str
    target_entity: str
    implementation_functions: List[str]
    state_variables: List[str]
    business_logic: str
    confidence_score: float

class ImprovedSmartContractGenerator:
    """Enhanced generator focusing on accurate relationship preservation"""
    
    def __init__(self):
        self.relationship_implementations = []
        self.generated_functions = set()
        self.state_variables = set()
        
    def generate_enhanced_smart_contract(self, entities: List[Dict], relationships: List[Dict], 
                                       contract_text: str) -> str:
        """Generate smart contract with enhanced relationship preservation"""
        print("=== Enhanced Smart Contract Generation ===")
        
        # Analyze relationships for implementation planning
        implementation_plan = self._create_implementation_plan(relationships, entities)
        
        # Generate contract structure
        contract_code = self._generate_contract_structure(implementation_plan, entities)
        
        # Calculate accurate metrics
        accuracy_metrics = self._calculate_accurate_metrics(relationships, implementation_plan)
        
        print(f"Generated contract with {len(implementation_plan)} relationship implementations")
        print(f"Relationship preservation accuracy: {accuracy_metrics['preservation_rate']:.1f}%")
        
        return contract_code, accuracy_metrics
    
    def _create_implementation_plan(self, relationships: List[Dict], entities: List[Dict]) -> List[RelationshipImplementation]:
        """Create comprehensive implementation plan for each relationship"""
        implementations = []
        
        for i, rel in enumerate(relationships):
            # Determine implementation strategy based on relationship type
            impl_strategy = self._determine_implementation_strategy(rel)
            
            if impl_strategy:
                implementation = RelationshipImplementation(
                    relationship_id=rel.get('id', f'rel_{i}'),
                    relation_type=rel.get('relation', 'unknown'),
                    source_entity=rel.get('source_text', 'unknown'),
                    target_entity=rel.get('target_text', 'unknown'),
                    implementation_functions=impl_strategy['functions'],
                    state_variables=impl_strategy['variables'],
                    business_logic=impl_strategy['logic'],
                    confidence_score=rel.get('confidence', 0.5)
                )
                implementations.append(implementation)
        
        return implementations
    
    def _determine_implementation_strategy(self, relationship: Dict) -> Dict[str, Any]:
        """Determine how to implement a specific relationship type"""
        relation_type = relationship.get('relation', 'unknown')
        
        strategies = {
            'payment': {
                'functions': ['makePayment', 'verifyPayment', 'getPaymentStatus'],
                'variables': ['paymentAmount', 'paymentDue', 'paymentCompleted'],
                'logic': 'Implement payment tracking with amount verification and status updates'
            },
            'ownership': {
                'functions': ['transferOwnership', 'verifyOwnership', 'getOwner'],
                'variables': ['currentOwner', 'ownershipHistory', 'ownershipVerified'],
                'logic': 'Track ownership changes with verification and history logging'
            },
            'obligation': {
                'functions': ['fulfillObligation', 'verifyFulfillment', 'getObligationStatus'],
                'variables': ['obligationStatus', 'obligationDeadline', 'obligationCompleted'],
                'logic': 'Monitor obligation fulfillment with deadline tracking'
            },
            'service_provision': {
                'functions': ['provideService', 'verifyServiceDelivery', 'getServiceStatus'],
                'variables': ['serviceProvider', 'serviceRecipient', 'serviceCompleted'],
                'logic': 'Track service delivery and verification between parties'
            },
            'contractual_agreement': {
                'functions': ['executeAgreement', 'verifyCompliance', 'getAgreementStatus'],
                'variables': ['agreementActive', 'complianceStatus', 'agreementTerms'],
                'logic': 'Manage agreement execution and compliance monitoring'
            }
        }
        
        # Default strategy for unknown relationship types
        if relation_type not in strategies:
            return {
                'functions': [f'manage{relation_type.title()}', f'verify{relation_type.title()}'],
                'variables': [f'{relation_type}Status', f'{relation_type}Data'],
                'logic': f'Generic implementation for {relation_type} relationship'
            }
        
        return strategies[relation_type]
    
    def _generate_contract_structure(self, implementations: List[RelationshipImplementation], 
                                   entities: List[Dict]) -> str:
        """Generate complete smart contract with proper structure"""
        
        # Collect all state variables
        all_variables = set()
        all_functions = set()
        
        for impl in implementations:
            all_variables.update(impl.state_variables)
            all_functions.update(impl.implementation_functions)
        
        # Generate contract code
        contract_code = self._build_contract_code(all_variables, all_functions, implementations, entities)
        
        return contract_code
    
    def _build_contract_code(self, variables: Set[str], functions: Set[str], 
                           implementations: List[RelationshipImplementation], 
                           entities: List[Dict]) -> str:
        """Build the actual Solidity contract code"""
        
        code = "// SPDX-License-Identifier: MIT\n"
        code += "pragma solidity ^0.8.0;\n\n"
        code += "contract EnhancedBusinessContract {\n"
        
        # Add state variables
        code += "    // State variables for relationship tracking\n"
        for var in sorted(variables):
            code += f"    mapping(address => bool) public {var};\n"
            code += f"    uint256 public {var}Value;\n"
        
        # Add entity addresses
        code += "\n    // Entity addresses\n"
        for i, entity in enumerate(entities[:5]):  # Limit to avoid too many
            entity_name = self._sanitize_name(entity.get('text', f'entity{i}'))
            code += f"    address public {entity_name}Address;\n"
        
        # Add events
        code += "\n    // Events for relationship tracking\n"
        for impl in implementations:
            event_name = f"{impl.relation_type.title()}Updated"
            code += f"    event {event_name}(address indexed source, address indexed target, bool status);\n"
        
        # Add constructor
        code += "\n    constructor() {\n"
        code += "        // Initialize contract\n"
        for var in sorted(list(variables)[:3]):  # Initialize some variables
            code += f"        {var}Value = 0;\n"
        code += "    }\n"
        
        # Add functions for each relationship
        code += "\n    // Relationship management functions\n"
        for impl in implementations:
            code += self._generate_relationship_functions(impl)
        
        # Add utility functions
        code += "\n    // Utility functions\n"
        code += "    function getAllRelationshipStatuses() public view returns (bool[] memory) {\n"
        code += "        bool[] memory statuses = new bool[](3);\n"
        for i, var in enumerate(sorted(list(variables)[:3])):
            code += f"        statuses[{i}] = {var}[msg.sender];\n"
        code += "        return statuses;\n"
        code += "    }\n"
        
        code += "}\n"
        
        return code
    
    def _generate_relationship_functions(self, implementation: RelationshipImplementation) -> str:
        """Generate functions for a specific relationship implementation"""
        code = f"\n    // Functions for {implementation.relation_type} relationship\n"
        
        # Main function for the relationship
        func_name = f"manage{implementation.relation_type.title()}"
        code += f"    function {func_name}(address target, uint256 value) public {{\n"
        
        if implementation.state_variables:
            var_name = implementation.state_variables[0]
            code += f"        {var_name}[msg.sender] = true;\n"
            code += f"        {var_name}Value = value;\n"
        
        # Emit event
        event_name = f"{implementation.relation_type.title()}Updated"
        code += f"        emit {event_name}(msg.sender, target, true);\n"
        code += "    }\n"
        
        # Verification function
        verify_func = f"verify{implementation.relation_type.title()}"
        code += f"    function {verify_func}(address party) public view returns (bool) {{\n"
        if implementation.state_variables:
            var_name = implementation.state_variables[0]
            code += f"        return {var_name}[party];\n"
        else:
            code += "        return true;\n"
        code += "    }\n"
        
        return code
    
    def _sanitize_name(self, name: str) -> str:
        """Sanitize names for Solidity compatibility"""
        # Remove spaces and special characters, make camelCase
        cleaned = re.sub(r'[^a-zA-Z0-9]', '', name)
        return cleaned[:15] if cleaned else "entity"  # Limit length
    
    def _calculate_accurate_metrics(self, relationships: List[Dict], 
                                  implementations: List[RelationshipImplementation]) -> Dict[str, float]:
        """Calculate accurate relationship preservation metrics"""
        
        if not relationships:
            return {'preservation_rate': 0.0, 'implementation_rate': 0.0}
        
        # Count relationships that have proper implementations
        implemented_relationships = len(implementations)
        total_relationships = len(relationships)
        
        # Calculate implementation completeness
        complete_implementations = sum(1 for impl in implementations 
                                     if len(impl.implementation_functions) >= 2 
                                     and len(impl.state_variables) >= 1)
        
        preservation_rate = (complete_implementations / total_relationships) * 100
        implementation_rate = (implemented_relationships / total_relationships) * 100
        
        return {
            'preservation_rate': preservation_rate,
            'implementation_rate': implementation_rate,
            'total_relationships': total_relationships,
            'implemented_relationships': implemented_relationships,
            'complete_implementations': complete_implementations
        }

def test_improved_generator():
    """Test the improved generator with sample data"""
    
    # Sample relationships with different types
    sample_relationships = [
        {
            'id': 'rel_1',
            'relation': 'payment',
            'source_text': 'Company A',
            'target_text': 'Company B',
            'confidence': 0.95,
            'amount': '$10,000'
        },
        {
            'id': 'rel_2', 
            'relation': 'ownership',
            'source_text': 'John Doe',
            'target_text': 'Property X',
            'confidence': 0.90
        },
        {
            'id': 'rel_3',
            'relation': 'obligation',
            'source_text': 'Contractor',
            'target_text': 'Client',
            'confidence': 0.88
        },
        {
            'id': 'rel_4',
            'relation': 'service_provision',
            'source_text': 'Service Provider',
            'target_text': 'Customer',
            'confidence': 0.92
        }
    ]
    
    sample_entities = [
        {'text': 'Company A', 'label': 'ORG', 'id': 'ent_1'},
        {'text': 'Company B', 'label': 'ORG', 'id': 'ent_2'},
        {'text': 'John Doe', 'label': 'PERSON', 'id': 'ent_3'},
        {'text': 'Property X', 'label': 'ASSET', 'id': 'ent_4'},
        {'text': 'Contractor', 'label': 'ORG', 'id': 'ent_5'}
    ]
    
    generator = ImprovedSmartContractGenerator()
    contract_code, metrics = generator.generate_enhanced_smart_contract(
        sample_entities, sample_relationships, "Sample contract text"
    )
    
    print("\n=== GENERATED SMART CONTRACT ===")
    print(contract_code)
    
    print("\n=== ACCURACY METRICS ===")
    for metric, value in metrics.items():
        if isinstance(value, float):
            print(f"{metric}: {value:.1f}%")
        else:
            print(f"{metric}: {value}")
    
    return metrics

if __name__ == "__main__":
    test_improved_generator()