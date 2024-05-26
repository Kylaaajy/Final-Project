import streamlit as st
import openai

# Ensure your OpenAI API key is set in the Streamlit secrets
openai.api_key = st.secrets["API_key"]

def generate_recipe(ingredients, cuisine, dietary_restrictions, cooking_time):
    prompt_text = (
        f"I have the following ingredients: {ingredients}. "
        f"I want to make a {cuisine} dish that fits my dietary restrictions ({dietary_restrictions}) and can be prepared in {cooking_time} minutes."
    )
    st.write(f"Prompt: {prompt_text}")  # Debug line to show the prompt
    try:
        response = openai.ChatCompletion.create(
            model="gpt-4-turbo",
            messages=[
                {"role": "system", "content": "You are a helpful assistant."},
                {"role": "user", "content": prompt_text},
            ],
            temperature=0.7,
            max_tokens=150
        )
        st.write(f"Response: {response}")  # Debug line to show the raw API response
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Error generating recipe: {e}")
        return None

def app():
    st.title("Custom Recipe Creator")

    if 'step' not in st.session_state:
        st.session_state.step = 1

    st.write(f"Current Step: {st.session_state.step}")  # Debug line to show the current step

    if st.session_state.step == 1:
        ingredients = st.text_input("Enter the ingredients you have (comma-separated)")
        cuisine_options = ["Italian", "Mexican", "Asian", "Mediterranean", "American", "Indian", "French", "Japanese", "Chinese", "Thai", "Spanish", "Greek", "Middle Eastern", "Caribbean", "African"]
        cuisine = st.selectbox("Select cuisine type", cuisine_options)
        dietary_options = ["None", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "Paleo", "Low-Carb", "Low-Fat", "Dairy-Free", "Nut-Free", "Halal", "Kosher"]
        dietary_restrictions = st.multiselect("Any dietary restrictions?", dietary_options)
        cooking_time = st.number_input("Maximum cooking time (minutes)", min_value=10, max_value=240, step=5)
 
