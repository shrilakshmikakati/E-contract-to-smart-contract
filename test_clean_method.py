"""
Clean version of semantic relation similarity method
"""

def _calculate_semantic_relation_similarity(self, e_relation, s_relation):
    """Calculate semantic similarity for relationships"""
    e_context = (e_relation.get('relation', '') + ' ' + 
                str(e_relation.get('properties', {}))).lower()
    s_context = (s_relation.get('relation', '') + ' ' + 
                str(s_relation.get('properties', {}))).lower()
    
    relation_semantic_groups = {
        'control': ['obligation', 'condition', 'requires', 'controls', 'validates', 'modifies'],
        'data': ['contains', 'has_member', 'stores', 'references', 'includes'],
        'temporal': ['temporal', 'deadline', 'triggers', 'depends_on', 'schedule'],
        'financial': ['payment', 'financial', 'transfers', 'updates', 'monetary'],
        'structural': ['has_parameter', 'inherits_from', 'calls', 'part_of']
    }
    
    e_groups = set()
    s_groups = set()
    
    for group_name, keywords in relation_semantic_groups.items():
        if any(keyword in e_context for keyword in keywords):
            e_groups.add(group_name)
        if any(keyword in s_context for keyword in keywords):
            s_groups.add(group_name)
    
    if not e_groups and not s_groups:
        return 0.0
    
    intersection = len(e_groups & s_groups)
    union = len(e_groups | s_groups)
    
    return intersection / union if union > 0 else 0.0

print("Clean method created successfully")