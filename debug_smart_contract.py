#!/usr/bin/env python3
"""
Debug script to identify smart contract analysis errors
"""

import sys
import os

# Add the src directory to the path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def debug_smart_contract_analysis():
    """Debug smart contract analysis to find specific errors"""
    
    print("Debugging Smart Contract Analysis...")
    print("="*50)
    
    try:
        # Import required modules
        from core.econtract_processor import EContractProcessor
        from core.smartcontract_processor import SmartContractProcessor
        
        # Simple test contract text
        sample_contract = """
        This is a service agreement between Company ABC as the client and John Doe as the service provider.
        The service provider agrees to provide consulting services for a total amount of $5,000.
        The contract period is from January 1, 2024 to December 31, 2024.
        Payment will be made in monthly installments of $500 each.
        """
        
        print("Step 1: Processing e-contract...")
        econtract_processor = EContractProcessor()
        econtract_kg = econtract_processor.process_contract(sample_contract)
        
        if not econtract_kg:
            print("❌ E-contract processing failed")
            return
            
        print(f"✓ E-contract processed: {len(econtract_kg.entities)} entities, {len(econtract_kg.relationships)} relationships")
        
        print("\nStep 2: Generating smart contract...")
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
        
        print("Step 3: Attempting smart contract generation...")
        try:
            result = smartcontract_processor.generate_smart_contract_from_econtract(econtract_analysis)
            
            if 'error' in result:
                print(f"❌ Smart contract generation error: {result['error']}")
                return
                
            print(f"✓ Smart contract generated successfully!")
            print(f"  - Accuracy Score: {result.get('accuracy_score', 0):.2%}")
            print(f"  - Contract Type: {result.get('contract_type', 'unknown')}")
            print(f"  - Deployment Ready: {result.get('deployment_ready', False)}")
            
            # Now try to analyze the generated contract
            print("\nStep 4: Analyzing generated smart contract...")
            contract_code = result.get('contract_code', '')
            
            if not contract_code:
                print("❌ No contract code generated")
                return
                
            print(f"Contract code length: {len(contract_code)} characters")
            print("Contract preview (first 200 chars):")
            print(contract_code[:200] + "..." if len(contract_code) > 200 else contract_code)
            
            # Try to process the generated smart contract
            print("\nStep 5: Processing generated smart contract for analysis...")
            try:
                smart_contract_kg = smartcontract_processor.process_contract(contract_code)
                print(f"✓ Smart contract analyzed successfully!")
                print(f"  - Entities: {len(smart_contract_kg.entities) if smart_contract_kg else 0}")
                print(f"  - Relationships: {len(smart_contract_kg.relationships) if smart_contract_kg else 0}")
                
            except Exception as analysis_error:
                print(f"❌ Smart contract analysis failed: {str(analysis_error)}")
                print(f"Error type: {type(analysis_error).__name__}")
                import traceback
                print("Full traceback:")
                traceback.print_exc()
                return
                
        except Exception as generation_error:
            print(f"❌ Smart contract generation failed: {str(generation_error)}")
            print(f"Error type: {type(generation_error).__name__}")
            import traceback
            print("Full traceback:")
            traceback.print_exc()
            return
            
        print("\n🎉 All steps completed successfully!")
        
    except Exception as e:
        print(f"❌ Debug failed with error: {str(e)}")
        print(f"Error type: {type(e).__name__}")
        import traceback
        print("Full traceback:")
        traceback.print_exc()

if __name__ == "__main__":
    debug_smart_contract_analysis()
    print("\nPress Enter to exit...")
    input()