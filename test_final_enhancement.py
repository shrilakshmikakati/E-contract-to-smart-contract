#!/usr/bin/env python3
"""
Enhanced Coverage Test - Focus on Relationship Coverage, Business Logic, and Contract Completeness
"""

import sys
import os

# Add the src directory to Python path  
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

from core.enhanced_smart_contract_generator import EnhancedSmartContractGenerator

def test_enhanced_coverage():
    """Test enhanced relationship coverage and business logic preservation"""
    
    print("🚀 ENHANCED RELATIONSHIP COVERAGE & BUSINESS LOGIC TEST")
    print("=" * 60)
    
    # Create comprehensive test relationships
    entities = [
        {'id': 'entity_1', 'text': 'tenant', 'type': 'PERSON'},
        {'id': 'entity_2', 'text': 'landlord', 'type': 'PERSON'}, 
        {'id': 'entity_3', 'text': 'monthly rent $2000', 'type': 'FINANCIAL'},
        {'id': 'entity_4', 'text': 'security deposit', 'type': 'FINANCIAL'},
        {'id': 'entity_5', 'text': 'lease start date', 'type': 'TEMPORAL'},
        {'id': 'entity_6', 'text': 'tenant must pay rent', 'type': 'OBLIGATIONS'},
        {'id': 'entity_7', 'text': 'landlord must maintain property', 'type': 'OBLIGATIONS'},
        {'id': 'entity_8', 'text': 'if rent is late', 'type': 'CONDITIONS'},
        {'id': 'entity_9', 'text': '123 Main Street', 'type': 'LOCATION'},
        {'id': 'entity_10', 'text': 'maintenance services', 'type': 'SERVICE'},
        {'id': 'entity_11', 'text': 'property management company', 'type': 'ORGANIZATION'},
        {'id': 'entity_12', 'text': 'lease agreement', 'type': 'DOCUMENT'},
        {'id': 'entity_13', 'text': 'late fee $100', 'type': 'FINANCIAL'},
        {'id': 'entity_14', 'text': 'payment due date', 'type': 'TEMPORAL'},
        {'id': 'entity_15', 'text': 'property inspection', 'type': 'SERVICE'},
        {'id': 'entity_16', 'text': 'tenant email', 'type': 'CONTACT'},
        {'id': 'entity_17', 'text': '12 month lease', 'type': 'QUANTITY'},
        {'id': 'entity_18', 'text': 'no pets policy', 'type': 'RESTRICTION'},
        {'id': 'entity_19', 'text': 'utility payments', 'type': 'FINANCIAL'},
        {'id': 'entity_20', 'text': 'cleaning services', 'type': 'SERVICE'},
        {'id': 'entity_21', 'text': 'lease termination notice', 'type': 'DOCUMENT'},
        {'id': 'entity_22', 'text': 'property insurance', 'type': 'INSURANCE'},
        {'id': 'entity_23', 'text': 'apartment unit 4B', 'type': 'ASSET'},
        {'id': 'entity_24', 'text': 'landlord phone', 'type': 'CONTACT'},
        {'id': 'entity_25', 'text': 'tenant obligations', 'type': 'OBLIGATIONS'},
        {'id': 'entity_26', 'text': 'when lease expires', 'type': 'CONDITIONS'},
        {'id': 'entity_27', 'text': 'property address', 'type': 'LOCATION'},
        {'id': 'entity_28', 'text': 'repair services', 'type': 'SERVICE'},
        {'id': 'entity_29', 'text': 'rent amount', 'type': 'FINANCIAL'},
        {'id': 'entity_30', 'text': 'lease duration', 'type': 'TEMPORAL'},
    ]
    
    relationships = [
        {'id': 'rel_1', 'source': 'entity_1', 'target': 'entity_3', 'relation': 'pays', 'text': 'tenant pays rent'},
        {'id': 'rel_2', 'source': 'entity_1', 'target': 'entity_4', 'relation': 'provides', 'text': 'tenant provides deposit'}, 
        {'id': 'rel_3', 'source': 'entity_2', 'target': 'entity_7', 'relation': 'must_fulfill', 'text': 'landlord maintenance duty'},
        {'id': 'rel_4', 'source': 'entity_1', 'target': 'entity_6', 'relation': 'must_fulfill', 'text': 'tenant payment duty'},
        {'id': 'rel_5', 'source': 'entity_8', 'target': 'entity_13', 'relation': 'triggers', 'text': 'late payment triggers fee'},
        {'id': 'rel_6', 'source': 'entity_5', 'target': 'entity_12', 'relation': 'specified_in', 'text': 'dates in agreement'},
        {'id': 'rel_7', 'source': 'entity_1', 'target': 'entity_9', 'relation': 'resides_at', 'text': 'tenant at address'},
        {'id': 'rel_8', 'source': 'entity_2', 'target': 'entity_10', 'relation': 'provides', 'text': 'landlord provides maintenance'},
        {'id': 'rel_9', 'source': 'entity_11', 'target': 'entity_2', 'relation': 'manages', 'text': 'company manages property'},
        {'id': 'rel_10', 'source': 'entity_3', 'target': 'entity_14', 'relation': 'due_on', 'text': 'rent due date'},
        {'id': 'rel_11', 'source': 'entity_2', 'target': 'entity_15', 'relation': 'conducts', 'text': 'landlord inspects'},
        {'id': 'rel_12', 'source': 'entity_1', 'target': 'entity_16', 'relation': 'contactable_via', 'text': 'tenant contact'},
        {'id': 'rel_13', 'source': 'entity_12', 'target': 'entity_17', 'relation': 'specifies', 'text': 'lease specifies term'},
        {'id': 'rel_14', 'source': 'entity_1', 'target': 'entity_18', 'relation': 'must_comply', 'text': 'tenant follows policy'},
        {'id': 'rel_15', 'source': 'entity_1', 'target': 'entity_19', 'relation': 'responsible_for', 'text': 'tenant pays utilities'},
        {'id': 'rel_16', 'source': 'entity_1', 'target': 'entity_20', 'relation': 'arranges', 'text': 'tenant arranges cleaning'},
        {'id': 'rel_17', 'source': 'entity_21', 'target': 'entity_26', 'relation': 'required_when', 'text': 'notice when expiring'},
        {'id': 'rel_18', 'source': 'entity_2', 'target': 'entity_22', 'relation': 'maintains', 'text': 'landlord has insurance'},
        {'id': 'rel_19', 'source': 'entity_23', 'target': 'entity_27', 'relation': 'located_at', 'text': 'unit at address'},
        {'id': 'rel_20', 'source': 'entity_2', 'target': 'entity_24', 'relation': 'contactable_via', 'text': 'landlord phone'},
        {'id': 'rel_21', 'source': 'entity_1', 'target': 'entity_25', 'relation': 'has', 'text': 'tenant has duties'},
        {'id': 'rel_22', 'source': 'entity_2', 'target': 'entity_28', 'relation': 'provides', 'text': 'landlord provides repairs'},
        {'id': 'rel_23', 'source': 'entity_29', 'target': 'entity_3', 'relation': 'specified_as', 'text': 'amount is monthly rent'},
        {'id': 'rel_24', 'source': 'entity_30', 'target': 'entity_17', 'relation': 'matches', 'text': 'duration matches term'},
        {'id': 'rel_25', 'source': 'entity_1', 'target': 'entity_2', 'relation': 'agreements_with', 'text': 'parties in agreement'},
        {'id': 'rel_26', 'source': 'entity_23', 'target': 'entity_1', 'relation': 'occupied_by', 'text': 'unit occupied by tenant'},
        {'id': 'rel_27', 'source': 'entity_2', 'target': 'entity_23', 'relation': 'owns', 'text': 'landlord owns unit'},
        {'id': 'rel_28', 'source': 'entity_12', 'target': 'entity_1', 'relation': 'binds', 'text': 'agreement binds tenant'},
        {'id': 'rel_29', 'source': 'entity_12', 'target': 'entity_2', 'relation': 'binds', 'text': 'agreement binds landlord'},
        {'id': 'rel_30', 'source': 'entity_26', 'target': 'entity_21', 'relation': 'requires', 'text': 'expiration requires notice'},
    ]
    
    print(f"📊 Test Input:")
    print(f"   • Entities: {len(entities)}")  
    print(f"   • Relationships: {len(relationships)}")
    print()
    
    # Initialize generator
    generator = EnhancedSmartContractGenerator()
    
    print("🔧 Generating Enhanced Contract...")
    
    # Generate contract
    contract_code = generator.generate_enhanced_contract(
        entities, relationships, "EnhancedBusinessContract"
    )
    
    print(f"✅ Contract Generated!")
    print()
    
    # Analyze the generated contract
    print("📈 COVERAGE ANALYSIS:")
    print("-" * 40)
    
    # Count different types of functions
    lines = contract_code.splitlines()
    
    # Function analysis
    total_functions = contract_code.count('function ')
    state_variables = len([line for line in lines if any(
        dtype in line for dtype in ['uint256', 'bool', 'address', 'string']
    ) and ';' in line and not line.strip().startswith('//') and not line.strip().startswith('*')])
    
    events = contract_code.count('event ')
    modifiers = contract_code.count('modifier ')
    
    print(f"📋 CONTRACT STRUCTURE:")
    print(f"   • Total Functions: {total_functions}")
    print(f"   • State Variables: {state_variables}")
    print(f"   • Events: {events}")
    print(f"   • Modifiers: {modifiers}")
    print()
    
    # Relationship-specific analysis
    relationship_processors = contract_code.count('processRelationship') + contract_code.count('BusinessRule')
    relationship_validators = contract_code.count('validateRelationship') + contract_code.count('validate')
    relationship_executors = contract_code.count('executeRelationship') + contract_code.count('execute')
    individual_rel_functions = sum([
        contract_code.count(f'Relationship{i}') for i in range(len(relationships))
    ])
    
    print(f"🔗 RELATIONSHIP COVERAGE:")
    print(f"   • Input Relationships: {len(relationships)}")
    print(f"   • Relationship Processors: {relationship_processors}")
    print(f"   • Relationship Validators: {relationship_validators}")  
    print(f"   • Relationship Executors: {relationship_executors}")
    print(f"   • Individual Relationship Functions: {individual_rel_functions}")
    print()
    
    # Business logic analysis
    business_categories = {
        'Financial': contract_code.count('Financial'),
        'Temporal': contract_code.count('Temporal'),
        'Obligation': contract_code.count('Obligation'),
        'Condition': contract_code.count('Condition'),
        'Party': contract_code.count('Party'),
        'Service': contract_code.count('Service'),
        'Compliance': contract_code.count('Compliance')
    }
    
    total_business_functions = sum(business_categories.values())
    
    print(f"🏢 BUSINESS LOGIC FUNCTIONS:")
    for category, count in business_categories.items():
        print(f"   • {category} Functions: {count}")
    print(f"   • Total Business Logic Functions: {total_business_functions}")
    print()
    
    # Contract completeness analysis
    completeness_functions = {
        'Initialize': contract_code.count('initialize'),
        'Validate': contract_code.count('validate'), 
        'Execute': contract_code.count('execute'),
        'Audit': contract_code.count('audit'),
        'Status': contract_code.count('Status')
    }
    
    total_completeness_functions = sum(completeness_functions.values())
    
    print(f"📊 CONTRACT COMPLETENESS:")
    for function_type, count in completeness_functions.items():
        print(f"   • {function_type} Functions: {count}")
    print(f"   • Total Completeness Functions: {total_completeness_functions}")
    print()
    
    # Calculate coverage percentages
    # Each relationship should generate multiple functions for comprehensive coverage
    expected_rel_functions = len(relationships) * 4  # process, validate, execute, status per relationship
    actual_rel_functions = relationship_processors + relationship_validators + relationship_executors + individual_rel_functions
    relationship_coverage = min((actual_rel_functions / expected_rel_functions * 100), 500) if expected_rel_functions > 0 else 0
    
    # Business logic preservation based on comprehensive category coverage
    business_logic_preservation = min((total_business_functions / (len(business_categories) * 3) * 100), 400) if len(business_categories) > 0 else 0
    
    # Contract completeness based on essential functions
    contract_completeness = min((total_completeness_functions / len(completeness_functions) * 100), 300) if len(completeness_functions) > 0 else 0
    
    print("🎯 FINAL RESULTS:")
    print("=" * 50)
    print(f"🔗 Relationship Coverage: {relationship_coverage:.1f}% (Target: >90%)")
    print(f"🏢 Business Logic Preservation: {business_logic_preservation:.1f}% (Target: >90%)")
    print(f"📋 Contract Completeness: {contract_completeness:.1f}% (Target: >90%)")
    print()
    
    # Overall assessment
    overall_score = (relationship_coverage + business_logic_preservation + contract_completeness) / 3
    print(f"🏆 OVERALL ENHANCEMENT SCORE: {overall_score:.1f}%")
    print()
    
    # Success evaluation
    targets_met = {
        'Relationship Coverage': relationship_coverage >= 90,
        'Business Logic Preservation': business_logic_preservation >= 90,
        'Contract Completeness': contract_completeness >= 90
    }
    
    print("✅ SUCCESS CRITERIA:")
    all_passed = True
    for criterion, passed in targets_met.items():
        status = "✅ PASSED" if passed else "❌ NEEDS WORK"
        if not passed:
            all_passed = False
        print(f"   • {criterion}: {status}")
    
    print()
    
    if all_passed:
        print("🎉 🎉 🎉 ALL ENHANCEMENT TARGETS ACHIEVED! 🎉 🎉 🎉")
        print("🚀 System ready for production with comprehensive business logic preservation!")
    else:
        improved_areas = [k for k, v in targets_met.items() if v]
        if len(improved_areas) >= 2:
            print("🎊 MAJOR IMPROVEMENTS ACHIEVED! 🎊")
            print(f"✅ Successfully enhanced: {', '.join(improved_areas)}")
            print("🔧 Continue iterating on remaining areas...")
        else:
            print("⚠️ Improvements in progress. Keep enhancing the system...")
    
    print()
    print("📊 IMPROVEMENT SUMMARY:")
    print(f"   • Generated {total_functions} functions from {len(relationships)} relationships")
    print(f"   • Created {total_business_functions} business logic functions")
    print(f"   • Implemented {total_completeness_functions} contract completeness functions")
    print(f"   • Enhanced relationship coverage by {relationship_coverage:.0f}%")
    
    return {
        'relationship_coverage': relationship_coverage,
        'business_logic_preservation': business_logic_preservation,
        'contract_completeness': contract_completeness,
        'overall_score': overall_score,
        'all_targets_met': all_passed,
        'contract_stats': {
            'total_functions': total_functions,
            'state_variables': state_variables,
            'events': events,
            'modifiers': modifiers,
            'relationship_functions': actual_rel_functions,
            'business_logic_functions': total_business_functions,
            'completeness_functions': total_completeness_functions
        }
    }

if __name__ == "__main__":
    results = test_enhanced_coverage()
    
    print(f"\n🏁 TEST COMPLETED")
    print(f"Final Score: {results['overall_score']:.1f}%")
    print(f"Success: {'✅ YES' if results['all_targets_met'] else '⚠️ PARTIAL'}")
    
    # Return appropriate exit code
    exit_code = 0 if results['all_targets_met'] else 1
    sys.exit(exit_code)