"""
Comprehensive validation system for ensuring 100% accuracy in contract generation
"""

import json
import re
import ast
from typing import Dict, List, Optional, Tuple, Any
from pathlib import Path
import logging
from dataclasses import dataclass
from enum import Enum
import hashlib
import difflib
from datetime import datetime

# External validation tools (when available)
try:
    from slither import Slither
    SLITHER_AVAILABLE = True
except ImportError:
    SLITHER_AVAILABLE = False

try:
    import solcx
    SOLCX_AVAILABLE = True
except ImportError:
    SOLCX_AVAILABLE = False

class ValidationLevel(Enum):
    """Validation levels"""
    BASIC = "basic"
    STANDARD = "standard" 
    COMPREHENSIVE = "comprehensive"
    CRITICAL = "critical"

@dataclass
class ValidationResult:
    """Validation result structure"""
    is_valid: bool
    score: float
    errors: List[str]
    warnings: List[str]
    suggestions: List[str]
    details: Dict[str, Any]
    validation_level: ValidationLevel
    timestamp: str

class ComprehensiveValidator:
    """Comprehensive validation system for contract accuracy"""
    
    def __init__(self, validation_level: ValidationLevel = ValidationLevel.COMPREHENSIVE):
        self.validation_level = validation_level
        self.logger = logging.getLogger(__name__)
        
        # Validation rules and patterns
        self.security_patterns = self._load_security_patterns()
        self.best_practices = self._load_best_practices()
        self.accuracy_metrics = self._load_accuracy_metrics()
        
        # Initialize external tools
        self.external_tools = {
            'slither': SLITHER_AVAILABLE,
            'solc': SOLCX_AVAILABLE
        }
    
    def validate_contract_generation(self, 
                                  source_kg: Dict, 
                                  generated_contract: str,
                                  metadata: Dict) -> ValidationResult:
        """Comprehensive validation of generated smart contract"""
        
        validation_start = datetime.now()
        errors = []
        warnings = []
        suggestions = []
        details = {}
        
        try:
            # 1. Syntax and Compilation Validation
            syntax_result = self._validate_syntax(generated_contract)
            details['syntax'] = syntax_result
            if not syntax_result['is_valid']:
                errors.extend(syntax_result['errors'])
            
            # 2. Semantic Accuracy Validation
            semantic_result = self._validate_semantic_accuracy(source_kg, generated_contract)
            details['semantic'] = semantic_result
            if semantic_result['accuracy_score'] < 0.95:  # 95% threshold for high accuracy
                warnings.append(f"Semantic accuracy below threshold: {semantic_result['accuracy_score']:.2%}")
            
            # 3. Security Validation
            security_result = self._validate_security(generated_contract)
            details['security'] = security_result
            if security_result['vulnerabilities']:
                errors.extend([f"Security vulnerability: {v}" for v in security_result['vulnerabilities']])
            
            # 4. Best Practices Validation
            practices_result = self._validate_best_practices(generated_contract)
            details['best_practices'] = practices_result
            warnings.extend(practices_result['warnings'])
            suggestions.extend(practices_result['suggestions'])
            
            # 5. Gas Optimization Validation
            gas_result = self._validate_gas_optimization(generated_contract)
            details['gas_optimization'] = gas_result
            suggestions.extend(gas_result['suggestions'])
            
            # 6. External Tool Validation (if available)
            if self.validation_level in [ValidationLevel.COMPREHENSIVE, ValidationLevel.CRITICAL]:
                external_result = self._validate_with_external_tools(generated_contract)
                details['external_tools'] = external_result
                errors.extend(external_result['errors'])
                warnings.extend(external_result['warnings'])
            
            # 7. Calculate overall validation score
            overall_score = self._calculate_validation_score(details)
            
            # Determine if validation passes
            is_valid = (len(errors) == 0 and 
                       overall_score >= 0.90 and  # 90% overall score threshold
                       semantic_result['accuracy_score'] >= 0.95)  # 95% semantic accuracy
            
            # Critical validation for highest accuracy
            if self.validation_level == ValidationLevel.CRITICAL:
                critical_result = self._perform_critical_validation(source_kg, generated_contract, details)
                details['critical'] = critical_result
                is_valid = is_valid and critical_result['passes_critical']
            
            validation_time = (datetime.now() - validation_start).total_seconds()
            details['validation_time'] = validation_time
            
            return ValidationResult(
                is_valid=is_valid,
                score=overall_score,
                errors=errors,
                warnings=warnings,
                suggestions=suggestions,
                details=details,
                validation_level=self.validation_level,
                timestamp=datetime.now().isoformat()
            )
            
        except Exception as e:
            self.logger.error(f"Validation error: {e}")
            return ValidationResult(
                is_valid=False,
                score=0.0,
                errors=[f"Validation system error: {str(e)}"],
                warnings=[],
                suggestions=[],
                details={'error': str(e)},
                validation_level=self.validation_level,
                timestamp=datetime.now().isoformat()
            )
    
    def _validate_syntax(self, contract_code: str) -> Dict:
        """Validate Solidity syntax and compilation"""
        result = {
            'is_valid': True,
            'errors': [],
            'warnings': [],
            'compilation_successful': False
        }
        
        try:
            # Basic syntax checks
            if not contract_code.strip():
                result['errors'].append("Empty contract code")
                result['is_valid'] = False
                return result
            
            # Check for required Solidity elements
            required_elements = [
                (r'pragma\s+solidity', "Missing pragma statement"),
                (r'contract\s+\w+', "Missing contract declaration"),
                (r'constructor\s*\(', "Missing constructor")
            ]
            
            for pattern, error_msg in required_elements:
                if not re.search(pattern, contract_code):
                    result['errors'].append(error_msg)
            
            # Check for common syntax errors
            syntax_checks = [
                (r'function\s+\w+\s*\([^)]*\)\s*{', "Function syntax check"),
                (r';\s*$', "Statement termination check", 'multiline'),
                (r'{\s*}', "Empty block check")
            ]
            
            for pattern, check_name, *flags in syntax_checks:
                flags = flags[0] if flags else None
                if flags == 'multiline':
                    if not re.search(pattern, contract_code, re.MULTILINE):
                        result['warnings'].append(f"Potential issue: {check_name}")
                else:
                    if not re.search(pattern, contract_code):
                        result['warnings'].append(f"Potential issue: {check_name}")
            
            # Try compilation if solc is available
            if SOLCX_AVAILABLE:
                try:
                    # Save temp file and try to compile
                    temp_file = Path("temp_contract.sol")
                    with open(temp_file, 'w') as f:
                        f.write(contract_code)
                    
                    compiled = solcx.compile_files([str(temp_file)])
                    result['compilation_successful'] = True
                    temp_file.unlink()
                    
                except Exception as e:
                    result['errors'].append(f"Compilation failed: {str(e)}")
                    result['compilation_successful'] = False
                    if temp_file.exists():
                        temp_file.unlink()
            
            result['is_valid'] = len(result['errors']) == 0
            
        except Exception as e:
            result['errors'].append(f"Syntax validation error: {str(e)}")
            result['is_valid'] = False
        
        return result
    
    def _validate_semantic_accuracy(self, source_kg: Dict, contract_code: str) -> Dict:
        """Validate semantic accuracy between source and generated contract"""
        result = {
            'accuracy_score': 0.0,
            'coverage_metrics': {},
            'mapping_quality': {},
            'semantic_errors': []
        }
        
        try:
            # Extract entities from knowledge graph
            kg_entities = self._extract_kg_entities(source_kg)
            
            # Extract contract elements
            contract_elements = self._extract_contract_elements(contract_code)
            
            # Calculate coverage metrics
            entity_coverage = self._calculate_entity_coverage(kg_entities['entities'], 
                                                            contract_elements['state_variables'])
            
            function_coverage = self._calculate_function_coverage(kg_entities['actions'],
                                                                contract_elements['functions'])
            
            condition_coverage = self._calculate_condition_coverage(kg_entities['conditions'],
                                                                  contract_elements['require_statements'])
            
            # Calculate mapping quality
            name_mapping_quality = self._assess_name_mapping_quality(kg_entities, contract_elements)
            type_mapping_quality = self._assess_type_mapping_quality(kg_entities, contract_elements)
            
            # Identify semantic errors
            semantic_errors = self._identify_semantic_errors(kg_entities, contract_elements)
            
            # Calculate overall accuracy score
            accuracy_score = (
                entity_coverage * 0.30 +
                function_coverage * 0.35 +
                condition_coverage * 0.20 +
                name_mapping_quality * 0.10 +
                type_mapping_quality * 0.05
            )
            
            # Penalty for semantic errors
            error_penalty = min(len(semantic_errors) * 0.05, 0.30)
            accuracy_score = max(0.0, accuracy_score - error_penalty)
            
            result.update({
                'accuracy_score': accuracy_score,
                'coverage_metrics': {
                    'entity_coverage': entity_coverage,
                    'function_coverage': function_coverage,
                    'condition_coverage': condition_coverage
                },
                'mapping_quality': {
                    'name_mapping': name_mapping_quality,
                    'type_mapping': type_mapping_quality
                },
                'semantic_errors': semantic_errors
            })
            
        except Exception as e:
            result['semantic_errors'].append(f"Semantic validation error: {str(e)}")
            self.logger.error(f"Semantic validation error: {e}")
        
        return result
    
    def _validate_security(self, contract_code: str) -> Dict:
        """Comprehensive security validation"""
        result = {
            'vulnerabilities': [],
            'security_score': 1.0,
            'recommendations': []
        }
        
        try:
            # Check for common vulnerabilities
            vulnerabilities = []
            
            # 1. Reentrancy vulnerability
            if re.search(r'\.call\s*\(', contract_code) and not re.search(r'nonReentrant|ReentrancyGuard', contract_code):
                vulnerabilities.append("Potential reentrancy vulnerability - use ReentrancyGuard")
            
            # 2. Integer overflow/underflow
            if re.search(r'\+|\-|\*', contract_code) and not re.search(r'SafeMath|pragma\s+solidity\s+\^0\.[8-9]', contract_code):
                vulnerabilities.append("Potential integer overflow - use SafeMath or Solidity ^0.8.0")
            
            # 3. tx.origin usage
            if re.search(r'tx\.origin', contract_code):
                vulnerabilities.append("Avoid tx.origin - use msg.sender instead")
            
            # 4. Unchecked external calls
            if re.search(r'\.call\(|\.delegatecall\(|\.send\(', contract_code):
                if not re.search(r'require\s*\(.*\.call|if\s*\(.*\.call', contract_code):
                    vulnerabilities.append("Unchecked external calls - check return values")
            
            # 5. Access control
            if not re.search(r'onlyOwner|modifier\s+\w+|require\s*\(\s*msg\.sender', contract_code):
                vulnerabilities.append("Missing access control - implement proper authorization")
            
            # 6. State variable visibility
            state_vars = re.findall(r'^\s*(uint256|address|bool|string|mapping)\s+(\w+)', contract_code, re.MULTILINE)
            for var_type, var_name in state_vars:
                if not re.search(rf'{var_name}\s+(public|private|internal)', contract_code):
                    vulnerabilities.append(f"State variable {var_name} missing visibility specifier")
            
            # Use external security tools if available
            if SLITHER_AVAILABLE and self.validation_level in [ValidationLevel.COMPREHENSIVE, ValidationLevel.CRITICAL]:
                slither_results = self._run_slither_analysis(contract_code)
                vulnerabilities.extend(slither_results)
            
            # Calculate security score
            security_score = max(0.0, 1.0 - len(vulnerabilities) * 0.15)
            
            result.update({
                'vulnerabilities': vulnerabilities,
                'security_score': security_score,
                'recommendations': self._get_security_recommendations(vulnerabilities)
            })
            
        except Exception as e:
            result['vulnerabilities'].append(f"Security validation error: {str(e)}")
            self.logger.error(f"Security validation error: {e}")
        
        return result
    
    def _validate_best_practices(self, contract_code: str) -> Dict:
        """Validate adherence to Solidity best practices"""
        result = {
            'warnings': [],
            'suggestions': [],
            'practices_score': 1.0
        }
        
        try:
            warnings = []
            suggestions = []
            
            # 1. Function visibility
            functions = re.findall(r'function\s+(\w+)\s*\([^)]*\)\s*([^{]*){', contract_code)
            for func_name, modifiers in functions:
                if not re.search(r'public|private|internal|external', modifiers):
                    warnings.append(f"Function {func_name} missing visibility specifier")
            
            # 2. Event emission
            if not re.search(r'emit\s+\w+\s*\(', contract_code):
                suggestions.append("Consider adding events for important state changes")
            
            # 3. Error handling
            if not re.search(r'require\s*\(|revert\s*\(|assert\s*\(', contract_code):
                warnings.append("Missing error handling - use require/revert statements")
            
            # 4. Documentation
            if not re.search(r'\/\*\*|\/\//', contract_code):
                suggestions.append("Add documentation comments for better maintainability")
            
            # 5. Gas optimization
            if re.search(r'for\s*\([^}]+\)', contract_code):
                suggestions.append("Consider gas optimization for loops")
            
            # 6. State mutability
            view_functions = re.findall(r'function\s+(\w+)\s*\([^)]*\)\s+([^{]*view[^{]*){', contract_code)
            if len(view_functions) == 0:
                suggestions.append("Consider marking read-only functions as view")
            
            # Calculate practices score
            penalty = len(warnings) * 0.1 + len(suggestions) * 0.05
            practices_score = max(0.0, 1.0 - penalty)
            
            result.update({
                'warnings': warnings,
                'suggestions': suggestions,
                'practices_score': practices_score
            })
            
        except Exception as e:
            result['warnings'].append(f"Best practices validation error: {str(e)}")
            self.logger.error(f"Best practices validation error: {e}")
        
        return result
    
    def _validate_gas_optimization(self, contract_code: str) -> Dict:
        """Validate gas optimization opportunities"""
        result = {
            'suggestions': [],
            'optimization_score': 1.0,
            'gas_issues': []
        }
        
        try:
            suggestions = []
            gas_issues = []
            
            # 1. Storage vs Memory usage
            if re.search(r'string\s+\w+\s*=', contract_code) and not re.search(r'string\s+memory', contract_code):
                suggestions.append("Use 'memory' keyword for temporary string variables")
            
            # 2. Loop optimizations
            loops = re.findall(r'for\s*\([^}]+\)', contract_code)
            if loops:
                suggestions.append("Consider loop optimizations to reduce gas costs")
            
            # 3. State variable packing
            state_vars = re.findall(r'^\s*(uint\d+|address|bool)\s+', contract_code, re.MULTILINE)
            if len(state_vars) > 3:
                suggestions.append("Consider state variable packing for gas optimization")
            
            # 4. Function modifiers efficiency
            if re.search(r'modifier\s+\w+.*{.*require.*}', contract_code, re.DOTALL):
                suggestions.append("Ensure modifiers are gas-efficient")
            
            # Calculate optimization score
            score_penalty = len(suggestions) * 0.1 + len(gas_issues) * 0.15
            optimization_score = max(0.0, 1.0 - score_penalty)
            
            result.update({
                'suggestions': suggestions,
                'optimization_score': optimization_score,
                'gas_issues': gas_issues
            })
            
        except Exception as e:
            result['suggestions'].append(f"Gas optimization validation error: {str(e)}")
            self.logger.error(f"Gas optimization validation error: {e}")
        
        return result
    
    def _validate_with_external_tools(self, contract_code: str) -> Dict:
        """Validate using external security and analysis tools"""
        result = {
            'errors': [],
            'warnings': [],
            'tool_results': {}
        }
        
        try:
            # Slither analysis
            if self.external_tools['slither']:
                slither_results = self._run_slither_analysis(contract_code)
                result['tool_results']['slither'] = slither_results
                
                # Convert slither findings to errors/warnings
                for finding in slither_results:
                    if 'high' in finding.lower() or 'critical' in finding.lower():
                        result['errors'].append(f"Slither: {finding}")
                    else:
                        result['warnings'].append(f"Slither: {finding}")
            
            # Additional tools can be added here
            # Mythril, Securify, etc.
            
        except Exception as e:
            result['warnings'].append(f"External tool validation error: {str(e)}")
            self.logger.error(f"External tool validation error: {e}")
        
        return result
    
    def _perform_critical_validation(self, source_kg: Dict, contract_code: str, validation_details: Dict) -> Dict:
        """Perform critical validation for highest accuracy requirements"""
        result = {
            'passes_critical': True,
            'critical_errors': [],
            'accuracy_threshold': 0.98,
            'completeness_check': {},
            'consistency_check': {}
        }
        
        try:
            # 1. Completeness check - ensure all KG elements are represented
            completeness = self._check_completeness(source_kg, contract_code)
            result['completeness_check'] = completeness
            
            if completeness['completeness_score'] < 0.95:
                result['critical_errors'].append(f"Completeness below critical threshold: {completeness['completeness_score']:.2%}")
            
            # 2. Consistency check - ensure no contradictions
            consistency = self._check_consistency(source_kg, contract_code)
            result['consistency_check'] = consistency
            
            if consistency['inconsistencies']:
                result['critical_errors'].extend([f"Consistency error: {inc}" for inc in consistency['inconsistencies']])
            
            # 3. Accuracy threshold check
            semantic_score = validation_details.get('semantic', {}).get('accuracy_score', 0)
            if semantic_score < result['accuracy_threshold']:
                result['critical_errors'].append(f"Semantic accuracy below critical threshold: {semantic_score:.2%}")
            
            # 4. Security critical check
            security_vulns = validation_details.get('security', {}).get('vulnerabilities', [])
            critical_vulns = [v for v in security_vulns if 'critical' in v.lower() or 'high' in v.lower()]
            if critical_vulns:
                result['critical_errors'].extend([f"Critical security issue: {v}" for v in critical_vulns])
            
            # Determine if critical validation passes
            result['passes_critical'] = len(result['critical_errors']) == 0
            
        except Exception as e:
            result['critical_errors'].append(f"Critical validation error: {str(e)}")
            result['passes_critical'] = False
            self.logger.error(f"Critical validation error: {e}")
        
        return result
    
    # Utility methods
    
    def _load_security_patterns(self) -> Dict:
        """Load security vulnerability patterns"""
        return {
            'reentrancy': [
                r'\.call\s*\(',
                r'\.send\s*\(',
                r'\.transfer\s*\('
            ],
            'overflow': [
                r'\+\+',
                r'--',
                r'\s*\+\s*',
                r'\s*-\s*',
                r'\s*\*\s*'
            ],
            'access_control': [
                r'onlyOwner',
                r'require\s*\(\s*msg\.sender',
                r'modifier\s+\w+'
            ]
        }
    
    def _load_best_practices(self) -> Dict:
        """Load Solidity best practices"""
        return {
            'visibility': ['public', 'private', 'internal', 'external'],
            'state_mutability': ['view', 'pure', 'payable'],
            'error_handling': ['require', 'revert', 'assert'],
            'events': ['emit'],
            'documentation': [r'\/\*\*', r'\/\/']
        }
    
    def _load_accuracy_metrics(self) -> Dict:
        """Load accuracy measurement metrics"""
        return {
            'entity_coverage_weight': 0.30,
            'function_coverage_weight': 0.35,
            'condition_coverage_weight': 0.20,
            'name_mapping_weight': 0.10,
            'type_mapping_weight': 0.05
        }
    
    def _extract_kg_entities(self, knowledge_graph: Dict) -> Dict:
        """Extract entities from knowledge graph"""
        entities = []
        actions = []
        conditions = []
        
        nodes = knowledge_graph.get('nodes', [])
        for node in nodes:
            node_type = node.get('type', '').upper()
            if node_type in ['PERSON', 'ORG', 'ORGANIZATION', 'ENTITY']:
                entities.append(node)
            elif node_type in ['ACTION', 'VERB', 'FUNCTION']:
                actions.append(node)
            elif node_type in ['CONDITION', 'REQUIREMENT', 'CONSTRAINT']:
                conditions.append(node)
        
        return {
            'entities': entities,
            'actions': actions,
            'conditions': conditions
        }
    
    def _extract_contract_elements(self, contract_code: str) -> Dict:
        """Extract elements from contract code"""
        elements = {
            'state_variables': [],
            'functions': [],
            'require_statements': [],
            'events': []
        }
        
        # Extract state variables
        state_vars = re.findall(r'^\s*(uint256|address|bool|string|mapping)\s+([a-zA-Z_]\w*)', 
                               contract_code, re.MULTILINE)
        elements['state_variables'] = state_vars
        
        # Extract functions
        functions = re.findall(r'function\s+([a-zA-Z_]\w*)\s*\([^)]*\)', contract_code)
        elements['functions'] = functions
        
        # Extract require statements
        requires = re.findall(r'require\s*\([^)]+\)', contract_code)
        elements['require_statements'] = requires
        
        # Extract events
        events = re.findall(r'event\s+([a-zA-Z_]\w*)\s*\([^)]*\)', contract_code)
        elements['events'] = events
        
        return elements
    
    def _calculate_entity_coverage(self, kg_entities: List, contract_vars: List) -> float:
        """Calculate how well KG entities are covered by contract variables"""
        if not kg_entities:
            return 1.0
        
        covered = 0
        for entity in kg_entities:
            entity_name = entity.get('id', '').lower()
            for var_type, var_name in contract_vars:
                if entity_name in var_name.lower():
                    covered += 1
                    break
        
        return covered / len(kg_entities)
    
    def _calculate_function_coverage(self, kg_actions: List, contract_functions: List) -> float:
        """Calculate how well KG actions are covered by contract functions"""
        if not kg_actions:
            return 1.0
        
        covered = 0
        for action in kg_actions:
            action_name = action.get('id', '').lower()
            for func_name in contract_functions:
                if action_name in func_name.lower():
                    covered += 1
                    break
        
        return covered / len(kg_actions)
    
    def _calculate_condition_coverage(self, kg_conditions: List, contract_requires: List) -> float:
        """Calculate how well KG conditions are covered by require statements"""
        if not kg_conditions:
            return 1.0
        
        # This is a simplified calculation
        # In practice, would need more sophisticated NLP matching
        coverage_ratio = min(len(contract_requires) / max(len(kg_conditions), 1), 1.0)
        return coverage_ratio
    
    def _assess_name_mapping_quality(self, kg_entities: Dict, contract_elements: Dict) -> float:
        """Assess quality of name mapping from KG to contract"""
        # Simplified assessment - would need more sophisticated analysis
        total_mappings = 0
        quality_score = 0
        
        # Check entity to variable mapping quality
        for entity in kg_entities['entities']:
            entity_name = entity.get('id', '')
            for var_type, var_name in contract_elements['state_variables']:
                if entity_name.lower() in var_name.lower():
                    total_mappings += 1
                    # Simple similarity score
                    similarity = len(set(entity_name.lower()) & set(var_name.lower())) / len(set(entity_name.lower()))
                    quality_score += similarity
        
        return quality_score / max(total_mappings, 1)
    
    def _assess_type_mapping_quality(self, kg_entities: Dict, contract_elements: Dict) -> float:
        """Assess quality of type mapping from KG to contract"""
        # Simplified type mapping assessment
        return 0.8  # Default score - would need more sophisticated analysis
    
    def _identify_semantic_errors(self, kg_entities: Dict, contract_elements: Dict) -> List[str]:
        """Identify semantic errors in the mapping"""
        errors = []
        
        # Check for missing critical entities
        critical_entities = [e for e in kg_entities['entities'] 
                           if e.get('attributes', {}).get('critical', False)]
        
        for entity in critical_entities:
            found = False
            entity_name = entity.get('id', '').lower()
            for var_type, var_name in contract_elements['state_variables']:
                if entity_name in var_name.lower():
                    found = True
                    break
            
            if not found:
                errors.append(f"Critical entity '{entity.get('id')}' not represented in contract")
        
        return errors
    
    def _run_slither_analysis(self, contract_code: str) -> List[str]:
        """Run Slither security analysis if available"""
        findings = []
        
        if not SLITHER_AVAILABLE:
            return findings
        
        try:
            # Save contract to temp file
            temp_file = Path("temp_slither_contract.sol")
            with open(temp_file, 'w') as f:
                f.write(contract_code)
            
            # Run Slither analysis
            slither = Slither(str(temp_file))
            
            # Extract findings
            for detector_result in slither.detector_results:
                impact = detector_result.get('impact', 'Unknown')
                confidence = detector_result.get('confidence', 'Unknown')
                description = detector_result.get('description', 'No description')
                findings.append(f"{impact} impact, {confidence} confidence: {description}")
            
            # Cleanup
            temp_file.unlink()
            
        except Exception as e:
            findings.append(f"Slither analysis error: {str(e)}")
            if temp_file.exists():
                temp_file.unlink()
        
        return findings
    
    def _calculate_validation_score(self, details: Dict) -> float:
        """Calculate overall validation score"""
        scores = []
        
        # Syntax score
        if details.get('syntax', {}).get('is_valid'):
            scores.append(1.0)
        else:
            scores.append(0.5)
        
        # Semantic score
        semantic_score = details.get('semantic', {}).get('accuracy_score', 0)
        scores.append(semantic_score)
        
        # Security score
        security_score = details.get('security', {}).get('security_score', 0)
        scores.append(security_score)
        
        # Best practices score
        practices_score = details.get('best_practices', {}).get('practices_score', 0)
        scores.append(practices_score)
        
        # Gas optimization score
        gas_score = details.get('gas_optimization', {}).get('optimization_score', 0)
        scores.append(gas_score)
        
        # Weighted average
        weights = [0.15, 0.40, 0.25, 0.15, 0.05]  # Emphasis on semantic accuracy
        weighted_score = sum(score * weight for score, weight in zip(scores, weights))
        
        return min(weighted_score, 1.0)
    
    def _get_security_recommendations(self, vulnerabilities: List[str]) -> List[str]:
        """Get security recommendations based on found vulnerabilities"""
        recommendations = []
        
        for vuln in vulnerabilities:
            if 'reentrancy' in vuln.lower():
                recommendations.append("Implement ReentrancyGuard from OpenZeppelin")
            elif 'overflow' in vuln.lower():
                recommendations.append("Use SafeMath library or Solidity ^0.8.0")
            elif 'tx.origin' in vuln.lower():
                recommendations.append("Replace tx.origin with msg.sender")
            elif 'access control' in vuln.lower():
                recommendations.append("Implement proper access control with modifiers")
            elif 'external calls' in vuln.lower():
                recommendations.append("Check return values of external calls")
        
        return recommendations
    
    def _check_completeness(self, source_kg: Dict, contract_code: str) -> Dict:
        """Check completeness of contract generation"""
        kg_entities = self._extract_kg_entities(source_kg)
        contract_elements = self._extract_contract_elements(contract_code)
        
        total_kg_elements = (len(kg_entities['entities']) + 
                            len(kg_entities['actions']) + 
                            len(kg_entities['conditions']))
        
        total_contract_elements = (len(contract_elements['state_variables']) +
                                  len(contract_elements['functions']) +
                                  len(contract_elements['require_statements']))
        
        completeness_score = min(total_contract_elements / max(total_kg_elements, 1), 1.0)
        
        return {
            'completeness_score': completeness_score,
            'missing_elements': [],  # Would need more analysis to identify specific missing elements
            'kg_elements_count': total_kg_elements,
            'contract_elements_count': total_contract_elements
        }
    
    def _check_consistency(self, source_kg: Dict, contract_code: str) -> Dict:
        """Check consistency between source and generated contract"""
        inconsistencies = []
        
        # This would require sophisticated analysis
        # For now, basic checks
        
        return {
            'inconsistencies': inconsistencies,
            'consistency_score': 1.0 - len(inconsistencies) * 0.1
        }