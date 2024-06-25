from openai import OpenAI
import tiktoken

CONTEXT = 128000
MODEL = "gpt-4o"

import dotenv
import os
dotenv.load_dotenv()
API_KEY = os.getenv("GPT_API_KEY")

def perform_gpt_query(query: str) -> str: 
    system_message = """
    You are a bot for a discord server, and you are here to answer queries with flair and kindness. You give honesty, rather than flattery. 
    """
    try:
        client = OpenAI(api_key=API_KEY)
        if get_number_of_tokens(query + system_message) < CONTEXT:
            completion = client.chat.completions.create(
                model=MODEL,
                messages=[
                    {"role": "system", "content": system_message},
                    {"role": "user", "content": query},
                ],
            )
            return f"""{completion.choices[0].message.content}"""
        return "The query is too long. Please try again with a shorter query."
    except Exception as e:
        return f"An error occurred: {e}"

def get_encodings(text: str, model=MODEL) -> list:
    encoding = tiktoken.encoding_for_model(model)
    return encoding.encode(text)


def get_number_of_tokens(text: str, model=MODEL) -> list:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))

if __name__ == "__main__":
    print(perform_gpt_query("What is the purpose of using discord?"))