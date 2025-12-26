#!/usr/bin/env python3
"""
Test script to check the comparison functionality after fixes
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_comparison_system():
    """Test the enhanced comparison system"""
    print("🧪 TESTING ENHANCED COMPARISON SYSTEM")
    print("=" * 50)
    
    try:
        from src.core.econtract_processor import EContractProcessor
        from src.core.smartcontract_processor import SmartContractProcessor
        from src.core.comparator import ContractComparator
        
        print("✅ All imports successful")
        
        # Create simple test data
        test_econtract_text = """
        This rental agreement is between John Smith (tenant) and ABC Properties (landlord).
        The monthly rent is $1200 payable on the 1st of each month.
        The lease term begins January 1, 2024 and ends December 31, 2024.
        The tenant shall maintain the property in good condition.
        """
        
        test_smartcontract_code = """
        pragma solidity ^0.8.0;
        
        contract RentalAgreement {
            address public tenant;
            address public landlord;
            uint256 public monthlyRent;
            bool public active;
            
            constructor(address _tenant, address _landlord, uint256 _monthlyRent) {
                tenant = _tenant;
                landlord = _landlord;
                monthlyRent = _monthlyRent;
                active = true;
            }
            
            function payRent() external payable {
                require(msg.sender == tenant, "Only tenant can pay rent");
                require(msg.value == monthlyRent, "Incorrect rent amount");
            }
        }
        """
        
        print("📝 Processing test E-contract...")
        econtract_processor = EContractProcessor()
        e_kg = econtract_processor.process_contract(test_econtract_text, "test_econtract")
        
        print(f"   E-contract entities: {len(e_kg.entities)}")
        print(f"   E-contract relationships: {len(e_kg.relationships)}")
        
        print("📝 Processing test Smart contract...")
        smartcontract_processor = SmartContractProcessor()
        s_kg = smartcontract_processor.process_contract(test_smartcontract_code, "test_smartcontract")
        
        print(f"   Smart contract entities: {len(s_kg.entities)}")
        print(f"   Smart contract relationships: {len(s_kg.relationships)}")
        
        print("🔍 Running bidirectional comparison...")
        comparator = ContractComparator()
        comparison_results = comparator.compare_knowledge_graphs(e_kg, s_kg, "test_comparison")
        
        print("📊 COMPARISON RESULTS:")
        accuracy_data = comparison_results.get('accuracy_analysis', {})
        print(f"   Overall Accuracy: {accuracy_data.get('accuracy_score', 0):.2%}")
        print(f"   Base Accuracy: {accuracy_data.get('base_accuracy_score', 0):.2%}")
        print(f"   Coverage Penalty: {accuracy_data.get('critical_coverage_penalty', 1.0):.2%}")
        print(f"   Entity Coverage (E→S): {accuracy_data.get('entity_coverage_e_to_s', 0):.2%}")
        print(f"   Entity Coverage (S→E): {accuracy_data.get('entity_coverage_s_to_e', 0):.2%}")
        print(f"   Deployment Ready: {accuracy_data.get('deployment_ready', False)}")
        
        coverage_status = accuracy_data.get('coverage_status', {})
        if coverage_status:
            print(f"   E-contract entities: {coverage_status.get('total_entity_count_econtract', 0)}")
            print(f"   Smart contract entities: {coverage_status.get('total_entity_count_smartcontract', 0)}")
            print(f"   Matched entities: {coverage_status.get('matched_entities_e_to_s', 0)}")
        
        print("\n✅ Test completed successfully!")
        return True
        
    except Exception as e:
        print(f"❌ Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_comparison_system()
    if not success:
        sys.exit(1)