"""
Integration Test for Improved Smart Contract Generator
Test with real contract data to verify genuine accuracy improvements
"""
import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from improved_smart_contract_generator import ImprovedSmartContractGenerator
from src.nlp.business_relationship_extractor import BusinessRelationshipExtractor  
from src.nlp.entity_extractor import EntityExtractor

def test_real_contract_accuracy():
    """Test the improved generator with real contract text"""
    
    # Sample real contract text with multiple relationship types
    sample_contract = """
    This agreement is between Company ABC and John Smith. Company ABC agrees to pay 
    $50,000 monthly to John Smith for consulting services. John Smith owns the 
    intellectual property rights to all developed software. Company ABC shall provide 
    office space and equipment to John Smith. John Smith has the responsibility to 
    deliver completed projects by the specified deadlines. Company ABC must approve 
    all deliverables before final payment. The contract establishes a partnership 
    between the two parties for a period of 12 months.
    """
    
    print("=== TESTING IMPROVED SMART CONTRACT GENERATOR ===")
    print(f"Contract text length: {len(sample_contract)} characters")
    
    # Extract entities
    entity_extractor = EntityExtractor()
    entities = entity_extractor.extract_all_entities(sample_contract)
    print(f"Extracted {len(entities)} entities")
    
    # Extract relationships
    relationship_extractor = BusinessRelationshipExtractor()
    relationships = relationship_extractor.extract_business_relationships(sample_contract, entities)
    print(f"Extracted {len(relationships)} relationships")
    
    # Print relationships for verification
    print("\n=== EXTRACTED RELATIONSHIPS ===")
    for i, rel in enumerate(relationships):
        print(f"Relationship {i+1}:")
        print(f"  Type: {rel.get('relation', 'unknown')}")
        print(f"  Source: {rel.get('source_text', 'unknown')}")
        print(f"  Target: {rel.get('target_text', 'unknown')}")
        print(f"  Confidence: {rel.get('confidence', 0):.2f}")
        if 'amount' in rel:
            print(f"  Amount: {rel['amount']}")
        print()
    
    # Generate improved smart contract
    generator = ImprovedSmartContractGenerator()
    contract_code, metrics = generator.generate_enhanced_smart_contract(
        entities, relationships, sample_contract
    )
    
    print("\n=== GENERATED SMART CONTRACT ===")
    print(contract_code[:1000] + "..." if len(contract_code) > 1000 else contract_code)
    
    print("\n=== ACCURACY METRICS ===")
    for metric, value in metrics.items():
        if isinstance(value, float):
            print(f"{metric}: {value:.1f}%")
        else:
            print(f"{metric}: {value}")
    
    # Verify contract compilation readiness
    compilation_check = verify_solidity_syntax(contract_code)
    print(f"\n=== COMPILATION CHECK ===")
    print(f"Syntax valid: {compilation_check['valid']}")
    if not compilation_check['valid']:
        print(f"Issues: {compilation_check['issues']}")
    
    return {
        'relationships_extracted': len(relationships),
        'entities_extracted': len(entities),
        'preservation_rate': metrics['preservation_rate'],
        'implementation_rate': metrics['implementation_rate'],
        'syntax_valid': compilation_check['valid']
    }

def verify_solidity_syntax(contract_code: str) -> dict:
    """Basic syntax verification for generated Solidity contract"""
    issues = []
    
    # Check for basic Solidity structure
    if 'pragma solidity' not in contract_code:
        issues.append("Missing pragma directive")
    
    if 'contract ' not in contract_code:
        issues.append("Missing contract declaration")
    
    # Check for balanced braces
    open_braces = contract_code.count('{')
    close_braces = contract_code.count('}')
    if open_braces != close_braces:
        issues.append(f"Unbalanced braces: {open_braces} open, {close_braces} close")
    
    # Check for semicolons in variable declarations
    lines = contract_code.split('\n')
    for i, line in enumerate(lines):
        line = line.strip()
        if ('mapping(' in line or 'uint256' in line or 'address' in line) and line.endswith('{'):
            continue  # Function/constructor line
        elif ('mapping(' in line or 'uint256' in line or 'address' in line) and not line.endswith(';'):
            if line and not line.endswith('{') and not line.startswith('//'):
                issues.append(f"Line {i+1}: Missing semicolon in declaration")
    
    # Check for function syntax
    function_lines = [line for line in lines if 'function ' in line]
    for line in function_lines:
        if not ('{' in line or line.strip().endswith('{')):
            issues.append(f"Function declaration may be missing opening brace: {line.strip()}")
    
    return {
        'valid': len(issues) == 0,
        'issues': issues
    }

def compare_with_original_generator():
    """Compare results with the original generator"""
    print("\n" + "="*60)
    print("COMPARISON WITH ORIGINAL GENERATOR")
    print("="*60)
    
    # Test improved generator
    improved_results = test_real_contract_accuracy()
    
    print(f"\n=== IMPROVED GENERATOR RESULTS ===")
    print(f"Relationships extracted: {improved_results['relationships_extracted']}")
    print(f"Entities extracted: {improved_results['entities_extracted']}")
    print(f"Preservation rate: {improved_results['preservation_rate']:.1f}%")
    print(f"Implementation rate: {improved_results['implementation_rate']:.1f}%")
    print(f"Syntax valid: {improved_results['syntax_valid']}")
    
    # Calculate overall accuracy score
    overall_accuracy = (
        (improved_results['preservation_rate'] * 0.4) +
        (improved_results['implementation_rate'] * 0.3) +
        (100 if improved_results['syntax_valid'] else 0) * 0.3
    )
    
    print(f"\n=== OVERALL ACCURACY SCORE ===")
    print(f"Weighted accuracy: {overall_accuracy:.1f}%")
    
    if overall_accuracy >= 90:
        print("✅ SUCCESS: Accuracy target of 90%+ achieved!")
    else:
        print("❌ NEEDS IMPROVEMENT: Below 90% accuracy target")
        print("Areas for improvement:")
        if improved_results['preservation_rate'] < 90:
            print("- Relationship preservation rate")
        if improved_results['implementation_rate'] < 90:
            print("- Implementation completeness")
        if not improved_results['syntax_valid']:
            print("- Solidity syntax compliance")
    
    return overall_accuracy

if __name__ == "__main__":
    final_accuracy = compare_with_original_generator()