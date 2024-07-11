import asyncio
from openai import OpenAI
import tiktoken
from .scrapeWebsites import scrape_p_text

models = {
    "gpt-4o",
    "gpt-4o-2024-05-13",
    "gpt-3.5-turbo",
    "gpt-4-turbo-2024-04-09",
    "gpt-4-turbo-preview",
    "gpt-4-0125-preview",
    "gpt-4-1106-preview",
    "gpt-4",
    "gpt-4-0613",
    "gpt-4-0314",
    "gpt-3.5-turbo-0125",
    "gpt-3.5-turbo",
    "gpt-3.5-turbo-1106",
    "gpt-3.5-turbo-instruct",
}

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
    """

    :param context: str:  (Default value = system_message)
    :param query: str:  (Default value = "Hi!")
    :param model: str:  (Default value = "gpt-4o")
    :param context: str:  (Default value = system_message)
    :param query: str:  (Default value = "Hi!")
    :param model: str:  (Default value = "gpt-4o")
    :param context: str:  (Default value = system_message)
    :param query: str:  (Default value = "Hi!")
    :param model: str:  (Default value = "gpt-4o")
    :param context: str:  (Default value = system_message)
    :param query: str:  (Default value = "Hi!")
    :param model: str:  (Default value = "gpt-4o")
    :param context: str:  (Default value = system_message)
    :param query: str:  (Default value = "Hi!")
    :param model: str:  (Default value = "gpt-4o")
    :param context: str:  (Default value = system_message)
    :param query: str:  (Default value = "Hi!")
    :param model: str:  (Default value = "gpt-4o")
    :param context: str:  (Default value = system_message)
    :param query: str:  (Default value = "Hi!")
    :param model: str:  (Default value = "gpt-4o")
    :param context: str:  (Default value = system_message)
    :param query: str:  (Default value = "Hi!")
    :param model: str:  (Default value = "gpt-4o")

    """
    if model not in models:
        return f"Invalid model. Please run the prompting help command to find the right model to use."
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
    
    
# def perform_facebook_query(context: str = system_message, query: str = "Hi!", model: str = ) -> str:


async def createQOTW(websites: str, model: str = "gpt-4o") -> str:
    if model not in models:
        return f"Invalid model. Please run the prompting help command to find the right model to use."
    try:
        client = OpenAI(api_key=API_KEY)
        website_list = [
            website.strip().replace('"', "") for website in websites.split(",")
        ]
        data = "\n".join(
            [
                f"Website Source: {website} \n {await scrape_p_text(website)}"
                for website in website_list
            ]
        )
        context = f"""
        You job is the generate a nonbiased question of the week for the discord server.
        The question should be engaging and thought-provoking, and related to AI's impact on the field beind discussed. 
        Provide sufficient information from the article to ensure the question can be understood with no previous knowledge of the topic or figures involved by an audience of NYC High School students :).
    
        
        Here are a few examples:
         - hello @everyone! Recent developments in the robotics industry (Boston Dynamics' All New Atlas and OpenAI's Figure 1) have been creating concerns of a replacement robotic work force. Morals aside, what areas of work would you think the combination of the physical capabilities of robots and the "mental" capabilties of AI excel in?
bonus business question, have you noticed any problems with how current robotics companies are approaching mundane task completion?
         - Hello @everyone! Just recently, both the UK and US signed a landmark agreement to collaborate on developing rigorous testing for advanced AI systems, representing a major step forward in ensuring their safe deployments. Do you agree with government intervention regarding the prototyping of AI? What industries do you think will be affected the most by this pact?
         - hello @everyone! There is a lot of tension occurring within the field of comptuer science, especially with devin, the first "AI software engineer". Nvidia CEO Jensen Huang believes that "English will be the new primary coding language" while others disagree, saying that if calculators never replaced mathematicians,  why would AI replace software engineers? What are your thoughts on this? Do you beleive that the tides of CS will shift towards AI or remain in the hands of humans?
         - hello @everyone! As AI permeates into creative industries, the art of video game storytelling in regards to AI has been a topic of heated debate. What video game genres do you think developer AI would excel in? Story games? Puzzle platformers? Shooters?
         - hello @everyone! As more people join in on the AI bandwagon, who are the figures within the AI field that you look up to or admire?
        
        Here is the context to generate the question:
        {data}
        """
        message = "What is the question of the week?"

        if get_number_of_tokens(message + context) < openAI_max_context[model]:
            completion = client.chat.completions.create(
                model=model,
                messages=[
                    {"role": "system", "content": context},
                    {"role": "user", "content": message},
                ],
            )
            return f"""{completion.choices[0].message.content}"""
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


async def main():
    response = await createQOTW(
        "https://www.bbc.com/news/articles/cp08y5p52e2o, https://www.bbc.com/news/articles/cldyeykzp33o"
    )
    return response


if __name__ == "__main__":
    response = asyncio.run(main())
    print(response)
