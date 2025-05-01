import streamlit as st
import joblib
import pandas as pd

# ==== Custom CSS ====
st.markdown("""
    <style>
    .main {
        background-color: #f4f6f9;
        padding: 2rem;
        border-radius: 12px;
    }
    h1 {
        color: #1f77b4;
        text-align: center;
    }
    .stButton>button {
        background-color: #1f77b4;
        color: white;
        border-radius: 10px;
        padding: 0.5rem 1rem;
    }
    .stButton>button:hover {
        background-color: #105b8d;
        color: #ffffff;
    }
    .stSlider>div>div>div {
        background: #1f77b4;
    }
    .stNumberInput input {
        border-radius: 10px;
    }
    .stSelectbox>div>div {
        border-radius: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# ==== App Title ====
st.title("🎓 Student Score Prediction System")

# ==== Load Model ====
model = joblib.load("student_score_model.pkl")

# ==== Input UI ====
with st.container():
    st.subheader("📋 Student Details")

    col1, col2 = st.columns(2)
    with col1:
        G1 = st.number_input("G1 (First Term Grade)", min_value=0, max_value=20, value=10)
        absences = st.number_input("Absences", min_value=0, max_value=100, value=5)
        romantic = st.selectbox("In a Romantic Relationship?", ["No", "Yes"])
        reason = st.selectbox("Reason for Choosing School", ["Home", "Reputation", "Course", "Other"])
        health = st.slider("Health Status (1-5)", 1, 5, 3)
        activities = st.selectbox("Extracurricular Activities", ["No", "Yes"])
        Walc = st.slider("Weekend Alcohol Consumption (1-5)", 1, 5, 2)

    with col2:
        G2 = st.number_input("G2 (Second Term Grade)", min_value=0, max_value=20, value=10)
        age = st.number_input("Age", min_value=15, max_value=22, value=18)
        famrel = st.slider("Family Relationship Quality (1-5)", 1, 5, 3)
        guardian = st.selectbox("Guardian", ["Mother", "Father", "Other"])
        Mjob = st.selectbox("Mother's Job", ["Teacher", "Health", "Services", "At_home", "Other"])
        Fjob = st.selectbox("Father's Job", ["Teacher", "Health", "Services", "At_home", "Other"])
        studytime = st.slider("Weekly Study Time (1-4)", 1, 4, 2)

    Fedu = st.slider("Father's Education Level (0-4)", 0, 4, 2)
    Medu = st.slider("Mother's Education Level (0-4)", 0, 4, 2)
    schoolsup = st.selectbox("Extra Educational Support", ["No", "Yes"])
    goout = st.slider("Going Out with Friends (1-5)", 1, 5, 3)
    traveltime = st.slider("Home to School Travel Time (1-4)", 1, 4, 2)

# ==== Convert categorical values ====
romantic = 1 if romantic == "Yes" else 0
schoolsup = 1 if schoolsup == "Yes" else 0
activities = 1 if activities == "Yes" else 0

reason_dict = {"Home": 0, "Reputation": 1, "Course": 2, "Other": 3}
guardian_dict = {"Mother": 0, "Father": 1, "Other": 2}
Mjob_dict = {"Teacher": 0, "Health": 1, "Services": 2, "At_home": 3, "Other": 4}
Fjob_dict = {"Teacher": 0, "Health": 1, "Services": 2, "At_home": 3, "Other": 4}

reason = reason_dict[reason]
guardian = guardian_dict[guardian]
Mjob = Mjob_dict[Mjob]
Fjob = Fjob_dict[Fjob]

# ==== Create DataFrame ====
input_data = pd.DataFrame([[
    G2, absences, G1, age, romantic, famrel, reason, guardian, health,
    goout, Mjob, studytime, schoolsup, Fedu, activities, Fjob, Walc,
    traveltime, Medu
]], columns=[
    "G2", "absences", "G1", "age", "romantic", "famrel", "reason", "guardian", "health",
    "goout", "Mjob", "studytime", "schoolsup", "Fedu", "activities", "Fjob", "Walc",
    "traveltime", "Medu"
])

# ==== Predict Button ====
if st.button("🔍 Predict Score"):
    prediction = model.predict(input_data)
    final_score = round(prediction[0], 2)

    # Comment logic
    if final_score >= 18:
        comment = "🌟 Excellent! Keep up the great work!"
    elif final_score >= 15:
        comment = "👍 Good job! You are doing well, keep pushing!"
    elif final_score >= 10:
        comment = "📚 You can do better! Focus on improving your study habits."
    else:
        comment = "⚠️ Your score is quite low. Consider seeking extra help and studying more effectively."

    st.success(f"📊 Predicted Final Grade (G3): {final_score}")
    st.info(comment)
