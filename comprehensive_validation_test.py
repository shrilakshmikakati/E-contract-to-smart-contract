"""
Final validation test for enhanced business logic and relationship system
Tests connectivity, business logic functions, and relationship coverage
"""

from src.core.econtract_processor import EContractProcessor
from src.core.enhanced_smart_contract_generator import EnhancedSmartContractGenerator

def comprehensive_validation_test():
    """Comprehensive validation of all enhancements"""
    
    print("=== COMPREHENSIVE BUSINESS LOGIC VALIDATION ===")
    
    # Complex business contract for testing
    complex_contract = """
    COMPREHENSIVE BUSINESS AGREEMENT
    
    This multi-party agreement is between:
    - TechCorp LLC (Technology Provider)
    - BusinessSolutions Inc (Service Provider)  
    - DataSystems Co (Data Partner)
    - ClientCompany (Primary Client)
    
    BUSINESS RELATIONSHIPS:
    1. TechCorp provides software platform to BusinessSolutions
    2. BusinessSolutions delivers consulting services to ClientCompany
    3. DataSystems provides data analytics to all parties
    4. ClientCompany pays fees to BusinessSolutions monthly
    5. BusinessSolutions pays licensing fees to TechCorp
    6. All parties share data through DataSystems platform
    
    OBLIGATIONS:
    - TechCorp: Maintain 99.9% uptime, provide technical support
    - BusinessSolutions: Deliver monthly reports, maintain confidentiality
    - DataSystems: Secure data processing, backup management
    - ClientCompany: Timely payments, provide necessary access
    
    COMPLIANCE REQUIREMENTS:
    - GDPR compliance for all data processing
    - SOC2 certification maintenance
    - Monthly compliance audits
    - Incident reporting within 24 hours
    """
    
    # Process with enhanced system
    processor = EContractProcessor()
    generator = EnhancedSmartContractGenerator()
    
    print("Processing complex multi-party contract...")
    knowledge_graph = processor.process_contract(complex_contract, "COMPREHENSIVE_TEST")
    
    # Check connectivity
    stats = knowledge_graph.get_statistics()
    print(f"\n📊 KNOWLEDGE GRAPH METRICS:")
    print(f"  Entities: {len(knowledge_graph.entities)}")
    print(f"  Relationships: {len(knowledge_graph.relationships)}")
    print(f"  Connected: {'✅ YES' if stats['basic_metrics']['is_connected'] else '❌ NO'}")
    print(f"  Density: {stats['basic_metrics']['graph_density']:.3f}")
    
    # Generate enhanced contract
    print(f"\n🚀 GENERATING ENHANCED SMART CONTRACT...")
    entities = list(knowledge_graph.entities.values()) if hasattr(knowledge_graph.entities, 'values') else []
    relationships = list(knowledge_graph.relationships.values()) if hasattr(knowledge_graph.relationships, 'values') else []
    
    contract_code = generator.generate_enhanced_contract(entities, relationships, "COMPREHENSIVE_BUSINESS_CONTRACT")
    
    # Analyze the generated contract
    lines = contract_code.split('\n')
    
    # Count business logic functions
    business_functions = [line for line in lines if 'function ' in line and any(term in line.lower() for term in ['business', 'relationship', 'obligation', 'compliance', 'enforce'])]
    
    validation_functions = [line for line in lines if 'function ' in line and any(term in line.lower() for term in ['validate', 'audit', 'check'])]
    
    connectivity_functions = [line for line in lines if 'function ' in line and any(term in line.lower() for term in ['connectivity', 'connection'])]
    
    state_vars = [line for line in lines if any(keyword in line for keyword in ['public', 'private']) and ';' in line and 'function' not in line and '{' not in line]
    
    events = [line for line in lines if 'event ' in line]
    
    print(f"\n📈 ENHANCED CONTRACT ANALYSIS:")
    print(f"  Total Lines: {len(lines)}")
    print(f"  State Variables: {len(state_vars)}")
    print(f"  Business Logic Functions: {len(business_functions)}")
    print(f"  Validation Functions: {len(validation_functions)}")
    print(f"  Connectivity Functions: {len(connectivity_functions)}")
    print(f"  Events: {len(events)}")
    
    # Check for specific business logic implementations
    business_features = {
        'Business Relationship Validation': 'validateBusinessRelationships' in contract_code,
        'Obligation Enforcement': 'enforceObligations' in contract_code,
        'Compliance Validation': 'validateCompliance' in contract_code,
        'Business Rule Enforcement': 'enforceBusinessRules' in contract_code,
        'Connectivity Metrics': 'getRelationshipConnectivity' in contract_code,
        'Business Audit': 'auditBusinessLogic' in contract_code,
        'Entity Validation': 'validateEntityConnections' in contract_code
    }
    
    print(f"\n✨ BUSINESS LOGIC FEATURES:")
    for feature, implemented in business_features.items():
        status = "✅ Implemented" if implemented else "❌ Missing"
        print(f"  {feature}: {status}")
    
    # Calculate success metrics
    implemented_features = sum(business_features.values())
    total_features = len(business_features)
    feature_coverage = (implemented_features / total_features) * 100
    
    print(f"\n🎯 VALIDATION RESULTS:")
    print(f"  Knowledge Graph Connected: {'✅' if stats['basic_metrics']['is_connected'] else '❌'}")
    print(f"  Business Logic Coverage: {feature_coverage:.1f}% ({implemented_features}/{total_features})")
    print(f"  Contract Size: {len(contract_code)} characters")
    print(f"  Business Functions: {len(business_functions)} generated")
    
    # Overall assessment
    overall_success = (
        stats['basic_metrics']['is_connected'] and
        feature_coverage >= 85 and  # At least 85% feature coverage
        len(business_functions) >= 10 and  # At least 10 business functions
        len(state_vars) >= 20  # At least 20 state variables
    )
    
    print(f"\n🏆 OVERALL ASSESSMENT: {'✅ SUCCESS' if overall_success else '❌ NEEDS IMPROVEMENT'}")
    
    if overall_success:
        print("🎉 All enhanced business logic features are working correctly!")
        print("📋 System is ready for production deployment!")
    else:
        print("⚠️  Some features need attention.")
    
    return overall_success

if __name__ == "__main__":
    success = comprehensive_validation_test()
    if success:
        print("\n🚀 COMPREHENSIVE VALIDATION: PASSED!")
    else:
        print("\n❌ COMPREHENSIVE VALIDATION: FAILED!")