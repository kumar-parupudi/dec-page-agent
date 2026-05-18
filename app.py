import streamlit as st
import json
from dotenv import load_dotenv

load_dotenv()

from main import process_dec_page


def plain(text: str) -> str:
    """Strip backtick code spans so markdown boxes don't switch to monospace font."""
    import re
    return re.sub(r"`([^`]+)`", r"\1", text)

st.set_page_config(
    page_title="Dec Page Intelligence Agent",
    layout="wide",
    page_icon="📋"
)

st.title("Dec Page Intelligence Agent")
st.caption("Customer's current Dec Page in. Side-by-side comparison and proposed quote out.")

# Sidebar: load sample or paste
st.sidebar.header("Input")
sample_choice = st.sidebar.radio(
    "Choose a sample or paste custom:",
    ["Sample 1 (Clean)", "Sample 2 (Ambiguous)", "Custom"]
)

if sample_choice == "Sample 1 (Clean)":
    with open("sample_data/dec_page_clean.txt") as f:
        default_text = f.read()
elif sample_choice == "Sample 2 (Ambiguous)":
    with open("sample_data/dec_page_ambiguous.txt") as f:
        default_text = f.read()
else:
    default_text = ""

document_text = st.text_area(
    "Dec page text:",
    value=default_text,
    height=300
)

if st.button("Process Dec Page", type="primary"):
    if not document_text.strip():
        st.error("Please paste a dec page first.")
        st.stop()

    with st.spinner("Running 5-stage pipeline..."):
        result = process_dec_page(document_text)

    # Stage 1
    st.success(f"✓ Classified as {result['classification']['policy_form']} "
               f"(confidence: {result['classification']['confidence']:.0%})")

    # Stage 2 summary
    with st.expander("Stage 2 · Extracted Data", expanded=False):
        st.json(result['extracted_dec_page'])

    # Stage 3
    with st.expander("Stage 3 · Risk Analysis", expanded=True):
        risk = result['risk_profile']
        if risk.get('underinsurance_flags'):
            st.subheader("Underinsurance Flags")
            for flag in risk['underinsurance_flags']:
                st.warning(f"**{flag['type']}** ({flag['severity']}): {flag['rationale']}")
        if risk.get('coverage_gaps'):
            st.subheader("Coverage Gaps")
            for gap in risk['coverage_gaps']:
                st.info(f"**{gap['missing_coverage']}**: {gap['rationale']}")
        if risk.get('property_risk_factors'):
            st.subheader("Property Risk Factors (from Home Factors)")
            for factor in risk['property_risk_factors']:
                st.write(f"• **{factor['factor']}** — {factor['underwriting_impact']}")

    # Stage 4 + 5: The comparison
    st.subheader("Current vs Proposed Coverage")
    comparison = result['comparison']

    col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
    with col1: st.markdown("**Coverage Element**")
    with col2: st.markdown("**Current**")
    with col3: st.markdown("**Proposed**")
    with col4: st.markdown("**Signal**")

    for row in comparison['comparison_rows']:
        col1, col2, col3, col4 = st.columns([3, 2, 2, 2])
        with col1: st.write(row['coverage_element'])
        with col2: st.write(row['current'])
        with col3: st.write(row['proposed'])
        with col4: st.write(row['signal'])

    # Premium
    st.subheader("Premium")
    pc = comparison['premium_comparison']
    col1, col2, col3 = st.columns(3)
    with col1: st.metric("Current Annual", pc['current_annual'])
    with col2: st.metric("Proposed Annual", pc['proposed_annual'], pc['difference'])
    with col3: st.metric("Monthly Difference", pc['monthly_difference'])

    # Agent talking script
    st.subheader("Agent Talking Script")
    st.info(plain(comparison['agent_talking_script']))

    st.subheader("Customer Summary")
    st.success(plain(comparison['customer_summary']))
