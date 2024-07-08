# Chainlit Langchain Chatbot
Welcome to the Chainlit Langchain Chatbot project! This chatbot uses Chainlit and Langchain, combined with a quantized Llama 2 model, to provide helpful responses and collect user information when requested.

## Features
- **General Conversation:** Engage in natural language interactions.
 
+ **Conversational Form:** Seamlessly collect user information (name, phone number, email) when a call is requested.

## Requirements
To get started, you'll need:

* Python 3.7 or higher

The following Python libraries:

+ Chainlit

- Langchain

* Langchain-Community

+ Langchain-Core

- CTransformers

## Installation
1. **Clone the Repository:**
```
git clone https://github.com/shailesh00000/my-chatbot.git

cd my-chatbot
```

2. **Set Up a Virtual Environment:**
```
python -m venv venv

source venv/Scripts/activate
```

3. **Install the Required Packages:**
```
pip install -r requirements.txt
```
4. **Download the Model:**

Get the quantized Llama 2 model: **'TheBloke/Llama-2-7B-Chat-GGUF'**

Place the model file **('llama-2-7b-chat.Q2_K.gguf')** in the project directory.

## Usage
To run the chatbot, use the following command:
```
python chatbot.py
```
You can then interact with the chatbot via the console or web interface.
```
chainlit run chatbot.py
```
## Example Interaction
Here's a sample conversation to demonstrate the chatbot's capabilities:

1. **Start the Chat:**

User: "Hello, can you help me with some information?"

Bot: "Of course! What do you need help with?"


2. **Request a Call:**

User: "Can you call me?"

Bot: "Sure, I can help with that. May I know your name?"


3. **Provide Your Name:**

User: "John Doe"

Bot: "Please provide your phone number."


4. **Provide Your Phone Number:**

User: "123-456-7890"

Bot: "Please provide your email address."


5. **Provide Your Email:**

User: "john.doe@example.com"

Bot: "Thank you! We will contact you soon."

## Code Breakdown
**StreamHandler Class:**
This class manages the streaming of tokens and sending messages.

**LLM Setup:**
We load a quantized version of the Llama 2 model to handle the language processing.

**PromptTemplate:**
Defines the structure for prompts, including placeholders for context and user instructions.

**on_chat_start Function:**
Initializes the conversation memory and LLM chain, storing them in the user session.

**handle_form Function:**
Handles the steps of the conversational form, asking for and storing user information.

**on_message Function:**
Check if a form is in progress, either managing the form or processing the message with the LLM chain.


## License
This project is licensed under the MIT License. For more details, see the [LICENSE](https://github.com/shailesh00000/my-chatbot/blob/main/LICENSE) file.

