"""
Test e-contract processing directly
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from src.core.econtract_processor import EContractProcessor

def test_processing():
    processor = EContractProcessor()
    
    test_text = """
    RENTAL AGREEMENT
    
    This rental agreement is entered into on January 1, 2024, between John Smith (Owner) and Alice Johnson (Tenant).
    
    PROPERTY: The property located at 123 Main Street, Anytown, USA shall be rented to the tenant.
    
    RENT: The monthly rent is $1,500 due on the 1st day of each month.
    """
    
    try:
        print("Starting e-contract processing test...")
        result = processor.process_contract(test_text)
        print(f"Success! Entities: {len(result.entities)}, Relationships: {len(result.relationships)}")
        return result
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()
        return None

if __name__ == "__main__":
    test_processing()