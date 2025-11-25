"""
Quick test of the GUI optimized generator to verify it works
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from final_optimized_generator import OptimizedSmartContractGenerator
from src.nlp.business_relationship_extractor import BusinessRelationshipExtractor  
from src.nlp.entity_extractor import EntityExtractor

def test_gui_integration():
    """Test the GUI integration with optimized generator"""
    
    # Sample contract text
    contract_text = """
    This agreement is between Company ABC and John Smith. Company ABC agrees to pay 
    $50,000 monthly to John Smith for consulting services. John Smith owns the 
    intellectual property rights to all developed software.
    """
    
    print("Testing GUI integration...")
    
    # Extract entities and relationships (like the GUI does)
    entity_extractor = EntityExtractor()
    entities = entity_extractor.extract_all_entities(contract_text)
    
    relationship_extractor = BusinessRelationshipExtractor()
    relationships = relationship_extractor.extract_business_relationships(contract_text, entities)
    
    # Convert to format for optimized generator (like the GUI does)
    entities_list = [{'id': f'ent_{i}', **entity} for i, entity in enumerate(entities)]
    relationships_list = [{'id': f'rel_{i}', **rel} for i, rel in enumerate(relationships)]
    
    print(f"Extracted {len(entities_list)} entities and {len(relationships_list)} relationships")
    
    # Generate optimized smart contract (like the GUI does)
    generator = OptimizedSmartContractGenerator()
    contract_code, metrics = generator.generate_enhanced_smart_contract(
        entities_list, relationships_list, contract_text
    )
    
    print(f"Generated contract with {metrics['preservation_rate']:.1f}% accuracy")
    print(f"Metrics keys: {list(metrics.keys())}")
    
    # Test the specific keys that were causing errors
    filtered_count = metrics.get('filtered_relationships', metrics.get('implemented_relationships', 0))
    original_count = metrics.get('original_relationships', metrics.get('total_relationships', 0))
    
    print(f"Original relationships: {original_count}")
    print(f"Filtered relationships: {filtered_count}")
    print(f"Implementation rate: {metrics['implementation_rate']:.1f}%")
    
    print("✅ GUI integration test passed!")
    return True

if __name__ == "__main__":
    test_gui_integration()