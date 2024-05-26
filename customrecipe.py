import streamlit as st
import openai

# Ensure your OpenAI API key is set in the Streamlit secrets
openai.api_key = st.secrets["API_key"]

def generate_recipe(ingredients, cuisine, dietary_restrictions, cooking_time):
    prompt_text = (
        f"I have the following ingredients: {ingredients}. "
        f"I want to make a {cuisine} dish that fits my dietary restrictions ({dietary_restrictions}) and can be prepared in {cooking_time} minutes."
    )
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
        return response['choices'][0]['message']['content'].strip()
    except Exception as e:
        st.error(f"Error generating recipe: {e}")
        return None

def app():
    st.title("Custom Recipe Creator")

    if 'step' not in st.session_state:
        st.session_state.step = 1

    if st.session_state.step == 1:
        ingredients = st.text_input("Enter the ingredients you have (comma-separated)")
        cuisine_options = ["Italian", "Mexican", "Asian", "Mediterranean", "American", "Indian", "French", "Japanese", "Chinese", "Thai", "Spanish", "Greek", "Middle Eastern", "Caribbean", "African"]
        cuisine = st.selectbox("Select cuisine type", cuisine_options)
        dietary_options = ["None", "Vegetarian", "Vegan", "Gluten-Free", "Keto", "Paleo", "Low-Carb", "Low-Fat", "Dairy-Free", "Nut-Free", "Halal", "Kosher"]
        dietary_restrictions = st.multiselect("Any dietary restrictions?", dietary_options)
        cooking_time = st.number_input("Maximum cooking time (minutes)", min_value=10, max_value=240, step=5)
        
        if st.button("Get Recipe"):
            st.session_state.ingredients = ingredients
            st.session_state.cuisine = cuisine
            st.session_state.dietary_restrictions = dietary_restrictions
            st.session_state.cooking_time = cooking_time
            st.session_state.step = 2
            st.experimental_rerun()

    if st.session_state.step == 2:
        dietary_restrictions = ", ".join(st.session_state.dietary_restrictions) if st.session_state.dietary_restrictions else "None"
        recipe = generate_recipe(
            st.session_state.ingredients,
            st.session_state.cuisine,
            dietary_restrictions,
            st.session_state.cooking_time
        )
        if recipe:
            st.session_state.recipe = recipe
            st.session_state.step = 3
        else:
            st.session_state.step = 1
        st.experimental_rerun()

    if st.session_state.step == 3:
        st.write(f"Custom recipe based on your ingredients, cuisine preference, dietary restrictions, and cooking time:\n\n{st.session_state.recipe}")
        if st.button("Start Over"):
            for key in ['step', 'ingredients', 'cuisine', 'dietary_restrictions', 'cooking_time', 'recipe']:
                if key in st.session_state:
                    del st.session_state[key]
            st.experimental_rerun()

if __name__ == "__main__":
    app()
