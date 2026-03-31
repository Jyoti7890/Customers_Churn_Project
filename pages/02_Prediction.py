import streamlit as st
import pandas as pd
from utils.data_loader import load_model, load_data
from utils.ui_components import load_css


def show_prediction():
    """
    Customer churn prediction using a saved ML model.
    No retraining. Only prediction.
    """

    # =============================
    # Load UI Theme
    # =============================
    load_css()

    st.markdown("""
        <div class="glass-card">
            <h1 style='text-align:center;'>Customer Churn Prediction</h1>
            <p style='text-align:center; color:#a78bfa;'>
            Check if a customer is likely to leave the bank
            </p>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="hr-glow"></div>', unsafe_allow_html=True)

    # =============================
    # Load Model & Data
    # =============================
    model = load_model()   # churn_prediction_model.pkl
    df = load_data()

    if model is None or df is None:
        st.error("System error: Model or data not found.")
        return

    # Colors
    RED = "#ef4444"
    GREEN = "#22c55e"
    ORANGE = "#f59e0b"
    WHITE = "#e5e7eb"

    # =============================
    # Input Section
    # =============================
    st.markdown('<div class="glass-card">', unsafe_allow_html=True)
    st.markdown("### Customer Details")
    st.caption("Fill customer information to predict churn risk.")

    with st.form("prediction_form"):

        col1, col2 = st.columns(2)

        with col1:
            st.markdown("**Basic Information**")
            country = st.selectbox("Country", df["country"].unique())
            gender = st.selectbox("Gender", df["gender"].unique())
            age = st.slider("Age", 18, 95, 35)
            tenure = st.slider("Years with Bank", 0, 10, 5)
            credit_score = st.slider("Credit Score", 300, 850, 650)

        with col2:
            st.markdown("**Banking Information**")
            balance = st.number_input("Account Balance ($)", 0.0, 300000.0, 50000.0, step=1000.0)
            products_number = st.selectbox("Number of Bank Products", [1, 2, 3, 4])
            credit_card = st.selectbox("Has Credit Card?", ["Yes", "No"])
            active_member = st.selectbox("Active Customer?", ["Yes", "No"])
            estimated_salary = st.number_input("Estimated Salary ($)", 0.0, 300000.0, 75000.0, step=1000.0)

        submit = st.form_submit_button("Predict Churn Risk")

    st.markdown('</div>', unsafe_allow_html=True)

    # =============================
    # Prediction
    # =============================
    if submit:

        input_df = pd.DataFrame([{
            "credit_score": credit_score,
            "country": country,
            "gender": gender,
            "age": age,
            "tenure": tenure,
            "balance": balance,
            "products_number": products_number,
            "credit_card": 1 if credit_card == "Yes" else 0,
            "active_member": 1 if active_member == "Yes" else 0,
            "estimated_salary": estimated_salary
        }])

        try:
            churn_prob = model.predict_proba(input_df)[0][1]
            churn_percent = churn_prob * 100

            # Risk Level
            if churn_prob > 0.6:
                risk = "High"
                color = RED
            elif churn_prob > 0.3:
                risk = "Medium"
                color = ORANGE
            else:
                risk = "Low"
                color = GREEN

            st.markdown('<div class="hr-glow"></div>', unsafe_allow_html=True)

            # =============================
            # Result Section
            # =============================
            st.markdown(f"""
            <div class="glass-card">
                <h3 style="margin-bottom:5px;">Prediction Result</h3>
                <h1 style="color:{color};">{risk} Risk of Churn</h1>
                <p style="color:{WHITE}; font-size:18px;">
                Chance of leaving the bank: <b>{churn_percent:.1f}%</b>
                </p>
            </div>
            """, unsafe_allow_html=True)

            col_r1, col_r2 = st.columns(2)

            with col_r1:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("**Risk Explanation**")
                # Fix: Cast to float to avoid "invalid type: float32" error
                st.progress(float(churn_prob))
                st.write(
                    f"Based on customer details, the model estimates a "
                    f"{churn_percent:.1f}% chance that the customer may leave."
                )
                st.markdown('</div>', unsafe_allow_html=True)

            with col_r2:
                st.markdown('<div class="glass-card">', unsafe_allow_html=True)
                st.markdown("**Suggested Action**")

                if risk == "High":
                    st.error("Customer is likely to leave. Immediate retention action needed.")
                elif risk == "Medium":
                    st.warning("Customer may leave. Offer discounts or engagement plans.")
                else:
                    st.success("Customer is stable. No immediate action required.")

                st.markdown('</div>', unsafe_allow_html=True)

            # Restoring Session State for other pages (Explainability, Retention)
            st.session_state['last_prediction'] = {
                'input': input_df,
                'probability': float(churn_prob),
                'status': risk
            }

        except Exception as e:
            st.error(f"Prediction failed: {e}")


if __name__ == "__main__":
    show_prediction()
