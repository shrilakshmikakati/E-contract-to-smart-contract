#!/usr/bin/env python3
"""
Diagnostic script to debug the comparison issue
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def debug_comparison_issue():
    """Debug why entity matches are 0 but similarity score is 98.4%"""
    print("🔍 DEBUGGING COMPARISON ISSUE")
    print("=" * 50)
    
    try:
        from src.core.econtract_processor import EContractProcessor
        from src.core.smartcontract_processor import SmartContractProcessor
        from src.core.comparator import ContractComparator
        
        # Simple test case
        econtract_text = "John Smith rents apartment for $1200 monthly from ABC Properties."
        smartcontract_code = """
        contract RentalAgreement {
            address public tenant;
            address public landlord;
            uint256 public monthlyRent;
        }
        """
        
        print("📝 Processing contracts...")
        econtract_processor = EContractProcessor()
        e_kg = econtract_processor.process_contract(econtract_text, "test")
        
        smartcontract_processor = SmartContractProcessor()
        s_kg = smartcontract_processor.process_contract(smartcontract_code, "test")
        
        print(f"E-contract entities: {len(e_kg.entities)}")
        for eid, entity in e_kg.entities.items():
            print(f"  {eid}: {entity}")
        
        print(f"Smart contract entities: {len(s_kg.entities)}")
        for sid, entity in s_kg.entities.items():
            print(f"  {sid}: {entity}")
        
        print("\n🔍 Running comparison...")
        comparator = ContractComparator()
        results = comparator.compare_knowledge_graphs(e_kg, s_kg)
        
        print("\n📊 RAW RESULTS:")
        print(f"Overall similarity: {results['overall_similarity_score']}")
        
        summary = results.get('summary', {})
        print(f"Entity matches E→S: {summary.get('total_entity_matches_e_to_s', 0)}")
        print(f"Entity matches S→E: {summary.get('total_entity_matches_s_to_e', 0)}")
        print(f"Relation matches E→S: {summary.get('total_relation_matches_e_to_s', 0)}")
        print(f"Relation matches S→E: {summary.get('total_relation_matches_s_to_e', 0)}")
        
        # Check bidirectional metrics
        metrics = results.get('bidirectional_metrics', {})
        print(f"\nBidirectional metrics:")
        for key, value in metrics.items():
            print(f"  {key}: {value}")
        
        # Check if the issue is in how metrics are calculated
        print(f"\nEntity coverage E→S: {metrics.get('econtract_entity_coverage', 0)}")
        print(f"Entity coverage S→E: {metrics.get('smartcontract_entity_coverage', 0)}")
        
    except Exception as e:
        print(f"❌ Debug failed: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_comparison_issue()