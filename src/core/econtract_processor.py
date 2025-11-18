"""
E-Contract processor implementing Algorithm 1: E-Contract Knowledge Graph Construction
"""

from typing import Dict, Any, List, Optional
import os
from datetime import datetime

try:
    from ..nlp.preprocessor import TextPreprocessor
    from ..nlp.entity_extractor import EntityExtractor
    from ..nlp.dependency_parser import DependencyParser
    from ..nlp.business_relationship_extractor import BusinessRelationshipExtractor
    from .knowledge_graph import KnowledgeGraph
    from ..utils.file_handler import FileHandler
    from ..utils.config import Config
except ImportError:
    from nlp.preprocessor import TextPreprocessor
    from nlp.entity_extractor import EntityExtractor
    from nlp.dependency_parser import DependencyParser
    from nlp.business_relationship_extractor import BusinessRelationshipExtractor
    from core.knowledge_graph import KnowledgeGraph
    from utils.file_handler import FileHandler
    from utils.config import Config

class EContractProcessor:
    """
    Processes e-contracts to generate knowledge graphs
    Implements Algorithm 1 from the research paper
    """
    
    def __init__(self):
        self.preprocessor = TextPreprocessor()
        self.entity_extractor = EntityExtractor()
        self.dependency_parser = DependencyParser()
        self.business_relationship_extractor = BusinessRelationshipExtractor()
        self.processed_contracts = {}
    
    def process_contract(self, contract_text: str, contract_id: str = None) -> KnowledgeGraph:
        """
        Algorithm 1: E-Contract Knowledge Graph Construction
        
        Args:
            contract_text: Raw e-contract text
            contract_id: Optional identifier for the contract
            
        Returns:
            Knowledge graph G_e = (V_e, E_e)
        """
        if contract_id is None:
            contract_id = f"contract_{datetime.now().strftime('%Y%m%d_%H%M%S')}"
        
        print(f"Processing e-contract: {contract_id}")
        
        # Step 1: Preprocess the text (T'_e ← Preprocess(T_e))
        print("Step 1: Preprocessing contract text...")
        preprocessed_data = self.preprocessor.preprocess_contract(contract_text)
        
        # Step 2: Extract entities (V_e ← ExtractEntities(T'_e))
        print("Step 2: Extracting entities...")
        entities = self.entity_extractor.extract_all_entities(preprocessed_data['cleaned_text'])
        
        # Step 3: Extract relations (E_e ← ExtractRelations(T'_e))
        print("Step 3: Extracting relationships...")
        # Use enhanced business relationship extractor
        relationships = self.business_relationship_extractor.extract_business_relationships(
            preprocessed_data['cleaned_text'], entities
        )
        
        # Fallback to dependency parser if business extractor returns few relationships
        if len(relationships) < 3:
            print("Step 3b: Adding dependency-based relationships...")
            dependency_relationships = self.dependency_parser.extract_all_relationships(
                preprocessed_data['cleaned_text'], entities
            )
            relationships.extend(dependency_relationships)
        
        # Step 4: Construct knowledge graph (G_e ← (V_e, E_e))
        print("Step 4: Constructing knowledge graph...")
        knowledge_graph = self._construct_knowledge_graph(
            entities, relationships, preprocessed_data, contract_id
        )
        
        # Store processed contract data
        self.processed_contracts[contract_id] = {
            'original_text': contract_text,
            'preprocessed_data': preprocessed_data,
            'entities': entities,
            'relationships': relationships,
            'knowledge_graph': knowledge_graph,
            'processing_time': datetime.now().isoformat()
        }
        
        print(f"E-contract processing completed for {contract_id}")
        print(f"Generated {len(entities)} entities and {len(relationships)} relationships")
        
        return knowledge_graph
    
    def _construct_knowledge_graph(self, entities: List[Dict[str, Any]], 
                                 relationships: List[Dict[str, Any]],
                                 preprocessed_data: Dict[str, Any],
                                 contract_id: str) -> KnowledgeGraph:
        """Construct the knowledge graph from entities and relationships"""
        
        # Initialize knowledge graph
        kg = KnowledgeGraph('econtract')
        kg.metadata.update({
            'source_file': contract_id,
            'creation_time': datetime.now().isoformat(),
            'preprocessing_stats': {
                'word_count': preprocessed_data.get('word_count', 0),
                'sentence_count': preprocessed_data.get('sentence_count', 0),
                'section_count': preprocessed_data.get('section_count', 0)
            }
        })
        
        # Add entities to the graph
        for entity in entities:
            entity_data = {
                'text': entity['text'],
                'type': entity['label'],
                'confidence': entity.get('confidence', 1.0),
                'start_pos': entity.get('start', -1),
                'end_pos': entity.get('end', -1),
                'extraction_method': entity.get('type', 'unknown'),
                'category': self._categorize_entity(entity)
            }
            
            kg.add_entity(entity['id'], entity_data)
        
        # Add relationships to the graph
        for relationship in relationships:
            # Check if relationship already has entity IDs
            source_id = relationship.get('source')
            target_id = relationship.get('target')
            
            # If source/target are already entity IDs, use them directly
            if source_id in [e['id'] for e in entities] and target_id in [e['id'] for e in entities]:
                source_entity = next(e for e in entities if e['id'] == source_id)
                target_entity = next(e for e in entities if e['id'] == target_id)
            else:
                # Otherwise, find entities by text
                source_entity = self._find_entity_by_text(entities, relationship.get('source', ''))
                target_entity = self._find_entity_by_text(entities, relationship.get('target', ''))
            
            if source_entity and target_entity:
                rel_data = {
                    'relation': relationship.get('relation', 'unknown'),
                    'confidence': relationship.get('confidence', 1.0),
                    'sentence': relationship.get('sentence', ''),
                    'pattern': relationship.get('pattern', ''),
                    'source_type': source_entity.get('label', 'UNKNOWN'),
                    'target_type': target_entity.get('label', 'UNKNOWN'),
                    'extraction_method': relationship.get('extraction_method', 'unknown')
                }
                
                kg.add_relationship(
                    relationship['id'],
                    source_entity['id'],
                    target_entity['id'],
                    rel_data
                )
        
        return kg
    
    def _categorize_entity(self, entity: Dict[str, Any]) -> str:
        """Categorize entity into contract-specific categories"""
        entity_type = entity.get('label', 'UNKNOWN').upper()
        
        # Contract-specific categorization
        category_mapping = {
            'PERSON': 'PARTY',
            'ORG': 'ORGANIZATION', 
            'PARTIES': 'PARTY',
            'CONTRACT_PARTY': 'PARTY',
            'MONEY': 'FINANCIAL',
            'MONETARY_AMOUNT': 'FINANCIAL',
            'CURRENCY': 'FINANCIAL',
            'PERCENTAGE': 'FINANCIAL',
            'DATE': 'TEMPORAL',
            'DATE_TERMS': 'TEMPORAL',
            'TIME': 'TEMPORAL',
            'OBLIGATIONS': 'LEGAL_OBLIGATION',
            'LEGAL_TERMS': 'LEGAL_PROVISION',
            'CONDITIONS': 'CONDITION',
            'GPE': 'LOCATION',
            'ADDRESS': 'LOCATION',
            'EMAIL': 'CONTACT_INFO',
            'PHONE': 'CONTACT_INFO',
            'CONTRACT_REF': 'REFERENCE'
        }
        
        return category_mapping.get(entity_type, 'OTHER')
    
    def _find_entity_by_text(self, entities: List[Dict[str, Any]], text: str) -> Optional[Dict[str, Any]]:
        """Find entity by text content"""
        text_lower = text.lower().strip()
        
        for entity in entities:
            entity_text = entity.get('text', '').lower().strip()
            if entity_text == text_lower or text_lower in entity_text:
                return entity
        
        return None
    
    def process_contract_file(self, file_path: str) -> KnowledgeGraph:
        """
        Process an e-contract from file
        
        Args:
            file_path: Path to the contract file
            
        Returns:
            Knowledge graph for the contract
        """
        try:
            # Validate file
            if not FileHandler.validate_file_path(file_path, Config.SUPPORTED_CONTRACT_FORMATS):
                raise ValueError(f"Unsupported file format: {file_path}")
            
            # Read contract text
            contract_text = FileHandler.read_text_file(file_path)
            if not contract_text:
                raise ValueError(f"Could not read contract file: {file_path}")
            
            # Extract contract ID from filename
            contract_id = os.path.splitext(os.path.basename(file_path))[0]
            
            # Process the contract
            knowledge_graph = self.process_contract(contract_text, contract_id)
            
            # Update metadata with file information
            knowledge_graph.metadata['source_file'] = file_path
            knowledge_graph.metadata['file_info'] = FileHandler.get_file_info(file_path)
            
            return knowledge_graph
            
        except Exception as e:
            print(f"Error processing contract file {file_path}: {e}")
            raise
    
    def get_contract_summary(self, contract_id: str) -> Dict[str, Any]:
        """Get summary of processed contract"""
        if contract_id not in self.processed_contracts:
            return {}
        
        contract_data = self.processed_contracts[contract_id]
        kg = contract_data['knowledge_graph']
        
        return {
            'contract_id': contract_id,
            'processing_time': contract_data['processing_time'],
            'statistics': kg.get_statistics(),
            'preprocessing_stats': contract_data['preprocessed_data'],
            'entity_categories': self._get_entity_category_distribution(contract_data['entities']),
            'relationship_types': self._get_relationship_type_distribution(contract_data['relationships']),
            'key_entities': self._get_key_entities(contract_data['entities']),
            'contract_sections': contract_data['preprocessed_data'].get('sections', {})
        }
    
    def _get_entity_category_distribution(self, entities: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get distribution of entity categories"""
        categories = {}
        for entity in entities:
            category = self._categorize_entity(entity)
            categories[category] = categories.get(category, 0) + 1
        return categories
    
    def _get_relationship_type_distribution(self, relationships: List[Dict[str, Any]]) -> Dict[str, int]:
        """Get distribution of relationship types"""
        types = {}
        for rel in relationships:
            rel_type = rel.get('relation', 'unknown')
            types[rel_type] = types.get(rel_type, 0) + 1
        return types
    
    def _get_key_entities(self, entities: List[Dict[str, Any]], top_n: int = 10) -> List[Dict[str, Any]]:
        """Get the most important entities based on confidence and type"""
        
        # Score entities based on importance
        scored_entities = []
        for entity in entities:
            score = entity.get('confidence', 0.5)
            
            # Boost score for important entity types
            entity_type = entity.get('label', '').upper()
            if entity_type in ['PERSON', 'ORG', 'PARTIES', 'CONTRACT_PARTY']:
                score += 0.3
            elif entity_type in ['MONEY', 'MONETARY_AMOUNT', 'DATE']:
                score += 0.2
            elif entity_type in ['OBLIGATIONS', 'LEGAL_TERMS']:
                score += 0.15
            
            scored_entities.append({
                'entity': entity,
                'importance_score': score
            })
        
        # Sort by importance and return top entities
        scored_entities.sort(key=lambda x: x['importance_score'], reverse=True)
        
        return [item['entity'] for item in scored_entities[:top_n]]
    
    def export_contract_analysis(self, contract_id: str, output_dir: str) -> Dict[str, str]:
        """
        Export comprehensive contract analysis to files
        
        Args:
            contract_id: ID of the processed contract
            output_dir: Directory to save output files
            
        Returns:
            Dictionary of output file paths
        """
        if contract_id not in self.processed_contracts:
            return {}
        
        os.makedirs(output_dir, exist_ok=True)
        output_paths = {}
        
        contract_data = self.processed_contracts[contract_id]
        kg = contract_data['knowledge_graph']
        
        try:
            # Export knowledge graph
            kg_base_path = os.path.join(output_dir, f"{contract_id}_knowledge_graph")
            kg_export_results = kg.export_to_formats(kg_base_path)
            output_paths.update({f"kg_{fmt}": f"{kg_base_path}.{fmt}" 
                               for fmt, success in kg_export_results.items() if success})
            
            # Export visualization
            viz_path = os.path.join(output_dir, f"{contract_id}_visualization.png")
            if kg.visualize(viz_path):
                output_paths['visualization'] = viz_path
            
            # Export summary report
            summary = self.get_contract_summary(contract_id)
            summary_path = os.path.join(output_dir, f"{contract_id}_summary.json")
            if FileHandler.write_json_file(summary_path, summary):
                output_paths['summary'] = summary_path
            
            # Export processed text
            processed_text_path = os.path.join(output_dir, f"{contract_id}_processed_text.json")
            processed_data = {
                'original_text': contract_data['original_text'],
                'preprocessed_data': contract_data['preprocessed_data'],
                'entities': contract_data['entities'],
                'relationships': contract_data['relationships']
            }
            if FileHandler.write_json_file(processed_text_path, processed_data):
                output_paths['processed_text'] = processed_text_path
            
            return output_paths
            
        except Exception as e:
            print(f"Error exporting contract analysis for {contract_id}: {e}")
            return output_paths
    
    def compare_contracts(self, contract_id1: str, contract_id2: str) -> Dict[str, Any]:
        """Compare two processed e-contracts"""
        if (contract_id1 not in self.processed_contracts or 
            contract_id2 not in self.processed_contracts):
            return {}
        
        contract1_data = self.processed_contracts[contract_id1]
        contract2_data = self.processed_contracts[contract_id2]
        
        # Compare entities
        entities1 = {e['text'].lower(): e for e in contract1_data['entities']}
        entities2 = {e['text'].lower(): e for e in contract2_data['entities']}
        
        common_entities = set(entities1.keys()) & set(entities2.keys())
        unique_entities1 = set(entities1.keys()) - set(entities2.keys())
        unique_entities2 = set(entities2.keys()) - set(entities1.keys())
        
        # Compare relationships
        rels1 = {f"{r.get('source', '')}-{r.get('relation', '')}-{r.get('target', '')}" 
                for r in contract1_data['relationships']}
        rels2 = {f"{r.get('source', '')}-{r.get('relation', '')}-{r.get('target', '')}" 
                for r in contract2_data['relationships']}
        
        common_relationships = rels1 & rels2
        unique_relationships1 = rels1 - rels2
        unique_relationships2 = rels2 - rels1
        
        return {
            'contract_1': contract_id1,
            'contract_2': contract_id2,
            'entity_comparison': {
                'common_entities': list(common_entities),
                'unique_to_contract_1': list(unique_entities1),
                'unique_to_contract_2': list(unique_entities2),
                'similarity_ratio': len(common_entities) / max(len(entities1), len(entities2), 1)
            },
            'relationship_comparison': {
                'common_relationships': list(common_relationships),
                'unique_to_contract_1': list(unique_relationships1),
                'unique_to_contract_2': list(unique_relationships2),
                'similarity_ratio': len(common_relationships) / max(len(rels1), len(rels2), 1)
            }
        }