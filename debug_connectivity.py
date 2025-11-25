from src.core.econtract_processor import EContractProcessor

def debug_knowledge_graph_connectivity():
    """Debug why knowledge graph shows 'Connected: No'"""
    
    # Sample contract with clear relationships
    sample_contract = """
    CONSULTING AGREEMENT BETWEEN Company A AND Company B
    
    This Agreement is entered into on January 1, 2024, between Company A (consultant) and Company B (client).
    
    1. SERVICES: Company A shall provide consulting services to Company B
    2. PAYMENT: Company B shall pay $10,000 monthly to Company A  
    3. TERM: This agreement is valid for 12 months
    4. LOCATION: Services will be provided in New York
    5. OBLIGATIONS:
       - Company A must deliver monthly reports
       - Company B must provide necessary resources
       - Both parties must maintain confidentiality
    """
    
    print("=== KNOWLEDGE GRAPH CONNECTIVITY DEBUG ===")
    
    processor = EContractProcessor()
    knowledge_graph = processor.process_contract(sample_contract, "CONNECTIVITY_TEST")
    
    # Access entities and relationships correctly
    entities_count = len(knowledge_graph.entities) if hasattr(knowledge_graph, 'entities') else 0
    relationships_count = len(knowledge_graph.relationships) if hasattr(knowledge_graph, 'relationships') else 0
    
    print(f"Entities: {entities_count}")
    print(f"Relationships: {relationships_count}")
    
    # Debug: Check what type of data structures these are
    if hasattr(knowledge_graph, 'entities'):
        print(f"Entities type: {type(knowledge_graph.entities)}")
        if entities_count > 0:
            sample_entity = list(knowledge_graph.entities)[0] if hasattr(knowledge_graph.entities, '__iter__') else None
            if sample_entity:
                print(f"Sample entity type: {type(sample_entity)}")
                print(f"Sample entity: {sample_entity}")
    
    if hasattr(knowledge_graph, 'relationships'):
        print(f"Relationships type: {type(knowledge_graph.relationships)}")
        if relationships_count > 0:
            sample_rel = list(knowledge_graph.relationships)[0] if hasattr(knowledge_graph.relationships, '__iter__') else None
            if sample_rel:
                print(f"Sample relationship type: {type(sample_rel)}")
                print(f"Sample relationship: {sample_rel}")
    
    # Check graph connectivity
    stats = knowledge_graph.get_statistics()
    print(f"\nGraph Statistics:")
    print(f"  Total nodes: {len(knowledge_graph.graph.nodes())}")
    print(f"  Total edges: {len(knowledge_graph.graph.edges())}")
    print(f"  Is connected: {stats['basic_metrics']['is_connected']}")
    print(f"  Graph density: {stats['basic_metrics']['graph_density']:.3f}")
    
    # Show actual graph nodes and edges
    print(f"\nActual Graph Nodes ({len(knowledge_graph.graph.nodes())}):")
    for node in list(knowledge_graph.graph.nodes())[:10]:
        print(f"  - {node}")
    
    print(f"\nActual Graph Edges ({len(knowledge_graph.graph.edges())}):")
    for edge in list(knowledge_graph.graph.edges())[:10]:
        print(f"  - {edge[0]} -> {edge[1]}")
    
    # Check for isolated nodes
    isolated_nodes = list(knowledge_graph.graph.nodes())
    connected_nodes = set()
    for edge in knowledge_graph.graph.edges():
        connected_nodes.add(edge[0])
        connected_nodes.add(edge[1])
    
    isolated = [node for node in isolated_nodes if node not in connected_nodes]
    print(f"\nIsolated nodes: {len(isolated)}")
    for node in isolated[:5]:
        print(f"  - {node}")
    
    return knowledge_graph

if __name__ == "__main__":
    debug_knowledge_graph_connectivity()