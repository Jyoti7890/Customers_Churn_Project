import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import streamlit as st

from utils.data_loader import load_data
from utils.ui_components import load_css

try:
    from utils.ui_components import style_plotly_figure
except ImportError:
    def style_plotly_figure(fig, title=None):
        fig.update_layout(
            template="plotly_dark",
            plot_bgcolor="rgba(15, 23, 42, 0.35)",
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
                bgcolor="rgba(15, 23, 42, 0.7)",
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
GRAY = "#94a3b8"
RED = "#ef4444"
TEXT = "#F8FAFC"


def show_overview():
    load_css()

    st.markdown(
        """
        <div class="glass-card">
            <h1 style="text-align:center;">Bank Customer Churn Overview</h1>
            <p style="text-align:center; color:#e2e8f0; font-size:1.05rem;">
                Customer Stability, Risk Signals, and Retention Intelligence
            </p>
        </div>
        """,
        unsafe_allow_html=True,
    )

    df = load_data()
    if df is None:
        st.error("Data could not be loaded.")
        return

    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Customer Segmentation Filters")
    st.caption("Use these filters to analyze churn behavior for specific customer groups.")

    c1, c2, c3 = st.columns(3)
    with c1:
        countries = st.multiselect(
            "Region",
            options=sorted(df["country"].dropna().unique().tolist()),
            default=sorted(df["country"].dropna().unique().tolist()),
        )
    with c2:
        genders = st.multiselect(
            "Gender",
            options=sorted(df["gender"].dropna().unique().tolist()),
            default=sorted(df["gender"].dropna().unique().tolist()),
        )
    with c3:
        products = st.multiselect(
            "Products",
            options=sorted(df["products_number"].dropna().unique().tolist()),
            default=sorted(df["products_number"].dropna().unique().tolist()),
        )

    st.markdown("</div>", unsafe_allow_html=True)

    filtered_df = df[
        (df["country"].isin(countries))
        & (df["gender"].isin(genders))
        & (df["products_number"].isin(products))
    ].copy()

    if filtered_df.empty:
        st.warning("No records match the selected filters. Please adjust your selections.")
        return

    st.markdown('<div class="hr-glow"></div>', unsafe_allow_html=True)
    st.markdown("## Customer Churn Health Snapshot")
    st.caption("High-contrast KPIs for quick business review.")

    k1, k2, k3, k4, k5 = st.columns(5)
    with k1:
        st.metric("Total Customers", f"{len(filtered_df):,}")
    with k2:
        st.metric("Churn Rate", f"{filtered_df['churn'].mean() * 100:.1f}%")
    with k3:
        st.metric("Active Customers", f"{filtered_df['active_member'].mean() * 100:.1f}%")
    with k4:
        st.metric("Avg Credit Score", f"{filtered_df['credit_score'].mean():.0f}")
    with k5:
        st.metric("Avg Balance", f"${filtered_df['balance'].mean():,.0f}")

    st.markdown('<div class="hr-glow"></div>', unsafe_allow_html=True)
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        risk_country = (
            filtered_df.groupby("country", observed=False)["churn"].mean().reset_index()
        )
        risk_country["Risk %"] = risk_country["churn"] * 100

        fig_country = px.bar(
            risk_country,
            x="country",
            y="Risk %",
            text="Risk %",
            color_discrete_sequence=[PURPLE],
            labels={"country": "Country", "Risk %": "Churn Risk (%)"},
        )
        fig_country.update_traces(
            texttemplate="%{text:.1f}%",
            textposition="outside",
            textfont=dict(color=TEXT, size=13),
            cliponaxis=False,
        )
        style_plotly_figure(fig_country, title="Churn Risk by Region")
        fig_country.update_xaxes(showgrid=False, title_text="Country")
        fig_country.update_yaxes(title_text="Churn Risk (%)")

        st.plotly_chart(fig_country, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    with col_b:
        st.markdown('<div class="glass-card">', unsafe_allow_html=True)

        gender_mix = filtered_df["gender"].value_counts().reset_index()
        gender_mix.columns = ["Gender", "Count"]

        fig_gender = px.pie(
            gender_mix,
            values="Count",
            names="Gender",
            hole=0.65,
            color_discrete_sequence=[PURPLE, GRAY],
        )
        fig_gender.update_traces(
            textinfo="percent+label",
            textfont=dict(color=TEXT, size=13),
            marker=dict(line=dict(color="#0b1220", width=1.5)),
        )
        style_plotly_figure(fig_gender, title="Customer Gender Distribution")
        fig_gender.update_layout(
            legend=dict(
                orientation="h",
                y=-0.15,
                x=0.5,
                xanchor="center",
                font=dict(size=13, color=TEXT),
            )
        )

        st.plotly_chart(fig_gender, use_container_width=True)
        st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="hr-glow"></div>', unsafe_allow_html=True)
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)

    age_bins = [18, 25, 35, 45, 55, 65, 100]
    age_labels = ["18-24", "25-34", "35-44", "45-54", "55-64", "65+"]

    age_frame = filtered_df.copy()
    age_frame["Age Group"] = pd.cut(age_frame["age"], bins=age_bins, labels=age_labels, right=False)

    age_data = age_frame.groupby("Age Group", observed=False)["churn"].mean().reset_index()
    age_data["Stable"] = (1 - age_data["churn"]) * 100
    age_data["Risk"] = age_data["churn"] * 100

    fig_age = go.Figure()
    fig_age.add_bar(x=age_data["Age Group"], y=age_data["Stable"], name="Stable", marker_color=PURPLE)
    fig_age.add_bar(x=age_data["Age Group"], y=age_data["Risk"], name="Risk", marker_color=RED)

    style_plotly_figure(fig_age, title="Customer Stability Across Age Groups")
    fig_age.update_layout(
        barmode="stack",
        xaxis_title="Age Group",
        yaxis_title="Customer Share (%)",
        legend=dict(orientation="h", y=1.08, x=1, xanchor="right"),
    )
    fig_age.update_yaxes(range=[0, 100])

    st.plotly_chart(fig_age, use_container_width=True)
    st.markdown("</div>", unsafe_allow_html=True)

    st.markdown('<div class="hr-glow"></div>', unsafe_allow_html=True)
    st.markdown(
        """
        <center style="color:#cbd5e1; font-size:0.95rem;">
            Smart Banking Intelligence - Overview Module
        </center>
        """,
        unsafe_allow_html=True,
    )


if __name__ == "__main__":
    show_overview()
