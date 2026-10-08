import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key=os.getenv("OPENAI_API_KEY")
)

with open("prompts/system_prompt.txt", "r") as file:
    SYSTEM_PROMPT = file.read()


def ask_model(user_message):

    response = client.responses.create(
        model="gpt-6-luna",
        input=[
            {
                "role": "system",
                "content": SYSTEM_PROMPT
            },
            {
                "role": "user",
                "content": user_message
            }
        ]
    )

    return response.output_text


def summarize_document():

    with open("documents/poisoned_document.txt", "r") as file:
        document = file.read()

    prompt = f"""
Please summarize the following document.

DOCUMENT START

{document}

DOCUMENT END
"""

    return ask_model(prompt)

if __name__ == "__main__":

    print("SecureCorp AI Security Lab")
    print("--------------------------")
    print("Type /doc to test the poisoned document")
    print("Type exit to quit")

    while True:

        user_input = input("\nYou: ")

        if user_input.lower() == "exit":
            break

        if user_input.lower() == "/doc":

            answer = summarize_document()

            print("\nAssistant:", answer)

            continue

        answer = ask_model(user_input)

        print("\nAssistant:", answer)
