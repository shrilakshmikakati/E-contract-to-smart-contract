#!/usr/bin/env python3
"""
Test script to verify the comparison fix
"""

import sys
import os
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from core.econtract_processor import EContractProcessor
from core.smartcontract_processor import SmartContractProcessor  
from core.comparator import KnowledgeGraphComparator

def test_comparison():
    """Test the comparison functionality"""
    
    # Sample e-contract text
    econtract_text = """
    EMPLOYMENT CONTRACT
    
    This Employment Contract is entered into between ABC Company ("Company") and John Smith ("Employee").
    
    1. Position: Software Developer
    2. Salary: $80,000 per year
    3. Start Date: January 1, 2024
    4. Benefits: Health insurance, 401k matching
    5. Termination: 30 days notice required
    
    The Employee agrees to perform software development duties and maintain confidentiality.
    The Company agrees to provide salary and benefits as specified.
    """
    
    # Sample smart contract
    smart_contract = """
    pragma solidity ^0.8.0;
    
    contract EmploymentContract {
        address public company;
        address public employee;
        uint256 public salary;
        bool public isActive;
        
        constructor(address _employee, uint256 _salary) {
            company = msg.sender;
            employee = _employee;
            salary = _salary;
            isActive = true;
        }
        
        function terminate() public {
            require(msg.sender == company || msg.sender == employee, "Unauthorized");
            isActive = false;
        }
        
        function updateSalary(uint256 newSalary) public {
            require(msg.sender == company, "Only company can update salary");
            salary = newSalary;
        }
    }
    """
    
    print("=== TESTING COMPARISON FIX ===")
    
    # Process e-contract
    print("Processing e-contract...")
    econtract_processor = EContractProcessor()
    econtract_kg = econtract_processor.process_contract(econtract_text)
    print(f"E-contract: {len(econtract_kg.entities)} entities, {len(econtract_kg.relationships)} relationships")
    
    # Process smart contract  
    print("Processing smart contract...")
    smart_processor = SmartContractProcessor()
    smart_kg = smart_processor.process_contract(smart_contract)
    print(f"Smart contract: {len(smart_kg.entities)} entities, {len(smart_kg.relationships)} relationships")
    
    # Compare
    print("Running comparison...")
    comparator = KnowledgeGraphComparator()
    results = comparator.compare_knowledge_graphs(econtract_kg, smart_kg)
    
    # Print results
    print("\n=== COMPARISON RESULTS ===")
    print(f"Overall Similarity Score: {results['summary']['overall_similarity_score']:.3f}")
    print(f"Entity Matches: {results['summary']['total_entity_matches']}")
    print(f"Relationship Matches: {results['summary']['total_relation_matches']}")
    print(f"Entity Coverage (E-Contract): {results['summary']['entity_coverage_econtract']:.1f}%")
    print(f"Relationship Coverage (E-Contract): {results['summary']['relation_coverage_econtract']:.1f}%")
    
    print("\nCompliance Assessment:")
    print(f"Compliance Score: {results['compliance_assessment']['overall_compliance_score']:.3f}")
    print(f"Compliance Level: {results['compliance_assessment']['compliance_level']}")
    print(f"Is Compliant: {results['compliance_assessment']['is_compliant']}")
    
    print("\nRecommendations:")
    for i, rec in enumerate(results['recommendations'], 1):
        print(f"{i}. {rec}")
    
    print("\n=== TEST COMPLETE ===")
    return results

if __name__ == "__main__":
    test_comparison()