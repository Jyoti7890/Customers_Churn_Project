import os
from typing import Optional

import streamlit as st


PLOTLY_TEXT = "#F8FAFC"
PLOTLY_GRID = "rgba(148, 163, 184, 0.25)"
PLOTLY_BG = "rgba(15, 23, 42, 0.35)"


def load_css():
    """Load assets/style.css and inject it into the Streamlit app."""
    css_path = os.path.join(os.getcwd(), "assets", "style.css")

    if os.path.exists(css_path):
        with open(css_path, encoding="utf-8") as f:
            st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

    st.sidebar.markdown("### Simple - Smart - Reliable")
    st.sidebar.markdown('<div class="hr-glow"></div>', unsafe_allow_html=True)


def style_plotly_figure(fig, title: Optional[str] = None):
    """Apply a consistent high-contrast dark theme to Plotly figures."""
    fig.update_layout(
        template="plotly_dark",
        plot_bgcolor=PLOTLY_BG,
        paper_bgcolor="rgba(0, 0, 0, 0)",
        font=dict(color=PLOTLY_TEXT, size=14, family="Poppins"),
        title=(
            dict(
                text=title,
                font=dict(size=18, color=PLOTLY_TEXT, family="Poppins"),
                x=0.02,
                xanchor="left",
            )
            if title
            else None
        ),
        legend=dict(
            font=dict(color=PLOTLY_TEXT, size=13),
            bgcolor="rgba(15, 23, 42, 0.7)",
            bordercolor="rgba(148, 163, 184, 0.45)",
            borderwidth=1,
        ),
        margin=dict(l=20, r=20, t=60, b=40),
    )

    fig.update_xaxes(
        title_font=dict(color=PLOTLY_TEXT, size=15),
        tickfont=dict(color=PLOTLY_TEXT, size=13),
        showgrid=True,
        gridcolor=PLOTLY_GRID,
        zeroline=False,
    )
    fig.update_yaxes(
        title_font=dict(color=PLOTLY_TEXT, size=15),
        tickfont=dict(color=PLOTLY_TEXT, size=13),
        showgrid=True,
        gridcolor=PLOTLY_GRID,
        zeroline=False,
    )

    return fig
