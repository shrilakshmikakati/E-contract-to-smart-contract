"""
Solidity parser for smart contract analysis and processing
"""

import re
from typing import Dict, Any, List, Optional, Tuple
from .ast_generator import ASTGenerator
from .grammar_engine import GrammarEngine
try:
    from ..utils.file_handler import FileHandler
except ImportError:
    from utils.file_handler import FileHandler

class SolidityParser:
    """Parses Solidity smart contracts and converts them to human-readable descriptions"""
    
    def __init__(self):
        self.ast_generator = ASTGenerator()
        self.grammar_engine = GrammarEngine()
        self.parsed_contracts = {}
    
    def parse_contract_file(self, file_path: str) -> Dict[str, Any]:
        """
        Parse a Solidity contract file and generate comprehensive analysis
        
        Args:
            file_path: Path to Solidity file
            
        Returns:
            Dictionary containing parsed contract information
        """
        try:
            # Read the Solidity file
            solidity_data = FileHandler.read_solidity_file(file_path)
            if not solidity_data:
                return {}
            
            source_code = solidity_data['content']
            
            # Generate AST
            ast_data = self.ast_generator.generate_ast_from_file(file_path)
            if not ast_data:
                print(f"Failed to generate AST for {file_path}")
                return {}
            
            # Extract contract structure
            contract_structure = self.ast_generator.extract_contract_structure(ast_data)
            
            # Generate human-readable descriptions
            semantic_descriptions = self.grammar_engine.generate_semantic_description(contract_structure)
            
            # Parse additional contract information
            contract_info = self._extract_contract_metadata(source_code)
            
            # Combine all information
            parsed_contract = {
                'file_info': solidity_data,
                'ast_data': ast_data,
                'contract_structure': contract_structure,
                'semantic_descriptions': semantic_descriptions,
                'contract_metadata': contract_info,
                'analysis_summary': self._generate_analysis_summary(
                    contract_structure, semantic_descriptions, contract_info
                )
            }
            
            # Cache the parsed contract
            self.parsed_contracts[file_path] = parsed_contract
            
            return parsed_contract
            
        except Exception as e:
            print(f"Error parsing contract file {file_path}: {e}")
            return {}
    
    def _extract_contract_metadata(self, source_code: str) -> Dict[str, Any]:
        """Extract metadata and additional information from contract source"""
        metadata = {
            'pragma_version': self._extract_pragma_version(source_code),
            'imports': self._extract_imports(source_code),
            'licenses': self._extract_licenses(source_code),
            'comments': self._extract_comments(source_code),
            'natspec': self._extract_natspec_comments(source_code),
            'security_patterns': self._identify_security_patterns(source_code),
            'complexity_metrics': self._calculate_complexity_metrics(source_code)
        }
        
        return metadata
    
    def _extract_pragma_version(self, source_code: str) -> List[str]:
        """Extract pragma statements"""
        pragma_pattern = r'pragma\s+(\w+)\s+([^;]+);'
        matches = re.findall(pragma_pattern, source_code, re.IGNORECASE)
        return [f"{lang} {version}" for lang, version in matches]
    
    def _extract_imports(self, source_code: str) -> List[str]:
        """Extract import statements"""
        import_pattern = r'import\s+([^;]+);'
        matches = re.findall(import_pattern, source_code, re.MULTILINE)
        return [match.strip() for match in matches]
    
    def _extract_licenses(self, source_code: str) -> List[str]:
        """Extract license identifiers"""
        license_pattern = r'//\s*SPDX-License-Identifier:\s*([^\n\r]+)'
        matches = re.findall(license_pattern, source_code, re.IGNORECASE)
        return [match.strip() for match in matches]
    
    def _extract_comments(self, source_code: str) -> Dict[str, List[str]]:
        """Extract different types of comments"""
        comments = {
            'single_line': [],
            'multi_line': [],
            'natspec_single': [],
            'natspec_multi': []
        }
        
        # Single line comments
        single_line_pattern = r'//(?!\/)([^\n\r]*)'
        comments['single_line'] = re.findall(single_line_pattern, source_code)
        
        # Multi-line comments
        multi_line_pattern = r'/\*(?!\*).*?\*/'
        comments['multi_line'] = re.findall(multi_line_pattern, source_code, re.DOTALL)
        
        # NatSpec single line
        natspec_single_pattern = r'///([^\n\r]*)'
        comments['natspec_single'] = re.findall(natspec_single_pattern, source_code)
        
        # NatSpec multi-line
        natspec_multi_pattern = r'/\*\*.*?\*/'
        comments['natspec_multi'] = re.findall(natspec_multi_pattern, source_code, re.DOTALL)
        
        return comments
    
    def _extract_natspec_comments(self, source_code: str) -> Dict[str, Any]:
        """Extract and parse NatSpec documentation"""
        natspec = {
            'title': [],
            'author': [],
            'notice': [],
            'dev': [],
            'param': [],
            'return': []
        }
        
        # Extract NatSpec tags
        natspec_patterns = {
            'title': r'@title\s+([^\n\r@]*)',
            'author': r'@author\s+([^\n\r@]*)',
            'notice': r'@notice\s+([^\n\r@]*)',
            'dev': r'@dev\s+([^\n\r@]*)',
            'param': r'@param\s+(\w+)\s+([^\n\r@]*)',
            'return': r'@return\s+([^\n\r@]*)'
        }
        
        for tag, pattern in natspec_patterns.items():
            matches = re.findall(pattern, source_code, re.IGNORECASE)
            if tag == 'param':
                natspec[tag] = [{'name': m[0], 'description': m[1].strip()} for m in matches]
            else:
                natspec[tag] = [match.strip() for match in matches if match.strip()]
        
        return natspec
    
    def _identify_security_patterns(self, source_code: str) -> Dict[str, List[str]]:
        """Identify common security patterns and potential issues"""
        patterns = {
            'access_control': [],
            'reentrancy_guards': [],
            'overflow_checks': [],
            'external_calls': [],
            'state_changes': [],
            'modifiers': []
        }
        
        # Access control patterns
        access_patterns = [
            r'onlyOwner',
            r'require\s*\(\s*msg\.sender\s*==',
            r'modifier\s+only\w+'
        ]
        
        for pattern in access_patterns:
            if re.search(pattern, source_code, re.IGNORECASE):
                patterns['access_control'].append(pattern)
        
        # Reentrancy guard patterns
        reentrancy_patterns = [
            r'nonReentrant',
            r'ReentrancyGuard',
            r'mutex',
            r'locked'
        ]
        
        for pattern in reentrancy_patterns:
            if re.search(pattern, source_code, re.IGNORECASE):
                patterns['reentrancy_guards'].append(pattern)
        
        # Overflow check patterns
        overflow_patterns = [
            r'SafeMath',
            r'using\s+SafeMath',
            r'add\(',
            r'sub\(',
            r'mul\(',
            r'div\('
        ]
        
        for pattern in overflow_patterns:
            if re.search(pattern, source_code, re.IGNORECASE):
                patterns['overflow_checks'].append(pattern)
        
        # External calls
        external_call_patterns = [
            r'\.call\(',
            r'\.delegatecall\(',
            r'\.staticcall\(',
            r'\.send\(',
            r'\.transfer\('
        ]
        
        for pattern in external_call_patterns:
            matches = re.findall(pattern, source_code, re.IGNORECASE)
            if matches:
                patterns['external_calls'].extend(matches)
        
        return patterns
    
    def _calculate_complexity_metrics(self, source_code: str) -> Dict[str, int]:
        """Calculate basic complexity metrics"""
        metrics = {
            'lines_of_code': len([line for line in source_code.split('\n') if line.strip()]),
            'function_count': len(re.findall(r'function\s+\w+', source_code, re.IGNORECASE)),
            'modifier_count': len(re.findall(r'modifier\s+\w+', source_code, re.IGNORECASE)),
            'event_count': len(re.findall(r'event\s+\w+', source_code, re.IGNORECASE)),
            'state_variable_count': len(re.findall(r'^\s*\w+\s+(?:public|private|internal)?\s*\w+\s*;', source_code, re.MULTILINE)),
            'if_statements': len(re.findall(r'\bif\s*\(', source_code, re.IGNORECASE)),
            'loop_statements': len(re.findall(r'\b(for|while)\s*\(', source_code, re.IGNORECASE)),
            'require_statements': len(re.findall(r'\brequire\s*\(', source_code, re.IGNORECASE)),
            'assert_statements': len(re.findall(r'\bassert\s*\(', source_code, re.IGNORECASE))
        }
        
        # Cyclomatic complexity (simplified)
        complexity_keywords = ['if', 'else', 'for', 'while', 'case', '&&', '||', '?']
        metrics['cyclomatic_complexity'] = sum(
            len(re.findall(rf'\b{keyword}\b', source_code, re.IGNORECASE))
            for keyword in complexity_keywords
        ) + 1  # Base complexity
        
        return metrics
    
    def _generate_analysis_summary(self, contract_structure: Dict[str, Any], 
                                 semantic_descriptions: Dict[str, List[str]], 
                                 contract_metadata: Dict[str, Any]) -> Dict[str, Any]:
        """Generate comprehensive analysis summary"""
        
        # Count different elements
        element_counts = {key: len(items) for key, items in contract_structure.items()}
        
        # Security analysis
        security_score = self._calculate_security_score(contract_metadata.get('security_patterns', {}))
        
        # Complexity analysis
        complexity_metrics = contract_metadata.get('complexity_metrics', {})
        complexity_level = self._assess_complexity_level(complexity_metrics)
        
        summary = {
            'element_counts': element_counts,
            'total_elements': sum(element_counts.values()),
            'security_score': security_score,
            'complexity_level': complexity_level,
            'complexity_metrics': complexity_metrics,
            'has_documentation': bool(contract_metadata.get('natspec', {}).get('title', [])),
            'license_info': contract_metadata.get('licenses', []),
            'pragma_versions': contract_metadata.get('pragma_version', []),
            'import_count': len(contract_metadata.get('imports', [])),
            'key_features': self._identify_key_features(contract_structure, contract_metadata)
        }
        
        return summary
    
    def _calculate_security_score(self, security_patterns: Dict[str, List[str]]) -> float:
        """Calculate a basic security score based on identified patterns"""
        score = 0.0
        max_score = 100.0
        
        # Positive security indicators
        if security_patterns.get('access_control'):
            score += 25.0  # Access control present
        
        if security_patterns.get('reentrancy_guards'):
            score += 25.0  # Reentrancy protection
        
        if security_patterns.get('overflow_checks'):
            score += 20.0  # Overflow protection
        
        # Moderate indicators
        external_calls = len(security_patterns.get('external_calls', []))
        if external_calls == 0:
            score += 15.0  # No external calls (safer)
        elif external_calls <= 3:
            score += 10.0  # Limited external calls
        else:
            score += 5.0   # Many external calls (riskier)
        
        # Base security score
        score += 15.0
        
        return min(score, max_score)
    
    def _assess_complexity_level(self, complexity_metrics: Dict[str, int]) -> str:
        """Assess complexity level based on metrics"""
        lines_of_code = complexity_metrics.get('lines_of_code', 0)
        cyclomatic_complexity = complexity_metrics.get('cyclomatic_complexity', 1)
        function_count = complexity_metrics.get('function_count', 0)
        
        # Simple scoring system
        complexity_score = 0
        
        if lines_of_code > 500:
            complexity_score += 3
        elif lines_of_code > 200:
            complexity_score += 2
        elif lines_of_code > 50:
            complexity_score += 1
        
        if cyclomatic_complexity > 20:
            complexity_score += 3
        elif cyclomatic_complexity > 10:
            complexity_score += 2
        elif cyclomatic_complexity > 5:
            complexity_score += 1
        
        if function_count > 20:
            complexity_score += 2
        elif function_count > 10:
            complexity_score += 1
        
        if complexity_score >= 6:
            return 'High'
        elif complexity_score >= 3:
            return 'Medium'
        else:
            return 'Low'
    
    def _identify_key_features(self, contract_structure: Dict[str, Any], 
                             contract_metadata: Dict[str, Any]) -> List[str]:
        """Identify key features of the contract"""
        features = []
        
        # Contract type features
        contracts = contract_structure.get('contracts', [])
        for contract in contracts:
            if contract.get('kind') == 'interface':
                features.append('Interface Contract')
            elif contract.get('kind') == 'library':
                features.append('Library Contract')
            elif contract.get('abstract'):
                features.append('Abstract Contract')
            else:
                features.append('Standard Contract')
        
        # Functional features
        functions = contract_structure.get('functions', [])
        for func in functions:
            if func.get('stateMutability') == 'payable':
                features.append('Payable Functions')
                break
        
        events = contract_structure.get('events', [])
        if events:
            features.append('Event Logging')
        
        modifiers = contract_structure.get('modifiers', [])
        if modifiers:
            features.append('Custom Modifiers')
        
        structs = contract_structure.get('structs', [])
        if structs:
            features.append('Custom Data Structures')
        
        # Security features
        security_patterns = contract_metadata.get('security_patterns', {})
        if security_patterns.get('access_control'):
            features.append('Access Control')
        
        if security_patterns.get('reentrancy_guards'):
            features.append('Reentrancy Protection')
        
        if security_patterns.get('overflow_checks'):
            features.append('Overflow Protection')
        
        return list(set(features))  # Remove duplicates
    
    def get_human_readable_contract(self, file_path: str) -> str:
        """
        Get human-readable description of the entire contract
        
        Args:
            file_path: Path to Solidity file
            
        Returns:
            Human-readable contract description
        """
        if file_path not in self.parsed_contracts:
            self.parse_contract_file(file_path)
        
        if file_path not in self.parsed_contracts:
            return "Failed to parse contract"
        
        contract_data = self.parsed_contracts[file_path]
        descriptions = contract_data['semantic_descriptions']
        summary = contract_data['analysis_summary']
        
        # Build readable description
        readable_parts = []
        
        # Contract overview
        readable_parts.append("=== CONTRACT OVERVIEW ===")
        readable_parts.append(f"Complexity Level: {summary.get('complexity_level', 'Unknown')}")
        readable_parts.append(f"Security Score: {summary.get('security_score', 0):.1f}/100")
        readable_parts.append(f"Key Features: {', '.join(summary.get('key_features', []))}")
        readable_parts.append("")
        
        # Contracts
        if descriptions.get('contracts'):
            readable_parts.append("=== CONTRACTS ===")
            readable_parts.extend(descriptions['contracts'])
            readable_parts.append("")
        
        # Functions
        if descriptions.get('functions'):
            readable_parts.append("=== FUNCTIONS ===")
            readable_parts.extend(descriptions['functions'])
            readable_parts.append("")
        
        # Variables
        if descriptions.get('variables'):
            readable_parts.append("=== STATE VARIABLES ===")
            readable_parts.extend(descriptions['variables'])
            readable_parts.append("")
        
        # Events
        if descriptions.get('events'):
            readable_parts.append("=== EVENTS ===")
            readable_parts.extend(descriptions['events'])
            readable_parts.append("")
        
        # Other elements (structs, enums, modifiers)
        for section_name, section_desc in [
            ('structs', 'STRUCTS'),
            ('enums', 'ENUMERATIONS'), 
            ('modifiers', 'MODIFIERS')
        ]:
            if descriptions.get(section_name):
                readable_parts.append(f"=== {section_desc} ===")
                readable_parts.extend(descriptions[section_name])
                readable_parts.append("")
        
        return "\n".join(readable_parts)
    
    def extract_entities_from_contract(self, file_path: str) -> List[Dict[str, Any]]:
        """
        Extract entities from smart contract for knowledge graph construction
        
        Args:
            file_path: Path to Solidity file
            
        Returns:
            List of entities with their properties
        """
        if file_path not in self.parsed_contracts:
            self.parse_contract_file(file_path)
        
        if file_path not in self.parsed_contracts:
            return []
        
        contract_data = self.parsed_contracts[file_path]
        structure = contract_data['contract_structure']
        
        entities = []
        entity_id = 0
        
        # Extract contracts as entities
        for contract in structure.get('contracts', []):
            entities.append({
                'id': f"contract_{entity_id}",
                'text': contract['name'],
                'type': 'CONTRACT',
                'properties': {
                    'kind': contract.get('kind', 'contract'),
                    'abstract': contract.get('abstract', False)
                }
            })
            entity_id += 1
        
        # Extract functions as entities
        for function in structure.get('functions', []):
            entities.append({
                'id': f"function_{entity_id}",
                'text': function['name'],
                'type': 'FUNCTION',
                'properties': {
                    'visibility': function.get('visibility', 'public'),
                    'stateMutability': function.get('stateMutability', 'nonpayable'),
                    'contract': function.get('contract', '')
                }
            })
            entity_id += 1
        
        # Extract variables as entities
        for variable in structure.get('variables', []):
            entities.append({
                'id': f"variable_{entity_id}",
                'text': variable['name'],
                'type': 'VARIABLE',
                'properties': {
                    'type': variable.get('type', 'unknown'),
                    'visibility': variable.get('visibility', 'internal'),
                    'constant': variable.get('constant', False),
                    'contract': variable.get('contract', '')
                }
            })
            entity_id += 1
        
        return entities