import streamlit as st
import google.generativeai as genai
from api_key import api_key

# Configure genai with API key
genai.configure(api_key=api_key)

generation_config = {
    "temperature": 0.4,
    "top_p": 0.95,
    "top_k": 64,
    "max_output_tokens": 8192,
    "response_mime_type": "text/plain",
}

system_prompt = """
You are an AI assistant trained to assist healthcare professionals in analyzing medical images. Your role is to provide preliminary observations and insights 
based on image analysis, which should then be reviewed by a qualified healthcare professional.

Your Responsibilities include:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.
3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.

Important Notes:

1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the provided image.'
3. Emphasize that your analysis is only to support decision-making and is NOT a diagnosis. Make suggestions based on knowledge of solutions and remedies. 
4. Clearly state that any observations or recommendations are for informational purposes only and should not replace professional medical consultation.

Example Analysis:
- Image: Skin with visible acne.
- Response: "The image shows multiple small, red, inflamed spots, commonly associated with acne. This is a preliminary observation and not a diagnosis."

Disclaimer: Accompany your analysis with the disclaimer: "I am an AI assistant and cannot provide medical advice. Consult with a Doctor before making any decisions."

Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above.
"""

# Model configuration 
model = genai.GenerativeModel(
   model_name="gemini-1.5-flash",
    generation_config=generation_config
)

# Set the page configuration 
st.set_page_config(page_title="VitalImage Analytics", page_icon=":robot:")

# Set the title 
st.title("👩‍⚕️ Vital❤️Image📷 Analytics📊 🩺")

# Set the subtitle
st.subheader("An application that can help users to identify medical images")
uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png", "jpg", "jpeg"])

if uploaded_file:
    st.image(uploaded_file, width=300, caption="Uploaded Medical Image")
    submit_button = st.button("Generate the Analysis")

    if submit_button:
        # Convert uploaded file to bytes
        image_data = uploaded_file.read()

        # Prepare the image part for the API
        image_parts = [
            {
                "mime_type": uploaded_file.type,  # get the MIME type of the uploaded file
                "data": image_data  # directly use the bytes from the uploaded file
            }
        ]

        # Prepare the prompt parts
        prompt_parts = [
            image_parts[0], 
            system_prompt
        ]

        # Generate a response based on prompt and image
        st.title("Here is the analysis based on your image")
        response = model.generate_content(prompt_parts)

        st.write(response.text)
