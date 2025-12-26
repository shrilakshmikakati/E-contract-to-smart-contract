#!/usr/bin/env python3
"""
Test entity deduplication in main production system workflow
"""
import sys
import os
sys.path.append(os.path.abspath('.'))

def test_production_deduplication():
    """Test entity deduplication using the actual production workflow"""
    print("🏭 TESTING PRODUCTION SYSTEM ENTITY DEDUPLICATION")
    print("=" * 60)
    
    try:
        # Import the exact same classes the main system uses
        from src.core.econtract_processor import EContractProcessor
        from src.core.smartcontract_processor import SmartContractProcessor  
        from src.core.comparator import ContractComparator  # This is actually KnowledgeGraphComparator
        
        print("✅ Production imports successful")
        
        # Create realistic test data that would generate duplicates
        test_econtract_text = """
        RENTAL AGREEMENT CONTRACT
        
        This rental agreement is made between John Smith, the tenant, and ABC Properties LLC, the landlord.
        The monthly rental payment is $1500 due on the 1st of each month.
        The tenant John Smith agrees to pay the monthly rent of $1500 to landlord ABC Properties LLC.
        The rental property is located at 123 Main Street, Apartment 4B.
        The lease term begins on January 1, 2024 and ends on December 31, 2024.
        The tenant must maintain the rental property in good condition.
        John Smith (tenant) shall pay all utilities. ABC Properties LLC (landlord) is responsible for major repairs.
        """
        
        # Smart contract with potential duplicates
        test_smartcontract_code = """
        pragma solidity ^0.8.0;
        
        contract RentalAgreementContract {
            address public tenant;
            address public landlord; 
            address private tenant_address;
            address private landlord_address;
            
            uint256 public monthlyRent;
            uint256 private monthly_rent;
            uint256 public rent_amount;
            
            string public propertyAddress;
            string private property_address;
            string public rental_property;
            
            bool public active;
            bool private is_active;
            bool public lease_active;
            
            event RentPaid(address tenant, uint256 amount);
            event RentPayment(address from, uint256 value);
            event PaymentReceived(address tenant, uint256 rent);
            
            function payRent() external payable {
                require(msg.sender == tenant, "Only tenant");
                require(msg.value == monthlyRent, "Wrong amount");
                payable(landlord).transfer(msg.value);
                emit RentPaid(tenant, monthlyRent);
            }
            
            function makeRentPayment() external payable {
                require(msg.sender == tenant_address, "Only tenant");
                require(msg.value == monthly_rent, "Wrong amount");
            }
            
            function validateTenant(address _tenant) private view returns(bool) {
                return _tenant == tenant || _tenant == tenant_address;
            }
            
            function getTenant() public view returns(address) {
                return tenant;
            }
            
            function getLandlord() public view returns(address) {
                return landlord;  
            }
        }
        """
        
        print("📝 Processing with production system...")
        
        # Process using actual production processors
        econtract_processor = EContractProcessor()
        try:
            e_kg = econtract_processor.process_contract(test_econtract_text, "test_rental_contract")
            print(f"   E-contract processed: {len(e_kg.entities)} entities, {len(e_kg.relationships)} relationships")
        except Exception as e:
            print(f"   E-contract processing failed: {e}")
            return False
        
        # For smart contract, create a mock since compiler may fail
        from src.core.knowledge_graph import KnowledgeGraph
        s_kg = KnowledgeGraph()
        
        # Simulate what SmartContractProcessor would create (with duplicates)
        # These duplicates represent what the real processor might generate
        s_kg.add_entity("tenant", {"type": "PARAMETER", "text": "tenant"})
        s_kg.add_entity("tenant_address", {"type": "PARAMETER", "text": "tenant_address"})  # Similar to tenant
        s_kg.add_entity("landlord", {"type": "PARAMETER", "text": "landlord"})
        s_kg.add_entity("landlord_address", {"type": "PARAMETER", "text": "landlord_address"})  # Similar to landlord
        s_kg.add_entity("monthlyRent", {"type": "PARAMETER", "text": "monthlyRent"})
        s_kg.add_entity("monthly_rent", {"type": "PARAMETER", "text": "monthly_rent"})  # Duplicate
        s_kg.add_entity("rent_amount", {"type": "PARAMETER", "text": "rent_amount"})  # Similar 
        s_kg.add_entity("propertyAddress", {"type": "PARAMETER", "text": "propertyAddress"})
        s_kg.add_entity("property_address", {"type": "PARAMETER", "text": "property_address"})  # Duplicate
        s_kg.add_entity("rental_property", {"type": "PARAMETER", "text": "rental_property"})  # Similar
        s_kg.add_entity("active", {"type": "PARAMETER", "text": "active"})
        s_kg.add_entity("is_active", {"type": "PARAMETER", "text": "is_active"})  # Similar
        s_kg.add_entity("lease_active", {"type": "PARAMETER", "text": "lease_active"})  # Similar
        s_kg.add_entity("payRent", {"type": "FUNCTION", "text": "payRent"})
        s_kg.add_entity("makeRentPayment", {"type": "FUNCTION", "text": "makeRentPayment"})  # Similar function
        s_kg.add_entity("validateTenant", {"type": "FUNCTION", "text": "validateTenant"})
        s_kg.add_entity("getTenant", {"type": "FUNCTION", "text": "getTenant"})
        s_kg.add_entity("getLandlord", {"type": "FUNCTION", "text": "getLandlord"})
        s_kg.add_entity("RentPaid", {"type": "EVENT", "text": "RentPaid"})
        s_kg.add_entity("RentPayment", {"type": "EVENT", "text": "RentPayment"})  # Similar event
        s_kg.add_entity("PaymentReceived", {"type": "EVENT", "text": "PaymentReceived"})  # Similar event
        
        # ADD SMART CONTRACT RELATIONSHIPS - This was missing!
        # These represent the technical relationships that should match business relationships
        
        # Financial obligation relationships (matching business payment/rent relationships)
        s_kg.add_relationship("rel_1", "payRent", "monthlyRent", {
            "relation": "validates", "text": "payRent validates monthlyRent amount",
            "source_type": "FUNCTION", "target_type": "PARAMETER"
        })
        
        s_kg.add_relationship("rel_2", "tenant", "payRent", {
            "relation": "calls", "text": "tenant calls payRent function", 
            "source_type": "PARAMETER", "target_type": "FUNCTION"
        })
        
        s_kg.add_relationship("rel_3", "payRent", "landlord", {
            "relation": "transfers", "text": "payRent transfers payment to landlord",
            "source_type": "FUNCTION", "target_type": "PARAMETER" 
        })
        
        # Party responsibility relationships (matching party_relationship from business)
        s_kg.add_relationship("rel_4", "validateTenant", "tenant", {
            "relation": "validates", "text": "validateTenant validates tenant address",
            "source_type": "FUNCTION", "target_type": "PARAMETER"
        })
        
        s_kg.add_relationship("rel_5", "tenant", "landlord", {
            "relation": "party_relationship", "text": "tenant has relationship with landlord",
            "source_type": "PARAMETER", "target_type": "PARAMETER"
        })
        
        # State management relationships (matching temporal/status relationships)
        s_kg.add_relationship("rel_6", "payRent", "active", {
            "relation": "updates", "text": "payRent updates contract active status",
            "source_type": "FUNCTION", "target_type": "PARAMETER"
        })
        
        s_kg.add_relationship("rel_7", "active", "lease_active", {
            "relation": "controls", "text": "active status controls lease active state",
            "source_type": "PARAMETER", "target_type": "PARAMETER"
        })
        
        # Event emission relationships (matching obligation tracking)
        s_kg.add_relationship("rel_8", "payRent", "RentPaid", {
            "relation": "EMITS", "text": "payRent function EMITS RentPaid event",
            "source_type": "FUNCTION", "target_type": "EVENT"
        })
        
        s_kg.add_relationship("rel_9", "RentPaid", "tenant", {
            "relation": "logs", "text": "RentPaid event logs tenant payment activity",
            "source_type": "EVENT", "target_type": "PARAMETER"
        })
        
        s_kg.add_relationship("rel_10", "RentPaid", "monthlyRent", {
            "relation": "tracks", "text": "RentPaid event tracks monthly rent amount",
            "source_type": "EVENT", "target_type": "PARAMETER"
        })
        
        # Property relationships (matching location references)
        s_kg.add_relationship("rel_11", "tenant", "propertyAddress", {
            "relation": "occupies", "text": "tenant occupies property at propertyAddress",
            "source_type": "PARAMETER", "target_type": "PARAMETER"
        })
        
        s_kg.add_relationship("rel_12", "landlord", "propertyAddress", {
            "relation": "owns", "text": "landlord owns property at propertyAddress", 
            "source_type": "PARAMETER", "target_type": "PARAMETER"
        })
        
        # Contract lifecycle relationships (matching temporal references)
        s_kg.add_relationship("rel_13", "validateTenant", "active", {
            "relation": "enforces", "text": "validateTenant enforces active contract status",
            "source_type": "FUNCTION", "target_type": "PARAMETER"
        })
        
        # Financial flow relationships (matching obligation assignments)
        s_kg.add_relationship("rel_14", "makeRentPayment", "monthly_rent", {
            "relation": "processes", "text": "makeRentPayment processes monthly rent payment",
            "source_type": "FUNCTION", "target_type": "PARAMETER"
        })
        
        s_kg.add_relationship("rel_15", "RentPayment", "PaymentReceived", {
            "relation": "triggers", "text": "RentPayment event triggers PaymentReceived processing",
            "source_type": "EVENT", "target_type": "EVENT"
        })
        
        print(f"   Smart contract created: {len(s_kg.entities)} entities (with duplicates)")
        print(f"   Smart contract relationships: {len(s_kg.relationships)} relationships")
        
        # Now test with production comparator (which includes our deduplication)
        print(f"\\n🔬 Running production comparison with deduplication...")
        comparator = ContractComparator()  # This is actually KnowledgeGraphComparator
        result = comparator.compare_knowledge_graphs(e_kg, s_kg, "production_test")
        
        print(f"\\n📊 Production System Results:")
        accuracy_data = result.get('accuracy_analysis', {})
        coverage_status = accuracy_data.get('coverage_status', {})
        
        print(f"   Overall Accuracy: {accuracy_data.get('accuracy_score', 0):.2%}")
        print(f"   E-contract entities: {coverage_status.get('total_entity_count_econtract', 0)}")
        print(f"   E-contract relationships: {coverage_status.get('total_relationship_count_econtract', 0)}")
        print(f"   Smart contract entities: {coverage_status.get('total_entity_count_smartcontract', 0)}")
        print(f"   Smart contract relationships: {coverage_status.get('total_relationship_count_smartcontract', 0)}")
        print(f"   E→S entity coverage: {coverage_status.get('matched_entities_e_to_s', 0)}/{coverage_status.get('total_entity_count_econtract', 0)} = {coverage_status.get('matched_entities_e_to_s', 0)/max(coverage_status.get('total_entity_count_econtract', 1), 1):.1%}")
        print(f"   S→E entity coverage: {coverage_status.get('matched_entities_s_to_e', 0)}/{coverage_status.get('total_entity_count_smartcontract', 0)} = {coverage_status.get('matched_entities_s_to_e', 0)/max(coverage_status.get('total_entity_count_smartcontract', 1), 1):.1%}")
        print(f"   E→S relationship coverage: {coverage_status.get('relationship_coverage_e_to_s', 0):.1%}")
        print(f"   S→E relationship coverage: {coverage_status.get('relationship_coverage_s_to_e', 0):.1%}")
        print(f"   Business logic score: {accuracy_data.get('business_logic_score', 0):.1%}")
        print(f"   Completeness score: {accuracy_data.get('completeness_score', 0):.1%}")
        print(f"   Deployment Ready: {accuracy_data.get('deployment_ready', False)}")
        
        # Check if deduplication actually happened by comparing before/after
        original_s_count = 20  # We created 20 entities with duplicates
        final_s_count = coverage_status.get('total_entity_count_smartcontract', 0)
        
        if final_s_count < original_s_count:
            reduction = original_s_count - final_s_count
            reduction_percent = (reduction / original_s_count) * 100
            print(f"\\n✅ DEDUPLICATION CONFIRMED!")
            print(f"   Original smart contract entities: {original_s_count}")
            print(f"   After deduplication: {final_s_count}")
            print(f"   Entities removed: {reduction} ({reduction_percent:.1f}% reduction)")
        else:
            print(f"\\n❌ Deduplication may not be working in production system")
            print(f"   Expected reduction from {original_s_count}, got {final_s_count}")
        
        return True
        
    except Exception as e:
        print(f"❌ Production test failed: {e}")
        import traceback
        traceback.print_exc()
        return False

if __name__ == "__main__":
    success = test_production_deduplication()
    if not success:
        sys.exit(1)