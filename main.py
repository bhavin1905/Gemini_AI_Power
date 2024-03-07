import streamlit as st
import os 
from streamlit_option_menu import option_menu
from gemini_utility import load_gemini_pro_model
from gemini_utility import gemini_pro_vision_response
from gemini_utility import embeddings_model_response
from gemini_utility import gemini_pro_response
from PIL import Image


working_directory = os.path.dirname(os.path.abspath(__file__))

# page config 

st.set_page_config(
    page_title="Gemini AI Power",
    page_icon="🧊",
    layout="centered",
)

with st.sidebar:
    selected = option_menu("Gemini AI Power",
                        ["chatBot", 
                        "Image Captioning",
                        "Embed Text",
                        "Ask me anything"],
                        menu_icon= "robot", icons=['chat-left-dots','image-fill','cursor-text','chat-square-quote-fill'], 
                    default_index=0
    )   


#fuction to translate role between gemini-pro and streamlit terminology 
def translate_role_for_streamlit(user_model):
    if user_model == "model":
        return "assistant"
    else:
        return user_model

if selected == "chatBot":
    model = load_gemini_pro_model()

    # initialize chat session with streamlit if not already present 

    if "chat_session" not in st.session_state:
        st.session_state.chat_session = model.start_chat(history=[])

    # streamlit page title
    st.title(" 🤖 ChatBot ")

    #display the chat history 
    for message in st.session_state.chat_session.history:
        with st.chat_message(translate_role_for_streamlit(message.role)):
            st.markdown(message.parts[0].text)

    # get user input
    user_prompt = st.chat_input("Ask Gemini Ai Power.... ")

    if user_prompt:
        st.chat_message("user").markdown(user_prompt)

        gemini_response = st.session_state.chat_session.send_message(user_prompt) 

        #display gemini response 
        with st.chat_message("assistant"):
            for part in gemini_response.parts:
                st.markdown(part.text)


if selected == "Image Captioning":
    # streamlit page title
    st.title("🖼️ Image Captioning")
    uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png", "jpeg"])

    if st.button("Generated Caption"):

        image = Image.open(uploaded_file)

        col1, col2 = st.columns(2)

        with col1:
            resized_image = image.resize((800, 500))
            st.image(resized_image)

        default_prompt = "Write a short caption for image"

        #Getting response from gemini pro vision model

        caption = gemini_pro_vision_response(default_prompt, image)

        with col2:
            st.info(caption)

# text embedding model
if selected == "Embed Text":

    st.title("🔡 Embed Text")

    # text box to enter prompt
    user_prompt = st.text_area(label='', placeholder="Enter the text to get embeddings")

    if st.button("Get Response"):
        response = embeddings_model_response(user_prompt)
        st.markdown(response)


# text embedding model
if selected == "Ask me anything":

    st.title("❓ Ask me a question")

    # text box to enter prompt
    user_prompt = st.text_area(label='', placeholder="Ask me anything...")

    if st.button("Get Response"):
        response = gemini_pro_response(user_prompt)
        st.markdown(response)