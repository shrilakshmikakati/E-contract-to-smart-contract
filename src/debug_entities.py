#!/usr/bin/env python3
"""
Debug script to analyze entity generation and comparison
"""

import sys
import os

def debug_entity_generation():
    """Debug entity extraction and comparison process"""
    
    print("🔍 ENTITY GENERATION & COMPARISON ANALYSIS")
    print("=" * 50)
    
    try:
        # Import processors directly
        from core.econtract_processor import EContractProcessor
        from core.smartcontract_processor import SmartContractProcessor
        
        # Test contract with clear entities
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
        
        print("📝 ANALYZING SAMPLE CONTRACT:")
        print("=" * 30)
        print(f"Contract length: {len(sample_contract)} characters")
        print(f"Sample text: {sample_contract[:200]}...")
        
        # Process e-contract
        print("\n🔍 STEP 1: E-CONTRACT ENTITY EXTRACTION")
        print("=" * 40)
        
        econtract_processor = EContractProcessor()
        econtract_kg = econtract_processor.process_contract(sample_contract)
        
        print(f"E-Contract Knowledge Graph:")
        print(f"  Total Entities: {len(econtract_kg.entities)}")
        print(f"  Total Relationships: {len(econtract_kg.relationships)}")
        
        print(f"\n📋 E-CONTRACT ENTITIES BY TYPE:")
        entity_types = {}
        for entity_id, entity_data in econtract_kg.entities.items():
            entity_type = entity_data.get('type', 'UNKNOWN')
            entity_text = entity_data.get('text', '')
            
            if entity_type not in entity_types:
                entity_types[entity_type] = []
            entity_types[entity_type].append(entity_text)
        
        for etype, texts in entity_types.items():
            print(f"  {etype}: {len(texts)} entities")
            for i, text in enumerate(texts[:3]):  # Show first 3
                print(f"    - '{text}'")
            if len(texts) > 3:
                print(f"    ... and {len(texts)-3} more")
        
        # Generate smart contract
        print(f"\n🔍 STEP 2: SMART CONTRACT GENERATION")
        print("=" * 40)
        
        smartcontract_processor = SmartContractProcessor()
        
        # Prepare entities for smart contract generation
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
            print(f"❌ Smart contract generation failed: {result['error']}")
            return
        
        contract_code = result.get('contract_code', '')
        print(f"✅ Smart contract generated: {len(contract_code)} characters")
        print(f"Smart contract preview: {contract_code[:200]}...")
        
        # Process smart contract to extract entities
        print(f"\n🔍 STEP 3: SMART CONTRACT ENTITY EXTRACTION")
        print("=" * 40)
        
        smartcontract_kg = smartcontract_processor.process_contract(contract_code)
        
        print(f"Smart Contract Knowledge Graph:")
        print(f"  Total Entities: {len(smartcontract_kg.entities)}")
        print(f"  Total Relationships: {len(smartcontract_kg.relationships)}")
        
        print(f"\n📋 SMART CONTRACT ENTITIES BY TYPE:")
        sc_entity_types = {}
        for entity_id, entity_data in smartcontract_kg.entities.items():
            entity_type = entity_data.get('type', 'UNKNOWN')
            entity_text = entity_data.get('text', '')
            
            if entity_type not in sc_entity_types:
                sc_entity_types[entity_type] = []
            sc_entity_types[entity_type].append(entity_text)
        
        for etype, texts in sc_entity_types.items():
            print(f"  {etype}: {len(texts)} entities")
            for i, text in enumerate(texts[:3]):  # Show first 3
                print(f"    - '{text}'")
            if len(texts) > 3:
                print(f"    ... and {len(texts)-3} more")
        
        # Test the actual comparator
        print(f"\n🔍 STEP 4: ACTUAL COMPARATOR TESTING")
        print("=" * 40)
        
        from core.comparator import KnowledgeGraphComparator
        
        comparator = KnowledgeGraphComparator()
        comparison_result = comparator.compare_knowledge_graphs(econtract_kg, smartcontract_kg)
        
        print(f"Comparator Results:")
        print(f"  Entity Preservation: {comparison_result.get('entity_preservation_percentage', 0):.2f}%")
        print(f"  Relationship Preservation: {comparison_result.get('relationship_preservation_percentage', 0):.2f}%")
        print(f"  Entity Matches: {len(comparison_result.get('entity_matches', []))}")
        print(f"  Relationship Matches: {len(comparison_result.get('relationship_matches', []))}")
        
        # Show specific entity matches
        entity_matches = comparison_result.get('entity_matches', [])
        if entity_matches:
            print(f"\n📋 ACTUAL ENTITY MATCHES:")
            for match in entity_matches[:5]:  # Show first 5
                e1 = match.get('entity1', {})
                e2 = match.get('entity2', {})
                score = match.get('similarity_score', 0)
                print(f"  Match: '{e1.get('text', '')}' ↔ '{e2.get('text', '')}' (Score: {score:.2f})")
        else:
            print(f"\n❌ NO ENTITY MATCHES FOUND")
            
        # Analyze why no matches
        print(f"\n🔍 STEP 5: WHY NO ENTITY MATCHES?")
        print("=" * 40)
        
        print("E-CONTRACT ENTITY SAMPLES:")
        for i, (entity_id, entity_data) in enumerate(list(econtract_kg.entities.items())[:5]):
            print(f"  {i+1}. '{entity_data.get('text', '')}' (Type: {entity_data.get('type', 'UNKNOWN')})")
        
        print("\nSMART CONTRACT ENTITY SAMPLES:")
        for i, (entity_id, entity_data) in enumerate(list(smartcontract_kg.entities.items())[:5]):
            print(f"  {i+1}. '{entity_data.get('text', '')}' (Type: {entity_data.get('type', 'UNKNOWN')})")
        
        print(f"\n💡 ANALYSIS CONCLUSIONS:")
        print("=" * 25)
        print("1. E-contracts extract business terms and natural language entities")
        print("2. Smart contracts extract code structure and Solidity identifiers")
        print("3. These operate in completely different semantic spaces")
        print("4. Direct text matching between 'ABC Corporation' and 'client' fails")
        print("5. Need semantic mapping between business entities and code variables")
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_entity_generation()
    print("\nPress Enter to exit...")
    input()