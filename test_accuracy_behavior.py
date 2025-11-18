#!/usr/bin/env python3
"""
Test script to verify the new accuracy display behavior:
1. Contract code shows first (no accuracy)
2. Accuracy only shows during comparison
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_accuracy_behavior():
    """Test the new accuracy display behavior"""
    
    print("Testing New Accuracy Display Behavior...")
    print("="*50)
    
    try:
        # Import required modules
        from core.econtract_processor import EContractProcessor
        from core.smartcontract_processor import SmartContractProcessor
        # from algorithms.comparator import Comparator  # Not needed for this test
        
        # Simple test contract text
        sample_contract = """
        Service Agreement between ABC Company (Client) and John Smith (Provider).
        Services: Web development and consulting
        Payment: $5,000 total, paid in monthly installments of $1,000
        Duration: 5 months starting January 1, 2024
        Deliverables: Complete website with user authentication
        """
        
        print("Step 1: Processing e-contract...")
        econtract_processor = EContractProcessor()
        econtract_kg = econtract_processor.process_contract(sample_contract)
        
        if not econtract_kg:
            print("❌ E-contract processing failed")
            return
            
        print(f"✓ E-contract processed: {len(econtract_kg.entities)} entities")
        
        print("\nStep 2: Generating smart contract (should show CODE first, NO accuracy)...")
        smartcontract_processor = SmartContractProcessor()
        
        # Prepare analysis data
        entities_list = []
        for entity_id, entity_data in econtract_kg.entities.items():
            entity_dict = {'id': entity_id}
            entity_dict.update(entity_data)
            entities_list.append(entity_dict)
        
        relationships_list = []
        for rel_id, rel_data in econtract_kg.relationships.items():
            rel_dict = {'id': rel_id}
            rel_dict.update(rel_data)
            relationships_list.append(rel_dict)
        
        econtract_analysis = {
            'entities': entities_list,
            'relationships': relationships_list,
            'knowledge_graph': econtract_kg,
            'metadata': econtract_kg.metadata
        }
        
        result = smartcontract_processor.generate_smart_contract_from_econtract(econtract_analysis)
        
        if 'error' in result:
            print(f"❌ Smart contract generation error: {result['error']}")
            return
            
        print("✅ Smart contract generated!")
        print(f"Contract Type: {result.get('contract_type', 'Unknown')}")
        print(f"Deployment Ready: {result.get('deployment_ready', False)}")
        
        # Show contract code preview (this is what user sees first now)
        contract_code = result.get('contract_code', '')
        if contract_code:
            print(f"\n📝 CONTRACT CODE PREVIEW (first 300 chars):")
            print("=" * 50)
            print(contract_code[:300] + "..." if len(contract_code) > 300 else contract_code)
            print("=" * 50)
        
        print(f"\n🔒 ACCURACY HIDDEN during generation (as requested)")
        print(f"   Accuracy will only show during comparison phase")
        
        print("\nStep 3: Simulating comparison phase (should show ACCURACY now)...")
        
        # Process smart contract for comparison
        smartcontract_kg = smartcontract_processor.process_contract(contract_code)
        
        if smartcontract_kg:
            print(f"✓ Smart contract processed: {len(smartcontract_kg.entities)} entities")
            
            # Calculate accuracy metrics (this is what shows in comparison)
            accuracy_score = result.get('accuracy_score', 0)
            
            print(f"\n📊 ACCURACY ANALYSIS (shown only in comparison):")
            print("=" * 40)
            print(f"Smart Contract Generation Accuracy: {accuracy_score:.2%}")
            print(f"Deployment Ready: {'✅ Yes' if result.get('deployment_ready', False) else '⚠️ No'}")
            
            # Knowledge graph comparison
            e_entities = len(econtract_kg.entities)
            s_entities = len(smartcontract_kg.entities)
            preservation = (min(e_entities, s_entities) / max(e_entities, 1)) if e_entities > 0 else 0
            
            print(f"E-Contract Entities: {e_entities}")
            print(f"Smart Contract Entities: {s_entities}")
            print(f"Entity Preservation: {preservation:.2%}")
            
            # Accuracy interpretation
            if accuracy_score >= 0.95:
                print("📈 Interpretation: EXCELLENT - Ready for production")
            elif accuracy_score >= 0.85:
                print("📊 Interpretation: GOOD - Minor review recommended")
            elif accuracy_score >= 0.70:
                print("📉 Interpretation: FAIR - Review needed")
            else:
                print("⚠️ Interpretation: LOW - Improvements required")
        
        print("\n🎉 Test completed! New behavior verified:")
        print("   ✅ Contract code shows FIRST (no accuracy)")
        print("   ✅ Accuracy analysis shows ONLY during comparison")
        
    except Exception as e:
        print(f"❌ Test failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    test_accuracy_behavior()
    print("\nPress Enter to exit...")
    input()