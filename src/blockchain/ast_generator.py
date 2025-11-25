
import os
import json
import re
import subprocess
from typing import Dict, Any, Optional, List
from pathlib import Path

try:
    from solcx import compile_source, install_solc, get_installed_solc_versions, set_solc_version
    SOLCX_AVAILABLE = True
except ImportError:
    SOLCX_AVAILABLE = False
    print("solcx not available. Install with: pip install py-solc-x")

try:
    from ..utils.config import Config
    from ..utils.file_handler import FileHandler
except ImportError:
    from utils.config import Config
    from utils.file_handler import FileHandler

class ASTGenerator:
    
    _installation_attempted = False
    _compiler_available = False
    
    def __init__(self):
        self.solc_version = None
        self.compiler_output = None
        if not ASTGenerator._installation_attempted:
            self._ensure_solc_installation()
        else:
            self.solc_version = None if not ASTGenerator._compiler_available else 'fallback'
    
    def _ensure_solc_installation(self):
        ASTGenerator._installation_attempted = True
        
        if not SOLCX_AVAILABLE:
            print("⚠️  solcx not available - using fallback AST generation")
            ASTGenerator._compiler_available = False
            return
        
        try:
            installed_versions = get_installed_solc_versions()
            if installed_versions:
                self.solc_version = str(max(installed_versions))
                ASTGenerator._compiler_available = True
                print(f"Using existing Solidity compiler version: {self.solc_version}")
                return
            
            import ssl
            import urllib3
            
            try:
                urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
            except:
                pass
            
            ssl._create_default_https_context = ssl._create_unverified_context
            
            print("🔄 Installing Solidity compiler (one-time setup)...")
            try:
                install_solc('0.8.16', timeout=30)
                set_solc_version('0.8.16')
                self.solc_version = '0.8.16'
                ASTGenerator._compiler_available = True
                print("✅ Solidity compiler installed successfully")
                return
            except Exception as install_error:
                print("⚠️  Compiler installation failed: Network/SSL certificate issues detected")
                print("✅ Continuing with fallback AST generation (offline mode)")
            
            self.solc_version = None
            ASTGenerator._compiler_available = False
            
        except Exception as e:
            print(f"Error setting up Solidity compiler: {e}")
            print("Continuing with fallback AST generation...")
            self.solc_version = None
            ASTGenerator._compiler_available = False
    
    def extract_solidity_version(self, source_code: str) -> Optional[str]:
        pragma_pattern = r'pragma\s+solidity\s+([^;]+);'
        match = re.search(pragma_pattern, source_code, re.IGNORECASE)
        
        if match:
            version_spec = match.group(1).strip()
            
            version_patterns = [
                r'(\d+\.\d+\.\d+)',  # Exact version like 0.8.19
                r'\^(\d+\.\d+\.\d+)',  # Compatible version like ^0.8.0
                r'>=(\d+\.\d+\.\d+)',  # Minimum version
            ]
            
            for pattern in version_patterns:
                version_match = re.search(pattern, version_spec)
                if version_match:
                    return version_match.group(1)
            
            version_match = re.search(r'(\d+\.\d+)', version_spec)
            if version_match:
                return version_match.group(1) + '.0'
        
        return None
    
    def select_compiler_version(self, version: str) -> bool:
        if not SOLCX_AVAILABLE:
            return False
        
        try:
            installed_versions = get_installed_solc_versions()
            
            if version in [str(v) for v in installed_versions]:
                set_solc_version(version)
                self.solc_version = version
                return True
            
            print(f"Installing Solidity compiler version {version}...")
            install_solc(version)
            set_solc_version(version)
            self.solc_version = version
            return True
            
        except Exception as e:
            print(f"Error selecting compiler version {version}: {e}")
            if installed_versions:
                fallback_version = str(max(installed_versions))
                set_solc_version(fallback_version)
                self.solc_version = fallback_version
                print(f"Using fallback compiler version {fallback_version}")
                return True
            return False
    
    def generate_ast(self, source_code: str) -> Dict[str, Any]:
        if self.solc_version is None or not SOLCX_AVAILABLE:
            return self._generate_fallback_ast(source_code)
            
        result = self.compile_and_generate_ast(source_code)
        if result is None:
            return self._generate_fallback_ast(source_code)
        return result
        
    def _generate_fallback_ast(self, source_code: str) -> Dict[str, Any]:
        try:
            import re
            
            contract_match = re.search(r'contract\s+(\w+)', source_code)
            contract_name = contract_match.group(1) if contract_match else 'UnknownContract'
            
            function_matches = re.findall(r'function\s+(\w+)\s*\([^)]*\)', source_code)
            
            event_matches = re.findall(r'event\s+(\w+)\s*\([^)]*\)', source_code)
            
            return {
                'contract_name': contract_name,
                'ast': {
                    'functions': function_matches,
                    'events': event_matches,
                    'type': 'fallback_ast'
                },
                'compilation_successful': False,
                'fallback_parsing': True,
                'compiler_version': 'fallback'
            }
            
        except Exception as e:
            return {
                'contract_name': 'ErrorContract',
                'ast': {},
                'compilation_successful': False,
                'error': str(e),
                'compiler_version': 'error'
            }

    def compile_and_generate_ast(self, source_code: str, contract_name: str = None) -> Optional[Dict[str, Any]]:
        if not SOLCX_AVAILABLE:
            print("Solidity compiler not available")
            return None
        
        try:
            version = self.extract_solidity_version(source_code)
            if version:
                if not self.select_compiler_version(version):
                    print(f"Failed to set compiler version {version}")
            
            try:
                compiled_sol = compile_source(
                    source_code,
                    output_values=['ast', 'abi', 'bin']
                )
            except Exception as compile_error:
                print(f"Modern compilation failed: {compile_error}")
                try:
                    compiled_sol = compile_source(
                        source_code,
                        output_values=['ast', 'abi']
                    )
                except Exception as fallback_error:
                    print(f"Basic compilation also failed: {fallback_error}")
                    return self._generate_fallback_ast(source_code)
            
            self.compiler_output = compiled_sol
            
            ast_data = {}
            for contract_id, contract_data in compiled_sol.items():
                if 'ast' in contract_data:
                    ast_data[contract_id] = contract_data['ast']
                
                ast_data[f"{contract_id}_info"] = {
                    'abi': contract_data.get('abi', []),
                    'bytecode': contract_data.get('bin', contract_data.get('bytecode', '')),
                    'devdoc': contract_data.get('devdoc', {}),
                    'userdoc': contract_data.get('userdoc', {}),
                    'compilation_success': True
                }
            
            return ast_data
            
        except Exception as e:
            print(f"Error compiling Solidity code: {e}")
            return None
    
    def save_ast_as_json(self, ast_data: Dict[str, Any], output_path: str) -> bool:
        try:
            return FileHandler.write_json_file(output_path, ast_data)
        except Exception as e:
            print(f"Error saving AST to JSON: {e}")
            return False
    
    def extract_contract_structure(self, ast_data: Dict[str, Any]) -> Dict[str, Any]:
        structure = {
            'contracts': [],
            'functions': [],
            'variables': [],
            'events': [],
            'modifiers': [],
            'structs': [],
            'enums': []
        }
        
        def traverse_node(node, parent_contract=None):
            if not isinstance(node, dict):
                return
            
            node_type = node.get('nodeType', '')
            
            if node_type == 'ContractDefinition':
                contract_info = {
                    'name': node.get('name', ''),
                    'kind': node.get('contractKind', ''),
                    'abstract': node.get('abstract', False),
                    'id': node.get('id', ''),
                    'linearizedBaseContracts': node.get('linearizedBaseContracts', [])
                }
                structure['contracts'].append(contract_info)
                parent_contract = contract_info['name']
            
            elif node_type == 'FunctionDefinition':
                function_info = {
                    'name': node.get('name', ''),
                    'visibility': node.get('visibility', ''),
                    'stateMutability': node.get('stateMutability', ''),
                    'virtual': node.get('virtual', False),
                    'override': node.get('override', False),
                    'contract': parent_contract,
                    'id': node.get('id', '')
                }
                
                parameters = node.get('parameters', {}).get('parameters', [])
                function_info['parameters'] = [
                    {
                        'name': p.get('name', ''),
                        'type': self._extract_type_name(p.get('typeName', {}))
                    } for p in parameters
                ]
                
                return_params = node.get('returnParameters', {}).get('parameters', [])
                function_info['returnParameters'] = [
                    {
                        'name': p.get('name', ''),
                        'type': self._extract_type_name(p.get('typeName', {}))
                    } for p in return_params
                ]
                
                structure['functions'].append(function_info)
            
            elif node_type == 'VariableDeclaration':
                variable_info = {
                    'name': node.get('name', ''),
                    'type': self._extract_type_name(node.get('typeName', {})),
                    'visibility': node.get('visibility', ''),
                    'constant': node.get('constant', False),
                    'immutable': node.get('immutable', False),
                    'contract': parent_contract,
                    'id': node.get('id', '')
                }
                structure['variables'].append(variable_info)
            
            elif node_type == 'EventDefinition':
                event_info = {
                    'name': node.get('name', ''),
                    'anonymous': node.get('anonymous', False),
                    'contract': parent_contract,
                    'id': node.get('id', '')
                }
                
                parameters = node.get('parameters', {}).get('parameters', [])
                event_info['parameters'] = [
                    {
                        'name': p.get('name', ''),
                        'type': self._extract_type_name(p.get('typeName', {})),
                        'indexed': p.get('indexed', False)
                    } for p in parameters
                ]
                
                structure['events'].append(event_info)
            
            elif node_type == 'ModifierDefinition':
                modifier_info = {
                    'name': node.get('name', ''),
                    'virtual': node.get('virtual', False),
                    'override': node.get('override', False),
                    'contract': parent_contract,
                    'id': node.get('id', '')
                }
                structure['modifiers'].append(modifier_info)
            
            elif node_type == 'StructDefinition':
                struct_info = {
                    'name': node.get('name', ''),
                    'contract': parent_contract,
                    'id': node.get('id', ''),
                    'members': []
                }
                
                members = node.get('members', [])
                for member in members:
                    struct_info['members'].append({
                        'name': member.get('name', ''),
                        'type': self._extract_type_name(member.get('typeName', {}))
                    })
                
                structure['structs'].append(struct_info)
            
            elif node_type == 'EnumDefinition':
                enum_info = {
                    'name': node.get('name', ''),
                    'contract': parent_contract,
                    'id': node.get('id', ''),
                    'members': [m.get('name', '') for m in node.get('members', [])]
                }
                structure['enums'].append(enum_info)
            
            if 'nodes' in node:
                for child_node in node['nodes']:
                    traverse_node(child_node, parent_contract)
            
            for key in ['body', 'statements', 'trueBody', 'falseBody']:
                if key in node:
                    if isinstance(node[key], list):
                        for child in node[key]:
                            traverse_node(child, parent_contract)
                    else:
                        traverse_node(node[key], parent_contract)
        
        for contract_id, ast in ast_data.items():
            if isinstance(ast, dict) and 'nodes' in ast:
                for node in ast['nodes']:
                    traverse_node(node)
        
        return structure
    
    def _extract_type_name(self, type_node: Dict[str, Any]) -> str:
        if not isinstance(type_node, dict):
            return 'unknown'
        
        node_type = type_node.get('nodeType', '')
        
        if node_type == 'ElementaryTypeName':
            return type_node.get('name', 'unknown')
        elif node_type == 'UserDefinedTypeName':
            return type_node.get('name', 'unknown')
        elif node_type == 'ArrayTypeName':
            base_type = self._extract_type_name(type_node.get('baseType', {}))
            return f"{base_type}[]"
        elif node_type == 'Mapping':
            key_type = self._extract_type_name(type_node.get('keyType', {}))
            value_type = self._extract_type_name(type_node.get('valueType', {}))
            return f"mapping({key_type} => {value_type})"
        else:
            return type_node.get('name', 'unknown')
    
    def generate_ast_from_file(self, file_path: str) -> Optional[Dict[str, Any]]:
        try:
            solidity_data = FileHandler.read_solidity_file(file_path)
            if not solidity_data:
                return None
            
            source_code = solidity_data['content']
            contract_name = solidity_data['file_name']
            
            return self.compile_and_generate_ast(source_code, contract_name)
            
        except Exception as e:
            print(f"Error generating AST from file {file_path}: {e}")
            return None