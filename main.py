"""
Main application entry point for E-Contract and Smart Contract Analysis System
"""

import sys
import os

# Add the src directory to the path so we can import our modules
sys.path.insert(0, os.path.join(os.path.dirname(__file__), 'src'))

def setup_dependencies():
    """Setup and verify dependencies"""
    print("Checking and setting up dependencies...")
    
    # Download NLTK data if needed
    try:
        import nltk
        try:
            nltk.data.find('corpora/stopwords')
        except LookupError:
            print("Downloading NLTK data...")
            nltk.download('stopwords', quiet=True)
            nltk.download('punkt', quiet=True)
            nltk.download('wordnet', quiet=True)
            nltk.download('averaged_perceptron_tagger', quiet=True)
    except ImportError:
        print("NLTK not available. Some NLP features will be limited.")
    
    # Check spaCy model
    try:
        import spacy
        try:
            nlp = spacy.load('en_core_web_sm')
            print("✓ spaCy model available")
        except OSError:
            print("spaCy model 'en_core_web_sm' not found. Run: python -m spacy download en_core_web_sm")
    except ImportError:
        print("spaCy not available. Some NLP features will be limited.")
    
    print("Dependency setup complete.")

try:
    from src.gui.main_window import MainWindow
except ImportError as e:
    print(f"Error importing GUI modules: {e}")
    print("Please ensure all required dependencies are installed:")
    print("- pip install tkinter (usually included with Python)")
    print("- pip install matplotlib")
    print("- pip install networkx")
    print("- pip install numpy")
    print("\nOptional dependencies for enhanced functionality:")
    print("- pip install nltk")
    print("- pip install spacy")
    print("- pip install py-solc-x")
    sys.exit(1)

def main():
    """Main entry point for the application"""
    
    print("Starting E-Contract and Smart Contract Analysis System...")
    print("=" * 60)
    
    # Setup dependencies
    setup_dependencies()
    
    try:
        # Create and run the main application
        app = MainWindow()
        app.run()
        
    except Exception as e:
        print(f"Error starting application: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

if __name__ == "__main__":
    main()