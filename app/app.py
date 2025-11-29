import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import networkx as nx

from readiness_engine.readiness_model import compute_readiness_for_batch
from knowledge_graph.build_graph import build_governance_graph
from playbooks.decision_playbooks import run_playbook

st.set_page_config(page_title="Decision-Aware Data Platform", layout="wide")

st.title("🔎 Decision-Aware Data Platform (Financial Services Demonstration)")
st.write("This demo application evaluates data readiness for key financial decision contexts and executes automated playbooks.")


# ---------------------------
# Sidebar
# ---------------------------
st.sidebar.header("Configuration")

context = st.sidebar.selectbox(
    "Select Decision Context:",
    ["FraudReview", "CreditDecision", "AMLReport"]
)

uploaded_file = st.sidebar.file_uploader(
    "Upload Data File (CSV)",
    type=["csv"]
)


# ---------------------------
# Data Loading
# ---------------------------
if uploaded_file:
    df = pd.read_csv(uploaded_file)
    st.subheader("📊 Uploaded Data")
    st.dataframe(df)

    # ---------------------------
    # Run Readiness Engine
    # ---------------------------
    st.subheader("⚙ Readiness Assessment")

    result = compute_readiness_for_batch(df, context)

    st.metric("Readiness Score", result.readiness_score)
    st.write(f"Status: **{result.status}**")

    if result.issues:
        st.warning("Issues detected:")
        for issue in result.issues:
            st.write(f"- {issue}")
    else:
        st.success("No issues detected.")

    # ---------------------------
    # Run Playbook
    # ---------------------------
    st.subheader("📘 Executing Playbook")

    playbook_output = run_playbook(context, df)
    st.write(playbook_output["status"])

    with st.expander("Playbook Logs"):
        for line in playbook_output["logs"]:
            st.text(line)

    # ---------------------------
    # Governance Graph
    # ---------------------------
    st.subheader("🕸 Governance Knowledge Graph")

    G = build_governance_graph()

    plt.figure(figsize=(8, 6))
    pos = nx.spring_layout(G, seed=42)

    nx.draw_networkx_nodes(G, pos, node_color="lightblue")
    nx.draw_networkx_edges(G, pos, arrows=True)
    nx.draw_networkx_labels(G, pos, font_size=8)

    st.pyplot(plt.gcf())
else:
    st.info("Upload a CSV file from the sidebar to begin.")


st.write("---")
st.caption("Research prototype for INFS-890-Fall-2025-Conference — Jephte Noutsa")
