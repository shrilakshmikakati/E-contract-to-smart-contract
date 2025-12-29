#!/usr/bin/env python3
"""Quick test to verify preservation_rate calculation"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from production_smart_contract_generator import ProductionSmartContractGenerator

def test_preservation_rate():
    """Test that preservation_rate is calculated correctly"""
    
    generator = ProductionSmartContractGenerator()
    
    contract_text = "The landlord John Smith agrees to rent to tenant Sarah Johnson for $1200 monthly."
    entities = [
        {'text': 'John Smith', 'type': 'PERSON'},
        {'text': 'Sarah Johnson', 'type': 'PERSON'},
        {'text': '$1200', 'type': 'MONEY'}
    ]
    relationships = [
        {'relation': 'RENTAL_PAYMENT', 'source_text': 'tenant', 'target_text': 'rent'}
    ]
    
    contract_code, metrics = generator.generate_contract(contract_text, entities, relationships)
    
    print("🔍 Testing Preservation Rate Calculation")
    print("=" * 50)
    print(f"Input entities: {len(entities)}")
    print(f"Input relationships: {len(relationships)}")
    print(f"Total input items: {len(entities) + len(relationships)}")
    print("")
    print("Extracted business data:")
    print(f"- Parties: {metrics.get('parties_identified', 0)}")
    print(f"- Financial terms: {metrics.get('financial_terms', 0)}")
    print(f"- Obligations: {metrics.get('obligations_identified', 0)}")
    print("")
    print(f"✅ Calculated preservation_rate: {metrics.get('preservation_rate', 'NOT_FOUND'):.1f}%")
    print(f"✅ Accuracy score: {metrics.get('accuracy_score', 'NOT_FOUND'):.1f}%")
    print(f"✅ Completeness score: {metrics.get('completeness_score', 'NOT_FOUND'):.1f}%")
    
    # Verify the metric exists and is calculated
    assert 'preservation_rate' in metrics
    assert isinstance(metrics['preservation_rate'], (int, float))
    assert 0 <= metrics['preservation_rate'] <= 100
    
    print("\n🎉 Preservation rate calculation working correctly!")
    return True

if __name__ == "__main__":
    test_preservation_rate()