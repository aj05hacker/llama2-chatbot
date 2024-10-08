import streamlit as st
import replicate
import os

# App title and configuration
st.set_page_config(page_title="Ajees Llama 2 Chatbot")

# Custom CSS for Sidebar Styling
sidebar_style = """
    <style>
    /* Sidebar container */
    .sidebar .sidebar-content {
        padding: 20px;
    }
    /* Title Styling */
    .sidebar .sidebar-content h1 {
        font-size: 24px;
        color: #4B8BBE;
        margin-bottom: 20px;
    }
    /* API Token Input Styling */
    .sidebar .sidebar-content .api-input {
        margin-bottom: 20px;
    }
    /* Link Styling */
    .sidebar .sidebar-content .blog-link {
        margin-top: 20px;
    }
    </style>
"""

st.markdown(sidebar_style, unsafe_allow_html=True)

# Sidebar content
with st.sidebar:
    st.markdown("<div class='sidebar-content'>", unsafe_allow_html=True)
    
    # Sidebar Title
    st.markdown("<h1>🦙💬 Llama 2 Chatbot</h1>", unsafe_allow_html=True)
    
    # Replicate API Token Input
    st.markdown("<div class='api-input'>", unsafe_allow_html=True)
    if 'REPLICATE_API_TOKEN' in st.secrets:
        st.success('API key already provided!', icon='✅')
        replicate_api = st.secrets['REPLICATE_API_TOKEN']
    else:
        replicate_api = st.text_input('Enter Replicate API token:', type='password')
        if not (replicate_api.startswith('r8_') and len(replicate_api) == 40):
            st.warning('Please enter your credentials!', icon='⚠️')
        else:
            st.success('Proceed to entering your prompt message!', icon='👉')
    st.markdown("</div>", unsafe_allow_html=True)
    
    # Clear Chat History Button
    st.button('Clear Chat History', on_click=lambda: st.session_state.update({"messages": [{"role": "assistant", "content": "How may I assist you today?"}]}))
    
    # Blog Link
    st.markdown("<div class='blog-link'>📖 Learn how to build this app in this [blog](https://blog.streamlit.io/how-to-build-a-llama-2-chatbot/)! </div>", unsafe_allow_html=True)
    
    st.markdown("</div>", unsafe_allow_html=True)

# Set environment variable for Replicate API
os.environ['REPLICATE_API_TOKEN'] = replicate_api

# Initialize chat messages in session state
if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Display chat messages
for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.write(message["content"])

# Function to clear chat history
def clear_chat_history():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# (Note: The clear_chat_history function is now integrated into the sidebar button using a lambda function above)

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate.run(
        'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5', 
        input={
            "prompt": f"{string_dialogue} {prompt_input} Assistant: ",
            "temperature": 0.1, 
            "top_p": 0.9, 
            "max_length": 512, 
            "repetition_penalty": 1
        }
    )
    return output

# User-provided prompt input
if prompt := st.chat_input(disabled=not replicate_api):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

# Generate and display assistant response
if st.session_state.messages[-1]["role"] != "assistant":
    with st.chat_message("assistant"):
        with st.spinner("Thinking..."):
            response = generate_llama2_response(prompt)
            placeholder = st.empty()
            full_response = ''
            for item in response:
                full_response += item
                placeholder.markdown(full_response)
            placeholder.markdown(full_response)
    message = {"role": "assistant", "content": full_response}
    st.session_state.messages.append(message)
