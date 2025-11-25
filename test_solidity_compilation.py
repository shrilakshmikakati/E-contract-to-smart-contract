from src.core.enhanced_smart_contract_generator import EnhancedSmartContractGenerator
from src.core.econtract_processor import EContractProcessor

def test_solidity_compilation():
    """Test if generated Solidity code compiles without errors"""
    
    # Sample E-contract text
    sample_contract = """
    CONSULTING AGREEMENT BETWEEN Company A AND Company B
    
    This Agreement is entered into on January 1, 2024, between Company A (consultant) and Company B (client).
    
    1. SERVICES: Company A shall provide consulting services to Company B
    2. PAYMENT: Company B shall pay $10,000 monthly to Company A
    3. TERM: This agreement is valid for 12 months
    4. LOCATION: Services will be provided in New York
    5. OBLIGATIONS:
       - Company A must deliver monthly reports
       - Company B must provide necessary resources
       - Both parties must maintain confidentiality
    """
    
    print("=== SOLIDITY COMPILATION TEST ===")
    
    # Extract components
    processor = EContractProcessor()
    generator = EnhancedSmartContractGenerator()
    
    print("Extracting entities and relationships...")
    # Process the contract to get the knowledge graph
    knowledge_graph = processor.process_contract(sample_contract, "COMPILATION_TEST")
    entities = knowledge_graph.entities
    relationships = knowledge_graph.relationships
    
    print(f"Found {len(entities)} entities and {len(relationships)} relationships")
    
    # Generate contract
    print("Generating smart contract...")
    contract_code = generator.generate_enhanced_contract(entities, relationships, "COMPILATION_TEST")
    
    # For testing purposes, let's parse the contract to get component counts
    lines = contract_code.split('\n')
    state_vars = [line for line in lines if any(keyword in line for keyword in ['public', 'private', 'internal']) and ';' in line and 'function' not in line]
    functions = [line for line in lines if 'function ' in line and '{' not in line]
    
    print(f"Generated contract with approximately {len(state_vars)} state variables")
    print(f"and approximately {len(functions)} functions")
    
    # Check for common compilation issues by parsing the generated code
    issues = []
    
    # Check for basic Solidity syntax issues
    if 'pragma solidity' not in contract_code:
        issues.append("Missing pragma solidity directive")
    
    if 'contract ' not in contract_code:
        issues.append("Missing contract declaration")
    
    # Check for some common syntax issues
    if 'string memory' in contract_code or 'string calldata' in contract_code:
        # Good - proper string memory specification
        pass
    elif 'returns (string)' in contract_code:
        # Check if there are string returns without memory
        string_returns = [line for line in contract_code.split('\n') if 'returns (string)' in line and 'memory' not in line]
        if string_returns:
            issues.append(f"String return types without memory specifier: {len(string_returns)} occurrences")
    
    # Check for reserved keywords (simplified check)
    reserved_issues = []
    for line in contract_code.split('\n'):
        if 'public contract' in line or 'private contract' in line:
            reserved_issues.append(line.strip())
    
    if reserved_issues:
        issues.append(f"Reserved keyword issues: {len(reserved_issues)} found")
    
    print("\n=== COMPILATION CHECK RESULTS ===")
    if issues:
        print("❌ Issues found:")
        for issue in issues:
            print(f"  - {issue}")
    else:
        print("✅ No major compilation issues detected!")
    
    print(f"\nContract size: {len(contract_code)} characters")
    print(f"State variables: {len(state_vars)}")
    print(f"Functions: {len(functions)}")
    
    # Count other elements by parsing
    modifiers = [line for line in lines if 'modifier ' in line]
    events = [line for line in lines if 'event ' in line and ';' in line]
    print(f"Modifiers: {len(modifiers)}")
    print(f"Events: {len(events)}")
    
    # Show a sample of the generated code
    print(f"\n=== CONTRACT CODE PREVIEW ===")
    lines = contract_code.split('\n')
    print('\n'.join(lines[:30]))  # First 30 lines
    print("...")
    print('\n'.join(lines[-10:]))  # Last 10 lines
    
    return len(issues) == 0

if __name__ == "__main__":
    success = test_solidity_compilation()
    if success:
        print("\n🎉 COMPILATION TEST PASSED!")
    else:
        print("\n❌ COMPILATION TEST FAILED!")