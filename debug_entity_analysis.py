#!/usr/bin/env python3
"""
Debug script to analyze entity generation and comparison
"""

import sys
import os

# Add the src directory to the path and set up proper module resolution
current_dir = os.path.dirname(os.path.abspath(__file__))
src_dir = os.path.join(current_dir, 'src')
sys.path.insert(0, src_dir)

# Change to src directory for proper relative imports
os.chdir(src_dir)

def debug_entity_generation():
    """Debug entity extraction and comparison process"""
    
    print("🔍 ENTITY GENERATION & COMPARISON ANALYSIS")
    print("=" * 50)
    
    try:
        # Import with absolute paths from src
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
                print(f"    - {text}")
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
                print(f"    - {text}")
            if len(texts) > 3:
                print(f"    ... and {len(texts)-3} more")
        
        # Analyze entity matching potential
        print(f"\n🔍 STEP 4: ENTITY MATCHING ANALYSIS")
        print("=" * 40)
        
        print(f"POTENTIAL MATCHES:")
        matches_found = 0
        
        for e_id, e_data in econtract_kg.entities.items():
            e_text = e_data.get('text', '').lower()
            e_type = e_data.get('type', '')
            
            print(f"\nE-Contract Entity: '{e_text}' (Type: {e_type})")
            
            best_match = None
            best_score = 0
            
            for s_id, s_data in smartcontract_kg.entities.items():
                s_text = s_data.get('text', '').lower()
                s_type = s_data.get('type', '')
                
                # Simple similarity check
                if e_text in s_text or s_text in e_text:
                    score = max(len(e_text), len(s_text)) / (len(e_text) + len(s_text))
                elif e_text == s_text:
                    score = 1.0
                else:
                    # Check if both are same type and have similar content
                    if e_type == s_type and len(set(e_text.split()) & set(s_text.split())) > 0:
                        score = 0.3
                    else:
                        score = 0
                
                if score > best_score:
                    best_score = score
                    best_match = (s_text, s_type)
            
            if best_match and best_score > 0.2:
                print(f"  → Potential match: '{best_match[0]}' (Type: {best_match[1]}) - Score: {best_score:.2f}")
                matches_found += 1
            else:
                print(f"  → No match found")
        
        print(f"\n📊 MATCHING SUMMARY:")
        print(f"  Potential matches found: {matches_found}")
        print(f"  E-contract entities: {len(econtract_kg.entities)}")
        print(f"  Smart contract entities: {len(smartcontract_kg.entities)}")
        print(f"  Match rate: {(matches_found/len(econtract_kg.entities)*100):.1f}%" if len(econtract_kg.entities) > 0 else "  Match rate: 0%")
        
        # Show why matching fails
        print(f"\n🔍 WHY ENTITY MATCHING FAILS:")
        print("=" * 30)
        
        print("1. DIFFERENT EXTRACTION CONTEXTS:")
        print("   E-Contract: Extracts from natural language text")
        print("   Smart Contract: Extracts from Solidity code structure")
        
        print("\n2. DIFFERENT ENTITY TYPES:")
        print("   E-Contract types:", list(entity_types.keys())[:5])
        print("   Smart Contract types:", list(sc_entity_types.keys())[:5])
        
        print("\n3. DIFFERENT TEXT REPRESENTATIONS:")
        print("   E-Contract: 'ABC Corporation', 'John Smith', '$10,000'")
        print("   Smart Contract: 'client', 'provider', 'uint256'")
        
        print(f"\n💡 RECOMMENDATIONS TO IMPROVE ENTITY MATCHING:")
        print("=" * 45)
        print("1. Map business entities to smart contract variables during generation")
        print("2. Add metadata linking e-contract entities to smart contract elements")
        print("3. Improve entity type normalization between contexts")
        print("4. Use semantic similarity instead of text matching")
        print("5. Add contract-specific entity mapping rules")
        
    except Exception as e:
        print(f"❌ Analysis failed: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    debug_entity_generation()
    print("\nPress Enter to exit...")
    input()