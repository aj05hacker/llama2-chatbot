import streamlit as st
import os
import replicate
import streamlit.components.v1 as components

# App title
st.set_page_config(page_title="🦙💬 Llama Chatbot")

# Load the HTML file
def load_html():
    with open("index.html", "r") as f:
        html_content = f.read()
    return html_content

# Display the HTML UI
components.html(load_html(), height=100)

# Replicate Credentials
with st.sidebar:
    st.title('ajees Llama 2 Chatbot')
    st.write('This chatbot is created using the open-source Llama 2 LLM model from Meta.')
    replicate_api = st.text_input('Enter Replicate API token:', type='password')
    os.environ['REPLICATE_API_TOKEN'] = replicate_api

    st.subheader('Models')
    selected_model = st.sidebar.selectbox('Choose a Llama2 model', ['Llama2-7B', 'Llama2-13B'], key='selected_model')
    if selected_model == 'Llama2-7B':
        llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
    elif selected_model == 'Llama2-13B':
        llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'
    
    """temperature = st.sidebar.slider('temperature', min_value=0.01, max_value=1.0, value=0.1, step=0.01)
    top_p = st.sidebar.slider('top_p', min_value=0.01, max_value=1.0, value=0.9, step=0.01)
    max_length = st.sidebar.slider('max_length', min_value=20, max_value=80, value=50, step=5)"""
    
    st.markdown('Contact[Me](https://abdulhajees.in/)!')

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    string_dialogue = "You are the synonyms generator, just give the synanyms of the given words by the user."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += "User: " + dict_message["content"] + "\n\n"
        else:
            string_dialogue += "Assistant: " + dict_message["content"] + "\n\n"
    output = replicate.run(llm, 
                           input={"prompt": f"{string_dialogue} {prompt_input} Assistant: ",
                                  "temperature": temperature, "top_p": top_p, "max_length": max_length, "repetition_penalty": 1})
    return output

# Handling User Input
if prompt := st.text_input("Type your message here..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.write(prompt)

    # Generate a new response if the last message is not from assistant
    if st.session_state.messages[-1]["role"] != "assistant":
        with st.chat_message("assistant"):
            with st.spinner("Thinking..."):
                response = generate_llama2_response(prompt)
                full_response = ''
                for item in response:
                    full_response += item
                st.write(full_response)
        message = {"role": "assistant", "content": full_response}
        st.session_state.messages.append(message)
