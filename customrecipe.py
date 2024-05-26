import streamlit as st
import openai
import asyncio

from openai import AsyncOpenAI

client = AsyncOpenAI(api_key=st.secrets["API_key"])

async def generate_recipe(ingredients, cuisine, dietary_restrictions, cooking_time):
    prompt_text = (
        f"I have the following ingredients: {ingredients}. "
        f"I want to make a {cuisine} dish that fits my dietary restrictions ({dietary_restrictions}) and can be prepared in {cooking_time} minutes."
    )

    response = await client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a Chef"},
            {"role": "user", "content": prompt_text}
        ],
    )

    return response.choices[0].message.content

def app():
    st.title("Custom Recipe Creator")

    if 'step' not in st.session_state:
        st.session_state.step = 1

    if st.session_state.step == 1:
        st.session_state.ingredients = st.text_input("Enter the ingredients you have (comma-separated)")
        st.session_state.cuisine = st.selectbox("Select cuisine type", ["Italian", "Mexican", "Asian", "Mediterranean", "Other"])
        st.session_state.dietary_restrictions = st.text_input("Any dietary restrictions?")
        st.session_state.cooking_time = st.number_input("Maximum cooking time (minutes)", min_value=1, max_value=240, step=5)
        if st.button("Get Recipe"):
            st.session_state.step = 2

    if st.session_state.step == 2:
        if st.button("Generate Recipe"):
            st.session_state.step = 3  # Proceed to show the recipe
            st.experimental_rerun()

    if st.session_state.step == 3:
        if 'recipe' not in st.session_state:
            async def fetch_recipe():
                recipe = await generate_recipe(
                    st.session_state.ingredients,
                    st.session_state.cuisine,
                    st.session_state.dietary_restrictions,
                    st.session_state.cooking_time
                )
                st.session_state.recipe = recipe
                st.experimental_rerun()

            asyncio.run(fetch_recipe())
        else:
            st.write(f"Custom recipe based on your ingredients, cuisine preference, dietary restrictions, and cooking time: {st.session_state.recipe}")
            if st.button("Start Over"):
                for key in ['step', 'ingredients', 'cuisine', 'dietary_restrictions', 'cooking_time', 'recipe']:
                    if key in st.session_state:
                        del st.session_state[key]
                st.experimental_rerun()

if __name__ == "__main__":
    app()