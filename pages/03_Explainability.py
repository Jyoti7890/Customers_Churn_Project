import pandas as pd
import plotly.express as px
import streamlit as st

from utils.data_loader import load_model
from utils.ui_components import load_css

try:
    from utils.ui_components import style_plotly_figure
except ImportError:
    def style_plotly_figure(fig, title=None):
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(15, 23, 15, 0.35)",
            paper_bgcolor="rgba(0, 0, 0, 0)",
            font=dict(color="#F8FAFC", size=14, family="Poppins"),
            title=(
                dict(
                    text=title,
                    font=dict(size=18, color="#F8FAFC", family="Poppins"),
                    x=0.02,
                    xanchor="left",
                )
                if title
                else None
            ),
            legend=dict(
                font=dict(color="#F8FAFC", size=13),
                bgcolor="rgba(15, 23, 15, 0.7)",
                bordercolor="rgba(148, 163, 184, 0.45)",
                borderwidth=1,
            ),
            margin=dict(l=20, r=20, t=60, b=40),
        )
        fig.update_xaxes(
            title_font=dict(color="#F8FAFC", size=15),
            tickfont=dict(color="#F8FAFC", size=13),
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.25)",
            zeroline=False,
        )
        fig.update_yaxes(
            title_font=dict(color="#F8FAFC", size=15),
            tickfont=dict(color="#F8FAFC", size=13),
            showgrid=True,
            gridcolor="rgba(148, 163, 184, 0.25)",
            zeroline=False,
        )
        return fig

PURPLE = "#8b5cf6"
TEXT = "#F8FAFC"
ACCENT = "#10b981"


def show_explainability():
    load_css()

    st.markdown(
        """
        <div class="glass-card">
            <h1 style='text-align:center;'>Portfolio Intelligence Drivers</h1>
            <p style='text-align:center; color:#e2e8f0;'>
            Explain churn risk with clear, actionable language
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    st.markdown('<div class="hr-glow"></div>', unsafe_allow_html=True)

    model = load_model()
    tab_global, tab_local = st.tabs(["Portfolio-Wide Factors", "Account-Specific Explanation"])

    with tab_global:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.subheader("Portfolio-Wide Risk Drivers")
        st.markdown("These factors generally influence churn across the customer base.")

        if model is None:
            st.warning("Global insights are unavailable because the model could not be loaded.")
        else:
            try:
                xg_model = model.named_steps["model"]
                importances = xg_model.feature_importances_

                feature_names = [
                    "Credit Score",
                    "Geography",
                    "Customer Segment",
                    "Age",
                    "Tenure",
                    "Account Balance",
                    "Usage Level",
                    "Credit Card",
                    "Engagement",
                    "Estimated Income",
                ]

                min_len = min(len(feature_names), len(importances))
                imp_df = pd.DataFrame(
                    {
                        "Factor": feature_names[:min_len],
                        "Weight": importances[:min_len],
                    }
                ).sort_values("Weight", ascending=False).head(8)

                fig = px.bar(
                    imp_df,
                    x="Weight",
                    y="Factor",
                    orientation="h",
                    text="Weight",
                    color_discrete_sequence=[PURPLE],
                    labels={"Weight": "Relative Importance", "Factor": "Feature"},
                )
                fig.update_traces(
                    texttemplate="%{text:.3f}",
                    textposition="outside",
                    textfont=dict(color=TEXT, size=13),
                    marker_line=dict(color="#0b1a12", width=1),
                )

                style_plotly_figure(fig, title="Top Features Affecting Churn")
                fig.update_layout(yaxis={"categoryorder": "total ascending"}, showlegend=False)
                fig.update_xaxes(title_text="Relative Importance")
                fig.update_yaxes(title_text="Feature")

                st.plotly_chart(fig, use_container_width=True)
            except Exception as e:
                st.error(f"Unable to render global explainability chart: {e}")

        st.markdown("</div>", unsafe_allow_html=True)

    with tab_local:
        if "last_prediction" not in st.session_state:
            st.markdown('<div class="glass-card">', unsafe_allow_html=True)
            st.warning("Run a prediction first to view account-specific explanation.")
            st.markdown("</div>", unsafe_allow_html=True)
            return

        pred_data = st.session_state["last_prediction"]
        input_df = pred_data["input"]
        status = pred_data["status"]

        st.markdown(
            f"""
            <div class="glass-card">
                <p style="color:{ACCENT}; font-size:13px; margin:0;">PREDICTION RESULT</p>
                <h3 style="color:{TEXT}; margin:0;">Customer Risk Level: {status}</h3>
            </div>
            """,
            unsafe_allow_html=True,
        )

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 1) Why this customer is at risk")
        st.markdown("This customer is considered at risk mainly because:")

        reasons = []
        if input_df["active_member"].iloc[0] == 0:
            reasons.append("The customer is not actively using core bank services.")
        if input_df["credit_score"].iloc[0] < 600:
            reasons.append("The credit score is lower than the portfolio average.")
        if input_df["balance"].iloc[0] < 10000:
            reasons.append("The account balance is relatively low.")
        if input_df["age"].iloc[0] > 50:
            reasons.append("This age segment historically shows higher churn behavior.")

        if reasons:
            for reason in reasons:
                st.markdown(f"- {reason}")
        else:
            st.markdown("- This profile looks stable with no major warning signals.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 2) What action the bank should take")
        st.markdown("Recommended steps:")
        st.markdown("- Assign a relationship manager for direct outreach.")
        if input_df["active_member"].iloc[0] == 0:
            st.markdown("- Encourage usage of key banking products.")
        if input_df["balance"].iloc[0] < 20000:
            st.markdown("- Offer a loyalty incentive or account upgrade path.")
        st.markdown("- Review whether current products match customer needs.")
        st.markdown("</div>", unsafe_allow_html=True)

        st.markdown('<div class="glass-card">', unsafe_allow_html=True)
        st.markdown("### 3) What could improve the situation")
        st.markdown("- Becoming more active can reduce future churn probability.")
        st.markdown("- Improving credit profile can support long-term retention.")
        st.markdown("- Higher balances and deeper product use typically improve loyalty.")
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="hr-glow"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <center style='color:#cbd5e1;'>
        Smart Banking Intelligence - Explainability Module
        </center>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    show_explainability()

