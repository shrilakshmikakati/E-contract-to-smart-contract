"""
Simple test for enhanced E-contract analysis system
"""

import sys
from pathlib import Path

# Add the project root to the Python path
project_root = Path(__file__).parent
sys.path.insert(0, str(project_root))

from src.core.econtract_processor import EContractProcessor
from src.core.enhanced_smart_contract_generator import EnhancedSmartContractGenerator

def test_simple_enhanced():
    """Test the enhanced system simply"""
    
    # Sample rental contract text
    contract_text = """
    This Rental Agreement is between ABC Corporation (Landlord) and John Doe (Tenant).
    
    The Landlord owns the property at 123 Main Street, London.
    The Tenant agrees to pay monthly rent of $2000 to the Landlord.
    The lease starts on January 1, 2024 and ends on December 31, 2024.
    The Tenant must maintain the property in good condition.
    A security deposit of $4000 is required.
    """
    
    print("TESTING ENHANCED E-CONTRACT ANALYSIS SYSTEM")
    print("=" * 60)
    
    # Step 1: Process E-contract
    print("Step 1: Processing E-contract with enhanced extraction...")
    
    econtract_processor = EContractProcessor()
    e_kg = econtract_processor.process_contract(contract_text, "test_rental")
    
    print(f"Entities extracted: {len(e_kg.entities)}")
    print(f"Relationships extracted: {len(e_kg.relationships)}")
    print(f"Graph density: {e_kg.calculate_density():.3f}")
    
    # Display relationships
    print("\nExtracted Relationships:")
    for rel_id, rel_data in e_kg.relationships.items():
        source_entity = e_kg.entities.get(rel_data['source'], {})
        target_entity = e_kg.entities.get(rel_data['target'], {})
        source_text = source_entity.get('text', rel_data.get('source_text', 'Unknown'))
        target_text = target_entity.get('text', rel_data.get('target_text', 'Unknown'))
        
        print(f"  - {source_text} --[{rel_data['relation']}]--> {target_text}")
        print(f"    Confidence: {rel_data.get('confidence', 0):.2f}")
    
    # Step 2: Generate smart contract
    print("\nStep 2: Generating enhanced smart contract...")
    
    enhanced_generator = EnhancedSmartContractGenerator()
    
    # Convert to list format
    entities_list = [{'id': eid, **data} for eid, data in e_kg.entities.items()]
    relationships_list = [{'id': rid, **data} for rid, data in e_kg.relationships.items()]
    
    smart_contract_code = enhanced_generator.generate_enhanced_contract(
        entities_list, relationships_list, "RentalAgreement"
    )
    
    print(f"Contract lines: {smart_contract_code.count(chr(10)) + 1}")
    print(f"Functions: {smart_contract_code.count('function ')}")
    print(f"Events: {smart_contract_code.count('event ')}")
    
    print("\nGenerated Smart Contract:")
    print("-" * 40)
    print(smart_contract_code)
    
    print("\nSUMMARY:")
    print(f"- E-contract relationships improved: 0 -> {len(e_kg.relationships)}")
    print(f"- Smart contract enhanced with business logic")
    print(f"- Entity matching algorithm ready for testing")
    
    return e_kg, smart_contract_code

if __name__ == "__main__":
    test_simple_enhanced()