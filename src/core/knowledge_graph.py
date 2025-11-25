
import networkx as nx
import matplotlib.pyplot as plt
from typing import Dict, Any, List, Tuple, Optional
import json
import numpy as np
from collections import defaultdict, Counter
import re

class KnowledgeGraph:
    
    def __init__(self, graph_type: str = "contract"):
        self.graph = nx.DiGraph()
        self.graph_type = graph_type
        self.entities = {}
        self.relationships = {}
        self.metadata = {
            'creation_time': None,
            'source_file': None,
            'total_entities': 0,
            'total_relationships': 0,
            'entity_types': {},
            'relationship_types': {}
        }
    
    def add_entity(self, entity_id: str, entity_data: Dict[str, Any]) -> bool:
        try:
            if 'text' not in entity_data or 'type' not in entity_data:
                print(f"Invalid entity data for {entity_id}: missing 'text' or 'type'")
                return False
            
            self.graph.add_node(entity_id, **entity_data)
            
            self.entities[entity_id] = entity_data
            
            entity_type = entity_data.get('type', 'UNKNOWN')
            self.metadata['entity_types'][entity_type] = self.metadata['entity_types'].get(entity_type, 0) + 1
            self.metadata['total_entities'] = len(self.entities)
            
            return True
            
        except Exception as e:
            print(f"Error adding entity {entity_id}: {e}")
            return False
    
    def add_relationship(self, relationship_id: str, source_id: str, target_id: str, 
                        relationship_data: Dict[str, Any]) -> bool:
        try:
            if source_id not in self.entities or target_id not in self.entities:
                print(f"Cannot add relationship {relationship_id}: missing entities")
                return False
            
            self.graph.add_edge(source_id, target_id, 
                              relationship_id=relationship_id, **relationship_data)
            
            self.relationships[relationship_id] = {
                'source': source_id,
                'target': target_id,
                **relationship_data
            }
            
            relation_type = relationship_data.get('relation', 'UNKNOWN')
            self.metadata['relationship_types'][relation_type] = self.metadata['relationship_types'].get(relation_type, 0) + 1
            self.metadata['total_relationships'] = len(self.relationships)
            
            return True
            
        except Exception as e:
            print(f"Error adding relationship {relationship_id}: {e}")
            return False
    
    def get_entity(self, entity_id: str) -> Optional[Dict[str, Any]]:
        return self.entities.get(entity_id)
    
    def get_relationship(self, relationship_id: str) -> Optional[Dict[str, Any]]:
        return self.relationships.get(relationship_id)
    
    def get_entities_by_type(self, entity_type: str) -> List[Dict[str, Any]]:
        return [
            {'id': eid, **data} 
            for eid, data in self.entities.items() 
            if data.get('type') == entity_type
        ]
    
    def get_relationships_by_type(self, relation_type: str) -> List[Dict[str, Any]]:
        return [
            {'id': rid, **data} 
            for rid, data in self.relationships.items() 
            if data.get('relation') == relation_type
        ]
    
    def get_neighbors(self, entity_id: str, direction: str = 'both') -> List[str]:
        if entity_id not in self.graph:
            return []
        
        if direction == 'in':
            return list(self.graph.predecessors(entity_id))
        elif direction == 'out':
            return list(self.graph.successors(entity_id))
        else:  # both
            return list(set(self.graph.predecessors(entity_id) + 
                          self.graph.successors(entity_id)))
    
    def find_shortest_path(self, source_id: str, target_id: str) -> Optional[List[str]]:
        try:
            return nx.shortest_path(self.graph.to_undirected(), source_id, target_id)
        except (nx.NetworkXNoPath, nx.NodeNotFound):
            return None
    
    def calculate_centrality_measures(self) -> Dict[str, Dict[str, float]]:
        centrality_measures = {}
        
        if len(self.graph) == 0:
            return centrality_measures
        
        try:
            centrality_measures['degree'] = nx.degree_centrality(self.graph)
            
            centrality_measures['betweenness'] = nx.betweenness_centrality(self.graph)
            
            if nx.is_connected(self.graph.to_undirected()):
                centrality_measures['closeness'] = nx.closeness_centrality(self.graph)
            else:
                centrality_measures['closeness'] = {}
                for component in nx.connected_components(self.graph.to_undirected()):
                    subgraph = self.graph.subgraph(component)
                    closeness = nx.closeness_centrality(subgraph)
                    centrality_measures['closeness'].update(closeness)
            
            centrality_measures['pagerank'] = nx.pagerank(self.graph)
            
        except Exception as e:
            print(f"Error calculating centrality measures: {e}")
        
        return centrality_measures
    
    def detect_communities(self) -> List[List[str]]:
        try:
            undirected_graph = self.graph.to_undirected()
            communities = nx.community.greedy_modularity_communities(undirected_graph)
            return [list(community) for community in communities]
        except Exception as e:
            print(f"Error detecting communities: {e}")
            return []
    
    def get_subgraph(self, entity_ids: List[str]) -> 'KnowledgeGraph':
        subgraph_kg = KnowledgeGraph(self.graph_type + "_subgraph")
        
        for entity_id in entity_ids:
            if entity_id in self.entities:
                subgraph_kg.add_entity(entity_id, self.entities[entity_id])
        
        for rel_id, rel_data in self.relationships.items():
            source = rel_data['source']
            target = rel_data['target']
            if source in entity_ids and target in entity_ids:
                subgraph_kg.add_relationship(rel_id, source, target, {
                    k: v for k, v in rel_data.items() 
                    if k not in ['source', 'target']
                })
        
        return subgraph_kg
    
    def visualize(self, output_path: str = None, layout_algorithm: str = 'spring',
                 node_size_attr: str = None, edge_width_attr: str = None,
                 show_labels: bool = True, figsize: Tuple[int, int] = (12, 8)) -> bool:
        try:
            if len(self.graph) == 0:
                print("Cannot visualize empty graph")
                return False
            
            plt.figure(figsize=figsize)
            
            if layout_algorithm == 'spring':
                pos = nx.spring_layout(self.graph, k=1, iterations=50)
            elif layout_algorithm == 'circular':
                pos = nx.circular_layout(self.graph)
            elif layout_algorithm == 'random':
                pos = nx.random_layout(self.graph)
            elif layout_algorithm == 'shell':
                pos = nx.shell_layout(self.graph)
            else:
                pos = nx.spring_layout(self.graph)
            
            if node_size_attr and node_size_attr in self.graph.nodes[list(self.graph.nodes)[0]]:
                node_sizes = [
                    self.graph.nodes[node].get(node_size_attr, 1) * 100 
                    for node in self.graph.nodes
                ]
            else:
                node_sizes = [300 for _ in self.graph.nodes]
            
            if edge_width_attr:
                edge_widths = [
                    self.graph.edges[edge].get(edge_width_attr, 1) 
                    for edge in self.graph.edges
                ]
            else:
                edge_widths = [1 for _ in self.graph.edges]
            
            entity_types = list(set(data.get('type', 'UNKNOWN') for data in self.entities.values()))
            color_map = plt.cm.tab10(np.linspace(0, 1, len(entity_types)))
            type_to_color = dict(zip(entity_types, color_map))
            
            node_colors = [
                type_to_color.get(self.graph.nodes[node].get('type', 'UNKNOWN'), 'gray')
                for node in self.graph.nodes
            ]
            
            nx.draw_networkx_nodes(self.graph, pos, node_size=node_sizes, 
                                 node_color=node_colors, alpha=0.7)
            nx.draw_networkx_edges(self.graph, pos, width=edge_widths, 
                                 alpha=0.5, edge_color='gray')
            
            if show_labels:
                labels = {
                    node: self.graph.nodes[node].get('text', node)[:15] + '...' 
                    if len(self.graph.nodes[node].get('text', node)) > 15 
                    else self.graph.nodes[node].get('text', node)
                    for node in self.graph.nodes
                }
                nx.draw_networkx_labels(self.graph, pos, labels, font_size=8)
            
            plt.title(f"{self.graph_type.title()} Knowledge Graph", fontsize=16)
            
            legend_elements = [
                plt.scatter([], [], c=type_to_color[entity_type], 
                           label=entity_type, s=100, alpha=0.7)
                for entity_type in entity_types
            ]
            plt.legend(handles=legend_elements, loc='upper right', bbox_to_anchor=(1.15, 1))
            
            plt.axis('off')
            plt.tight_layout()
            
            if output_path:
                plt.savefig(output_path, dpi=300, bbox_inches='tight')
                print(f"Graph visualization saved to {output_path}")
            else:
                plt.show()
            
            plt.close()
            return True
            
        except Exception as e:
            print(f"Error visualizing graph: {e}")
            return False
    
    def export_to_formats(self, base_path: str) -> Dict[str, bool]:
        results = {}
        
        try:
            graphml_path = f"{base_path}.graphml"
            nx.write_graphml(self.graph, graphml_path)
            results['graphml'] = True
        except Exception as e:
            print(f"Error exporting to GraphML: {e}")
            results['graphml'] = False
        
        try:
            json_data = {
                'graph_type': self.graph_type,
                'entities': self.entities,
                'relationships': self.relationships,
                'metadata': self.metadata
            }
            json_path = f"{base_path}.json"
            with open(json_path, 'w', encoding='utf-8') as f:
                json.dump(json_data, f, indent=2, ensure_ascii=False)
            results['json'] = True
        except Exception as e:
            print(f"Error exporting to JSON: {e}")
            results['json'] = False
        
        try:
            gml_path = f"{base_path}.gml"
            nx.write_gml(self.graph, gml_path)
            results['gml'] = True
        except Exception as e:
            print(f"Error exporting to GML: {e}")
            results['gml'] = False
        
        try:
            edgelist_path = f"{base_path}_edges.csv"
            with open(edgelist_path, 'w', encoding='utf-8') as f:
                f.write("source,target,relation,confidence\n")
                for rel_id, rel_data in self.relationships.items():
                    f.write(f"{rel_data['source']},{rel_data['target']},{rel_data.get('relation', 'unknown')},{rel_data.get('confidence', 1.0)}\n")
            results['csv'] = True
        except Exception as e:
            print(f"Error exporting edge list: {e}")
            results['csv'] = False
        
        return results
    
    def import_from_json(self, json_path: str) -> bool:
        try:
            with open(json_path, 'r', encoding='utf-8') as f:
                data = json.load(f)
            
            self.graph.clear()
            self.entities.clear()
            self.relationships.clear()
            
            self.graph_type = data.get('graph_type', 'unknown')
            self.metadata = data.get('metadata', {})
            
            for entity_id, entity_data in data.get('entities', {}).items():
                self.add_entity(entity_id, entity_data)
            
            for rel_id, rel_data in data.get('relationships', {}).items():
                source = rel_data.pop('source')
                target = rel_data.pop('target')
                self.add_relationship(rel_id, source, target, rel_data)
            
            return True
            
        except Exception as e:
            print(f"Error importing from JSON: {e}")
            return False
    
    def get_statistics(self) -> Dict[str, Any]:
        stats = {
            'basic_metrics': {
                'total_entities': len(self.entities),
                'total_relationships': len(self.relationships),
                'graph_density': nx.density(self.graph),
                'is_connected': nx.is_connected(self.graph.to_undirected()) if len(self.graph) > 0 else False
            },
            'entity_types': dict(self.metadata.get('entity_types', {})),
            'relationship_types': dict(self.metadata.get('relationship_types', {})),
        }
        
        if len(self.graph) > 0:
            degrees = dict(self.graph.degree())
            if degrees:
                stats['degree_statistics'] = {
                    'average_degree': sum(degrees.values()) / len(degrees),
                    'max_degree': max(degrees.values()),
                    'min_degree': min(degrees.values())
                }
            
            components = list(nx.connected_components(self.graph.to_undirected()))
            stats['connectivity'] = {
                'number_of_components': len(components),
                'largest_component_size': max(len(comp) for comp in components) if components else 0
            }
        
        return stats
    
    def search_entities(self, query: str, search_fields: List[str] = None) -> List[Dict[str, Any]]:
        if search_fields is None:
            search_fields = ['text', 'type']
        
        query_lower = query.lower()
        results = []
        
        for entity_id, entity_data in self.entities.items():
            score = 0
            
            for field in search_fields:
                field_value = str(entity_data.get(field, '')).lower()
                if query_lower in field_value:
                    if query_lower == field_value:
                        score += 10
                    else:
                        score += 5
            
            if score > 0:
                results.append({
                    'entity_id': entity_id,
                    'entity_data': entity_data,
                    'relevance_score': score
                })
        
        results.sort(key=lambda x: x['relevance_score'], reverse=True)
        
        return results
    
    def calculate_density(self) -> float:
        if len(self.graph) == 0:
            return 0.0
        return nx.density(self.graph)