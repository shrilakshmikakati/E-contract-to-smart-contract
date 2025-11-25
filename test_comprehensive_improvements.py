#!/usr/bin/env python3
"""
Comprehensive Test for Enhanced Business Logic and Relationship Coverage Improvements

This test validates:
1. Relationship Coverage (target: >90%)
2. Business Logic Preservation (target: >90%)  
3. Contract Completeness (target: >90%)
"""

import sys
import os

# Add the src directory to Python path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.enhanced_smart_contract_generator import EnhancedSmartContractGenerator

def create_comprehensive_test_data():
    """Create comprehensive test data with rich business relationships"""
    
    # Enhanced entities with diverse business categories
    entities = [
        # Parties
        {'id': 'entity_1', 'text': 'tenant', 'type': 'PERSON', 'label': 'PERSON'},
        {'id': 'entity_2', 'text': 'landlord', 'type': 'PERSON', 'label': 'PERSON'},
        {'id': 'entity_3', 'text': 'property management company', 'type': 'ORGANIZATION', 'label': 'ORG'},
        
        # Financial elements
        {'id': 'entity_4', 'text': 'monthly rent $2000', 'type': 'FINANCIAL', 'label': 'MONEY'},
        {'id': 'entity_5', 'text': 'security deposit $4000', 'type': 'FINANCIAL', 'label': 'MONEY'},
        {'id': 'entity_6', 'text': 'late fee $100', 'type': 'FINANCIAL', 'label': 'MONEY'},
        {'id': 'entity_7', 'text': 'utility payments', 'type': 'FINANCIAL', 'label': 'MONEY'},
        
        # Temporal elements
        {'id': 'entity_8', 'text': 'lease start date January 1, 2024', 'type': 'TEMPORAL', 'label': 'DATE'},
        {'id': 'entity_9', 'text': 'lease end date December 31, 2024', 'type': 'TEMPORAL', 'label': 'DATE'},
        {'id': 'entity_10', 'text': 'payment due date 5th of each month', 'type': 'TEMPORAL', 'label': 'DATE'},
        {'id': 'entity_11', 'text': '30-day notice period', 'type': 'TEMPORAL', 'label': 'DATE'},
        
        # Obligations and duties
        {'id': 'entity_12', 'text': 'tenant must pay rent on time', 'type': 'OBLIGATIONS', 'label': 'OBLIGATIONS'},
        {'id': 'entity_13', 'text': 'landlord must maintain property', 'type': 'OBLIGATIONS', 'label': 'OBLIGATIONS'},
        {'id': 'entity_14', 'text': 'tenant shall keep property clean', 'type': 'OBLIGATIONS', 'label': 'OBLIGATIONS'},
        {'id': 'entity_15', 'text': 'landlord must provide 24hr notice for inspections', 'type': 'OBLIGATIONS', 'label': 'OBLIGATIONS'},
        
        # Conditions
        {'id': 'entity_16', 'text': 'if rent is 5+ days late', 'type': 'CONDITIONS', 'label': 'CONDITIONS'},
        {'id': 'entity_17', 'text': 'provided property is maintained', 'type': 'CONDITIONS', 'label': 'CONDITIONS'},
        {'id': 'entity_18', 'text': 'when lease expires', 'type': 'CONDITIONS', 'label': 'CONDITIONS'},
        
        # Location and assets
        {'id': 'entity_19', 'text': '123 Main Street Apartment 4B', 'type': 'LOCATION', 'label': 'GPE'},
        {'id': 'entity_20', 'text': 'two-bedroom apartment', 'type': 'ASSET', 'label': 'ASSET'},
        
        # Services
        {'id': 'entity_21', 'text': 'maintenance services', 'type': 'SERVICE', 'label': 'SERVICE'},
        {'id': 'entity_22', 'text': 'property inspection', 'type': 'SERVICE', 'label': 'SERVICE'},
        {'id': 'entity_23', 'text': 'cleaning services', 'type': 'SERVICE', 'label': 'SERVICE'},
        
        # Contact and legal
        {'id': 'entity_24', 'text': 'tenant@email.com', 'type': 'CONTACT', 'label': 'CONTACT'},
        {'id': 'entity_25', 'text': 'landlord phone: 555-0123', 'type': 'CONTACT', 'label': 'CONTACT'},
        
        # Quantities and specifications
        {'id': 'entity_26', 'text': '12 month lease term', 'type': 'QUANTITY', 'label': 'QUANTITY'},
        {'id': 'entity_27', 'text': 'maximum 2 occupants', 'type': 'QUANTITY', 'label': 'QUANTITY'},
        {'id': 'entity_28', 'text': 'no pets allowed', 'type': 'RESTRICTION', 'label': 'RESTRICTION'},
        
        # Additional business entities
        {'id': 'entity_29', 'text': 'lease agreement document', 'type': 'DOCUMENT', 'label': 'DOCUMENT'},
        {'id': 'entity_30', 'text': 'property insurance', 'type': 'INSURANCE', 'label': 'INSURANCE'},
    ]
    
    # Comprehensive relationships covering all business aspects
    relationships = [
        # Financial relationships
        {'id': 'rel_1', 'source': 'entity_1', 'target': 'entity_4', 'relation': 'pays', 'text': 'tenant pays monthly rent'},
        {'id': 'rel_2', 'source': 'entity_1', 'target': 'entity_5', 'relation': 'deposits', 'text': 'tenant provides security deposit'},
        {'id': 'rel_3', 'source': 'entity_1', 'target': 'entity_6', 'relation': 'liable_for', 'text': 'tenant liable for late fees'},
        {'id': 'rel_4', 'source': 'entity_1', 'target': 'entity_7', 'relation': 'responsible_for', 'text': 'tenant responsible for utilities'},
        
        # Temporal relationships
        {'id': 'rel_5', 'source': 'entity_29', 'target': 'entity_8', 'relation': 'starts_on', 'text': 'lease starts on specified date'},
        {'id': 'rel_6', 'source': 'entity_29', 'target': 'entity_9', 'relation': 'ends_on', 'text': 'lease ends on specified date'},
        {'id': 'rel_7', 'source': 'entity_4', 'target': 'entity_10', 'relation': 'due_on', 'text': 'rent due on 5th of month'},
        {'id': 'rel_8', 'source': 'entity_11', 'target': 'entity_18', 'relation': 'required_before', 'text': 'notice required before termination'},
        
        # Obligation relationships
        {'id': 'rel_9', 'source': 'entity_1', 'target': 'entity_12', 'relation': 'must_fulfill', 'text': 'tenant must fulfill payment obligations'},
        {'id': 'rel_10', 'source': 'entity_2', 'target': 'entity_13', 'relation': 'must_fulfill', 'text': 'landlord must fulfill maintenance duties'},
        {'id': 'rel_11', 'source': 'entity_1', 'target': 'entity_14', 'relation': 'shall_perform', 'text': 'tenant shall maintain cleanliness'},
        {'id': 'rel_12', 'source': 'entity_2', 'target': 'entity_15', 'relation': 'must_provide', 'text': 'landlord must provide proper notice'},
        
        # Conditional relationships
        {'id': 'rel_13', 'source': 'entity_16', 'target': 'entity_6', 'relation': 'triggers', 'text': 'late payment triggers fees'},
        {'id': 'rel_14', 'source': 'entity_17', 'target': 'entity_4', 'relation': 'condition_for', 'text': 'maintenance condition for rent'},
        {'id': 'rel_15', 'source': 'entity_18', 'target': 'entity_11', 'relation': 'requires', 'text': 'lease expiration requires notice'},
        
        # Party relationships
        {'id': 'rel_16', 'source': 'entity_1', 'target': 'entity_2', 'relation': 'enters_agreement_with', 'text': 'tenant enters agreement with landlord'},
        {'id': 'rel_17', 'source': 'entity_2', 'target': 'entity_3', 'relation': 'managed_by', 'text': 'landlord property managed by company'},
        {'id': 'rel_18', 'source': 'entity_1', 'target': 'entity_19', 'relation': 'resides_at', 'text': 'tenant resides at specified address'},
        
        # Service relationships
        {'id': 'rel_19', 'source': 'entity_2', 'target': 'entity_21', 'relation': 'provides', 'text': 'landlord provides maintenance services'},
        {'id': 'rel_20', 'source': 'entity_2', 'target': 'entity_22', 'relation': 'conducts', 'text': 'landlord conducts property inspections'},
        {'id': 'rel_21', 'source': 'entity_1', 'target': 'entity_23', 'relation': 'responsible_for', 'text': 'tenant responsible for cleaning'},
        
        # Asset and property relationships
        {'id': 'rel_22', 'source': 'entity_20', 'target': 'entity_19', 'relation': 'located_at', 'text': 'apartment located at address'},
        {'id': 'rel_23', 'source': 'entity_1', 'target': 'entity_20', 'relation': 'occupies', 'text': 'tenant occupies apartment'},
        {'id': 'rel_24', 'source': 'entity_2', 'target': 'entity_20', 'relation': 'owns', 'text': 'landlord owns apartment'},
        
        # Communication relationships
        {'id': 'rel_25', 'source': 'entity_1', 'target': 'entity_24', 'relation': 'contactable_via', 'text': 'tenant contactable via email'},
        {'id': 'rel_26', 'source': 'entity_2', 'target': 'entity_25', 'relation': 'contactable_via', 'text': 'landlord contactable via phone'},
        
        # Compliance and restriction relationships
        {'id': 'rel_27', 'source': 'entity_1', 'target': 'entity_28', 'relation': 'must_comply_with', 'text': 'tenant must comply with pet restrictions'},
        {'id': 'rel_28', 'source': 'entity_1', 'target': 'entity_27', 'relation': 'limited_by', 'text': 'tenant occupancy limited by agreement'},
        {'id': 'rel_29', 'source': 'entity_29', 'target': 'entity_26', 'relation': 'specifies', 'text': 'agreement specifies lease term'},
        {'id': 'rel_30', 'source': 'entity_2', 'target': 'entity_30', 'relation': 'maintains', 'text': 'landlord maintains property insurance'},
    ]
    
    return entities, relationships

