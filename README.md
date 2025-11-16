# E-Contract and Smart Contract Analysis System

This project implements a comprehensive system for analyzing and comparing e-contracts with smart contracts using knowledge graphs, NLP techniques, and Abstract Syntax Tree (AST) parsing.

## Features

- **E-Contract Analysis**: Preprocessing, entity extraction, and relationship identification using NLP
- **Smart Contract Analysis**: AST generation, grammar-driven parsing, and semantic extraction
- **Knowledge Graph Construction**: Building formal representations for both contract types
- **Comparative Analysis**: Identifying similarities, differences, and discrepancies
- **GUI Interface**: User-friendly graphical interface for interaction and visualization

## Project Structure

```
E-contact/
├── src/
│   ├── core/
│   │   ├── econtract_processor.py     # E-contract processing (Algorithm 1)
│   │   ├── smartcontract_processor.py # Smart contract processing (Algorithm 2)
│   │   ├── knowledge_graph.py         # Knowledge graph construction
│   │   └── comparator.py              # Graph comparison (Algorithm 3 & 4)
│   ├── nlp/
│   │   ├── preprocessor.py            # Text preprocessing
│   │   ├── entity_extractor.py        # Entity extraction
│   │   └── dependency_parser.py       # Dependency parsing
│   ├── blockchain/
│   │   ├── ast_generator.py           # AST generation
│   │   ├── solidity_parser.py         # Solidity code parsing
│   │   └── grammar_engine.py          # Grammar-driven translation
│   ├── gui/
│   │   ├── main_window.py             # Main GUI application
│   │   ├── contract_viewer.py         # Contract display components
│   │   ├── graph_visualizer.py        # Graph visualization
│   │   └── comparison_panel.py        # Comparison results display
│   └── utils/
│       ├── file_handler.py            # File operations
│       └── config.py                  # Configuration settings
├── data/
│   ├── sample_contracts/              # Sample e-contracts
│   ├── sample_smart_contracts/        # Sample Solidity files
│   └── outputs/                       # Generated graphs and reports
├── tests/
│   └── test_*.py                      # Unit tests
├── docs/
│   └── user_guide.md                  # Documentation
├── requirements.txt                   # Dependencies
└── main.py                           # Application entry point
```

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd E-contact
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Download required NLP models:
```bash
python -m spacy download en_core_web_sm
python -c "import nltk; nltk.download('punkt'); nltk.download('averaged_perceptron_tagger'); nltk.download('wordnet')"
```

## Usage

Run the main application:
```bash
python main.py
```

## Algorithms Implemented

1. **Algorithm 1**: E-Contract Knowledge Graph Construction
2. **Algorithm 2**: Smart Contract Knowledge Graph Construction  
3. **Algorithm 3**: Compare Knowledge Graphs
4. **Algorithm 4**: Integrated Contract Analysis and Comparison

## Research Contributions

This system addresses key challenges in contract analysis:
- **Complexity Discrepancy**: Captures complexities in smart contract implementations
- **Regulatory Compliance**: Ensures adherence to legal regulations
- **Semantic Alignment**: Accurate semantic alignment between contract types