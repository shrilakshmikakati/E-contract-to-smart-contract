
import os

class Config:
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
    DATA_DIR = os.path.join(BASE_DIR, 'data')
    SAMPLE_CONTRACTS_DIR = os.path.join(DATA_DIR, 'sample_contracts')
    SAMPLE_SMART_CONTRACTS_DIR = os.path.join(DATA_DIR, 'sample_smart_contracts')
    OUTPUTS_DIR = os.path.join(DATA_DIR, 'outputs')
    
    NLP_MODEL = 'en_core_web_sm'
    STOPWORDS = ['the', 'a', 'an', 'and', 'or', 'but', 'in', 'on', 'at', 'to', 'for', 'of', 'with', 'by']
    
    ENTITY_TYPES = [
        'PERSON',      # Parties involved
        'ORG',         # Organizations
        'DATE',        # Dates and deadlines
        'MONEY',       # Financial terms
        'CARDINAL',    # Numbers
        'GPE',         # Geographical entities
        'LAW',         # Legal references
        'EVENT',       # Contract events
    ]
    
    SOLIDITY_NODE_TYPES = [
        'ContractDefinition',
        'FunctionDefinition', 
        'VariableDeclaration',
        'ModifierDefinition',
        'EventDefinition',
        'StructDefinition',
        'EnumDefinition',
        'IfStatement',
        'WhileStatement',
        'ForStatement',
        'Return',
        'Assignment',
        'BinaryOperation',
        'UnaryOperation',
        'Identifier',
        'Literal'
    ]
    
    GRAPH_LAYOUT = 'spring'  # Options: spring, circular, random, shell
    NODE_SIZE_RANGE = (100, 1000)
    EDGE_WIDTH_RANGE = (0.5, 3.0)
    
    SIMILARITY_THRESHOLD = 0.7
    ENTITY_MATCH_THRESHOLD = 0.8
    RELATION_MATCH_THRESHOLD = 0.75
    
    WINDOW_WIDTH = 1200
    WINDOW_HEIGHT = 800
    THEME = 'clam'
    
    SUPPORTED_CONTRACT_FORMATS = ['.txt', '.pdf', '.docx', '.md']
    SUPPORTED_SMART_CONTRACT_FORMATS = ['.sol']
    
    @classmethod
    def create_directories(cls):
        directories = [
            cls.DATA_DIR,
            cls.SAMPLE_CONTRACTS_DIR,
            cls.SAMPLE_SMART_CONTRACTS_DIR,
            cls.OUTPUTS_DIR
        ]
        for directory in directories:
            os.makedirs(directory, exist_ok=True)