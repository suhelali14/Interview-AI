import requests
import json
from django.shortcuts import render,HttpResponse,redirect,HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import get_user
from home.models import Conversation
from django.urls import reverse
from google.cloud import texttospeech
import os
# Replace these with actual values
YOUR_SITE_URL = "https://your-site-url.com"
YOUR_APP_NAME = "YourAppName"
API_KEY = "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"  # Replace with your actual API key
MODEL_NAME = "mistralai/mistral-7b-instruct"  # The chat model you want to use

# Initialize an empty chat template and an instructions variable
chat_template = []
instructions = """You are interviewing for a software developer position, Your personality, attitude, and language should simulate an interviewer, start taking interview systmatically first ask user to introduce after start asking question,you have asked following questions please continue interview by asking only one question based on following questions you asked and answers you got ask only one next question if there is no question below start interview by asking first question to introduce himself,start interview with introduction if user is answering unapropriate answers or missbehaves then stop the interview and say get out to candidate.and try to ask question and please do not repeate the questions."""

def clear_chat_history():
    # Clear the chat history while retaining instructions
    global chat_template
    chat_template = []
    
def function(request,prompt):
    
    if len(chat_template)<5:
        
        # Ask the user for input
        user_input = prompt

        # Append the user's message to the chat template
        if 'quit' in prompt:
            return redirect('newchat')
        else:
            chat_template.append({"role": "user", "content": user_input})



            # Add any instructions to the instructions variable (won't be summarized)
            # For example, if you have instructions in a text file, you can read and append them here.
            # instructions = "Some instructions for the user."

            # Summarize the conversation so far
            conversation_summary = "\n".join(msg["content"] for msg in chat_template)

            # Send the conversation summary as a prompt to the chatbot along with instructions
            response = requests.post(
                url="https://openrouter.ai/api/v1/chat/completions",
                headers={
                    "HTTP-Referer": YOUR_SITE_URL,
                    "X-Title": YOUR_APP_NAME,
                    "Authorization": f"Bearer {API_KEY}"
                },
                json={
                    "model": MODEL_NAME,
                    "messages": [
                        {"role": "user", "content": instructions},  # Include instructions
                        {"role": "user", "content": conversation_summary}  # Include summarized conversation
                    ]
                }
            )

            # Check if the request was successful
            if response.status_code == 200:
                data = json.loads(response.content)
                # Extract the AI's response text
                ai_response = data['choices'][0]['message']['content']
                print(f"AI: {ai_response}")
                # Append the AI's message to the chat template
                chat_template.append({"role": "assistant", "content": ai_response})
                #text to speach 
                os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "E:\\nexus_hackathon\\nexus\\home\\scripts\\key.json"
                

                # Create a Text-to-Speech client
                client = texttospeech.TextToSpeechClient()

                # Text input
                text = ai_response

                # Configure the voice and parameters
                input_text = texttospeech.SynthesisInput(text=text)
                voice = texttospeech.VoiceSelectionParams(
                    language_code="en-US", name="en-US-Wavenet-D",
                )
                audio_config = texttospeech.AudioConfig(
                    audio_encoding=texttospeech.AudioEncoding.LINEAR16
                )

                # Generate the audio
                response = client.synthesize_speech(
                    input=input_text, voice=voice, audio_config=audio_config
                )

                # Save the audio to a file
                with open("./static/audio/output.mp3", "wb") as out_file:
                    out_file.write(response.audio_content)
                            
                return str(ai_response)

            else:
                # Print an error message if the request was not successful
                print(f"Request failed with status code: {response.status_code}")
                print(response.text)

            if user_input.lower() == "clear chat":
                clear_chat_history()
                print("Chat history cleared.")
                    # Skip the rest of the loop    
    elif len(chat_template)==5:
        #if you will give feedback then conlude the interview and rate the user answers
       
        ai_response = "please can you conlude this interview and tell why are you eligible to this role"
        print(f"AI: {ai_response}")
        # Append the AI's message to the chat template
        chat_template.append({"role": "assistant", "content": ai_response})
        user = get_user(request)
        conversation = Conversation(user=user)
        conversation.save()
        conversation.chat_data = json.dumps(chat_template)
        conversation.save()
        return ai_response
    else:
        #if you will give feedback then conlude the interview and rate the user answers

        prompt="""1.give me the feedback of my interview conversation only give positive points 
        2.give me the feedback of my interview conversation analyze give my negative points
        3.give me the feedback of my interview conversation analyze give me rating and one line review on my interview performance
        please give this 3 points in proper structured manner and seprate them with number
        """
        user_input = prompt
        chat_template.append({"role": "user", "content": user_input})


        # Add any instructions to the instructions variable (won't be summarized)
        # For example, if you have instructions in a text file, you can read and append them here.
        # instructions = "Some instructions for the user."

        # Summarize the conversation so far
        conversation_summary = "\n".join(msg["content"] for msg in chat_template)

        # Send the conversation summary as a prompt to the chatbot along with instructions
        response = requests.post(
            url="https://openrouter.ai/api/v1/chat/completions",
            headers={
                "HTTP-Referer": YOUR_SITE_URL,
                "X-Title": YOUR_APP_NAME,
                "Authorization": f"Bearer {API_KEY}"
            },
            json={
                "model": MODEL_NAME,
                "messages": [
                    {"role": "user", "content": instructions},  # Include instructions
                    {"role": "user", "content": conversation_summary}  # Include summarized conversation
                ]
            }
        )

        # Check if the request was successful
        if response.status_code == 200:
            data = json.loads(response.content)
            # Extract the AI's response text
            ai_response = data['choices'][0]['message']['content']
            print(f"AI: {ai_response}")
            # Append the AI's message to the chat template
            user = get_user(request)
            chat_template.append({"role": "assistant", "content": ai_response})
            conversation = Conversation(user=user)
            conversation.save()
            conversation.result=ai_response
            conversation.save()
           
            clear_chat_history()
            return 'Thank you for using our Troi Ai you can check your overall feedback and rating from result hitory '
        else:
            # Print an error message if the request was not successful
            print(f"Request failed with status code: {response.status_code}")
            print(response.text)

        if user_input.lower() == "clear chat":
            clear_chat_history()
            print("Chat history cleared.")
                # Skip the rest of the loop
