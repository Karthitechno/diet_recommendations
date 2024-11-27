import streamlit as st
import google.generativeai as genai
import os
from dotenv import load_dotenv
load_dotenv()


# Configure the Gemini API
genai.configure(api_key=os.getenv("GOOGLE_API_KEY"))

# Define the model
model = genai.GenerativeModel("gemini-1.5-flash")

# Function to classify the disease and get diet suggestions
def get_disease_info_and_diet(disease_name, language):
    # Classify the disease
    classification_prompt = (
        f"Classify the disease '{disease_name}' (e.g., genetic, fungal, viral, bacterial, or other). "
        f"Provide a simple explanation in {language} for a layperson."
    )
    classification_response = model.generate_content(classification_prompt)
    disease_classification = classification_response.text

    # Generate diet suggestions with explanations
    diet_prompt = (
        f"Provide detailed diet suggestions for the disease '{disease_name}' in {language}. "
        "List specific foods to eat and avoid, explaining why they are beneficial or harmful."
    )
    diet_response = model.generate_content(diet_prompt)
    diet_suggestions = diet_response.text

    return disease_classification, diet_suggestions

# Function to generate a meal plan
def generate_meal_plan(disease_name, language):
    meal_plan_prompt = (
        f"Create a personalized weekly meal plan for someone with '{disease_name}' in {language}. "
        "Include breakfast, lunch, and dinner with specific food items and simple recipes."
    )
    meal_plan_response = model.generate_content(meal_plan_prompt)
    return meal_plan_response.text

# Streamlit interface
st.title("Disease Classification and Diet Recommendations")

# User input
language = st.selectbox("Select your preferred language:", ["English", "Tamil", "Hindi", "Spanish", "French"])
disease = st.text_input("Enter the disease name:")
age = st.number_input("Enter your age:", min_value=0, max_value=120, step=1)
gender = st.selectbox("Select your gender:", ["Male", "Female", "Other"])
allergies = st.text_input("List any food allergies or dietary preferences (optional):")

# Process input and display results
if st.button("Get Recommendations"):
    if language and disease:
        classification, suggestions = get_disease_info_and_diet(disease, language)
        
        st.subheader("Disease Classification:")
        st.write(classification)
        
        st.subheader("Diet Suggestions:")
        st.write(suggestions)

        st.subheader("Meal Plan:")
        meal_plan = generate_meal_plan(disease, language)
        st.write(meal_plan)

        with st.expander("Learn more about recommended foods"):
            st.write("This section could provide nutritional facts and benefits of recommended foods.")
        
        # Option to download recommendations
        st.download_button(
            "Download Recommendations",
            data=f"Disease Classification:\n{classification}\n\nDiet Suggestions:\n{suggestions}\n\nMeal Plan:\n{meal_plan}",
            file_name="diet_recommendations.txt"
        )
    else:
        st.warning("Please enter both the language and the disease name.")

# Additional features
st.sidebar.header("Health Tips")
st.sidebar.write("Maintain a balanced diet, stay hydrated, and get regular exercise.")

st.sidebar.subheader("Contact Us")
st.sidebar.write("For queries or feedback, email us at support@healthapp.com")
