#!/usr/bin/env python3
"""Test enhanced relationship coverage"""

import sys
import os

# Add the project root to the path
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

from src.core.enhanced_smart_contract_generator import EnhancedSmartContractGenerator
from src.nlp.entity_extractor import EntityExtractor
from src.nlp.business_relationship_extractor import BusinessRelationshipExtractor

def test_enhanced_coverage():
    """Test actual relationship preservation without misleading metrics"""
    
    # Create instances  
    entity_extractor = EntityExtractor()
    relationship_extractor = BusinessRelationshipExtractor()
    gen = EnhancedSmartContractGenerator()
    
    # Test contract
    contract_text = """
    AGREEMENT BETWEEN Company A (located at New York) AND Company B (located at California)
    FOR SUPPLY SERVICES valued at $50,000.
    Company A agrees to provide consulting services to Company B.
    Payment due within 30 days of delivery.
    """
    
    # Extract entities and relationships
    entities = entity_extractor.extract_all_entities(contract_text)
    relationships = relationship_extractor.extract_business_relationships(contract_text, entities)
    
    # Generate smart contract
    result = gen.generate_enhanced_contract(entities, relationships, 'TEST_ENHANCED')
    
    # Only show actual results, no inflated metrics
    if isinstance(result, dict) and 'analysis' in result:
        analysis = result['analysis']
        functions = analysis.get('functions', [])
        
        actual_rel_funcs = 0
        for rel in relationships:
            # Check if this specific relationship is actually implemented
            rel_type = rel.get('relation', '')
            source = rel.get('source', '')
            target = rel.get('target', '')
            
            # Look for functions that actually implement this specific relationship
            found_implementation = False
            for func in functions:
                func_name = func.get('name', '').lower()
                func_desc = func.get('description', '').lower()
                if (rel_type.lower() in func_desc or 
                    source.lower() in func_desc or 
                    target.lower() in func_desc):
                    found_implementation = True
                    break
            
            if found_implementation:
                actual_rel_funcs += 1
        
        actual_coverage = (actual_rel_funcs / len(relationships)) * 100 if relationships else 0
        print(f"Actual relationship preservation: {actual_coverage:.1f}%")
    
    return result

if __name__ == "__main__":
    test_enhanced_coverage()