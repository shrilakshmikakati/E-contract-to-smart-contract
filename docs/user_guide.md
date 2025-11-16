# User Guide - E-Contract and Smart Contract Analysis System

## Table of Contents
1. [Getting Started](#getting-started)
2. [System Overview](#system-overview)
3. [User Interface Guide](#user-interface-guide)
4. [Processing Contracts](#processing-contracts)
5. [Analyzing Results](#analyzing-results)
6. [Comparison Features](#comparison-features)
7. [Export and Visualization](#export-and-visualization)
8. [Troubleshooting](#troubleshooting)

## Getting Started

### System Requirements
- **Operating System**: Windows 10/11, macOS, or Linux
- **Python Version**: 3.8 or higher
- **Memory**: 4GB RAM minimum, 8GB recommended
- **Storage**: 1GB free space for installation and data

### Installation Steps

1. **Download and Extract**: Extract the system files to your desired directory
2. **Install Python Dependencies**:
   ```bash
   pip install -r requirements.txt
   ```
3. **Install Optional NLP Components** (for enhanced analysis):
   ```bash
   # Download NLTK data
   python -c "import nltk; nltk.download('punkt'); nltk.download('stopwords'); nltk.download('wordnet')"
   
   # Download spaCy model
   python -m spacy download en_core_web_sm
   ```

4. **Launch the Application**:
   ```bash
   python main.py
   ```

### First Run Setup

When you first run the system, it will:
- Create necessary output directories
- Initialize configuration settings
- Check for optional dependencies
- Display a welcome message with system status

## System Overview

### Core Components

The system consists of four main analysis algorithms:

1. **E-Contract Analysis**: Processes traditional contracts using NLP techniques
2. **Smart Contract Analysis**: Analyzes Solidity contracts using AST parsing  
3. **Contract Comparison**: Compares different contract types and identifies relationships
4. **Integrated Analysis**: Provides comprehensive cross-contract insights

### Supported File Types

| Contract Type | Supported Formats | Description |
|---------------|------------------|-------------|
| E-Contracts | .txt, .pdf, .docx | Traditional legal documents |
| Smart Contracts | .sol | Solidity smart contract files |
| Output Formats | .json, .csv, .png, .graphml | Analysis results and visualizations |

## User Interface Guide

### Main Window Layout

The application features a tabbed interface with the following sections:

#### 1. File Selection Panel
- **E-Contract File**: Browse and select traditional contract files
- **Smart Contract File**: Browse and select Solidity contract files
- **File Info**: Displays selected file information and format validation

#### 2. Processing Controls
- **Process E-Contract**: Runs Algorithm 1 - E-Contract knowledge graph construction
- **Process Smart Contract**: Runs Algorithm 2 - Smart contract knowledge graph construction
- **Compare Contracts**: Runs Algorithms 3 & 4 - Comparative analysis
- **Clear Results**: Resets all analysis results

#### 3. Results Tabs

**E-Contract Results Tab**:
- Entity extraction results
- Relationship mapping
- Contract structure analysis
- Knowledge graph statistics

**Smart Contract Results Tab**:
- AST structure display
- Function and variable analysis
- Contract complexity metrics
- Security considerations

**Comparison Results Tab**:
- Side-by-side contract comparison
- Similarity metrics
- Identified differences
- Compliance analysis

**Visualization Tab**:
- Interactive knowledge graph display
- Graph statistics and metrics
- Export options for graphs
- Zoom and pan controls

#### 4. Menu System

**File Menu**:
- Open recent files
- Save current session
- Export results
- Exit application

**Edit Menu**:
- Copy results to clipboard
- Clear individual result sections
- Reset all data

**View Menu**:
- Toggle result panels
- Adjust graph visualization settings
- Change font sizes

**Tools Menu**:
- Configuration settings
- System diagnostics
- Update check

**Help Menu**:
- User guide
- About information
- System requirements
- Contact support

### Status and Progress Indicators

- **Status Bar**: Shows current operation status and progress
- **Progress Bars**: Display processing progress for long-running operations
- **Activity Indicators**: Show when background processing is occurring
- **Error/Warning Alerts**: Display issues and recommendations

## Processing Contracts

### E-Contract Processing (Algorithm 1)

1. **Select Contract File**:
   - Click "Browse E-Contract"
   - Choose a .txt, .pdf, or .docx file
   - Verify file appears in the file info panel

2. **Configure Processing Options**:
   - Set NLP processing parameters (optional)
   - Choose entity extraction methods
   - Select relationship parsing options

3. **Run Processing**:
   - Click "Process E-Contract"
   - Monitor progress in the status bar
   - Wait for completion notification

4. **Review Results**:
   - Switch to "E-Contract Results" tab
   - Examine extracted entities
   - Review identified relationships
   - Check contract structure analysis

### Smart Contract Processing (Algorithm 2)

1. **Select Smart Contract**:
   - Click "Browse Smart Contract"
   - Choose a .sol Solidity file
   - Ensure file syntax is valid

2. **Configure AST Options**:
   - Set Solidity compiler version (if needed)
   - Choose analysis depth
   - Select output format preferences

3. **Run Processing**:
   - Click "Process Smart Contract"
   - Monitor AST generation progress
   - Wait for analysis completion

4. **Review Results**:
   - Switch to "Smart Contract Results" tab
   - Examine contract structure
   - Review function analysis
   - Check security metrics

### Comparison Analysis (Algorithms 3 & 4)

1. **Ensure Both Contracts Processed**:
   - Verify e-contract processing completed
   - Verify smart contract processing completed
   - Check for any processing errors

2. **Run Comparison**:
   - Click "Compare Contracts"
   - Select comparison parameters
   - Monitor comparison progress

3. **Review Comparison Results**:
   - Switch to "Comparison Results" tab
   - Examine similarity metrics
   - Review identified differences
   - Check compliance analysis

## Analyzing Results

### E-Contract Analysis Results

**Entity Extraction**:
- **Parties**: Identified contract parties (individuals, organizations)
- **Terms**: Key contract terms and conditions
- **Obligations**: Specific obligations and responsibilities
- **Dates**: Important dates and deadlines
- **Amounts**: Financial amounts and calculations
- **Conditions**: Conditional clauses and triggers

**Relationship Analysis**:
- **Dependencies**: How contract elements depend on each other
- **Hierarchies**: Structural relationships between clauses
- **References**: Cross-references within the contract
- **Implications**: Logical implications and consequences

**Structure Analysis**:
- **Sections**: Identified contract sections and subsections
- **Clauses**: Individual contract clauses and their purposes
- **Definitions**: Defined terms and their usage
- **Signatures**: Signature requirements and validation

### Smart Contract Analysis Results

**AST Structure**:
- **Contracts**: Contract definitions and inheritance
- **Functions**: Function signatures, visibility, and modifiers
- **Variables**: State variables and their types
- **Events**: Event definitions and emissions
- **Modifiers**: Access control and validation modifiers

**Function Analysis**:
- **Public Functions**: External interface functions
- **Private Functions**: Internal utility functions
- **View Functions**: Read-only functions
- **Payable Functions**: Functions that accept Ether
- **Function Complexity**: Cyclomatic complexity metrics

**Security Analysis**:
- **Access Controls**: Who can call which functions
- **Reentrancy Risks**: Potential reentrancy vulnerabilities
- **Overflow Risks**: Integer overflow possibilities
- **Gas Optimization**: Gas usage patterns and optimizations

### Comparison Analysis Results

**Similarity Metrics**:
- **Structural Similarity**: How similar the contract structures are
- **Functional Similarity**: How similar the contract purposes are
- **Entity Overlap**: Common entities between contracts
- **Relationship Overlap**: Common relationships and patterns

**Difference Analysis**:
- **Missing Elements**: Elements in one contract but not the other
- **Conflicting Elements**: Contradictory clauses or functions
- **Implementation Gaps**: E-contract clauses without smart contract implementation
- **Extra Functionality**: Smart contract functions without e-contract equivalents

**Compliance Analysis**:
- **Legal Compliance**: How well smart contract matches legal requirements
- **Business Logic**: Whether business logic is properly implemented
- **Error Handling**: How errors and exceptions are handled
- **Edge Cases**: Coverage of edge cases and unusual scenarios

## Comparison Features

### Side-by-Side Comparison

The comparison feature provides detailed analysis of relationships between e-contracts and smart contracts:

**Visual Comparison**:
- Side-by-side display of contract elements
- Color-coded similarities and differences
- Interactive navigation between related elements
- Drill-down capability for detailed analysis

**Quantitative Metrics**:
- **Similarity Score**: Overall percentage similarity (0-100%)
- **Coverage Score**: How much of e-contract is covered by smart contract
- **Compliance Score**: Regulatory compliance assessment
- **Risk Score**: Potential risk assessment

**Detailed Mappings**:
- **Clause-to-Function Mapping**: Which smart contract functions implement which e-contract clauses
- **Entity Correspondence**: How entities are represented in both contracts
- **Condition Mapping**: How conditions and requirements are implemented
- **Exception Handling**: How exceptions and edge cases are addressed

### Interactive Analysis

**Filtering Options**:
- Filter by similarity level
- Filter by element type
- Filter by compliance status
- Filter by risk level

**Search Capabilities**:
- Search across all contract elements
- Find specific terms or patterns
- Locate functions or clauses
- Cross-reference related items

**Navigation Tools**:
- Jump between related elements
- Follow dependency chains
- Trace requirement implementations
- Explore contract relationships

## Export and Visualization

### Knowledge Graph Visualization

**Interactive Features**:
- **Zoom and Pan**: Navigate large graphs easily
- **Node Selection**: Click nodes to see detailed information
- **Edge Highlighting**: Highlight relationships and dependencies
- **Layout Options**: Choose from different graph layout algorithms
- **Filtering**: Hide/show specific types of nodes or relationships

**Customization Options**:
- **Color Schemes**: Choose different color themes
- **Node Sizes**: Adjust based on importance or frequency
- **Label Display**: Toggle node and edge labels
- **Graph Density**: Adjust the complexity of displayed relationships

### Export Options

**Graph Exports**:
- **PNG/JPG**: High-resolution images for documents
- **SVG**: Vector graphics for scalable displays
- **PDF**: Publication-ready format
- **GraphML**: Standard graph format for other tools
- **GEXF**: Gephi-compatible format

**Data Exports**:
- **CSV**: Tabular data for spreadsheet analysis
- **JSON**: Structured data for further processing
- **Excel**: Formatted spreadsheets with multiple sheets
- **XML**: Structured markup for integration

**Report Generation**:
- **Summary Reports**: High-level analysis overview
- **Detailed Reports**: Comprehensive analysis results
- **Comparison Reports**: Side-by-side comparison results
- **Custom Reports**: User-defined report templates

### Batch Processing

For processing multiple contracts:

1. **Prepare File Lists**: Organize contracts in folders
2. **Configure Batch Settings**: Set processing parameters
3. **Run Batch Analysis**: Process all files automatically
4. **Review Batch Results**: Compare results across multiple contracts
5. **Generate Batch Reports**: Create comparative analysis reports

## Troubleshooting

### Common Issues and Solutions

**Installation Issues**:
- **Missing Python**: Install Python 3.8+ from python.org
- **Dependency Errors**: Run `pip install -r requirements.txt`
- **Permission Issues**: Run terminal as administrator (Windows) or use sudo (Linux/Mac)

**File Processing Issues**:
- **Unsupported Format**: Check file format is .txt, .pdf, .docx, or .sol
- **Encoding Errors**: Ensure files are UTF-8 encoded
- **Large Files**: Break large contracts into smaller sections
- **Corrupted Files**: Verify file integrity and try different source

**NLP Processing Issues**:
- **NLTK Errors**: Run NLTK download commands as shown in installation
- **spaCy Errors**: Install language model with `python -m spacy download en_core_web_sm`
- **Memory Issues**: Close other applications and try processing smaller sections

**Solidity Processing Issues**:
- **Compiler Errors**: Check Solidity syntax and pragma version
- **Version Mismatch**: Update py-solc-x or specify different compiler version
- **Complex Contracts**: Simplify contract or increase processing timeout

**GUI Issues**:
- **Slow Performance**: Reduce graph complexity or increase system memory
- **Display Issues**: Update graphics drivers and check screen resolution
- **Freezing**: Check for background processing and wait for completion

**Graph Visualization Issues**:
- **Large Graphs**: Use filtering to reduce displayed elements
- **Slow Rendering**: Decrease node count or simplify layout
- **Export Failures**: Check available disk space and file permissions

### Getting Help

**Built-in Help**:
- Use the Help menu for documentation
- Check tool tips for feature explanations
- Review error messages for specific guidance

**System Diagnostics**:
- Use Tools > System Diagnostics to check system status
- Review log files in the output directory
- Check configuration settings for issues

**Performance Optimization**:
- Close unnecessary applications
- Increase available memory
- Use SSD storage for better performance
- Process contracts in smaller batches

**Contact Support**:
- Create detailed issue reports with steps to reproduce
- Include system information and error messages
- Provide sample files (if possible) that cause issues
- Check documentation and FAQ before contacting support

---

This user guide provides comprehensive information for effectively using the E-Contract and Smart Contract Analysis System. For additional support or advanced usage scenarios, refer to the technical documentation or contact the development team.