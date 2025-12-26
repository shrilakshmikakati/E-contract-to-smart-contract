#!/usr/bin/env python3
"""
Test the optimized comparison system on real project data with GUI display format
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_real_contract_with_gui_display():
    """Test on real project data and display as GUI would show"""
    print("🧪 TESTING ULTRA-OPTIMIZED SYSTEM ON REAL PROJECT DATA")
    print("=" * 80)
    
    try:
        from src.core.econtract_processor import EContractProcessor
        from src.core.smartcontract_processor import SmartContractProcessor
        from src.core.comparator import ContractComparator
        
        # Load real contracts
        econtract_file = os.path.join("data", "sample_contracts", "rental_agreement_complete.txt")
        smartcontract_file = os.path.join("data", "sample_smart_contracts", "rental_agreement_fixed.sol")
        
        if not os.path.exists(econtract_file):
            print(f"❌ E-contract file not found: {econtract_file}")
            return False
            
        if not os.path.exists(smartcontract_file):
            print(f"❌ Smart contract file not found: {smartcontract_file}")
            return False
        
        # Read files
        with open(econtract_file, 'r', encoding='utf-8') as f:
            econtract_text = f.read()
        
        with open(smartcontract_file, 'r', encoding='utf-8') as f:
            smartcontract_code = f.read()
        
        print(f"📄 E-contract size: {len(econtract_text)} characters")
        print(f"📄 Smart contract size: {len(smartcontract_code)} characters\n")
        
        # Process contracts
        print("🔄 Processing e-contract...")
        econtract_processor = EContractProcessor()
        e_kg = econtract_processor.process_contract(econtract_text, "real_econtract")
        
        print(f"   ✅ Extracted {len(e_kg.entities)} entities and {len(e_kg.relationships)} relationships")
        
        print("🔄 Processing smart contract...")
        smartcontract_processor = SmartContractProcessor()
        s_kg = smartcontract_processor.process_contract(smartcontract_code, "real_smartcontract")
        
        print(f"   ✅ Extracted {len(s_kg.entities)} entities and {len(s_kg.relationships)} relationships\n")
        
        # Run comparison
        print("🚀 Running ULTRA-OPTIMIZED comparison...")
        comparator = ContractComparator()
        comparison_results = comparator.compare_knowledge_graphs(e_kg, s_kg, "real_project_test")
        
        # Extract results as GUI would display
        print("\n" + "=" * 80)
        print("📊 REAL PROJECT TEST RESULTS (AS DISPLAYED IN GUI):")
        print("=" * 80 + "\n")
        
        summary = comparison_results.get('summary', {})
        bidirectional_metrics = comparison_results.get('bidirectional_metrics', {})
        compliance = comparison_results.get('compliance_assessment', {})
        bd_compliance = bidirectional_metrics.get('bidirectional_compliance', {})
        
        # Comparison Summary
        print("COMPARISON SUMMARY:")
        overall_similarity = summary.get('overall_similarity_score', 0)
        print(f"Overall Similarity Score: {overall_similarity:.3f}")
        
        entity_matches_e_to_s = summary.get('total_entity_matches_e_to_s', 0)
        entity_matches_s_to_e = summary.get('total_entity_matches_s_to_e', 0)
        total_entity_matches = entity_matches_e_to_s + entity_matches_s_to_e
        
        print(f"Entity Matches (E→S): {entity_matches_e_to_s}")
        print(f"Entity Matches (S→E): {entity_matches_s_to_e}")
        print(f"Total Entity Matches: {total_entity_matches}")
        
        rel_matches_e_to_s = summary.get('total_relation_matches_e_to_s', 0)
        rel_matches_s_to_e = summary.get('total_relation_matches_s_to_e', 0)
        total_rel_matches = rel_matches_e_to_s + rel_matches_s_to_e
        
        print(f"Relationship Matches (E→S): {rel_matches_e_to_s}")
        print(f"Relationship Matches (S→E): {rel_matches_s_to_e}")
        print(f"Total Relationship Matches: {total_rel_matches}\n")
        
        # Compliance Assessment
        print("COMPLIANCE ASSESSMENT:")
        compliance_score = compliance.get('overall_compliance_score', 0)
        print(f"Overall Compliance Score: {compliance_score:.3f}")
        print(f"Compliance Level: {compliance.get('compliance_level', 'Unknown')}")
        print(f"Is Compliant: {'Yes' if compliance.get('is_compliant', False) else 'No'}\n")
        
        # Bidirectional Alignment Metrics
        print("BIDIRECTIONAL ALIGNMENT METRICS:")
        print(f"Entity Alignment Score: {bidirectional_metrics.get('entity_alignment_score', 0):.1%}")
        print(f"Relationship Alignment Score: {bidirectional_metrics.get('relationship_alignment_score', 0):.1%}")
        print(f"Bidirectional Similarity: {bidirectional_metrics.get('bidirectional_similarity', 0):.1%}")
        print(f"Mutual Entity Coverage: {bidirectional_metrics.get('mutual_entity_coverage', 0):.1%}")
        print(f"Mutual Relationship Coverage: {bidirectional_metrics.get('mutual_relationship_coverage', 0):.1%}")
        
        if bd_compliance:
            print(f"\nBidirectional Compliance Level: {bd_compliance.get('compliance_level', 'Unknown')}")
            print(f"Compliance Percentage: {bd_compliance.get('compliance_percentage', 0):.1f}%")
        
        # Summary Assessment
        print("\n" + "=" * 80)
        print("🎖️ FINAL ASSESSMENT:")
        print("=" * 80)
        
        # Check performance tiers
        if overall_similarity >= 0.95 and entity_matches_e_to_s > 0 and rel_matches_e_to_s > 0:
            print("✅ EXCELLENT PERFORMANCE - World-class optimization")
            print(f"   • Overall Similarity: {overall_similarity:.1%}")
            print(f"   • Total Matches: {total_entity_matches} entities, {total_rel_matches} relationships")
            print(f"   • Bidirectional Alignment: {bidirectional_metrics.get('bidirectional_similarity', 0):.1%}")
            print(f"   • Compliance: {compliance_score:.1%}")
        elif overall_similarity >= 0.90:
            print("🥇 VERY GOOD PERFORMANCE - High-quality optimization")
            print(f"   • Overall Similarity: {overall_similarity:.1%}")
            print(f"   • Total Matches: {total_entity_matches} entities, {total_rel_matches} relationships")
        elif overall_similarity >= 0.85:
            print("🥈 GOOD PERFORMANCE - Solid optimization")
        else:
            print("🥉 NEEDS IMPROVEMENT")
        
        print("\n✅ Real project test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_real_contract_with_gui_display()
    if not success:
        sys.exit(1)