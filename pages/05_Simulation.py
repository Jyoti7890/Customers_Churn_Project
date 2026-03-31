import streamlit as st
from utils.ui_components import load_css


def show_simulation():
    # =============================
    # Page Setup
    # =============================
    load_css()

    st.markdown("""
        <div class="glass-card">
            <h1 style='text-align:center;'> Risk Reduction Simulation</h1>
            <p style='text-align:center; color:#a78bfa;'>
            See how customer behaviour improvements can reduce churn risk
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="hr-glow"></div>', unsafe_allow_html=True)

    if "last_prediction" not in st.session_state:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.warning(
            "Please run a churn prediction first. "
            "This page explains how the risk could change with better customer behaviour."
        )
        st.markdown('</div>', unsafe_allow_html=True)
        return

    pred_data = st.session_state["last_prediction"]
    input_df = pred_data["input"]
    base_risk = pred_data["probability"] * 100

    # =============================
    # Current Risk
    # =============================
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Current Customer Risk")
    st.markdown(
        f"Based on current details, the customer has a **{base_risk:.1f}% chance** of leaving the bank."
    )
    st.markdown('</div>', unsafe_allow_html=True)

    # =============================
    # Simulation Explanation
    # =============================
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("What Could Reduce This Risk?")
    st.markdown(
        "Below scenarios explain how customer behaviour improvements "
        "can help reduce churn risk. These are **examples only** — no data is changed."
    )

    improvements = []

    if input_df["active_member"].iloc[0] == 0:
        improvements.append(
            ("Customer becomes active",
             "Regular usage of bank services usually lowers exit risk.")
        )

    if input_df["credit_score"].iloc[0] < 700:
        improvements.append(
            ("Credit score improves",
             "Better financial health often leads to longer relationships.")
        )

    if input_df["balance"].iloc[0] < 50000:
        improvements.append(
            ("Account balance increases",
             "Customers with higher balances tend to stay longer.")
        )

    if input_df["products_number"].iloc[0] <= 1:
        improvements.append(
            ("Customer uses more bank products",
             "Using multiple services increases loyalty.")
        )

    if improvements:
        for title, desc in improvements:
            st.markdown(f"""
            <div style="margin-bottom:12px;">
                <strong>• {title}</strong><br>
                <span style="color:#94a3b8;">{desc}</span>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.markdown(
            "This customer already shows strong engagement. "
            "Maintaining current behaviour should keep risk low."
        )

    st.markdown('</div>', unsafe_allow_html=True)

    # =============================
    # Key Message
    # =============================
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.subheader("Key Takeaway for Managers")
    st.markdown("""
    - Small improvements in customer engagement can significantly reduce churn risk  
    - Early action is more effective than late recovery  
    - Focus on usage, balance growth, and relationship quality  
    """)
    st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="hr-glow"></div>', unsafe_allow_html=True)
    st.markdown("""
        <center style='color:#94a3b8;'>
        Smart Banking Intelligence • Simulation View
        </center>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    show_simulation()
