import openai

openai.api_key = "your_openai_api_key"

def generate_recipe(ingredients, cuisine, dietary_restrictions, cooking_time):
    prompt_text = (
        f"I have the following ingredients: {ingredients}. "
        f"I want to make a {cuisine} dish that fits my dietary restrictions ({dietary_restrictions}) and can be prepared in {cooking_time} minutes."
    )

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            {"role": "system", "content": "You are a helpful assistant."},
            {"role": "user", "content": prompt_text},
        ],
        temperature=0.7,
        max_tokens=150
    )

    return response['choices'][0]['message']['content'].strip()

# Test the function
ingredients = "chicken, rice, broccoli"
cuisine = "Asian"
dietary_restrictions = "None"
cooking_time = 30

recipe = generate_recipe(ingredients, cuisine, dietary_restrictions, cooking_time)
print(recipe)
