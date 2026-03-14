

import json
from google import genai
from google.genai import types

def analyze_food(image):
  
    food_image = image
    if not food_image:
        return {"error": "No image provided"}

    # 2. Initialize the New Client
    # Replace with your actual API key or use an environment variable
    client = genai.Client(api_key="AIzaSyAkDHWmhbzpUYxyMEoQ6mGLnNSzVdHPTQc")

    # 3. Read image bytes
    image_bytes = food_image.read()

    # 4. Define the Prompt & Schema
    prompt = "You are a nutrition expert. Identify the food in the image and estimate calories.get me response.txt with calorie_low, calorie_high, food name,and note as json."

    try:
        # Using the new SDK's generate_content
        response = client.models.generate_content(
            model="gemini-2.5-flash", # or gemini-1.5-flash
            contents=[
                prompt,
                types.Part.from_bytes(
                    data=image_bytes,
                    mime_type=food_image.content_type
                )
            ],
            config=types.GenerateContentConfig(
                system_instruction="You are a clinical nutritionist. Return ONLY JSON.",
                response_mime_type="application/json",
                # Explicit schema ensures the JSON structure is 100% consistent
                response_schema={
                    "type": "OBJECT",
                    "properties": {
                        "food_name": {"type": "STRING"},
                        "average_calorie": {"type": "NUMBER"},
                        # "calorie_high": {"type": "NUMBER"} # Changed to NUMBER for easier math later
                    },
                    "required": ["food_name", "average_calorie"]
                }
            )
        )

        # 5. Access the parsed JSON directly
        # The new SDK automatically parses JSON if response_mime_type is set
     
        return response.parsed

    except Exception as e:
        return {"error": str(e)}