#!/usr/bin/env python3
"""
Comprehensive test of the optimized comparison system on real project data
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_real_project_data():
    """Test the ultra-enhanced comparison system on actual project files"""
    print("🧪 TESTING OPTIMIZED SYSTEM ON REAL PROJECT DATA")
    print("=" * 60)
    
    try:
        from src.core.econtract_processor import EContractProcessor
        from src.core.smartcontract_processor import SmartContractProcessor
        from src.core.comparator import ContractComparator
        
        print("✅ All imports successful")
        
        # Load real e-contract
        econtract_file = os.path.join("data", "sample_contracts", "rental_agreement_complete.txt")
        smartcontract_file = os.path.join("data", "sample_smart_contracts", "rental_agreement_fixed.sol")
        
        if not os.path.exists(econtract_file):
            print(f"❌ E-contract file not found: {econtract_file}")
            return False
            
        if not os.path.exists(smartcontract_file):
            print(f"❌ Smart contract file not found: {smartcontract_file}")
            return False
        
        # Read the files
        print(f"📖 Reading e-contract from: {econtract_file}")
        with open(econtract_file, 'r', encoding='utf-8') as f:
            econtract_text = f.read()
        
        print(f"📖 Reading smart contract from: {smartcontract_file}")
        with open(smartcontract_file, 'r', encoding='utf-8') as f:
            smartcontract_code = f.read()
        
        print(f"📄 E-contract length: {len(econtract_text)} characters")
        print(f"📄 Smart contract length: {len(smartcontract_code)} characters")
        
        # Process the real e-contract
        print("\\n🔄 Processing real e-contract...")
        econtract_processor = EContractProcessor()
        e_kg = econtract_processor.process_contract(econtract_text, "real_econtract")
        
        print(f"   📊 E-contract entities: {len(e_kg.entities)}")
        print(f"   📊 E-contract relationships: {len(e_kg.relationships)}")
        
        # Show sample entities
        entity_samples = list(e_kg.entities.items())[:5]
        for eid, entity in entity_samples:
            print(f"      {eid}: {entity.get('text', '')[:50]}... (type: {entity.get('type', 'unknown')})")
        
        # Process the real smart contract
        print("\\n🔄 Processing real smart contract...")
        smartcontract_processor = SmartContractProcessor()
        s_kg = smartcontract_processor.process_contract(smartcontract_code, "real_smartcontract")
        
        print(f"   📊 Smart contract entities: {len(s_kg.entities)}")
        print(f"   📊 Smart contract relationships: {len(s_kg.relationships)}")
        
        # Show sample entities
        entity_samples = list(s_kg.entities.items())[:5]
        for sid, entity in entity_samples:
            print(f"      {sid}: {entity.get('text', '')[:50]}... (type: {entity.get('type', 'unknown')})")
        
        # Run the optimized comparison
        print("\\n🚀 Running ULTRA-OPTIMIZED comparison on real data...")
        comparator = ContractComparator()
        comparison_results = comparator.compare_knowledge_graphs(e_kg, s_kg, "real_project_test")
        
        # Extract and display comprehensive results
        print("\\n" + "=" * 80)
        print("📊 COMPREHENSIVE REAL PROJECT RESULTS:")
        print("=" * 80)
        
        summary = comparison_results.get('summary', {})
        bidirectional_metrics = comparison_results.get('bidirectional_metrics', {})
        compliance = bidirectional_metrics.get('bidirectional_compliance', {})
        accuracy_data = comparison_results.get('accuracy_analysis', {})
        
        # Core Performance Metrics
        print(f"\\n🎯 CORE PERFORMANCE METRICS:")
        print(f"   Overall Similarity Score: {summary.get('overall_similarity_score', 0):.1%}")
        print(f"   Entity Alignment Score: {summary.get('entity_alignment_score', 0):.1%}")
        print(f"   Relationship Alignment Score: {summary.get('relationship_alignment_score', 0):.1%}")
        print(f"   Bidirectional Similarity: {summary.get('bidirectional_similarity', 0):.1%}")
        
        # Entity Analysis
        print(f"\\n📈 ENTITY ANALYSIS:")
        print(f"   E-contract Entities: {len(e_kg.entities)}")
        print(f"   Smart Contract Entities: {len(s_kg.entities)}")
        print(f"   Entity Matches E→S: {summary.get('total_entity_matches_e_to_s', 0)}")
        print(f"   Entity Matches S→E: {summary.get('total_entity_matches_s_to_e', 0)}")
        print(f"   Entity Coverage E→S: {summary.get('econtract_entity_coverage', 0):.1%}")
        print(f"   Entity Coverage S→E: {summary.get('smartcontract_entity_coverage', 0):.1%}")
        
        # Relationship Analysis
        print(f"\\n🔗 RELATIONSHIP ANALYSIS:")
        print(f"   E-contract Relationships: {len(e_kg.relationships)}")
        print(f"   Smart Contract Relationships: {len(s_kg.relationships)}")
        print(f"   Relationship Matches E→S: {summary.get('total_relation_matches_e_to_s', 0)}")
        print(f"   Relationship Matches S→E: {summary.get('total_relation_matches_s_to_e', 0)}")
        print(f"   Relationship Coverage E→S: {summary.get('econtract_relationship_coverage', 0):.1%}")
        print(f"   Relationship Coverage S→E: {summary.get('smartcontract_relationship_coverage', 0):.1%}")
        
        # Compliance Assessment
        print(f"\\n✅ COMPLIANCE ASSESSMENT:")
        print(f"   Compliance Level: {compliance.get('compliance_level', 'Unknown')}")
        print(f"   Compliance Percentage: {compliance.get('compliance_percentage', 0):.1f}%")
        print(f"   Bidirectionally Compliant: {compliance.get('is_bidirectionally_compliant', False)}")
        
        criteria_met = compliance.get('criteria_met', {})
        print(f"   ✓ Entity Coverage: {'✅' if criteria_met.get('mutual_entity_coverage', False) else '❌'}")
        print(f"   ✓ Relationship Coverage: {'✅' if criteria_met.get('mutual_relationship_coverage', False) else '❌'}")
        print(f"   ✓ Entity Alignment Quality: {'✅' if criteria_met.get('entity_alignment_quality', False) else '❌'}")
        print(f"   ✓ Relationship Alignment Quality: {'✅' if criteria_met.get('relationship_alignment_quality', False) else '❌'}")
        
        # Quality Analysis
        entity_analysis = comparison_results.get('entity_analysis', {})
        match_quality_e_to_s = entity_analysis.get('match_quality_distribution_e_to_s', {})
        match_quality_s_to_e = entity_analysis.get('match_quality_distribution_s_to_e', {})
        
        print(f"\\n🏆 MATCH QUALITY ANALYSIS:")
        print(f"   E→S High Quality Matches: {match_quality_e_to_s.get('high_quality', 0)}")
        print(f"   E→S Medium Quality Matches: {match_quality_e_to_s.get('medium_quality', 0)}")
        print(f"   E→S Low Quality Matches: {match_quality_e_to_s.get('low_quality', 0)}")
        print(f"   S→E High Quality Matches: {match_quality_s_to_e.get('high_quality', 0)}")
        print(f"   S→E Medium Quality Matches: {match_quality_s_to_e.get('medium_quality', 0)}")
        print(f"   S→E Low Quality Matches: {match_quality_s_to_e.get('low_quality', 0)}")
        
        # Accuracy Analysis
        print(f"\\n📊 DETAILED ACCURACY ANALYSIS:")
        if accuracy_data:
            print(f"   Accuracy Score: {accuracy_data.get('accuracy_score', 0):.1%}")
            print(f"   Base Accuracy: {accuracy_data.get('base_accuracy_score', 0):.1%}")
            print(f"   Business Logic Score: {accuracy_data.get('business_logic_score', 0):.1%}")
            print(f"   Completeness Score: {accuracy_data.get('completeness_score', 0):.1%}")
            print(f"   Deployment Ready: {'✅' if accuracy_data.get('deployment_ready', False) else '❌'}")
        
        # Performance Assessment
        overall_score = summary.get('overall_similarity_score', 0)
        entity_alignment = summary.get('entity_alignment_score', 0)
        relationship_alignment = summary.get('relationship_alignment_score', 0)
        compliance_pct = compliance.get('compliance_percentage', 0)
        
        print(f"\\n🎖️ FINAL PERFORMANCE ASSESSMENT:")
        if overall_score >= 0.95 and entity_alignment >= 0.65 and relationship_alignment >= 0.80 and compliance_pct >= 90:
            print("   🏆 EXCELLENT PERFORMANCE - World-class optimization achieved!")
        elif overall_score >= 0.90 and entity_alignment >= 0.60 and relationship_alignment >= 0.70 and compliance_pct >= 80:
            print("   🥇 VERY GOOD PERFORMANCE - High-quality optimization")
        elif overall_score >= 0.85 and entity_alignment >= 0.50 and relationship_alignment >= 0.60 and compliance_pct >= 70:
            print("   🥈 GOOD PERFORMANCE - Solid optimization")
        else:
            print("   🥉 ROOM FOR IMPROVEMENT - Consider further optimization")
        
        print("\\n✅ Real project test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Real project test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_real_project_data()
    if not success:
        sys.exit(1)