#!/usr/bin/env python3
"""
Test entity deduplication with duplicate entities
"""
import sys
import os
sys.path.append(os.path.abspath('.'))

def test_entity_deduplication():
    """Test entity deduplication with actual duplicate entities"""
    print("🔄 TESTING ENTITY DEDUPLICATION")
    print("=" * 60)
    
    try:
        from src.core.knowledge_graph import KnowledgeGraph
        from src.core.comparator import KnowledgeGraphComparator
        
        print("✅ Imports successful")
        
        # Create test smart contract with duplicate entities
        s_kg = KnowledgeGraph()
        
        # Add entities that will be duplicates
        s_kg.add_entity("param__tenant_1", {"type": "PARAMETER", "text": "tenant"})
        s_kg.add_entity("param__tenant_2", {"type": "PARAMETER", "text": "tenant"})  # Duplicate
        s_kg.add_entity("param__tenant_address", {"type": "PARAMETER", "text": "tenant_address"})  # Similar
        
        s_kg.add_entity("param__landlord_5", {"type": "PARAMETER", "text": "landlord"})
        s_kg.add_entity("param__landlord_6", {"type": "PARAMETER", "text": "landlord"})  # Duplicate
        
        s_kg.add_entity("param__monthlyRent_8", {"type": "PARAMETER", "text": "monthlyRent"})
        s_kg.add_entity("monthlyRent", {"type": "STATE_VARIABLE", "text": "monthlyRent"})  # Different type, similar text
        s_kg.add_entity("monthly_rent", {"type": "PARAMETER", "text": "monthly_rent"})  # Variation
        
        s_kg.add_entity("payRent_func", {"type": "FUNCTION", "text": "payRent"})
        s_kg.add_entity("payRent", {"type": "FUNCTION", "text": "payRent"})  # Duplicate function
        
        s_kg.add_entity("contract_main", {"type": "CONTRACT", "text": "RentalContract"})
        s_kg.add_entity("rental_contract", {"type": "CONTRACT", "text": "RentalContract"})  # Duplicate
        
        # Create simple e-contract for comparison
        e_kg = KnowledgeGraph()
        e_kg.add_entity("tenant", {"type": "PERSON", "text": "John Smith"})
        e_kg.add_entity("landlord", {"type": "PERSON", "text": "Jane Doe"}) 
        e_kg.add_entity("rent", {"type": "AMOUNT", "text": "$1500"})
        
        print(f"📋 Before deduplication:")
        print(f"   Smart contract entities: {len(s_kg.entities)}")
        print(f"   E-contract entities: {len(e_kg.entities)}")
        
        # Test deduplication through comparator
        comparator = KnowledgeGraphComparator()
        
        # Test the _deduplicate_entities method directly
        print(f"\\n🔬 Testing entity deduplication...")
        deduplicated_s = comparator._deduplicate_entities(s_kg.entities)
        deduplicated_e = comparator._deduplicate_entities(e_kg.entities)
        
        print(f"\\n📊 After deduplication:")
        print(f"   Smart contract entities: {len(s_kg.entities)} → {len(deduplicated_s)}")
        print(f"   E-contract entities: {len(e_kg.entities)} → {len(deduplicated_e)}")
        
        print(f"\\n🔍 Remaining smart contract entities:")
        for eid, data in deduplicated_s.items():
            print(f"   - {eid}: {data.get('type', 'UNKNOWN')} = '{data.get('text', '')}'")
        
        print(f"\\n✅ Entity deduplication test completed!")
        
        # Calculate reduction percentage
        original_count = len(s_kg.entities)
        final_count = len(deduplicated_s)
        reduction_percent = ((original_count - final_count) / original_count) * 100 if original_count > 0 else 0
        
        print(f"\\n📈 Deduplication Results:")
        print(f"   Original entities: {original_count}")
        print(f"   Final entities: {final_count}")
        print(f"   Reduction: {reduction_percent:.1f}% ({original_count - final_count} entities removed)")
        
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_entity_deduplication()
    if not success:
        sys.exit(1)