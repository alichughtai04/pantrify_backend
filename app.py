from flask import Flask, jsonify, request
import google.generativeai as genai
import os
import requests
from flask_cors import CORS

app = Flask(__name__)
CORS(app) 
genai.configure(api_key="AIzaSyAaXySu_UBGasBnNJL3JkgewHoXayhWMJE")

model = genai.GenerativeModel('gemini-1.5-flash')

@app.route('/chat', methods=['POST'])
def chat():
    data = request.get_json()
    ingredients_list = data.get("ingredients", [])
    
    if not isinstance(ingredients_list, list):
        return jsonify({"error": "Ingredients should be a list"}), 400

    ingredients_as_string = ', '.join(ingredients_list)

    prompt = f"You are a personal recipe creator. Give me a recipe based on the ingredients in the pantry. Start by listing the Ingredients. Then list the cooking steps and directions. Even add an extra section for special additions. {ingredients_as_string}"
    try:
        response = model.generate_content(prompt, stream=False)

        # Extract the text content from the response
        response_text = response.text

        return jsonify({"reply": response_text})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
