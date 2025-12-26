#!/usr/bin/env python3
"""
Test relationship matching improvements
"""
import sys
import os
sys.path.append(os.path.abspath('.'))

def test_relationship_matching():
    """Test the improved relationship matching system"""
    print("🔗 TESTING RELATIONSHIP MATCHING")
    print("=" * 40)
    
    try:
        # Import required modules
        from src.core.knowledge_graph import KnowledgeGraph
        from src.core.comparator import KnowledgeGraphComparator
        
        print("✅ Imports successful")
        
        # Create test E-contract knowledge graph
        e_kg = KnowledgeGraph()
        e_kg.add_entity("tenant", {"type": "PERSON", "text": "John Smith"})
        e_kg.add_entity("landlord", {"type": "PERSON", "text": "Jane Doe"}) 
        e_kg.add_entity("rent", {"type": "AMOUNT", "text": "$1500"})
        e_kg.add_entity("property", {"type": "LOCATION", "text": "123 Main Street"})
        e_kg.add_entity("monthly", {"type": "TIME", "text": "monthly"})
        
        # E-contract relationships
        e_kg.add_relationship("party_relationship", "tenant", "landlord", {"relation": "party_relationship"})
        e_kg.add_relationship("financial_obligation", "tenant", "rent", {"relation": "financial_obligation"})
        e_kg.add_relationship("obligation_assignment", "tenant", "property", {"relation": "obligation_assignment"})
        e_kg.add_relationship("temporal_reference", "rent", "monthly", {"relation": "temporal_reference"})
        
        # Create test Smart contract knowledge graph  
        s_kg = KnowledgeGraph()
        s_kg.add_entity("tenant", {"type": "PARAMETER", "text": "tenant"})
        s_kg.add_entity("landlord", {"type": "PARAMETER", "text": "landlord"})
        s_kg.add_entity("monthlyRent", {"type": "PARAMETER", "text": "monthlyRent"})
        s_kg.add_entity("payRent", {"type": "FUNCTION", "text": "payRent"})
        s_kg.add_entity("validatePayment", {"type": "FUNCTION", "text": "validatePayment"})
        s_kg.add_entity("rentTracker", {"type": "STATE_VARIABLE", "text": "rentTracker"})
        s_kg.add_entity("contract", {"type": "CONTRACT", "text": "RentalAgreement"})
        s_kg.add_entity("constructor", {"type": "FUNCTION", "text": "constructor"})
        s_kg.add_entity("payment", {"type": "EVENT", "text": "payment"})
        s_kg.add_entity("PaymentEvent", {"type": "EVENT", "text": "PaymentEvent"})
        
        # Smart contract relationships with technical terms
        s_kg.add_relationship("CONTAINS", "contract", "tenant", {"relation": "CONTAINS"})
        s_kg.add_relationship("CONTAINS", "contract", "landlord", {"relation": "CONTAINS"})  
        s_kg.add_relationship("validates", "validatePayment", "monthlyRent", {"relation": "validates"})
        s_kg.add_relationship("enforces", "payRent", "monthlyRent", {"relation": "enforces"})
        s_kg.add_relationship("tracks", "rentTracker", "monthlyRent", {"relation": "tracks"})
        s_kg.add_relationship("initializes", "constructor", "tenant", {"relation": "initializes"})
        s_kg.add_relationship("logs", "payRent", "payment", {"relation": "logs"})
        s_kg.add_relationship("EMITS", "payRent", "PaymentEvent", {"relation": "EMITS"})
        
        print(f"📋 Test data created:")
        print(f"   E-contract: {len(e_kg.entities)} entities, {len(e_kg.relationships)} relationships")
        print(f"   Smart contract: {len(s_kg.entities)} entities, {len(s_kg.relationships)} relationships")
        
        # Test the comparison
        print(f"\\n🔬 Testing enhanced relationship matching...")
        comparator = KnowledgeGraphComparator()
        result = comparator.compare_knowledge_graphs(e_kg, s_kg, "test_relationships")
        
        print(f"\\n📊 RELATIONSHIP MATCHING RESULTS:")
        bidirectional = result.get('bidirectional_analysis', {})
        
        print(f"   Overall Accuracy: {result.get('overall_accuracy', 0) * 100:.2f}%")
        print(f"   E→S Relationship Coverage: {bidirectional.get('econtract_relationship_coverage', 0) * 100:.1f}%")
        print(f"   S→E Relationship Coverage: {bidirectional.get('smartcontract_relationship_coverage', 0) * 100:.1f}%")
        
        # Test individual relationship mappings
        print(f"\\n🔍 Testing individual relationship mappings:")
        test_mappings = [
            ("financial_obligation", "validates"),
            ("financial_obligation", "tracks"),
            ("obligation_assignment", "enforces"),
            ("obligation_assignment", "initializes"),
            ("party_relationship", "CONTAINS"),
            ("temporal_reference", "tracks")
        ]
        
        for e_rel, s_rel in test_mappings:
            e_relation = {"relation": e_rel}
            s_relation = {"relation": s_rel}
            technical_score = comparator._get_technical_relationship_mapping(e_relation, s_relation)
            print(f"   '{e_rel}' → '{s_rel}': {technical_score:.2f}")
        
        print(f"\\n✅ Relationship matching test completed!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_relationship_matching()
    if not success:
        sys.exit(1)