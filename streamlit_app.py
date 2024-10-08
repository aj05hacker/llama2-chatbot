import streamlit as st
import os
import requests

# App Configuration
st.set_page_config(
    page_title="🦙💬 Llama Chatbot",
    layout="wide",
    initial_sidebar_state="expanded",
    menu_items={
        'About': "## Llama Chatbot\nCreated by Abdul Hajees.\n[Learn more](https://abdulhajees.in/)"
    }
)

# Custom CSS Styling
st.markdown(
    """
    <style>
    /* Sidebar Styling */
    .sidebar .sidebar-content {
        padding: 20px;
    }
    .sidebar .sidebar-content h2 {
        font-size: 18px;
        margin-bottom: 10px;
    }
    .sidebar .sidebar-content .socials a img {
        width: 30px;
        margin-right: 10px;
    }
    
    /* Chat Interface Styling */
    .css-1aumxhk {
        background-color: #f4f4f4;
    }
    .st-chat-message.user .st-chat-message-content {
        background-color: #DCF8C6;
        border-radius: 10px;
    }
    .st-chat-message.assistant .st-chat-message-content {
        background-color: #F1F0F0;
        border-radius: 10px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

# Sidebar for Hugging Face Credentials and User Details
with st.sidebar:
    st.title('ajees Llama Chatbot')
    st.write('This chatbot is created using the open-source Llama 2 LLM model from Meta.')

    # API Key Input or Secrets
    if 'HUGGINGFACE_API_TOKEN' in st.secrets:
        hf_api_token = st.secrets['HUGGINGFACE_API_TOKEN']
        st.success('Hugging Face API key already provided!', icon='✅')
    else:
        hf_api_token = st.text_input('Enter Hugging Face API token:', type='password')
        if hf_api_token:
            if hf_api_token.startswith('hf_') and len(hf_api_token) == 51:
                st.success('API key set!', icon='✅')
            else:
                st.warning('Invalid API key format!', icon='⚠️')

    # Set environment variable
    os.environ['HUGGINGFACE_API_TOKEN'] = hf_api_token

    # Validate API Key
    if not hf_api_token or not (hf_api_token.startswith('hf_') and len(hf_api_token) == 51):
        st.error("Please provide a valid Hugging Face API token to use the chatbot.", icon="🚫")
        st.stop()  # Stops the app from running further

    # Model Selection and Parameters
    st.subheader('Models and Parameters')
    selected_model = st.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        model_id = 'meta-llama/Llama-3.2-1B'  # Replace with your specific model ID
    elif selected_model == 'Llama2-13B':
        model_id = 'meta-llama/Llama-3.2-13B'  # Replace with your specific model ID

    temperature = st.slider('Temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    top_p = st.slider('Top P', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.slider('Max Length', min_value=20, max_value=80, value=50, step=5)

    # Social Media Links
    st.subheader('Connect with Me')
    st.markdown("""
        <div style="display: flex; gap: 15px;">
            <a href="https://www.linkedin.com/in/abdulhajees/" target="_blank">
                <img src="https://img.icons8.com/fluent/48/000000/linkedin.png" alt="LinkedIn" />
            </a>
            <a href="https://github.com/aj05hacker" target="_blank">
                <img src="https://img.icons8.com/fluent/48/000000/github.png" alt="GitHub" />
            </a>
            <a href="https://instagram.com/abdul_hajees" target="_blank">
                <img src="https://img.icons8.com/fluent/48/000000/instagram-new.png" alt="Instagram" />
            </a>
            <a href="https://blogs.abdulhajees.in" target="_blank">
                <img src="https://img.icons8.com/fluent/48/000000/blog.png" alt="Blog" />
            </a>
        </div>
    """, unsafe_allow_html=True)

    st.markdown('📖 Learn how to build this app in this [blog](https://abdulhajees.in/)!')

# Initialize chat history if not already present
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Function for generating LLaMA2 response using Hugging Face Inference API
def generate_llama2_response(prompt_input):
    headers = {
        "Authorization": f"Bearer {os.environ.get('HUGGINGFACE_API_TOKEN')}",
        "Content-Type": "application/json"
    }
    api_url = f"https://api-inference.huggingface.co/models/{model_id}"
    payload = {
        "inputs": prompt_input,
        "parameters": {
            "temperature": temperature,
            "top_p": top_p,
            "max_new_tokens": max_length,
            "repetition_penalty": 1.0
        }
    }
    try:
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raises HTTPError for bad responses
        result = response.json()
        # Handle different response formats
        if isinstance(result, list) and 'generated_text' in result[0]:
            return result[0]['generated_text']
        elif 'error' in result:
            st.error(f"Error from model: {result['error']}")
            return "Sorry, I couldn't process your request."
        else:
            return "Sorry, I couldn't process your request."
    except requests.exceptions.RequestException as e:
        st.error(f"API request failed: {e}")
        return "Sorry, I couldn't process your request."

# Chat Interface
st.title("🦙💬 Chat with Llama!")

# User Input Handling
prompt = st.text_input("Type your message here...", key="input_prompt")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate a new response if the last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_llama2_response(prompt)
                full_response = response.strip()
                st.write(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)

# Display Chat History
if st.session_state.messages:
    st.write("### Chat History")
    for message in st.session_state.messages:
        if message["role"] == "assistant":
            st.markdown(f"**Assistant:** {message['content']}")
        else:
            st.markdown(f"**User:** {message['content']}")

# Clear Chat History Button
if st.button('Clear Chat History'):
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]
