import streamlit as st
import os
import replicate
import json

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
    string_dialogue = "You are a helpful assistant. You do not respond as 'User ' or pretend to be 'User '. You only respond once as 'Assistant'."
    for dict_message in st.session_state.messages:
        if dict_message["role"] == "user":
            string_dialogue += ":User  " + dict_message["content"] + "\n\n"
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

# Render the HTML code
html_code = """
    <html>
        <head>
            <meta charset="UTF-8">
            <meta name="viewport" content="width=device-width, initial-scale=1.0">
            <title>Abdul Hajees Llama Chatbot</title>
            <link rel="stylesheet" href="style.css">
            <style>
                body {
                    font-family: Arial, sans-serif;
                    margin: 0;
                    padding: 0;
                    background-color: #f4f4f4;
                }
                
                header {
                    text-align: center;
                    background-color: #4CAF50;
                    color: white;
                    padding: 20px;
                    border-bottom: 1px solid #ddd;
                }
                
                header h1 {
                    margin: 0;
                }
                
                header p {
                    margin: 5px 0 20px;
                }
                
                aside {
                    background-color: #fff;
                    padding: 20px;
                    position: fixed;
                    left: 0;
                    top: 80px; /* Below the header */
                    width: 200px;
                    height: calc(100% - 80px); /* Full height minus header */
                    overflow-y: auto; /* Scroll if content exceeds */
                    border-right: 1px solid #ddd;
                }
                
                aside h2 {
                    margin-top: 0;
                }
                
                .socials {
                    display: flex;
                    flex-direction: column;
                    gap: 10px; /* Space between icons */
                }
                
                .socials img {
                    width: 30px; /* Adjust icon size */
                }
                
                main {
                    margin-left: 220px; /* To accommodate the sidebar */
                    padding: 20px;
                }
                
                #chat-container {
                    background-color: #fff;
                    border-radius: 5px;
                    padding: 15px;
                    height: 400px; /* Adjust as needed */
                    overflow-y: auto; /* Scroll if content exceeds */
                    box-shadow: 0 0  10px rgba(0, 0, 0, 0.1);
                }
                
                #user-input {
                    width: calc(100% - 80px); /* Adjust width for button */
                    padding: 10px;
                    margin-top: 10px;
                    border: 1px solid #ccc;
                    border-radius: 5px;
                }
                
                #send-button {
                    padding: 10px 20px;
                    background-color: #4CAF50;  
                    color: white;
                    border: none;
                    border-radius: 5px;
                    cursor: pointer;
                }
                
                #send-button:hover {
                    background-color: #45a049;
                }
                
                @media only screen and (max-width: 768px) {
                    aside {
                        width: 100%;
                        height: auto;
                        position: relative;
                        border-right: none;
                    }
                    main {
                        margin-left: 0;
                    }
                }
            </style>
        </head>
        <body>
            <header>
                <h1>Abdul Hajees Llama Chatbot</h1>
                <p>This chatbot provides meanings (synonyms and antonyms) and examples of the word you enter.</p>
            </header>
            
            <aside>
                <h2>Connect with Me</h2>
                <div class="socials">
                    <a href="https://linkedin.com/in/abdulhajees" target="_blank"><img src="https://img.icons8.com/fluent/48/000000/linkedin.png" alt="LinkedIn"/></a>
                    <a href="https://github.com/aj05hacker" target="_blank"><img src="https://img.icons8.com/fluent/48/000000/github.png" alt="GitHub"/></a>
                    <a href="https://instagram.com/abdul_hajees" target="_blank"><img src="https://img.icons8.com/fluent/48/000000/instagram-new.png" alt="Instagram"/></a>
                    <a href="https://blogs.abdulhajees.in" target="_blank"><img src="https://img.icons8.com/fluent/48/000000/blog.png" alt="Blog"/></a>
                </div>
                
                <h2>API Key</h2>
                <input type="text" id="api-key" placeholder="Enter your API Key" />
            </aside>
            
            <main>
                <div id="chat-container">
                    <!-- Chat messages will be displayed here -->
                </div>
                <input type="text" id="user-input" placeholder="Type your message..." />
                <button id="send-button">Send</button>
            </main>
            
            <script>
                const userInput = document.getElementById('user-input');
                const sendButton = document.getElementById('send-button');
                const chatContainer = document.getElementById('chat-container');
                
                sendButton.addEventListener('click', () => {
                    const prompt = userInput.value;
                    userInput.value = '';
                    fetch('/handle_user_input', {
                        method: 'POST',
                        headers: {
                            'Content-Type': 'application/json'
                        },
                        body: JSON.stringify({ prompt: prompt })
                    })
                    .then(response => response.json())
                    .then(data => {
                        const messages = data.messages;
                        chatContainer.innerHTML = '';
                        messages.forEach(message => {
                            const messageElement = document.createElement('p');
                            messageElement.textContent = `${message.role}: ${message.content}`;
                            chatContainer.appendChild(messageElement);
                        });
                    });
                });
            </script>
        </body>
    </html>
"""

# Run the app
st.set_page_config(page_title="Llama Chatbot")
st.markdown(html_code, unsafe_allow_html=True)

# Handle user input
def handle_user_input(prompt):
    st.session_state.messages.append({"role": "user", "content": prompt})
    response = generate_llama2_response(prompt)
    full_response = ''
    for item in response:
        full_response += item
    st.session_state.messages.append({"role": "assistant", "content": full_response})
    return {"messages": st.session_state.messages}

# Create a endpoint to handle user input
def handle_user_input_endpoint():
    prompt = st.session_state.prompt
    return handle_user_input(prompt)

# Run the app
if __name__ == "__main__":
    st.run(handle_user_input_endpoint)