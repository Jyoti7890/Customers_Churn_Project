import streamlit as st
from utils.ui_components import load_css


def show_retention():
    # =============================
    # Page Settings & CSS
    # =============================
    load_css()

    st.markdown("""
        <div class="glass-card">
            <h1 style='text-align:center;'>🎯 Customer Retention Actions</h1>
            <p style='text-align:center; color:#a78bfa;'>
            Clear actions to reduce customer exit risk
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="hr-glow"></div>', unsafe_allow_html=True)

    # Colors
    RED = "#ef4444"
    GREEN = "#22c55e"
    ORANGE = "#F59E0B"
    WHITE = "#e5e7eb"
    ACCENT = "#a78bfa"

    if "last_prediction" in st.session_state:
        pred_data = st.session_state["last_prediction"]
        status = pred_data["status"]

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Recommended Bank Actions")
        st.markdown(
            f"This customer is classified as **{status} Risk**. "
            "Based on this, the following actions are recommended."
        )
        st.markdown('</div>', unsafe_allow_html=True)

        # =============================
        # Action Logic
        # =============================
        if status == "High":
            tier = "HIGH PRIORITY"
            color = RED
            title = "Immediate Retention Required"
            context = "The customer shows strong signs of leaving the bank."
            actions = [
                "Call the customer within 24 hours",
                "Assign a relationship manager",
                "Offer a personalized retention benefit"
            ]

        elif status == "Medium":
            tier = "MEDIUM PRIORITY"
            color = ORANGE
            title = "Preventive Engagement Needed"
            context = "The customer shows early signs of disengagement."
            actions = [
                "Encourage use of main bank services",
                "Offer a loyalty or usage-based reward",
                "Schedule a follow-up check-in"
            ]

        else:
            tier = "LOW PRIORITY"
            color = GREEN
            title = "Relationship Growth Opportunity"
            context = "The customer relationship is currently stable."
            actions = [
                "Introduce additional useful products",
                "Maintain regular engagement",
                "Offer referral or loyalty programs"
            ]

        # =============================
        # Display Card
        # =============================
        st.markdown(f"""
        <div class="glass-card" style="border-left: 6px solid {color};">
            <span style="color:{color}; font-weight:700; font-size:12px;">
                {tier}
            </span>
            <h3 style="color:{WHITE}; margin-top:6px;">
                {title}
            </h3>
            <p style="color:{ACCENT}; font-size:14px;">
                {context}
            </p>
            <div style="color:{WHITE}; font-size:14px;">
                <strong>Recommended Actions:</strong>
                <ul>
                    {''.join([f"<li>{a}</li>" for a in actions])}
                </ul>
            </div>
        </div>
        """, unsafe_allow_html=True)

    else:
        # =============================
        # No Prediction Case
        # =============================
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.warning(
            "Please run a churn prediction first to see customer-specific actions."
        )
        st.markdown('</div>', unsafe_allow_html=True)

        st.markdown('<div class="hr-glow"></div>', unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("General Retention Best Practices")

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("""
            **Customer Monitoring**
            - Track drop in account usage
            - Watch for sudden balance changes
            """)

        with col2:
            st.markdown("""
            **Customer Engagement**
            - Regular relationship calls
            - Simple loyalty rewards
            """)

        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown('<div class="hr-glow"></div>', unsafe_allow_html=True)
    st.markdown("""
        <center style='color:#94a3b8;'>
        Smart Banking Intelligence • Retention Strategy
        </center>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    show_retention()
