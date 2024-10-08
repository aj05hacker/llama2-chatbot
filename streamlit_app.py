import streamlit as st
import os
import replicate

# Replicate Credentials
replicate_api = os.environ['REPLICATE_API_TOKEN']

# Models and parameters
selected_model = 'Llama2-7B'
if selected_model == 'Llama2-7B':
    llm = 'a16z-infra/llama7b-v2-chat:4f0a4744c7295c024a1de15e1a63c880d3da035fa1f49bfd344fe076074c8eea'
elif selected_model == 'Llama2-13B':
    llm = 'a16z-infra/llama13b-v2-chat:df7690f1994d94e96ad9d568eac121aecf50684a0b0963b25a41cc40061269e5'

temperature = 0.1
top_p = 0.9
max_length = 50

# Store LLM generated responses
if "messages" not in st.session_state.keys():
    st.session_state.messages = [{"role": "assistant", "content": "How may I assist you today?"}]

# Function for generating LLaMA2 response
def generate_llama2_response(prompt_input):
    string_dialogue = "You are a helpful assistant. You do not respond as 'User' or pretend to be 'User'. You only respond once as 'Assistant'."
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
def handle_user_input(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = generate_llama2_response(prompt)
    full_response = ''
    for item in response:
        full_response += item
    st.session_state.messages.append({"role": "assistant", "content": full_response})

# Run the app
st.set_page_config(page_title="Llama Chatbot")