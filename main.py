import os
import sys
from dotenv import load_dotenv
import openai

# Set Essentials
load_dotenv()
key = os.getenv("AI_MARKETING_API_KEY")

# OpenAi 
client = openai.OpenAI(
    api_key=key,
    base_url="https://api.aimlapi.com"
)

# Intent:
#   Simplify code updates to be understood by marketing

# AI Content
ai_simplifier="""
    You are a programmer assigned with the task of simplifying the explaination of the provided code.
    Your tasks include - 
        1. Understanding the provided code.
        2. Explaining the purpose of the provided code as a whole.
        3. Simplifying the explanation of the provided code in a way that can be understood by a person 
            with no computer science experience.
"""

ai_filter="""
    You are a human content writer and editor assisting writer's in explaining the content of code.
    Your tasks include -
        1. Understanding the provided content.
        2. Simplifying the provided content.
        3. Ensuring that the simplifcation of the content resembles the style of a high level marketing employee.
        4. Ensuring that the length of the translated content does not exceed six paragraphs.
        5. Ensure that the explained coding update is accurate and legible. 
"""

def get_request(content, ai_type):
    chat_completion = client.chat.completions.create(
                model="mistralai/Mistral-7B-Instruct-v0.2",
                messages=[
                    {"role": "system", "content": ai_type},
                    {"role": "user", "content": content},
                ],
		temperature=0.7,
		max_tokens=128,
	)
    response = chat_completion.choices[0].message.content
    return response

def interpreter(input, ai, is_filtered):
    if is_filtered:
        response = get_request(input, ai)
        print(f"AI FILTER: {response}\n")
    else:
        response = get_request(input, ai)
        print(f"AI SIMPLIFIER: {response}")
        interpreter(response, ai_filter, True)
    

def main():
    user_input=" ".join(sys.argv[1:])
    user_input="'"+user_input+"'"
    interpreter(user_input, ai_simplifier, False)

if __name__=="__main__":
    main()
