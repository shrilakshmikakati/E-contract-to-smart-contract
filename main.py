
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def setup_dependencies():
    print("Setting up dependencies...")
    
    try:
        import nltk
        essential_datasets = ['stopwords', 'punkt', 'wordnet']
        for dataset in essential_datasets:
            try:
                nltk.data.find(f'corpora/{dataset}' if dataset in ['stopwords', 'wordnet'] else f'tokenizers/{dataset}')
            except LookupError:
                print(f"Downloading NLTK {dataset}...")
                nltk.download(dataset, quiet=True)
    except ImportError:
        print("NLTK not available - using basic processing")
    
    try:
        import spacy
        spacy.load('en_core_web_sm')
        print("✓ spaCy model available")
    except (ImportError, OSError):
        print("⚠️  spaCy model not found - using fallback processing")
    
    print("Dependency setup complete.")

def launch_gui():
    print("E-CONTRACT TO SMART CONTRACT ANALYSIS SYSTEM")
    print("=" * 60)
    print("Upload e-contracts and generate smart contracts")
    print("=" * 60)
    
    setup_dependencies()
    
    try:
        from gui.main_window import MainWindow
        
        print("Starting GUI...")
        app = MainWindow()
        app.run()
        
    except Exception as e:
        print(f"❌ Error starting GUI: {e}")
        print("\nTroubleshooting:")
        print("1. Ensure all dependencies are installed: pip install -r requirements.txt")
        print("2. Check that all source files are present in src/ directory")
        print("3. Verify Python version compatibility")
        import traceback
        traceback.print_exc()
        
        input("\nPress Enter to exit...")

def main():
    
    if len(sys.argv) > 1:
        if sys.argv[1] in ['--help', '-h']:
            print("E-Contract to Smart Contract Analysis System - Enhanced Edition")
            print("Usage: python main.py")
            print("This launches the GUI interface for:")
            print("• Uploading e-contracts (.txt, .pdf, .docx, .md)")
            print("• Smart contract generation with business logic extraction")
            print("• Solidity code generation with comprehensive business logic")
            print("• Quality relationship filtering and duplicate elimination")
            print("• Compilation validation and syntax verification")
            print("\nFeatures:")
            print("  - Business logic extraction from contract text")
            print("  - Relationship preservation and implementation")
            print("  - State variables, events, and function generation")
            print("  - Solidity syntax compliance")
            print("  - Intelligent filtering of duplicates and low-quality relationships")
            return
        else:
            print("Unknown argument. Use --help for usage information.")
            return
    
    launch_gui()

if __name__ == "__main__":
    main()