#!/usr/bin/env python3
"""
Test script to verify smart contract generation functionality
"""

import sys
import os
sys.path.append(os.path.dirname(__file__))

from src.core.econtract_processor import EContractProcessor
from src.core.smartcontract_processor import SmartContractProcessor

def test_smart_contract_generation():
    """Test the complete smart contract generation pipeline"""
    
    # Sample e-contract text
    sample_contract = """
    Service Agreement
    
    This agreement is between John Smith (Client) and Tech Solutions Inc (Provider).
    
    The Provider will deliver software development services for $5,000.
    The project duration is 3 months starting January 1, 2025.
    Payment terms: 50% upfront, 50% on completion.
    
    The Provider guarantees delivery of high-quality code meeting specifications.
    The Client agrees to provide necessary requirements and feedback within 48 hours.
    """
    
    print("Testing Smart Contract Generation...")
    print("=" * 50)
    
    try:
        # Step 1: Process e-contract
        print("Step 1: Processing e-contract...")
        econtract_processor = EContractProcessor()
        econtract_kg = econtract_processor.process_contract(sample_contract)
        
        if econtract_kg and econtract_kg.entities:
            print(f"✓ E-contract processed successfully!")
            print(f"  - Entities found: {len(econtract_kg.entities)}")
            print(f"  - Relationships found: {len(econtract_kg.relationships)}")
        else:
            print("✗ Failed to process e-contract")
            return False
            
        # Step 2: Generate smart contract
        print("\nStep 2: Generating smart contract...")
        smartcontract_processor = SmartContractProcessor()
        
        # Prepare analysis data (convert to list format)
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
        
        # Generate smart contract
        generation_result = smartcontract_processor.generate_smart_contract_from_econtract(econtract_analysis)
        
        if 'error' in generation_result:
            print(f"✗ Smart contract generation failed: {generation_result['error']}")
            return False
        else:
            print("✓ Smart contract generated successfully!")
            print(f"  - Accuracy Score: {generation_result.get('accuracy_score', 0):.2%}")
            print(f"  - Contract Type: {generation_result.get('contract_type', 'Unknown')}")
            print(f"  - Deployment Ready: {generation_result.get('deployment_ready', False)}")
            
            # Show a snippet of the generated contract
            contract_code = generation_result.get('contract_code', '')
            if contract_code:
                lines = contract_code.split('\n')[:10]
                print(f"\n  Contract Preview:")
                for i, line in enumerate(lines, 1):
                    print(f"    {i:2d}: {line}")
                if len(contract_code.split('\n')) > 10:
                    print(f"    ... ({len(contract_code.split('\n')) - 10} more lines)")
        
        print(f"\n✓ Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"✗ Test failed with error: {str(e)}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_smart_contract_generation()
    if success:
        print("\n🎉 All tests passed! Smart contract generation is working correctly.")
    else:
        print("\n❌ Tests failed. Please check the error messages above.")
    
    input("\nPress Enter to exit...")