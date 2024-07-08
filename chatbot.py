import chainlit as cl
from langchain.callbacks.base import BaseCallbackHandler
from langchain.chains import LLMChain
from langchain.memory import ConversationBufferMemory
from langchain_community.llms import CTransformers
from langchain_core.prompts import PromptTemplate


class StreamHandler(BaseCallbackHandler):
    def __init__(self):
        self.msg = cl.Message(content="")

    async def on_llm_new_token(self, token: str, **kwargs):
        await self.msg.stream_token(token)

    async def on_llm_end(self, response: str, **kwargs):
        await self.msg.send()
        self.msg = cl.Message(content="")


# Load quantized Llama 2
llm = CTransformers(
    model="TheBloke/Llama-2-7B-Chat-GGUF",
    model_file="llama-2-7b-chat.Q2_K.gguf",
    model_type="llama2",
    max_new_tokens=20,
)

template = """
[INST] <<SYS>>
You are a helpful, respectful and honest assistant.
Always provide a concise answer and use the following Context:
{context}
<</SYS>>
User:
{instruction}[/INST]"""

prompt = PromptTemplate(template=template, input_variables=["context", "instruction"])

@cl.on_chat_start
def on_chat_start():
    memory = ConversationBufferMemory(memory_key="context")
    llm_chain = LLMChain(prompt=prompt, llm=llm, verbose=False, memory=memory)
    cl.user_session.set("llm_chain", llm_chain)
    cl.user_session.set("form_state", None)
    cl.user_session.set("user_info", {})


async def handle_form(message, llm_chain):
    form_state = cl.user_session.get("form_state")
    user_info = cl.user_session.get("user_info")

    if form_state == "name":
        user_info["name"] = message.content
        cl.user_session.set("form_state", "phone")
        await cl.Message(content="Please provide your phone number.").send()
    elif form_state == "phone":
        user_info["phone"] = message.content
        cl.user_session.set("form_state", "email")
        await cl.Message(content="Please provide your email address.").send()
    elif form_state == "email":
        user_info["email"] = message.content
        cl.user_session.set("form_state", None)
        await cl.Message(content="Thank you! We will contact you soon.").send()
        # Process the collected information
    else:
        # This should not happen, reset the form state
        cl.user_session.set("form_state", None)

    cl.user_session.set("user_info", user_info)


@cl.on_message
async def on_message(message: cl.Message):
    llm_chain = cl.user_session.get("llm_chain")
    form_state = cl.user_session.get("form_state")

    if form_state:
        await handle_form(message, llm_chain)
    else:
        if "call me" in message.content.lower():
            cl.user_session.set("form_state", "name")
            await cl.Message(content="Sure, I can help with that. May I know your name?").send()
        else:
            await llm_chain.ainvoke(
                message.content,
                config={"callbacks": [cl.AsyncLangchainCallbackHandler(), StreamHandler()]},
            )
