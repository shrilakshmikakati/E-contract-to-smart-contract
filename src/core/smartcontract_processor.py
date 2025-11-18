"""
Smart Contract processor implementing Algorithm 2: Smart Contract Knowledge Graph Construction
"""

from typing import Dict, Any, List, Optional
import os
from datetime import datetime

try:
    from ..blockchain.ast_generator import ASTGenerator
    from ..blockchain.solidity_parser import SolidityParser
    from ..blockchain.grammar_engine import GrammarEngine
    from .knowledge_graph import KnowledgeGraph
    from ..utils.file_handler import FileHandler
    from ..utils.config import Config
    from ..realtime.smart_contract_generator import AccurateSmartContractGenerator
except ImportError:
    from blockchain.ast_generator import ASTGenerator
    from blockchain.solidity_parser import SolidityParser
    from blockchain.grammar_engine import GrammarEngine
    from core.knowledge_graph import KnowledgeGraph
    from utils.file_handler import FileHandler
    from utils.config import Config
    from realtime.smart_contract_generator import AccurateSmartContractGenerator

class SmartContractProcessor:
    """
    Processes smart contracts to generate knowledge graphs
    Implements Algorithm 2 from the research paper
    """
    
    def __init__(self):
        self.ast_generator = ASTGenerator()
        self.solidity_parser = SolidityParser()
        self.grammar_engine = GrammarEngine()
        self.contract_generator = AccurateSmartContractGenerator()
        self.processed_contracts = {}
    
    def process_contract(self, contract_code: str, contract_id: str = None) -> KnowledgeGraph:
        """
        Algorithm 2: Smart Contract Knowledge Graph Construction
        
        Args:
            contract_code: Solidity source code
            contract_id: Optional identifier for the contract
            
        Returns:
            Knowledge graph G_s = (V_s, E_s)
        """
        if contract_id is None:
            contract_id = f"smart_contract_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"Processing smart contract: {contract_id}")
        
        # Step 1: Extract Solidity version (v ← ExtractSolidityVersion(S))
        print("Step 1: Extracting Solidity version...")
        solidity_version = self.ast_generator.extract_solidity_version(contract_code)
        
        # Step 2: Select compiler (Compiler ← SelectCompiler(v))
        print("Step 2: Selecting compiler...")
        if solidity_version:
            compiler_selected = self.ast_generator.select_compiler_version(solidity_version)
            if not compiler_selected:
                print(f"Warning: Could not select compiler for version {solidity_version}")
        
        # Step 3: Compile and generate AST (AST ← CompileAndGenerateAST(S, Compiler))
        print("Step 3: Compiling and generating AST...")
        ast_data = self.ast_generator.compile_and_generate_ast(contract_code, contract_id)
        
        if not ast_data:
            raise ValueError("Failed to generate AST from smart contract code")
        
        # Step 4: Save AST as JSON (ASTjson ← SaveAsJSON(AST))
        print("Step 4: Processing AST structure...")
        contract_structure = self.ast_generator.extract_contract_structure(ast_data)
        
        # Steps 5-9: Apply grammar to each node and generate semantic structure
        print("Step 5-9: Applying grammar rules and generating semantic descriptions...")
        semantic_descriptions = self.grammar_engine.generate_semantic_description(contract_structure)
        
        # Step 10: Extract entities from semantic structure (V_s ← ExtractEntitiesFromSemanticStructure())
        print("Step 10: Extracting entities from semantic structure...")
        entities = self._extract_entities_from_structure(contract_structure, semantic_descriptions)
        
        # Step 11: Extract relations from semantic structure (E_s ← ExtractRelationsFromSemanticStructure())
        print("Step 11: Extracting relationships from semantic structure...")
        relationships = self._extract_relationships_from_structure(contract_structure, entities)
        
        # Step 12: Construct knowledge graph (G_s ← (V_s, E_s))
        print("Step 12: Constructing knowledge graph...")
        knowledge_graph = self._construct_knowledge_graph(
            entities, relationships, contract_structure, semantic_descriptions, contract_id
        )
        
        # Store processed contract data
        self.processed_contracts[contract_id] = {
            'source_code': contract_code,
            'solidity_version': solidity_version,
            'ast_data': ast_data,
            'contract_structure': contract_structure,
            'semantic_descriptions': semantic_descriptions,
            'entities': entities,
            'relationships': relationships,
            'knowledge_graph': knowledge_graph,
            'processing_time': datetime.now().isoformat()
        }
        
        print(f"Smart contract processing completed for {contract_id}")
        print(f"Generated {len(entities)} entities and {len(relationships)} relationships")
        
        return knowledge_graph
    
    def _extract_entities_from_structure(self, contract_structure: Dict[str, Any], 
                                       semantic_descriptions: Dict[str, List[str]]) -> List[Dict[str, Any]]:
        """Extract entities from contract structure and semantic descriptions"""
        entities = []
        entity_id = 0
        
        # Extract contracts as entities
        for contract in contract_structure.get('contracts', []):
            entities.append({
                'id': f"contract_entity_{entity_id}",
                'text': contract['name'],
                'type': 'CONTRACT',
                'label': 'SMART_CONTRACT',
                'confidence': 1.0,
                'properties': {
                    'kind': contract.get('kind', 'contract'),
                    'abstract': contract.get('abstract', False),
                    'ast_id': contract.get('id', ''),
                    'inheritance': contract.get('linearizedBaseContracts', [])
                },
                'source': 'ast_analysis'
            })
            entity_id += 1
        
        # Extract functions as entities
        for function in contract_structure.get('functions', []):
            entities.append({
                'id': f"function_entity_{entity_id}",
                'text': function['name'],
                'type': 'FUNCTION',
                'label': 'SMART_CONTRACT_FUNCTION',
                'confidence': 1.0,
                'properties': {
                    'visibility': function.get('visibility', 'public'),
                    'state_mutability': function.get('stateMutability', 'nonpayable'),
                    'virtual': function.get('virtual', False),
                    'override': function.get('override', False),
                    'contract': function.get('contract', ''),
                    'parameters': function.get('parameters', []),
                    'return_parameters': function.get('returnParameters', []),
                    'ast_id': function.get('id', '')
                },
                'source': 'ast_analysis'
            })
            entity_id += 1
        
        # Extract state variables as entities
        for variable in contract_structure.get('variables', []):
            entities.append({
                'id': f"variable_entity_{entity_id}",
                'text': variable['name'],
                'type': 'STATE_VARIABLE',
                'label': 'SMART_CONTRACT_VARIABLE',
                'confidence': 1.0,
                'properties': {
                    'data_type': variable.get('type', 'unknown'),
                    'visibility': variable.get('visibility', 'internal'),
                    'constant': variable.get('constant', False),
                    'immutable': variable.get('immutable', False),
                    'contract': variable.get('contract', ''),
                    'ast_id': variable.get('id', '')
                },
                'source': 'ast_analysis'
            })
            entity_id += 1
        
        # Extract events as entities
        for event in contract_structure.get('events', []):
            entities.append({
                'id': f"event_entity_{entity_id}",
                'text': event['name'],
                'type': 'EVENT',
                'label': 'SMART_CONTRACT_EVENT',
                'confidence': 1.0,
                'properties': {
                    'anonymous': event.get('anonymous', False),
                    'parameters': event.get('parameters', []),
                    'contract': event.get('contract', ''),
                    'ast_id': event.get('id', '')
                },
                'source': 'ast_analysis'
            })
            entity_id += 1
        
        # Extract modifiers as entities
        for modifier in contract_structure.get('modifiers', []):
            entities.append({
                'id': f"modifier_entity_{entity_id}",
                'text': modifier['name'],
                'type': 'MODIFIER',
                'label': 'SMART_CONTRACT_MODIFIER',
                'confidence': 1.0,
                'properties': {
                    'virtual': modifier.get('virtual', False),
                    'override': modifier.get('override', False),
                    'contract': modifier.get('contract', ''),
                    'ast_id': modifier.get('id', '')
                },
                'source': 'ast_analysis'
            })
            entity_id += 1
        
        # Extract structs as entities
        for struct in contract_structure.get('structs', []):
            entities.append({
                'id': f"struct_entity_{entity_id}",
                'text': struct['name'],
                'type': 'STRUCT',
                'label': 'SMART_CONTRACT_STRUCT',
                'confidence': 1.0,
                'properties': {
                    'members': struct.get('members', []),
                    'contract': struct.get('contract', ''),
                    'ast_id': struct.get('id', '')
                },
                'source': 'ast_analysis'
            })
            entity_id += 1
        
        # Extract enums as entities
        for enum in contract_structure.get('enums', []):
            entities.append({
                'id': f"enum_entity_{entity_id}",
                'text': enum['name'],
                'type': 'ENUM',
                'label': 'SMART_CONTRACT_ENUM',
                'confidence': 1.0,
                'properties': {
                    'members': enum.get('members', []),
                    'contract': enum.get('contract', ''),
                    'ast_id': enum.get('id', '')
                },
                'source': 'ast_analysis'
            })
            entity_id += 1
        
        return entities
    
    def _extract_relationships_from_structure(self, contract_structure: Dict[str, Any], 
                                            entities: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
        """Extract relationships from contract structure"""
        relationships = []
        rel_id = 0
        
        # Create entity lookup by name and contract
        entity_lookup = {}
        for entity in entities:
            key = f"{entity['properties'].get('contract', '')}.{entity['text']}"
            entity_lookup[key] = entity
            # Also add just the name for global lookup
            entity_lookup[entity['text']] = entity
        
        # Extract contract inheritance relationships
        for contract in contract_structure.get('contracts', []):
            contract_name = contract['name']
            base_contracts = contract.get('linearizedBaseContracts', [])
            
            for base_contract_id in base_contracts:
                # Find base contract entity
                for entity in entities:
                    if (entity['type'] == 'CONTRACT' and 
                        entity['properties'].get('ast_id') == str(base_contract_id) and
                        entity['text'] != contract_name):
                        
                        relationships.append({
                            'id': f"inheritance_rel_{rel_id}",
                            'source': entity_lookup.get(contract_name, {}).get('id', ''),
                            'target': entity['id'],
                            'relation': 'inherits_from',
                            'confidence': 1.0,
                            'source_type': 'CONTRACT',
                            'target_type': 'CONTRACT',
                            'description': f"{contract_name} inherits from {entity['text']}"
                        })
                        rel_id += 1
        
        # Extract containment relationships (contract contains functions, variables, etc.)
        for contract in contract_structure.get('contracts', []):
            contract_name = contract['name']
            contract_entity = entity_lookup.get(contract_name)
            
            if not contract_entity:
                continue
            
            # Functions contained in contract
            for function in contract_structure.get('functions', []):
                if function.get('contract') == contract_name:
                    function_entity = entity_lookup.get(f"{contract_name}.{function['name']}")
                    if function_entity:
                        relationships.append({
                            'id': f"contains_rel_{rel_id}",
                            'source': contract_entity['id'],
                            'target': function_entity['id'],
                            'relation': 'contains',
                            'confidence': 1.0,
                            'source_type': 'CONTRACT',
                            'target_type': 'FUNCTION',
                            'description': f"Contract {contract_name} contains function {function['name']}"
                        })
                        rel_id += 1
            
            # Variables contained in contract
            for variable in contract_structure.get('variables', []):
                if variable.get('contract') == contract_name:
                    variable_entity = entity_lookup.get(f"{contract_name}.{variable['name']}")
                    if variable_entity:
                        relationships.append({
                            'id': f"contains_rel_{rel_id}",
                            'source': contract_entity['id'],
                            'target': variable_entity['id'],
                            'relation': 'contains',
                            'confidence': 1.0,
                            'source_type': 'CONTRACT',
                            'target_type': 'STATE_VARIABLE',
                            'description': f"Contract {contract_name} contains variable {variable['name']}"
                        })
                        rel_id += 1
            
            # Events, modifiers, structs, enums
            for item_type, items in [
                ('events', 'EVENT'),
                ('modifiers', 'MODIFIER'),
                ('structs', 'STRUCT'),
                ('enums', 'ENUM')
            ]:
                for item in contract_structure.get(item_type, []):
                    if item.get('contract') == contract_name:
                        item_entity = entity_lookup.get(f"{contract_name}.{item['name']}")
                        if item_entity:
                            relationships.append({
                                'id': f"contains_rel_{rel_id}",
                                'source': contract_entity['id'],
                                'target': item_entity['id'],
                                'relation': 'contains',
                                'confidence': 1.0,
                                'source_type': 'CONTRACT',
                                'target_type': items,
                                'description': f"Contract {contract_name} contains {item_type[:-1]} {item['name']}"
                            })
                            rel_id += 1
        
        # Extract function parameter relationships
        for function in contract_structure.get('functions', []):
            function_name = function['name']
            contract_name = function.get('contract', '')
            function_entity = entity_lookup.get(f"{contract_name}.{function_name}")
            
            if not function_entity:
                continue
            
            # Parameters
            parameters = function.get('parameters', [])
            for param in parameters:
                param_name = param.get('name', '')
                if param_name:
                    relationships.append({
                        'id': f"param_rel_{rel_id}",
                        'source': function_entity['id'],
                        'target': f"param_{param_name}_{rel_id}",  # Virtual parameter entity
                        'relation': 'has_parameter',
                        'confidence': 1.0,
                        'source_type': 'FUNCTION',
                        'target_type': 'PARAMETER',
                        'description': f"Function {function_name} has parameter {param_name} of type {param.get('type', 'unknown')}"
                    })
                    rel_id += 1
        
        # Extract struct member relationships
        for struct in contract_structure.get('structs', []):
            struct_name = struct['name']
            contract_name = struct.get('contract', '')
            struct_entity = entity_lookup.get(f"{contract_name}.{struct_name}")
            
            if not struct_entity:
                continue
            
            members = struct.get('members', [])
            for member in members:
                member_name = member.get('name', '')
                if member_name:
                    relationships.append({
                        'id': f"member_rel_{rel_id}",
                        'source': struct_entity['id'],
                        'target': f"member_{member_name}_{rel_id}",  # Virtual member entity
                        'relation': 'has_member',
                        'confidence': 1.0,
                        'source_type': 'STRUCT',
                        'target_type': 'STRUCT_MEMBER',
                        'description': f"Struct {struct_name} has member {member_name} of type {member.get('type', 'unknown')}"
                    })
                    rel_id += 1
        
        return relationships
    
    def _construct_knowledge_graph(self, entities: List[Dict[str, Any]], 
                                 relationships: List[Dict[str, Any]],
                                 contract_structure: Dict[str, Any],
                                 semantic_descriptions: Dict[str, List[str]],
                                 contract_id: str) -> KnowledgeGraph:
        """Construct the knowledge graph from entities and relationships"""
        
        # Initialize knowledge graph
        kg = KnowledgeGraph('smartcontract')
        kg.metadata.update({
            'source_file': contract_id,
            'creation_time': datetime.now().isoformat(),
            'contract_structure_stats': {
                category: len(items) for category, items in contract_structure.items()
            },
            'semantic_description_stats': {
                category: len(descriptions) for category, descriptions in semantic_descriptions.items()
            }
        })
        
        # Add entities to the graph
        for entity in entities:
            entity_data = {
                'text': entity['text'],
                'type': entity['type'],
                'label': entity['label'],
                'confidence': entity.get('confidence', 1.0),
                'properties': entity.get('properties', {}),
                'source': entity.get('source', 'unknown'),
                'category': self._categorize_smart_contract_entity(entity)
            }
            
            kg.add_entity(entity['id'], entity_data)
        
        # Add relationships to the graph
        for relationship in relationships:
            rel_data = {
                'relation': relationship.get('relation', 'unknown'),
                'confidence': relationship.get('confidence', 1.0),
                'description': relationship.get('description', ''),
                'source_type': relationship.get('source_type', 'UNKNOWN'),
                'target_type': relationship.get('target_type', 'UNKNOWN')
            }
            
            # Handle virtual entities (parameters, members)
            source_id = relationship['source']
            target_id = relationship['target']
            
            # Create virtual target entity if it doesn't exist
            if target_id.startswith(('param_', 'member_')) and target_id not in kg.entities:
                virtual_entity_data = {
                    'text': target_id.split('_')[1],  # Extract name from virtual ID
                    'type': relationship.get('target_type', 'VIRTUAL'),
                    'label': relationship.get('target_type', 'VIRTUAL'),
                    'confidence': 0.8,
                    'properties': {'virtual': True},
                    'source': 'virtual_entity',
                    'category': 'VIRTUAL'
                }
                kg.add_entity(target_id, virtual_entity_data)
            
            kg.add_relationship(relationship['id'], source_id, target_id, rel_data)
        
        return kg
    
    def _categorize_smart_contract_entity(self, entity: Dict[str, Any]) -> str:
        """Categorize smart contract entity"""
        entity_type = entity.get('type', 'UNKNOWN').upper()
        
        category_mapping = {
            'CONTRACT': 'CONTRACT_DEFINITION',
            'FUNCTION': 'FUNCTION_DEFINITION',
            'STATE_VARIABLE': 'STATE_STORAGE',
            'EVENT': 'EVENT_DEFINITION',
            'MODIFIER': 'ACCESS_CONTROL',
            'STRUCT': 'DATA_STRUCTURE',
            'ENUM': 'DATA_STRUCTURE',
            'PARAMETER': 'FUNCTION_COMPONENT',
            'STRUCT_MEMBER': 'DATA_COMPONENT'
        }
        
        return category_mapping.get(entity_type, 'OTHER')
    
    def process_contract_file(self, file_path: str) -> KnowledgeGraph:
        """
        Process a smart contract from file
        
        Args:
            file_path: Path to the Solidity file
            
        Returns:
            Knowledge graph for the smart contract
        """
        try:
            # Validate file
            if not FileHandler.validate_file_path(file_path, Config.SUPPORTED_SMART_CONTRACT_FORMATS):
                raise ValueError(f"Unsupported file format: {file_path}")
            
            # Read contract code
            contract_code = FileHandler.read_text_file(file_path)
            if not contract_code:
                raise ValueError(f"Could not read smart contract file: {file_path}")
            
            # Extract contract ID from filename
            contract_id = os.path.splitext(os.path.basename(file_path))[0]
            
            # Process the contract
            knowledge_graph = self.process_contract(contract_code, contract_id)
            
            # Update metadata with file information
            knowledge_graph.metadata['source_file'] = file_path
            knowledge_graph.metadata['file_info'] = FileHandler.get_file_info(file_path)
            
            return knowledge_graph
            
        except Exception as e:
            print(f"Error processing smart contract file {file_path}: {e}")
            raise
    
    def get_contract_summary(self, contract_id: str) -> Dict[str, Any]:
        """Get summary of processed smart contract"""
        if contract_id not in self.processed_contracts:
            return {}
        
        contract_data = self.processed_contracts[contract_id]
        kg = contract_data['knowledge_graph']
        
        return {
            'contract_id': contract_id,
            'processing_time': contract_data['processing_time'],
            'solidity_version': contract_data['solidity_version'],
            'statistics': kg.get_statistics(),
            'contract_structure': contract_data['contract_structure'],
            'entity_categories': self._get_entity_category_distribution(contract_data['entities']),
            'relationship_types': self._get_relationship_type_distribution(contract_data['relationships']),
            'semantic_descriptions': contract_data['semantic_descriptions'],
            'complexity_analysis': self._analyze_contract_complexity(contract_data['contract_structure'])
        }
    
    def _get_entity_category_distribution(self, entities: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get distribution of entity categories"""
        categories = {}
        for entity in entities:
            category = self._categorize_smart_contract_entity(entity)
            categories[category] = categories.get(category, 0) + 1
        return categories
    
    def _get_relationship_type_distribution(self, relationships: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get distribution of relationship types"""
        types = {}
        for rel in relationships:
            rel_type = rel.get('relation', 'unknown')
            types[rel_type] = types.get(rel_type, 0) + 1
        return types
    
    def _analyze_contract_complexity(self, contract_structure: Dict[str, Any]) -> Dict[str, Any]:
        """Analyze smart contract complexity"""
        complexity_metrics = {
            'total_contracts': len(contract_structure.get('contracts', [])),
            'total_functions': len(contract_structure.get('functions', [])),
            'total_variables': len(contract_structure.get('variables', [])),
            'total_events': len(contract_structure.get('events', [])),
            'total_modifiers': len(contract_structure.get('modifiers', [])),
            'total_structs': len(contract_structure.get('structs', [])),
            'total_enums': len(contract_structure.get('enums', []))
        }
        
        # Calculate complexity score
        complexity_score = 0
        complexity_score += complexity_metrics['total_functions'] * 2
        complexity_score += complexity_metrics['total_variables'] * 1
        complexity_score += complexity_metrics['total_events'] * 1
        complexity_score += complexity_metrics['total_modifiers'] * 3
        complexity_score += complexity_metrics['total_structs'] * 2
        complexity_score += complexity_metrics['total_enums'] * 1
        
        # Determine complexity level
        if complexity_score > 100:
            complexity_level = 'Very High'
        elif complexity_score > 50:
            complexity_level = 'High'
        elif complexity_score > 20:
            complexity_level = 'Medium'
        elif complexity_score > 5:
            complexity_level = 'Low'
        else:
            complexity_level = 'Very Low'
        
        complexity_metrics.update({
            'complexity_score': complexity_score,
            'complexity_level': complexity_level
        })
        
        return complexity_metrics
    
    def get_human_readable_contract(self, contract_id: str) -> str:
        """Get human-readable description of the smart contract"""
        if contract_id not in self.processed_contracts:
            return "Contract not found"
        
        contract_data = self.processed_contracts[contract_id]
        semantic_descriptions = contract_data['semantic_descriptions']
        
        # Build readable description
        readable_parts = []
        
        readable_parts.append("=== SMART CONTRACT ANALYSIS ===")
        readable_parts.append(f"Contract ID: {contract_id}")
        readable_parts.append(f"Solidity Version: {contract_data.get('solidity_version', 'Unknown')}")
        readable_parts.append("")
        
        # Add semantic descriptions for each category
        for category, descriptions in semantic_descriptions.items():
            if descriptions:
                readable_parts.append(f"=== {category.upper().replace('_', ' ')} ===")
                readable_parts.extend(descriptions)
                readable_parts.append("")
        
        return "\n".join(readable_parts)
    
    def generate_smart_contract_from_econtract(self, econtract_analysis: Dict[str, Any]) -> Dict[str, Any]:
        """
        Generate accurate smart contract from e-contract analysis
        
        Args:
            econtract_analysis: Results from e-contract processing
            
        Returns:
            Dictionary containing generated smart contract and validation results
        """
        try:
            print("Generating smart contract from e-contract analysis...")
            
            # Generate smart contract using accurate generator
            generation_result = self.contract_generator.generate_smart_contract(econtract_analysis)
            
            if 'error' in generation_result:
                return generation_result
            
            # Process the generated contract through our analysis pipeline
            contract_code = generation_result['contract_code']
            knowledge_graph = self.process_contract(contract_code)
            
            # Enhance result with our analysis
            generation_result.update({
                'knowledge_graph': knowledge_graph,
                'ast_analysis': self._analyze_generated_contract(contract_code),
                'deployment_ready': generation_result['accuracy_score'] >= 0.95,
                'processor_metadata': {
                    'processed_at': datetime.now().isoformat(),
                    'processor_version': '2.0',
                    'analysis_complete': True
                }
            })
            
            return generation_result
            
        except Exception as e:
            return {
                'error': f"Smart contract generation failed: {str(e)}",
                'accuracy_score': 0,
                'deployment_ready': False,
                'generated_at': datetime.now().isoformat()
            }
    
    def _analyze_generated_contract(self, contract_code: str) -> Dict[str, Any]:
        """Analyze the generated smart contract for completeness"""
        try:
            # Parse with AST generator
            ast_data = self.ast_generator.generate_ast(contract_code)
            
            # Parse with Solidity parser
            contract_data = self.solidity_parser.parse_contract(contract_code)
            
            # Generate human-readable descriptions
            human_readable = self.grammar_engine.ast_to_human_readable(ast_data)
            
            return {
                'ast_structure': ast_data,
                'contract_metadata': contract_data,
                'human_readable': human_readable,
                'complexity_metrics': self._calculate_complexity_metrics(contract_data),
                'security_score': self._calculate_security_score(contract_code),
                'gas_efficiency': self._estimate_gas_efficiency(contract_code)
            }
            
        except Exception as e:
            return {
                'error': f"Contract analysis failed: {str(e)}",
                'analysis_complete': False
            }
    
    def _calculate_complexity_metrics(self, contract_data: Dict[str, Any]) -> Dict[str, int]:
        """Calculate complexity metrics for the generated contract"""
        return {
            'total_functions': len(contract_data.get('functions', [])),
            'public_functions': len([f for f in contract_data.get('functions', []) if f.get('visibility') == 'public']),
            'state_variables': len(contract_data.get('state_variables', [])),
            'modifiers': len(contract_data.get('modifiers', [])),
            'events': len(contract_data.get('events', [])),
            'total_lines': len(str(contract_data).split('\n'))
        }
    
    def _calculate_security_score(self, contract_code: str) -> float:
        """Calculate security score for the generated contract"""
        security_features = 0
        total_checks = 5
        
        # Check for access control
        if 'modifier only' in contract_code:
            security_features += 1
        
        # Check for input validation
        if 'require(' in contract_code:
            security_features += 1
        
        # Check for event emission
        if 'emit ' in contract_code:
            security_features += 1
        
        # Check for proper error messages
        if 'require(' in contract_code and '"' in contract_code:
            security_features += 1
        
        # Check for Solidity version
        if 'pragma solidity ^0.8' in contract_code:
            security_features += 1
        
        return security_features / total_checks
    
    def _estimate_gas_efficiency(self, contract_code: str) -> Dict[str, Any]:
        """Estimate gas efficiency of the generated contract"""
        # Simple heuristics for gas efficiency
        efficiency_score = 1.0
        issues = []
        
        # Check for loops (can be gas inefficient)
        if 'for(' in contract_code or 'while(' in contract_code:
            efficiency_score -= 0.1
            issues.append("Contains loops - monitor gas usage")
        
        # Check for string operations (more expensive)
        if 'string' in contract_code and 'memory' in contract_code:
            efficiency_score -= 0.05
            issues.append("Uses string operations - consider alternatives")
        
        # Check for mappings (efficient)
        if 'mapping(' in contract_code:
            efficiency_score += 0.1
            if efficiency_score > 1.0:
                efficiency_score = 1.0
        
        return {
            'efficiency_score': max(0.0, efficiency_score),
            'gas_optimization_issues': issues,
            'recommended_optimizations': self._get_optimization_recommendations(contract_code)
        }
    
    def _get_optimization_recommendations(self, contract_code: str) -> List[str]:
        """Get gas optimization recommendations"""
        recommendations = []
        
        if 'uint256' in contract_code:
            recommendations.append("Consider using smaller uint types (uint8, uint16) where appropriate")
        
        if 'public' in contract_code:
            recommendations.append("Consider making variables internal/private if external access not needed")
        
        if 'string' in contract_code:
            recommendations.append("Consider using bytes32 instead of string for fixed-length data")
        
        return recommendations