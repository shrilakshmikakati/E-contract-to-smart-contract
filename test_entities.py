"""
Test entity extraction directly to see what's happening
"""

# Test with minimal contract text
def test_entity_extraction():
    print("🔍 TESTING ENTITY EXTRACTION")
    print("=" * 40)
    
    # Simple test contract
    test_contract = """
    SERVICE AGREEMENT
    
    Party A: ABC Corporation
    Party B: John Smith
    Service: Web Development
    Payment: $5000
    Duration: 3 months
    """
    
    print(f"Test contract: {test_contract.strip()}")
    print()
    
    # Test different entity extraction methods
    
    # 1. Test spaCy if available
    try:
        import spacy
        print("Testing spaCy entity extraction:")
        try:
            nlp = spacy.load('en_core_web_sm')
            doc = nlp(test_contract)
            entities = [(ent.text, ent.label_) for ent in doc.ents]
            print(f"  spaCy entities: {entities}")
        except OSError:
            print("  spaCy model not available")
    except ImportError:
        print("  spaCy not available")
    
    # 2. Test NLTK
    try:
        import nltk
        from nltk import ne_chunk, pos_tag, word_tokenize
        print("\nTesting NLTK entity extraction:")
        try:
            tokens = word_tokenize(test_contract)
            pos_tags = pos_tag(tokens)
            entities = ne_chunk(pos_tags)
            nltk_entities = []
            for chunk in entities:
                if hasattr(chunk, 'label'):
                    entity_text = ' '.join([token for token, pos in chunk.leaves()])
                    nltk_entities.append((entity_text, chunk.label()))
            print(f"  NLTK entities: {nltk_entities}")
        except Exception as e:
            print(f"  NLTK error: {e}")
    except ImportError:
        print("  NLTK not available")
    
    # 3. Test regex patterns
    import re
    print("\nTesting regex entity extraction:")
    
    # Money patterns
    money_pattern = r'\$[\d,]+(?:\.\d{2})?'
    money_entities = re.findall(money_pattern, test_contract)
    print(f"  Money entities: {money_entities}")
    
    # Organization patterns
    org_pattern = r'(?:Corporation|Corp|Inc|LLC|Company|Ltd)'
    org_entities = re.findall(r'\b\w+\s+' + org_pattern, test_contract)
    print(f"  Organization entities: {org_entities}")
    
    # Email patterns
    email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
    email_entities = re.findall(email_pattern, test_contract)
    print(f"  Email entities: {email_entities}")
    
    # 4. Test domain-specific extraction
    print("\nTesting domain-specific extraction:")
    
    # Contract parties
    party_keywords = ['Party A:', 'Party B:', 'Client:', 'Provider:', 'Contractor:']
    parties = []
    for keyword in party_keywords:
        if keyword in test_contract:
            # Extract text after the keyword
            lines = test_contract.split('\n')
            for line in lines:
                if keyword in line:
                    party = line.split(keyword)[1].strip()
                    if party:
                        parties.append(party)
    print(f"  Party entities: {parties}")
    
    # Contract terms
    term_keywords = ['Service:', 'Payment:', 'Duration:', 'Amount:', 'Fee:']
    terms = []
    for keyword in term_keywords:
        if keyword in test_contract:
            lines = test_contract.split('\n')
            for line in lines:
                if keyword in line:
                    term = line.split(keyword)[1].strip()
                    if term:
                        terms.append(term)
    print(f"  Term entities: {terms}")
    
    print(f"\n💡 ENTITY EXTRACTION SUMMARY:")
    print("Different methods extract different types of entities")
    print("This explains why entity counts vary between processing methods")

def test_smart_contract_generation():
    print(f"\n🔍 TESTING SMART CONTRACT GENERATION")
    print("=" * 40)
    
    # Simple smart contract template
    smart_contract = """
    pragma solidity ^0.8.0;
    
    contract ServiceAgreement {
        address public client;
        address public provider;
        uint256 public amount;
        bool public completed;
        
        constructor(address _client, address _provider, uint256 _amount) {
            client = _client;
            provider = _provider;
            amount = _amount;
            completed = false;
        }
        
        function completeService() public {
            require(msg.sender == provider, "Only provider can complete");
            completed = true;
        }
    }
    """
    
    print("Smart contract code:")
    print(smart_contract.strip())
    
    # Test what entities can be extracted from smart contract
    print(f"\n🔍 SMART CONTRACT ENTITY EXTRACTION:")
    print("=" * 35)
    
    # Extract Solidity identifiers
    import re
    
    # Variables
    var_pattern = r'\b(?:address|uint256|bool|string)\s+(?:public\s+)?(\w+)'
    variables = re.findall(var_pattern, smart_contract)
    print(f"Variables: {variables}")
    
    # Functions
    func_pattern = r'function\s+(\w+)'
    functions = re.findall(func_pattern, smart_contract)
    print(f"Functions: {functions}")
    
    # Contract name
    contract_pattern = r'contract\s+(\w+)'
    contracts = re.findall(contract_pattern, smart_contract)
    print(f"Contract names: {contracts}")
    
    print(f"\n💡 SMART CONTRACT ENTITY SUMMARY:")
    print("Smart contracts contain code identifiers, not business terms")
    print("This creates a semantic gap with e-contract entities")

if __name__ == "__main__":
    test_entity_extraction()
    test_smart_contract_generation()
    
    print(f"\n🎯 ROOT CAUSE ANALYSIS:")
    print("=" * 25)
    print("1. E-contracts extract business entities: 'ABC Corporation', '$5000', 'John Smith'")
    print("2. Smart contracts extract code entities: 'client', 'amount', 'provider'") 
    print("3. No semantic bridge connects 'ABC Corporation' to 'client'")
    print("4. Text similarity between 'ABC Corporation' and 'client' is ~0%")
    print("5. Result: 0% entity matches despite sophisticated extraction")
    
    print(f"\n🔧 SOLUTION REQUIREMENTS:")
    print("=" * 25)
    print("1. Map business entities to code variables during generation")
    print("2. Store mapping metadata to enable reverse lookups")
    print("3. Use semantic similarity instead of text matching")
    print("4. Add entity type normalization")
    print("5. Implement business-to-code entity mapping rules")