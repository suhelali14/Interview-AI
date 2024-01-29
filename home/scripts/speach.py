# get a token: https://huggingface.co/docs/api-inference/quicktour#get-your-api-token

from getpass import getpass

from langchain.llms import HuggingFaceHub
from langchain.prompts import PromptTemplate
from langchain.chains import LLMChain

import requests
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate
import os
HUGGINGFACEHUB_API_TOKEN = "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"
repo_id = "meta-llama/Llama-2-7b"
#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
os.environ["HUGGINGFACEHUB_API_TOKEN"] = HUGGINGFACEHUB_API_TOKEN
question = "Who won the FIFA World Cup in the year 1994? "
llm = HuggingFaceHub(
    repo_id=repo_id, model_kwargs={"temperature": 0.5, "max_length": 64}
)

template = """You are interviewing for a software developer position, Your personality, attitude, and language should simulate an interviewer, you have asked following questions please continue interview by asking only one question based on following questions you asked and answers you got ask only one next question if there is no question below start interview by asking first question start interview with introduction if user is answering unapropriate answers or missbehaves then stop the interview and say get out to candidate.

Current conversation:
{history}
Human: {input}
AI Assistant:"""
PROMPT = PromptTemplate(input_variables=["history", "input"], template=template)
conversation = ConversationChain(
    prompt=PROMPT,
    llm=llm,
    verbose=True,
    memory=ConversationBufferMemory(ai_prefix="AI Assistant"),
)
prompt="hello i am suhel can we proced interviewe"


print(str(conversation.predict(input=str(prompt))))