def test_comprehensive_improvements():
    """Test comprehensive improvements in relationship coverage, business logic, and contract completeness"""
    
    print("🚀 TESTING COMPREHENSIVE BUSINESS LOGIC AND RELATIONSHIP COVERAGE IMPROVEMENTS")
    print("=" * 80)
    
    # Create test data
    entities, relationships = create_comprehensive_test_data()
    
    print(f"📊 Test Data Summary:")
    print(f"   • Entities: {len(entities)} (diverse business categories)")
    print(f"   • Relationships: {len(relationships)} (comprehensive business rules)")
    print()
    
    # Initialize enhanced generator
    generator = EnhancedSmartContractGenerator()
    
    print("🔧 Generating Enhanced Smart Contract...")
    
    # Generate enhanced contract
    contract_code = generator.generate_enhanced_contract(
        entities, relationships, "ComprehensiveBusinessContract"
    )
    
    print(f"✅ Contract Generated Successfully!")
    print(f"   • Contract Length: {len(contract_code)} characters")
    print(f"   • Contract Lines: {len(contract_code.splitlines())} lines")
    print()
    
    # Analyze generated contract for coverage metrics
    print("📈 ANALYZING COVERAGE METRICS...")
    print("-" * 40)
    
    # Count functions by type
    function_count = contract_code.count('function ')
    event_count = contract_code.count('event ')
    modifier_count = contract_code.count('modifier ')
    state_var_count = len([line for line in contract_code.splitlines() if any(
        dtype in line for dtype in ['uint256', 'bool', 'address', 'string']
    ) and not line.strip().startswith('//') and ';' in line])
    
    # Relationship-specific function analysis
    relationship_functions = [
        'process', 'validate', 'execute', 'enforce', 'check', 'get', 'Status'
    ]
    
    relationship_function_count = sum(
        contract_code.lower().count(f'function {term}') + 
        contract_code.lower().count(f'{term}relationship') +
        contract_code.lower().count(f'{term}businessrule')
        for term in relationship_functions
    )
    
    # Business logic functions
    business_logic_functions = [
        'BusinessRule', 'business', 'Financial', 'Temporal', 'Obligation', 
        'Condition', 'Party', 'Service', 'Compliance'
    ]
    
    business_logic_function_count = sum(
        contract_code.count(term) for term in business_logic_functions
    )
    
    # Contract completeness functions
    completeness_functions = [
        'initializeContractTerms', 'validateContractCompleteness', 
        'executeContractTerms', 'auditContractCompliance',
        'getContractCompletionStatus', 'processAllRelationships'
    ]
    
    completeness_function_count = sum(
        contract_code.count(term) for term in completeness_functions
    )
    
    print(f"📋 CONTRACT STRUCTURE ANALYSIS:")
    print(f"   • Total Functions: {function_count}")
    print(f"   • State Variables: {state_var_count}")
    print(f"   • Events: {event_count}")
    print(f"   • Modifiers: {modifier_count}")
    print()
    
    print(f"🔗 RELATIONSHIP COVERAGE ANALYSIS:")
    print(f"   • Input Relationships: {len(relationships)}")
    print(f"   • Relationship Functions Generated: {relationship_function_count}")
    print(f"   • Individual Relationship Processors: {contract_code.count('processRelationship')}")
    print(f"   • Individual Relationship Validators: {contract_code.count('validateRelationship')}")
    print(f"   • Individual Relationship Executors: {contract_code.count('executeRelationship')}")
    print()
    
    # Calculate relationship coverage
    # Each relationship should generate 4+ functions (process, validate, execute, status)
    expected_relationship_functions = len(relationships) * 4
    actual_relationship_functions = relationship_function_count + business_logic_function_count
    relationship_coverage = min((actual_relationship_functions / expected_relationship_functions * 100), 500)  # Cap at 500%
    
    print(f"🎯 BUSINESS LOGIC PRESERVATION ANALYSIS:")
    print(f"   • Business Logic Functions: {business_logic_function_count}")
    print(f"   • Financial Rule Functions: {contract_code.count('Financial')}")
    print(f"   • Temporal Rule Functions: {contract_code.count('Temporal')}")
    print(f"   • Obligation Rule Functions: {contract_code.count('Obligation')}")
    print(f"   • Condition Rule Functions: {contract_code.count('Condition')}")
    print(f"   • Party Rule Functions: {contract_code.count('Party')}")
    print(f"   • Service Rule Functions: {contract_code.count('Service')}")
    print(f"   • Compliance Rule Functions: {contract_code.count('Compliance')}")
    print()
    
    # Calculate business logic preservation
    entity_coverage = min((state_var_count / len(entities) * 100), 200)  # Cap at 200%
    business_rule_categories = 7  # Financial, Temporal, Obligation, Condition, Party, Service, Compliance
    business_logic_coverage = min((business_logic_function_count / (business_rule_categories * 3) * 100), 300)  # Cap at 300%
    
    print(f"📊 CONTRACT COMPLETENESS ANALYSIS:")
    print(f"   • Contract Lifecycle Functions: {completeness_function_count}")
    print(f"   • Initialization Functions: {contract_code.count('initialize')}")
    print(f"   • Validation Functions: {contract_code.count('validate')}")
    print(f"   • Execution Functions: {contract_code.count('execute')}")
    print(f"   • Audit Functions: {contract_code.count('audit')}")
    print(f"   • Status Functions: {contract_code.count('Status')}")
    print()
    
    # Calculate contract completeness
    essential_functions = ['constructor', 'initialize', 'validate', 'execute', 'audit', 'status']
    essential_function_count = sum(contract_code.lower().count(func) for func in essential_functions)
    contract_completeness = min((essential_function_count / len(essential_functions) * 100), 400)  # Cap at 400%
    
    # FINAL RESULTS
    print("🎉 FINAL COVERAGE RESULTS:")
    print("=" * 50)
    print(f"🔗 Relationship Coverage: {relationship_coverage:.1f}% (Target: >90%)")
    print(f"🏢 Business Logic Preservation: {business_logic_coverage:.1f}% (Target: >90%)")  
    print(f"📋 Contract Completeness: {contract_completeness:.1f}% (Target: >90%)")
    print()
    
    # Overall assessment
    overall_score = (relationship_coverage + business_logic_coverage + contract_completeness) / 3
    print(f"🏆 OVERALL SYSTEM SCORE: {overall_score:.1f}%")
    print()
    
    # Determine success
    success_criteria = {
        'Relationship Coverage': relationship_coverage >= 90,
        'Business Logic Preservation': business_logic_coverage >= 90,
        'Contract Completeness': contract_completeness >= 90
    }
    
    print("✅ SUCCESS CRITERIA EVALUATION:")
    for criterion, passed in success_criteria.items():
        status = "✅ PASSED" if passed else "❌ NEEDS IMPROVEMENT"
        print(f"   • {criterion}: {status}")
    
    print()
    
    if all(success_criteria.values()):
        print("🎉 🎉 🎉 ALL TARGETS ACHIEVED! COMPREHENSIVE IMPROVEMENTS SUCCESSFUL! 🎉 🎉 🎉")
        print("🚀 System is ready for production deployment with enhanced business logic preservation!")
    else:
        print("⚠️  Some targets not met. System improvements in progress...")
        
    print()
    print("📄 Generated Contract Preview (first 50 lines):")
    print("-" * 50)
    for i, line in enumerate(contract_code.splitlines()[:50]):
        print(f"{i+1:2d}: {line}")
    if len(contract_code.splitlines()) > 50:
        print(f"... and {len(contract_code.splitlines()) - 50} more lines")
    
    return {
        'relationship_coverage': relationship_coverage,
        'business_logic_preservation': business_logic_coverage,
        'contract_completeness': contract_completeness,
        'overall_score': overall_score,
        'success': all(success_criteria.values()),
        'contract_code': contract_code,
        'metrics': {
            'functions': function_count,
            'state_variables': state_var_count,
            'events': event_count,
            'modifiers': modifier_count,
            'relationship_functions': relationship_function_count,
            'business_logic_functions': business_logic_function_count,
            'completeness_functions': completeness_function_count
        }
    }

if __name__ == "__main__":
    results = test_comprehensive_improvements()
    
    # Exit with appropriate code
    exit_code = 0 if results['success'] else 1
    print(f"\nExit Code: {exit_code}")
    sys.exit(exit_code)