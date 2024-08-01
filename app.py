#import necessary modules
import streamlit as st
from pathlib import Path 
import google.generativeai as genai

from api_key import api_key

#configure genai with api key
genai.configure(api_key=api_key)

generation_config = {
  "temperature": 0.4,
  "top_p": 0.95,
  "top_k": 64,
  "max_output_tokens": 8192,
  "response_mime_type": "text/plain",
}

system_prompt = """

As a highly skilled medical practitioner specializing in image analysis, you are tasked with examining medical images for a renowned hospital. Your
expertise is crucial in identifying any anomalies, diseases, or health issues that may be present in the images.

Your Responsibilities include:

1. Detailed Analysis: Thoroughly analyze each image, focusing on identifying any abnormal findings.
2. Findings Report: Document all observed anomalies or signs of disease. Clearly articulate these findings in a structured format.
3. Recommendations and Next Steps: Based on your analysis, suggest potential next steps, including further tests or treatments as applicable.
4. Treatment Suggestions: If appropriate, recommend possible treatment options or interventions.

Important Notes:

1. Scope of Response: Only respond if the image pertains to human health issues.
2. Clarity of Image: In cases where the image quality impedes clear analysis, note that certain aspects are 'Unable to be determined based on the
provided image.'
3. Disclaimer: Accompany your analysis with the disclaimer: "Consult with a Doctor before making any decisions."

4. Your insights are invaluable in guiding clinical decisions. Please proceed with the analysis, adhering to the structured approach outlined above

Please provide me an output response with these 4 headings Detailed Analysis, Findings Reports, Reccomendations and Next Steps, Treatment Suggestions
"""

#model configuration 
model = genai.GenerativeModel(
  model_name="gemini-pro-vision",
  generation_config=generation_config)
  #saftey_settings=saftey_settings


#set the page configuration 

st.set_page_config(page_title="VitalImage Analytics", page_icon=":robot:")

#set the logo [can do this later] 

#set the title 

st.title("👩‍⚕️ Vital❤️Image📷 Analytics📊 🩺")

#set the subtitle

st.subheader("An application that can help users to identify medical images")
uploaded_file = st.file_uploader("Upload the medical image for analysis", type=["png", "jpg","jpeg"])

if uploaded_file:
    st.image(uploaded_file, width=300, caption="Uploaded Medical Image")

submit_button = st.button("Generate the Analysis")

if submit_button:
    #process the uploaded image
    iamge_data=uploaded_file.getvalue()

    #making our image ready 
    image_parts = [
        {
            "mime_type": "image/jpeg", 
            "data": Path("image0.jpeg").read_bytes() 
        }
    ]

    # making our prompt ready
    prompt_parts = [
        image_part[0], 
        system_prompt, 
    ]

     #Generate a response based on prompt and image
     
    st.title("Here is the analysis based on your image")
    response = model.generate_content(prompt_parts)

    st.write(response.text)

