"""
Test script to verify the E-Contract and Smart Contract Analysis System
Run this script to test basic functionality before using the GUI
"""

import sys
import os
import traceback

# Add src directory to path
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    
    try:
        # Test core modules
        from src.core.preprocessor import TextPreprocessor
        from src.core.entity_extractor import EntityExtractor
        from src.core.dependency_parser import DependencyParser
        from src.core.ast_generator import ASTGenerator
        print("✓ Core modules imported successfully")
        
        # Test blockchain modules
        from src.blockchain.grammar_engine import GrammarEngine
        from src.blockchain.solidity_parser import SolidityParser
        print("✓ Blockchain modules imported successfully")
        
        # Test graph module
        from src.graph.knowledge_graph import KnowledgeGraph
        print("✓ Graph module imported successfully")
        
        # Test algorithm modules
        from src.algorithms.econtract_processor import EContractProcessor
        from src.algorithms.smartcontract_processor import SmartContractProcessor  
        from src.algorithms.comparator import ContractComparator
        print("✓ Algorithm modules imported successfully")
        
        # Test utilities
        from src.utils.file_handler import FileHandler
        from src.config.config import Config
        print("✓ Utility modules imported successfully")
        
        return True
        
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_basic_functionality():
    """Test basic functionality of key components"""
    print("\nTesting basic functionality...")
    
    try:
        # Test text preprocessing
        from src.core.preprocessor import TextPreprocessor
        preprocessor = TextPreprocessor()
        
        test_text = "This is a test contract between Party A and Party B for $1000."
        processed = preprocessor.preprocess_text(test_text)
        print(f"✓ Text preprocessing: '{test_text[:30]}...' -> {len(processed)} tokens")
        
        # Test entity extraction
        from src.core.entity_extractor import EntityExtractor
        extractor = EntityExtractor()
        entities = extractor.extract_entities(test_text)
        print(f"✓ Entity extraction: Found {len(entities)} entities")
        
        # Test knowledge graph creation
        from src.graph.knowledge_graph import KnowledgeGraph
        kg = KnowledgeGraph()
        kg.add_entity("Party A", "PERSON")
        kg.add_entity("Party B", "PERSON")
        kg.add_relationship("Party A", "contracts_with", "Party B")
        print(f"✓ Knowledge graph: Created with {kg.get_node_count()} nodes")
        
        # Test file handler
        from src.utils.file_handler import FileHandler
        fh = FileHandler()
        print("✓ File handler initialized successfully")
        
        return True
        
    except Exception as e:
        print(f"✗ Functionality test error: {e}")
        traceback.print_exc()
        return False

def test_sample_files():
    """Test processing of sample files"""
    print("\nTesting sample file processing...")
    
    try:
        # Check if sample files exist
        econtract_file = "sample_data/sample_econtract.txt"
        smartcontract_file = "sample_data/sample_smartcontract.sol"
        
        if os.path.exists(econtract_file):
            print(f"✓ Sample e-contract found: {econtract_file}")
            
            # Test e-contract processing
            from src.algorithms.econtract_processor import EContractProcessor
            processor = EContractProcessor()
            
            with open(econtract_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic processing test
            result = processor.process_contract_content(content)
            print(f"✓ E-contract processing: Generated {result['knowledge_graph'].get_node_count()} graph nodes")
            
        else:
            print(f"✗ Sample e-contract not found: {econtract_file}")
        
        if os.path.exists(smartcontract_file):
            print(f"✓ Sample smart contract found: {smartcontract_file}")
            
            # Test smart contract processing  
            from src.algorithms.smartcontract_processor import SmartContractProcessor
            processor = SmartContractProcessor()
            
            with open(smartcontract_file, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Basic processing test
            result = processor.process_contract_content(content)
            print(f"✓ Smart contract processing: Generated {result['knowledge_graph'].get_node_count()} graph nodes")
            
        else:
            print(f"✗ Sample smart contract not found: {smartcontract_file}")
            
        return True
        
    except Exception as e:
        print(f"✗ Sample file test error: {e}")
        traceback.print_exc()
        return False

def test_gui_import():
    """Test if GUI can be imported"""
    print("\nTesting GUI import...")
    
    try:
        from src.gui.main_window import MainWindow
        print("✓ GUI module imported successfully")
        print("  Note: GUI functionality requires display and user interaction")
        return True
        
    except ImportError as e:
        print(f"✗ GUI import error: {e}")
        print("  This may be due to missing tkinter or display issues")
        return False

def check_dependencies():
    """Check for optional dependencies"""
    print("\nChecking optional dependencies...")
    
    optional_deps = {
        'nltk': 'Enhanced NLP processing',
        'spacy': 'Advanced entity extraction', 
        'solcx': 'Solidity compilation',
        'matplotlib': 'Graph visualization',
        'networkx': 'Graph operations'
    }
    
    available = []
    missing = []
    
    for dep, description in optional_deps.items():
        try:
            __import__(dep)
            available.append((dep, description))
            print(f"✓ {dep}: {description}")
        except ImportError:
            missing.append((dep, description))
            print(f"- {dep}: {description} (not available)")
    
    print(f"\nDependency summary: {len(available)} available, {len(missing)} missing")
    
    if missing:
        print("\nTo install missing dependencies:")
        print("pip install " + " ".join(dep for dep, _ in missing))
    
    return len(available) > 0

def main():
    """Run all tests"""
    print("=" * 60)
    print("E-Contract and Smart Contract Analysis System - Test Suite")
    print("=" * 60)
    
    tests = [
        ("Import Tests", test_imports),
        ("Dependency Check", check_dependencies), 
        ("Basic Functionality", test_basic_functionality),
        ("Sample Files", test_sample_files),
        ("GUI Import", test_gui_import)
    ]
    
    results = []
    
    for test_name, test_func in tests:
        print(f"\n{'-' * 20} {test_name} {'-' * 20}")
        try:
            result = test_func()
            results.append((test_name, result))
        except Exception as e:
            print(f"✗ {test_name} failed with exception: {e}")
            results.append((test_name, False))
    
    # Summary
    print("\n" + "=" * 60)
    print("TEST SUMMARY")
    print("=" * 60)
    
    passed = 0
    for test_name, result in results:
        status = "PASS" if result else "FAIL"
        print(f"{test_name}: {status}")
        if result:
            passed += 1
    
    print(f"\nPassed: {passed}/{len(results)} tests")
    
    if passed == len(results):
        print("\n✓ All tests passed! The system is ready to use.")
        print("Run 'python main.py' to start the GUI application.")
    else:
        print(f"\n⚠ {len(results) - passed} tests failed. Check error messages above.")
        print("Some functionality may be limited.")
    
    print("\nFor help and documentation, see:")
    print("- README.md: System overview and installation")
    print("- docs/user_guide.md: Comprehensive user guide")
    print("- sample_data/: Example contracts for testing")

if __name__ == "__main__":
    main()