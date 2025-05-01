import streamlit as st
import joblib
import pandas as pd

# ==== Page Setup ====
st.set_page_config(page_title="Student Score Predictor", layout="centered")

# ==== Load Model ====
model = joblib.load("GradientBoostingRegressor.pkl")

# ==== Styling with CSS ====
st.markdown("""
    <style>
    .stForm {
        border: 1px solid #cfcfcf;
        padding: 2rem;
        border-radius: 12px;
        background-color: #f9f9f9;
        box-shadow: 2px 2px 10px rgba(0,0,0,0.05);
    }
    .stSlider label div, .stSelectbox label div, .stNumberInput label div {
        font-weight: 600;
    }
    .stMarkdown h1 {
        color: #1f77b4;
    }
    </style>
""", unsafe_allow_html=True)

# ==== App Title ====
st.title("🎓 Student Final Grade Predictor (G3) -Gradient Boosting Regressor_Doo Wei Jie")

# ==== Input Form ====
with st.form("student_form"):
    st.subheader("📋 Enter Student Information")

    G1 = st.number_input("G1 - First Period Grade", 0, 20, help="First term grade (0-20).")
    G2 = st.number_input("G2 - Second Period Grade", 0, 20, help="Second term grade (0-20).")
    age = st.number_input("Age", 15, 22, help="Student's age (15-22).")
    absences = st.number_input("Absences", 0, 100, help="Number of school absences.")
    romantic = st.selectbox("In a Romantic Relationship?", ["No", "Yes"], help="Whether the student is in a romantic relationship.")
    reason = st.selectbox("Reason for Choosing School", ["Home", "Reputation", "Course", "Other"], help='Why student chose the school: home proximity, reputation, course preference, etc.')
    health = st.slider("Health Status (1 = very bad, 5 = very good)", 1, 5, 3, help="Student's current health status.")
    activities = st.selectbox("Extracurricular Activities", ["No", "Yes"], help="Is the student involved in extracurricular activities?")
    Walc = st.slider("Weekend Alcohol Consumption (1 = very low, 5 = very high)", 1, 5, 2, help="Alcohol consumption on weekends.")
  
    famrel = st.slider("Family Relationship Quality (1 = very bad, 5 = excellent)", 1, 5, 3, help="Quality of family relationships.")
  
    guardian = st.selectbox("Guardian", ["Mother", "Father", "Other"], help="Who is the student's primary guardian?")

    Mjob = st.selectbox("Mother's Job", ["Teacher", "Health", "Services", "At_home", "Other"], help="Mother's job: teacher, health, services, at home, or other.")
    Medu = st.slider("Mother's Education (0 = none, 4 = higher education)", 0, 4, 2, help="Mother's education level (0-4).")
  
    Fjob = st.selectbox("Father's Job", ["Teacher", "Health", "Services", "At_home", "Other"], help="Father's job: teacher, health, services, at home, or other.")
    Fedu = st.slider("Father's Education (0 = none, 4 = higher education)", 0, 4, 2, help="Father's education level (0-4).")

    schoolsup = st.selectbox("Extra Educational Support", ["No", "Yes"], help="Does the student receive extra educational support?")
    goout = st.slider("Going Out with Friends (1 = very low, 5 = very high)", 1, 5, 3, help="Frequency of going out with friends.")

    studytime_option = st.selectbox(
        "Weekly Study Time",
        options=["1 :   <2 hours", "2 :   2 to 5 hours", "3 :   5 to 10 hours", "4 :   >10 hours"],
        help="Estimated weekly study time."
    )
    studytime = int(studytime_option.split(" : ")[0])

    
    traveltime_option = st.selectbox(
        "Travel Time to School",
        options=["1 :   <15 minutes", "2 :   15 to 30 minutes", "3 :   30 minutes to 1 hour", "4 :   >1 hour"],
        help="Estimated time taken to travel from home to school."
    )
    traveltime = int(traveltime_option.split(" : ")[0])

    submitted = st.form_submit_button("🔍 Predict Final Score")

# ==== Data Preprocessing ====
if submitted:
    # Convert categorical to numeric
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

    # Create DataFrame for model input
    input_data = pd.DataFrame([[G2, absences, G1, age, romantic, famrel, reason, guardian, health,
                                 goout, Mjob, studytime, schoolsup, Fedu, activities, Fjob, Walc,
                                 traveltime, Medu]],
                               columns=["G2", "absences", "G1", "age", "romantic", "famrel", "reason",
                                        "guardian", "health", "goout", "Mjob", "studytime", "schoolsup",
                                        "Fedu", "activities", "Fjob", "Walc", "traveltime", "Medu"])

    # Prediction
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

    # Output
    st.success(f"📊 Predicted Final Grade (G3): {final_score}   / 20")
    st.info(comment) 
