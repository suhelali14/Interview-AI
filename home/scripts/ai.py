from langchain.llms import OpenAI
import requests
from langchain.chains import ConversationChain
from langchain.memory import ConversationBufferMemory
from langchain.prompts.prompt import PromptTemplate

import os

os.environ['OPENAI_API_KEY']="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"

llm=OpenAI(
           temperature=0
           )

# template="""You are interviewing for a software developer position, Your personality, attitude, and language should simulate an interviewer, you have asked following questions please continue interview by asking only one question based on following questions you asked and answers you got ask only one next question if there is no question below start interview by asking first question
#         current conversation:
#         {history}
#         Human:{input}
#         AI assistant:"""
# PROMPT=PromptTemplate(input_variables=["history","input"],template=template)
# conversation =ConversationChain(
#     prompt=PROMPT,
#     llm=llm,
#     verbose=True,
#     memory=ConversationBufferMemory(ai_prefix="AI assistant"),
# )
# # Now we can override it and set it to "AI Assistant"
# from langchain.prompts.prompt import PromptTemplate
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
def function(prompt):
    if 'quite' in prompt:
        return 'thank you for your time'
    else:
        

        
        print(str(conversation.predict(input=str(prompt))))
        CHUNK_SIZE = 1024
        url = "https://api.elevenlabs.io/v1/text-to-speech/Yko7PKHZNXotIFUBG7I9/stream"

        headers = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": "8826b2137958be68b307bfcc8cbb5e16"
        }

        data = {
        "text": str(conversation.predict(input=str(prompt))),
        "model_id": "eleven_monolingual_v1",
        "voice_settings": {
            "stability": 0.6,
            "similarity_boost": 0.5
        }
        }

        response = requests.post(url, json=data, headers=headers, stream=True)

        with open('static/audio/output.mp3', 'wb') as f:
            for chunk in response.iter_content(chunk_size=CHUNK_SIZE):
                if chunk:
                    f.write(chunk)

        return str(conversation.predict(input=str(prompt))),str(history)
        