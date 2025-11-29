import networkx as nx

def build_governance_graph():
    G = nx.DiGraph()

    # Decision nodes
    G.add_node("FraudReview")
    G.add_node("CreditDecision")
    G.add_node("AMLReport")

    # Attributes
    G.add_node("risk_score")
    G.add_node("quality_score")
    G.add_node("lineage_confidence")
    G.add_node("aml_flag")
    G.add_node("ofac_flag")

    # Edges
    G.add_edge("FraudReview", "risk_score")
    G.add_edge("FraudReview", "quality_score")

    G.add_edge("CreditDecision", "quality_score")
    G.add_edge("CreditDecision", "lineage_confidence")

    G.add_edge("AMLReport", "aml_flag")
    G.add_edge("AMLReport", "ofac_flag")
    G.add_edge("AMLReport", "lineage_confidence")

    return G
