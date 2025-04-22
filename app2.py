import streamlit as st
import joblib
import pandas as pd

# Load the model and model columns
model = joblib.load("xgboost_model.pkl")
model_columns = joblib.load("model_columns.pkl")

st.title("🎓 G3 Score Predictor")

# Input form
with st.form("prediction_form"):
    G1 = st.number_input("G1 Score", min_value=0, max_value=20, value=10)
    G2 = st.number_input("G2 Score", min_value=0, max_value=20, value=10)
    absences = st.number_input("Absences", min_value=0, value=0)
    famrel = st.slider("Family Relationship Quality (1 = very bad, 5 = excellent)", 1, 5, 3)
    schoolsup = st.selectbox("School Support", ["yes", "no"])
    reason = st.selectbox("Reason for Choosing School", ["home", "reputation", "course", "other"])
    Fjob = st.selectbox("Father's Job", ["teacher", "health", "services", "at_home", "other"])
    activities = st.selectbox("Extra-curricular Activities", ["yes", "no"])
    romantic = st.selectbox("In a Romantic Relationship", ["yes", "no"])
    submit = st.form_submit_button("Predict")

# Prediction
if submit:
    G1_G2_avg = (G1 + G2) / 2
    input_df = pd.DataFrame([{
        "G1_G2_avg": G1_G2_avg,
        "G2": G2,
        "absences": absences,
        "famrel": famrel,
        "schoolsup": schoolsup,
        "reason": reason,
        "Fjob": Fjob,
        "activities": activities,
        "romantic": romantic
    }])

    # One-hot encoding and align with model columns
    input_df = pd.get_dummies(input_df)
    input_df = input_df.reindex(columns=model_columns, fill_value=0)

    prediction = model.predict(input_df)[0]
    st.success(f"✅ Predicted G3 Score: {prediction:.2f}")
