"""
Grammar engine for translating AST nodes to human-readable descriptions
"""

from typing import Dict, Any, List, Optional
import re

class GrammarEngine:
    """Converts AST node types into human-readable descriptions using grammar rules"""
    
    def __init__(self):
        self.grammar_rules = self._define_grammar_rules()
        self.type_mappings = self._define_type_mappings()
    
    def _define_grammar_rules(self) -> Dict[str, Dict[str, str]]:
        """Define grammar rules for different AST node types"""
        return {
            'ContractDefinition': {
                'template': "Contract '{name}' is defined as a {kind} contract{abstract_info}{inheritance_info}.",
                'fields': ['name', 'contractKind', 'abstract', 'baseContracts']
            },
            
            'FunctionDefinition': {
                'template': "Function '{name}' is {visibility} and {state_mutability}{virtual_info}{override_info}. It takes {param_count} parameter(s) and returns {return_count} value(s).",
                'fields': ['name', 'visibility', 'stateMutability', 'virtual', 'override', 'parameters', 'returnParameters']
            },
            
            'VariableDeclaration': {
                'template': "Variable '{name}' of type {type} is declared as {visibility}{constant_info}{immutable_info}.",
                'fields': ['name', 'typeName', 'visibility', 'constant', 'immutable']
            },
            
            'EventDefinition': {
                'template': "Event '{name}' is defined{anonymous_info} with {param_count} parameter(s).",
                'fields': ['name', 'anonymous', 'parameters']
            },
            
            'ModifierDefinition': {
                'template': "Modifier '{name}' is defined{virtual_info}{override_info}.",
                'fields': ['name', 'virtual', 'override']
            },
            
            'StructDefinition': {
                'template': "Struct '{name}' is defined with {member_count} member(s): {members}.",
                'fields': ['name', 'members']
            },
            
            'EnumDefinition': {
                'template': "Enum '{name}' is defined with values: {members}.",
                'fields': ['name', 'members']
            },
            
            'IfStatement': {
                'template': "Conditional statement: if {condition} then {true_action}{false_action}.",
                'fields': ['condition', 'trueBody', 'falseBody']
            },
            
            'WhileStatement': {
                'template': "Loop statement: while {condition} do {body}.",
                'fields': ['condition', 'body']
            },
            
            'ForStatement': {
                'template': "For loop: initialize {init}, condition {condition}, update {update}, body {body}.",
                'fields': ['initializationExpression', 'condition', 'loopExpression', 'body']
            },
            
            'Assignment': {
                'template': "Assignment: {left} = {right}.",
                'fields': ['left', 'right']
            },
            
            'BinaryOperation': {
                'template': "Binary operation: {left} {operator} {right}.",
                'fields': ['left', 'operator', 'right']
            },
            
            'UnaryOperation': {
                'template': "Unary operation: {operator} {operand}.",
                'fields': ['operator', 'subExpression']
            },
            
            'FunctionCall': {
                'template': "Function call to {function} with {arg_count} argument(s).",
                'fields': ['expression', 'arguments']
            },
            
            'Return': {
                'template': "Return statement{return_value}.",
                'fields': ['expression']
            },
            
            'Throw': {
                'template': "Throw statement (deprecated).",
                'fields': []
            },
            
            'EmitStatement': {
                'template': "Emit event: {event}.",
                'fields': ['eventCall']
            },
            
            'RevertStatement': {
                'template': "Revert transaction{reason}.",
                'fields': ['errorCall']
            },
            
            'RequireStatement': {
                'template': "Require condition: {condition}{message}.",
                'fields': ['condition', 'message']
            }
        }
    
    def _define_type_mappings(self) -> Dict[str, str]:
        """Define human-readable type mappings"""
        return {
            'uint': 'unsigned integer',
            'uint256': 'unsigned 256-bit integer',
            'uint128': 'unsigned 128-bit integer',
            'uint64': 'unsigned 64-bit integer',
            'uint32': 'unsigned 32-bit integer',
            'uint16': 'unsigned 16-bit integer',
            'uint8': 'unsigned 8-bit integer',
            'int': 'signed integer',
            'int256': 'signed 256-bit integer',
            'bool': 'boolean',
            'address': 'Ethereum address',
            'bytes': 'byte array',
            'bytes32': '32-byte array',
            'string': 'text string',
            'mapping': 'key-value mapping',
            'array': 'array',
            'struct': 'structured data',
            'enum': 'enumeration',
            'function': 'function type'
        }
    
    def apply_grammar(self, node_type: str, node_data: Dict[str, Any]) -> str:
        """
        Apply grammar rules to convert AST node to human-readable description
        
        Args:
            node_type: Type of AST node
            node_data: Node data dictionary
            
        Returns:
            Human-readable description
        """
        if node_type not in self.grammar_rules:
            return f"Unknown node type: {node_type}"
        
        rule = self.grammar_rules[node_type]
        template = rule['template']
        
        # Process template variables
        processed_template = self._process_template(template, node_data)
        
        return processed_template
    
    def _process_template(self, template: str, node_data: Dict[str, Any]) -> str:
        """Process template with node data"""
        result = template
        
        # Replace simple field references
        for field, value in node_data.items():
            placeholder = f"{{{field}}}"
            if placeholder in result:
                result = result.replace(placeholder, str(value))
        
        # Process complex placeholders
        result = self._process_complex_placeholders(result, node_data)
        
        return result
    
    def _process_complex_placeholders(self, template: str, node_data: Dict[str, Any]) -> str:
        """Process complex template placeholders"""
        result = template
        
        # Abstract info
        if '{abstract_info}' in result:
            abstract_info = ""
            if node_data.get('abstract', False):
                abstract_info = " (abstract)"
            result = result.replace('{abstract_info}', abstract_info)
        
        # Inheritance info
        if '{inheritance_info}' in result:
            inheritance_info = ""
            base_contracts = node_data.get('baseContracts', [])
            if base_contracts:
                base_names = [bc.get('baseName', {}).get('name', 'Unknown') for bc in base_contracts]
                inheritance_info = f" inheriting from {', '.join(base_names)}"
            result = result.replace('{inheritance_info}', inheritance_info)
        
        # Virtual info
        if '{virtual_info}' in result:
            virtual_info = ""
            if node_data.get('virtual', False):
                virtual_info = " (virtual)"
            result = result.replace('{virtual_info}', virtual_info)
        
        # Override info
        if '{override_info}' in result:
            override_info = ""
            if node_data.get('override'):
                override_info = " (override)"
            result = result.replace('{override_info}', override_info)
        
        # Constant info
        if '{constant_info}' in result:
            constant_info = ""
            if node_data.get('constant', False):
                constant_info = " constant"
            result = result.replace('{constant_info}', constant_info)
        
        # Immutable info
        if '{immutable_info}' in result:
            immutable_info = ""
            if node_data.get('immutable', False):
                immutable_info = " immutable"
            result = result.replace('{immutable_info}', immutable_info)
        
        # Anonymous info
        if '{anonymous_info}' in result:
            anonymous_info = ""
            if node_data.get('anonymous', False):
                anonymous_info = " (anonymous)"
            result = result.replace('{anonymous_info}', anonymous_info)
        
        # Parameter count
        if '{param_count}' in result:
            parameters = node_data.get('parameters', {})
            if isinstance(parameters, dict):
                param_count = len(parameters.get('parameters', []))
            else:
                param_count = len(parameters) if parameters else 0
            result = result.replace('{param_count}', str(param_count))
        
        # Return count
        if '{return_count}' in result:
            return_params = node_data.get('returnParameters', {})
            if isinstance(return_params, dict):
                return_count = len(return_params.get('parameters', []))
            else:
                return_count = len(return_params) if return_params else 0
            result = result.replace('{return_count}', str(return_count))
        
        # Member count
        if '{member_count}' in result:
            members = node_data.get('members', [])
            result = result.replace('{member_count}', str(len(members)))
        
        # Members list
        if '{members}' in result:
            members = node_data.get('members', [])
            if isinstance(members, list) and len(members) > 0:
                if isinstance(members[0], dict):
                    member_names = [m.get('name', 'unnamed') for m in members]
                else:
                    member_names = [str(m) for m in members]
                result = result.replace('{members}', ', '.join(member_names))
            else:
                result = result.replace('{members}', 'none')
        
        # Type processing
        if '{type}' in result:
            type_name = self._extract_type_description(node_data.get('typeName', {}))
            result = result.replace('{type}', type_name)
        
        # Condition processing
        if '{condition}' in result:
            condition = node_data.get('condition', {})
            condition_desc = self._describe_expression(condition)
            result = result.replace('{condition}', condition_desc)
        
        # Action processing
        if '{true_action}' in result:
            true_body = node_data.get('trueBody', {})
            action_desc = self._describe_statement(true_body)
            result = result.replace('{true_action}', action_desc)
        
        if '{false_action}' in result:
            false_body = node_data.get('falseBody')
            if false_body:
                action_desc = " else " + self._describe_statement(false_body)
            else:
                action_desc = ""
            result = result.replace('{false_action}', action_desc)
        
        # Argument count
        if '{arg_count}' in result:
            arguments = node_data.get('arguments', [])
            result = result.replace('{arg_count}', str(len(arguments)))
        
        # Return value
        if '{return_value}' in result:
            expression = node_data.get('expression')
            if expression:
                return_desc = " returning " + self._describe_expression(expression)
            else:
                return_desc = ""
            result = result.replace('{return_value}', return_desc)
        
        # State mutability
        if '{state_mutability}' in result:
            state_mut = node_data.get('stateMutability', 'nonpayable')
            readable_mut = {
                'pure': 'pure (no state access)',
                'view': 'view (read-only)',
                'payable': 'payable (can receive Ether)',
                'nonpayable': 'non-payable'
            }.get(state_mut, state_mut)
            result = result.replace('{state_mutability}', readable_mut)
        
        return result
    
    def _extract_type_description(self, type_node: Dict[str, Any]) -> str:
        """Extract human-readable type description"""
        if not isinstance(type_node, dict):
            return 'unknown type'
        
        node_type = type_node.get('nodeType', '')
        
        if node_type == 'ElementaryTypeName':
            type_name = type_node.get('name', 'unknown')
            return self.type_mappings.get(type_name, type_name)
        
        elif node_type == 'UserDefinedTypeName':
            return f"custom type '{type_node.get('name', 'unknown')}'"
        
        elif node_type == 'ArrayTypeName':
            base_type = self._extract_type_description(type_node.get('baseType', {}))
            return f"array of {base_type}"
        
        elif node_type == 'Mapping':
            key_type = self._extract_type_description(type_node.get('keyType', {}))
            value_type = self._extract_type_description(type_node.get('valueType', {}))
            return f"mapping from {key_type} to {value_type}"
        
        else:
            return type_node.get('name', 'complex type')
    
    def _describe_expression(self, expression: Dict[str, Any]) -> str:
        """Describe an expression in human-readable form"""
        if not isinstance(expression, dict):
            return str(expression)
        
        node_type = expression.get('nodeType', '')
        
        if node_type == 'Identifier':
            return f"variable '{expression.get('name', 'unknown')}'"
        
        elif node_type == 'Literal':
            value = expression.get('value', '')
            kind = expression.get('kind', '')
            if kind == 'string':
                return f"string \"{value}\""
            elif kind == 'number':
                return f"number {value}"
            elif kind == 'bool':
                return f"boolean {value}"
            else:
                return f"literal {value}"
        
        elif node_type == 'BinaryOperation':
            left = self._describe_expression(expression.get('left', {}))
            right = self._describe_expression(expression.get('right', {}))
            operator = expression.get('operator', '?')
            return f"({left} {operator} {right})"
        
        elif node_type == 'UnaryOperation':
            operand = self._describe_expression(expression.get('subExpression', {}))
            operator = expression.get('operator', '?')
            return f"{operator}{operand}"
        
        elif node_type == 'FunctionCall':
            function = self._describe_expression(expression.get('expression', {}))
            return f"call to {function}"
        
        else:
            return f"expression of type {node_type}"
    
    def _describe_statement(self, statement: Dict[str, Any]) -> str:
        """Describe a statement in human-readable form"""
        if not isinstance(statement, dict):
            return str(statement)
        
        node_type = statement.get('nodeType', '')
        
        if node_type == 'Block':
            statements = statement.get('statements', [])
            return f"block with {len(statements)} statement(s)"
        
        elif node_type == 'ExpressionStatement':
            expression = statement.get('expression', {})
            return self._describe_expression(expression)
        
        elif node_type == 'Return':
            expression = statement.get('expression')
            if expression:
                return f"return {self._describe_expression(expression)}"
            else:
                return "return"
        
        elif node_type == 'IfStatement':
            condition = self._describe_expression(statement.get('condition', {}))
            return f"if {condition}"
        
        else:
            return f"statement of type {node_type}"
    
    def generate_semantic_description(self, ast_structure: Dict[str, Any]) -> Dict[str, List[str]]:
        """
        Generate semantic descriptions for all elements in AST structure
        
        Args:
            ast_structure: Structured AST data
            
        Returns:
            Dictionary of semantic descriptions by category
        """
        descriptions = {
            'contracts': [],
            'functions': [],
            'variables': [],
            'events': [],
            'modifiers': [],
            'structs': [],
            'enums': []
        }
        
        for category, items in ast_structure.items():
            if category in descriptions:
                for item in items:
                    # Determine node type based on category
                    node_type_mapping = {
                        'contracts': 'ContractDefinition',
                        'functions': 'FunctionDefinition',
                        'variables': 'VariableDeclaration',
                        'events': 'EventDefinition',
                        'modifiers': 'ModifierDefinition',
                        'structs': 'StructDefinition',
                        'enums': 'EnumDefinition'
                    }
                    
                    node_type = node_type_mapping[category]
                    description = self.apply_grammar(node_type, item)
                    descriptions[category].append(description)
        
        return descriptions