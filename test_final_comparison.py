#!/usr/bin/env python3
"""
Test the final enhanced comparison system
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_final_comparison():
    """Test the final enhanced comparison and show improvements"""
    
    print("=== TESTING FINAL ENHANCED COMPARISON ===\n")
    
    # Sample complex e-contract with multiple business elements
    complex_econtract = """
    ENHANCED RENTAL AGREEMENT
    
    This Rental Agreement ("Agreement") is entered into between:
    - ABC Property Management LLC ("Landlord") 
    - John Smith ("Tenant")
    
    TERMS AND CONDITIONS:
    1. Property: 123 Main Street, Apartment 2A
    2. Monthly Rent: $2,500 per month
    3. Security Deposit: $5,000 due upon signing
    4. Lease Term: 12 months starting January 1, 2024
    5. Payment Due: Monthly rent due by the 1st of each month
    
    OBLIGATIONS:
    - Tenant must pay rent on time each month
    - Tenant shall maintain the property in good condition
    - Landlord must provide 24-hour notice before entry
    - Landlord is responsible for major repairs and maintenance
    
    CONDITIONS:
    - If rent is more than 10 days late, landlord may charge late fees
    - Either party may terminate with 30 days written notice
    - Deposit will be returned within 30 days after move-out if no damages
    
    FINANCIAL DETAILS:
    - Late fee: $100 after 10 days
    - Pet fee: $500 (if applicable)
    - Utilities: Tenant responsible for electric and gas
    
    This contract becomes active upon signing by both parties and payment of first month's rent and security deposit.
    """
    
    try:
        # Import the enhanced modules
        from core.econtract_processor import EContractProcessor
        from core.enhanced_smart_contract_generator import EnhancedSmartContractGenerator
        from core.comparator import KnowledgeGraphComparator
        
        print("✅ Successfully imported enhanced modules\n")
        
        # Process e-contract
        print("📄 Processing enhanced e-contract...")
        econtract_processor = EContractProcessor()
        econtract_kg = econtract_processor.process_contract(complex_econtract)
        print(f"   Extracted: {len(econtract_kg.entities)} entities, {len(econtract_kg.relationships)} relationships")
        
        # Generate enhanced smart contract
        print("⚙️  Generating enhanced smart contract...")
        enhanced_generator = EnhancedSmartContractGenerator()
        
        # Convert KG entities and relationships to lists
        entities_list = list(econtract_kg.entities.values())
        relationships_list = list(econtract_kg.relationships.values())
        
        smart_contract_code = enhanced_generator.generate_enhanced_contract(
            entities_list, 
            relationships_list, 
            "EnhancedRentalContract"
        )
        
        print(f"   Generated smart contract: {len(smart_contract_code.split('function'))-1} functions")
        
        # Create smart contract KG from generated code
        print("🔧 Creating smart contract knowledge graph...")
        smartcontract_kg = econtract_processor.process_contract(smart_contract_code)
        print(f"   Smart contract KG: {len(smartcontract_kg.entities)} entities, {len(smartcontract_kg.relationships)} relationships")
        
        # Run enhanced comparison
        print("\n🔍 RUNNING ENHANCED COMPARISON:")
        comparator = KnowledgeGraphComparator()
        
        result = comparator.compare_knowledge_graphs(
            econtract_kg, 
            smartcontract_kg,
            comparison_id="enhanced_validation"
        )
        
        print("\n" + "="*80)
        print("🎯 ENHANCED COMPARISON RESULTS")
        print("="*80)
        
        # Debug: Show actual result structure
        print(f"\n🔍 DEBUG - Available keys: {list(result.keys())}")
        
        # Display main metrics with correct keys
        print(f"\n📊 ACCURACY METRICS:")
        print(f"   Overall Similarity: {result.get('overall_similarity_score', 0):.1%}")
        print(f"   Entity Preservation: {result.get('entity_preservation_percentage', 0):.1%}")
        print(f"   Relationship Preservation: {result.get('relationship_preservation_percentage', 0):.1%}")
        print(f"   Entity Matches: {result.get('entity_matches', 0)}")
        print(f"   Relationship Matches: {result.get('relationship_matches', 0)}")
        
        # Show accuracy analysis if available
        if 'accuracy_analysis' in result:
            acc_analysis = result['accuracy_analysis']
            print(f"   Accuracy Score: {acc_analysis.get('accuracy_score', 0):.1%}")
            print(f"   Business Logic Score: {acc_analysis.get('business_logic_preservation', 0):.1%}")
        
        print(f"\n🎨 DEPLOYMENT READINESS:")
        compliance = result.get('compliance_assessment', {})
        print(f"   Compliance Score: {compliance.get('overall_score', 0):.1%}")
        print(f"   Deployment Ready: {'✅ Yes' if compliance.get('deployment_ready', False) else '❌ No'}")
        
        # Show detailed breakdown
        if 'detailed_analysis' in result:
            analysis = result['detailed_analysis']
            print(f"\n📈 DETAILED BREAKDOWN:")
            print(f"   Entities Found: {analysis.get('entities_found', 0)}/{analysis.get('total_entities', 0)}")
            print(f"   Relationships Found: {analysis.get('relationships_found', 0)}/{analysis.get('total_relationships', 0)}")
            print(f"   Business Rules Preserved: {analysis.get('business_rules_preserved', 0)}/{analysis.get('total_business_rules', 0)}")
        
        # Show recommendations
        if result.get('recommendations'):
            print(f"\n💡 IMPROVEMENT RECOMMENDATIONS:")
            recs = result['recommendations'][:5] if isinstance(result['recommendations'], list) else [result['recommendations']]
            for i, rec in enumerate(recs, 1):
                print(f"   {i}. {rec}")
        
        print(f"\n🏆 COMPARISON SUMMARY:")
        print("="*50)
        
        overall_score = result.get('overall_similarity_score', 0)
        accuracy_score = result.get('accuracy_analysis', {}).get('accuracy_score', overall_score)
        
        if accuracy_score >= 0.70:
            print("✅ EXCELLENT: System meets deployment readiness criteria!")
        elif accuracy_score >= 0.50:
            print("⚠️ GOOD: System shows significant improvement but needs refinement")
        else:
            print("❌ NEEDS WORK: System requires further enhancement")
            
        print(f"✅ Overall similarity: {overall_score:.1%}")
        print(f"✅ Entity preservation: {result.get('entity_preservation_percentage', 0):.1%}")
        print(f"✅ Relationship preservation: {result.get('relationship_preservation_percentage', 0):.1%}")
        print(f"✅ Deployment readiness: {compliance.get('deployment_ready', 'Unknown')}")
        
        return True
        
    except ImportError as e:
        print(f"❌ Import error: {e}")
        return False
    except Exception as e:
        import traceback
        print(f"❌ Error during testing: {e}")
        print("Full traceback:")
        traceback.print_exc()
        return False

if __name__ == "__main__":
    test_final_comparison()