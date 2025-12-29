#!/usr/bin/env python3
"""
Test script to verify enhanced relationship preservation and alignment metrics
"""

from production_smart_contract_generator import ProductionSmartContractGenerator
from src.core.econtract_processor import EContractProcessor  
from src.core.smartcontract_processor import SmartContractProcessor
from src.core.comparator import KnowledgeGraphComparator

def test_enhanced_metrics():
    print("🧪 TESTING ENHANCED RELATIONSHIP PRESERVATION & ALIGNMENT METRICS")
    print("=" * 70)
    
    # Sample contract for testing
    contract_text = """
    This rental agreement is between Landlord ABC of London, United Kingdom and Tenant XYZ of Singapore. 
    The tenant agrees to pay monthly rent of 2000 GBP on the first day of each month. 
    The landlord is responsible for maintaining the property in good condition.
    The tenant must pay a security deposit of 2000 GBP upon signing this agreement.
    Either party may terminate this agreement with 30 days notice.
    """
    
    print("📄 Processing E-Contract...")
    processor = EContractProcessor()
    e_kg = processor.process_contract(contract_text, 'test_contract')
    print(f"   E-Contract: {len(e_kg.entities)} entities, {len(e_kg.relationships)} relationships")
    
    print("🔧 Generating Smart Contract...")
    generator = ProductionSmartContractGenerator()
    smart_contract, metrics = generator.generate_contract(contract_text, e_kg.entities, e_kg.relationships)
    
    print("📊 Processing Smart Contract...")
    s_processor = SmartContractProcessor()
    s_kg = s_processor.process_contract(smart_contract, 'generated_contract')
    print(f"   Smart Contract: {len(s_kg.entities)} entities, {len(s_kg.relationships)} relationships")
    
    print("🔍 Running Enhanced Comparison...")
    comparator = KnowledgeGraphComparator()
    results = comparator.compare_knowledge_graphs(e_kg, s_kg)
    
    print("\n🎯 ENHANCED METRICS RESULTS:")
    print("=" * 50)
    
    # Access metrics from the summary section
    summary = results.get('summary', {})
    bidirectional_metrics = results.get('bidirectional_metrics', {})
    
    entity_alignment = summary.get('entity_alignment_score', 0)
    relationship_alignment = summary.get('relationship_alignment_score', 0)
    overall_similarity = summary.get('overall_similarity_score', 0)
    entity_preservation = summary.get('entity_preservation', 0)
    relationship_preservation = summary.get('relationship_preservation', 0)
    bidirectional_similarity = summary.get('bidirectional_similarity', 0)
    mutual_entity_coverage = summary.get('mutual_entity_coverage', 0)
    mutual_relationship_coverage = summary.get('mutual_relationship_coverage', 0)
    
    print(f"Entity Alignment Score: {entity_alignment*100:.1f}%")
    print(f"Relationship Alignment Score: {relationship_alignment*100:.1f}%")  
    print(f"Overall Similarity Score: {overall_similarity*100:.1f}%")
    print(f"Entity Preservation: {entity_preservation*100:.1f}%")
    print(f"Relationship Preservation: {relationship_preservation*100:.1f}%")
    print(f"Bidirectional Similarity: {bidirectional_similarity*100:.1f}%")
    print(f"Mutual Entity Coverage: {mutual_entity_coverage*100:.1f}%")
    print(f"Mutual Relationship Coverage: {mutual_relationship_coverage*100:.1f}%")
    
    print("\n📈 IMPROVEMENT ANALYSIS:")
    print("=" * 40)
    if relationship_preservation > 0.60:
        print("✅ EXCELLENT: Relationship Preservation > 60%")
    elif relationship_preservation > 0.45:
        print("✅ GOOD: Relationship Preservation > 45%") 
    elif relationship_preservation > 0.30:
        print("⚠️ FAIR: Relationship Preservation > 30%")
    else:
        print("❌ POOR: Relationship Preservation < 30%")
        
    if entity_alignment > 0.75:
        print("✅ EXCELLENT: Entity Alignment > 75%")
    elif entity_alignment > 0.65:
        print("✅ GOOD: Entity Alignment > 65%")
    else:
        print("⚠️ NEEDS IMPROVEMENT: Entity Alignment < 65%")
        
    if relationship_alignment > 0.85:
        print("✅ EXCELLENT: Relationship Alignment > 85%")
    elif relationship_alignment > 0.75:
        print("✅ GOOD: Relationship Alignment > 75%")
    else:
        print("⚠️ NEEDS IMPROVEMENT: Relationship Alignment < 75%")
    
    print(f"\n📋 COMPARISON SUMMARY:")
    print(f"   Total Entity Matches: {results.get('entity_matches_e_to_s', 0)} + {results.get('entity_matches_s_to_e', 0)}")
    print(f"   Total Relationship Matches: {results.get('relation_matches_e_to_s', 0)} + {results.get('relation_matches_s_to_e', 0)}")
    
    return results

if __name__ == "__main__":
    test_enhanced_metrics()