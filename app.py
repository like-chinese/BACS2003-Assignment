import streamlit as st
import pandas as pd
import joblib

# ==== Custom Modern HCI CSS ====
st.markdown("""
    <style>
    body {
        background-color: #f5f7fa;
    }
    .main {
        background-color: #ffffff;
        padding: 2rem;
        border-radius: 12px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.1);
    }
    h1 {
        text-align: center;
        color: #2c3e50;
        font-size: 2.5rem;
    }
    .stButton>button {
        background-color: #2980b9;
        color: white;
        border-radius: 8px;
        padding: 0.6rem 1.2rem;
        font-size: 1.1rem;
    }
    .stButton>button:hover {
        background-color: #1f6391;
    }
    .stSlider>div>div>div {
        background: #2980b9;
    }
    .block-container {
        padding-top: 2rem;
    }
    </style>
""", unsafe_allow_html=True)

# ==== App Title ====
st.title("🎓 Student Score Prediction System")

# ==== Load Model ====
model = joblib.load("student_score_model.pkl")

st.markdown("### 📋 Please Fill in the Student Details Below")

# ==== Input UI - Single Column Flow ====
G1 = st.number_input("📘 G1 - First Term Grade", 0, 20, 10)
G2 = st.number_input("📗 G2 - Second Term Grade", 0, 20, 10)
age = st.slider("🎂 Age", 15, 22, 18)
absences = st.number_input("🏫 Number of Absences", 0, 100, 5)
famrel = st.slider("👨‍👩‍👧‍👦 Family Relationship Quality (1 = Poor, 5 = Excellent)", 1, 5, 3)
health = st.slider("🩺 Current Health Status", 1, 5, 3)
goout = st.slider("🎉 Going Out with Friends (1 = Rarely, 5 = Often)", 1, 5, 3)
romantic = st.radio("💘 In a Romantic Relationship?", ["No", "Yes"], horizontal=True)
activities = st.radio("🏀 Participates in Extracurricular Activities?", ["No", "Yes"], horizontal=True)
schoolsup = st.radio("📚 Receives Extra Educational Support?", ["No", "Yes"], horizontal=True)
reason = st.selectbox("📌 Reason for Choosing the School", ["Home", "Reputation", "Course", "Other"])
guardian = st.selectbox("👨‍👩‍👧 Guardian", ["Mother", "Father", "Other"])
Fedu = st.slider("👨‍🎓 Father's Education Level", 0, 4, 2)
Medu = st.slider("👩‍🎓 Mother's Education Level", 0, 4, 2)
Mjob = st.selectbox("👩 Mother's Job", ["Teacher", "Health", "Services", "At_home", "Other"])
Fjob = st.selectbox("👨 Father's Job", ["Teacher", "Health", "Services", "At_home", "Other"])
studytime = st.slider("📖 Weekly Study Time (1-4)", 1, 4, 2)
traveltime = st.slider("🚗 Home to School Travel Time (1-4)", 1, 4, 2)
Walc = st.slider("🍻 Weekend Alcohol Consumption (1-5)", 1, 5, 2)

# ==== Categorical Conversion ====
romantic = 1 if romantic == "Yes" else 0
activities = 1 if activities == "Yes" else 0
schoolsup = 1 if schoolsup == "Yes" else 0
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

# ==== Prediction ====
if st.button("🔍 Predict Final Score"):
    prediction = model.predict(input_data)
    final_score = round(prediction[0], 2)

    if final_score >= 18:
        comment = "🌟 Excellent! Keep up the great work!"
    elif final_score >= 15:
        comment = "👍 Good job! You're doing well, stay consistent!"
    elif final_score >= 10:
        comment = "📚 Needs improvement. Stay focused and ask for help if needed."
    else:
        comment = "⚠️ Your score is low. Please seek guidance and improve your study routine."

    st.success(f"📊 Predicted Final Grade (G3): {final_score}")
    st.info(comment)
