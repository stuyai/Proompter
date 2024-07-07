from openai import OpenAI
import tiktoken

CONTEXT = 128000

openAI_max_context = {
    "gpt-4o": 128000,
    "gpt-4o-2024-05-13": 128000,
    "gpt-3.5-turbo": 128000,
    "gpt-4-turbo-2024-04-09": 128000,
    "gpt-4-turbo-preview": 128000,
    "gpt-4-0125-preview": 128000,
    "gpt-4-1106-preview": 128000,
    "gpt-4": 8192,
    "gpt-4-0613": 8192,
    "gpt-4-0314": 8192,
    "gpt-3.5-turbo-0125": 16385,
    "gpt-3.5-turbo": 16385,
    "gpt-3.5-turbo-1106": 16385,
    "gpt-3.5-turbo-instruct": 4096,
}

OpenAI_Input_Million_Token_Cost = {
    "gpt-4o": 5,
    "gpt-4o-2024-05-13": 5,
    "gpt-3.5-turbo": 5,
    "gpt-4-turbo-2024-04-09": 5,
    "gpt-4-turbo-preview": 5,
    "gpt-4-0125-preview": 5,
    "gpt-4-1106-preview": 5,
    "gpt-4": 5,
    "gpt-4-0613": 5,
    "gpt-4-0314": 5,
    "gpt-3.5-turbo-0125": 0.5,
    "gpt-3.5-turbo": 0.5,
    "gpt-3.5-turbo-1106": 0.5,
    "gpt-3.5-turbo-instruct": 1.5,
}

OpenAI_Output_Million_Token_Cost = {
    "gpt-4o": 15,
    "gpt-4o-2024-05-13": 15,
    "gpt-3.5-turbo": 15,
    "gpt-4-turbo-2024-04-09": 15,
    "gpt-4-turbo-preview": 15,
    "gpt-4-0125-preview": 15,
    "gpt-4-1106-preview": 15,
    "gpt-4": 15,
    "gpt-4-0613": 15,
    "gpt-4-0314": 15,
    "gpt-3.5-turbo-0125": 1.5,
    "gpt-3.5-turbo": 1.5,
    "gpt-3.5-turbo-1106": 1.5,
    "gpt-3.5-turbo-instruct": 2,
}

import dotenv
import os

dotenv.load_dotenv()
API_KEY = os.getenv("GPT_API_KEY")
system_message = "You are a bot for a discord server, and you are here to answer queries with flair and kindness. You give honesty, rather than flattery. "


def perform_gpt_query(
    context: str = system_message, query: str = "Hi!", model: str = "gpt-4o"
) -> str:
    try:
        client = OpenAI(api_key=API_KEY)
        if get_number_of_tokens(query + system_message) < openAI_max_context[model]:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": query},
                ],
            )
            return f"""{completion.choices[0].message.content}"""
        return "The query is too long. Please try again with a shorter query."
    except Exception as e:
        print(e)
        return f"An error occurred: {e}"


def get_cost(prompt: str, output: str, model: str) -> int:
    # returns the cost in terms of dollars
    ...


def get_encodings(text: str, model: str = "gpt-4o") -> list:
    encoding = tiktoken.encoding_for_model(model)
    return encoding.encode(text)


def get_number_of_tokens(text: str, model: str = "gpt-4o") -> list:
    encoding = tiktoken.encoding_for_model(model)
    return len(encoding.encode(text))


if __name__ == "__main__":
    print(perform_gpt_query("What is the purpose of using discord?"))
