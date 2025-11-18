"""
Entity analysis test using main.py import structure
"""

import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def analyze_entities():
    """Analyze entity generation and matching"""
    
    print("🔍 ENTITY ANALYSIS WITH PROPER IMPORTS")
    print("=" * 50)
    
    try:
        # Import GUI modules to get processors
        from gui.main_window import MainWindow
        
        # Test contract
        sample_contract = """
        SERVICE AGREEMENT
        
        This agreement is between ABC Corporation (Client) and John Smith (Service Provider).
        
        Service Details:
        - Web development services 
        - Duration: 6 months starting January 1, 2024
        - Total payment: $10,000
        - Monthly payments: $1,667
        - Hourly rate: $75/hour
        
        Contact Information:
        Client: contact@abc-corp.com, +1-555-123-4567
        Provider: john.smith@email.com, +1-555-987-6543
        
        The client agrees to provide access to development servers.
        The provider shall deliver weekly progress reports.
        Payment is due within 30 days of invoice receipt.
        """
        
        print("📝 Testing with sample contract")
        print(f"Contract length: {len(sample_contract)} characters")
        
        # Create main window instance to access processors
        import tkinter as tk
        root = tk.Tk()
        root.withdraw()  # Hide the window
        
        main_window = MainWindow(root)
        
        # Process e-contract
        print("\n🔍 PROCESSING E-CONTRACT")
        print("=" * 30)
        
        econtract_kg = main_window.econtract_processor.process_contract(sample_contract)
        
        print(f"E-Contract Results:")
        print(f"  Entities: {len(econtract_kg.entities)}")
        print(f"  Relationships: {len(econtract_kg.relationships)}")
        
        # Show entity details
        print(f"\n📋 E-CONTRACT ENTITIES:")
        entity_types = {}
        for entity_id, entity_data in econtract_kg.entities.items():
            entity_type = entity_data.get('type', 'UNKNOWN')
            entity_text = entity_data.get('text', '')
            
            if entity_type not in entity_types:
                entity_types[entity_type] = []
            entity_types[entity_type].append(entity_text)
            
            print(f"  ID: {entity_id}")
            print(f"    Text: '{entity_text}'")
            print(f"    Type: {entity_type}")
            print(f"    Data: {entity_data}")
            print()
        
        # Generate smart contract
        print(f"\n🔍 GENERATING SMART CONTRACT")
        print("=" * 35)
        
        # Prepare data for smart contract generation
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
        
        result = main_window.smartcontract_processor.generate_smart_contract_from_econtract(econtract_analysis)
        
        if 'error' in result:
            print(f"❌ Generation failed: {result['error']}")
            return
        
        contract_code = result.get('contract_code', '')
        print(f"✅ Generated {len(contract_code)} characters of Solidity code")
        
        # Process smart contract
        print(f"\n🔍 PROCESSING SMART CONTRACT")
        print("=" * 35)
        
        smartcontract_kg = main_window.smartcontract_processor.process_contract(contract_code)
        
        print(f"Smart Contract Results:")
        print(f"  Entities: {len(smartcontract_kg.entities)}")
        print(f"  Relationships: {len(smartcontract_kg.relationships)}")
        
        # Show smart contract entities
        print(f"\n📋 SMART CONTRACT ENTITIES:")
        for entity_id, entity_data in smartcontract_kg.entities.items():
            entity_type = entity_data.get('type', 'UNKNOWN')
            entity_text = entity_data.get('text', '')
            
            print(f"  ID: {entity_id}")
            print(f"    Text: '{entity_text}'")
            print(f"    Type: {entity_type}")
            print(f"    Data: {entity_data}")
            print()
        
        # Run comparison
        print(f"\n🔍 RUNNING COMPARISON")
        print("=" * 25)
        
        comparison_result = main_window.comparator.compare_knowledge_graphs(econtract_kg, smartcontract_kg)
        
        print(f"Comparison Results:")
        print(f"  Entity preservation: {comparison_result.get('entity_preservation_percentage', 0):.2f}%")
        print(f"  Relationship preservation: {comparison_result.get('relationship_preservation_percentage', 0):.2f}%")
        print(f"  Entity matches: {len(comparison_result.get('entity_matches', []))}")
        
        # Show specific matches
        entity_matches = comparison_result.get('entity_matches', [])
        if entity_matches:
            print(f"\n📋 ENTITY MATCHES FOUND:")
            for match in entity_matches:
                e1 = match.get('entity1', {})
                e2 = match.get('entity2', {})
                score = match.get('similarity_score', 0)
                print(f"  '{e1.get('text', '')}' ↔ '{e2.get('text', '')}' (Score: {score:.3f})")
        else:
            print(f"\n❌ NO ENTITY MATCHES")
        
        print(f"\n💡 CONCLUSION:")
        print("The 0% entity match occurs because:")
        print("1. E-contracts extract business terms like 'ABC Corporation'")
        print("2. Smart contracts extract code identifiers like 'client'")
        print("3. There's no semantic bridge between these two domains")
        print("4. The system needs entity mapping during code generation")
        
        root.destroy()
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    analyze_entities()