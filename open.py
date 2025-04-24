from dotenv import load_dotenv
import os
from smolagents import HfApiModel, CodeAgent, ToolCallingAgent
import markdown
from openai import OpenAI
import json

load_dotenv()


def read_markdown_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content


villain_bg = read_markdown_file("stories/fake/villain.md")
wesley = read_markdown_file("stories/fake/wesley.md")
timothy = read_markdown_file("stories/fake/timothy.md")
zhuge = read_markdown_file("stories/fake/zhuge.md")


def get_prompt(story_history, agent_name, agent_background):

    prompt = f"""

    You are a character in a story. You will be given a background and a story. Your task is to write an action or dialogue for the character that is consistent with the existing story and background.
        
        Story:
        {story_history}
        Character:
        {agent_name}
        Background:
        {agent_background}
        
    Write two versions of the action or dialogue. 
        
        FORMAT:
        
        {{ "detailed" : "Your detailed and elaborate version of the action or dialogue." }}
        {{ "summarised" : "Your concise and summarised version of the action or dialogue." }}
        
        """

    return prompt


def process_response(response: str):
    # Parse the response to extract detailed and summarised versions
    try:
        # Split the string into two JSON objects
        json_objects = response.strip().split("\n", 1)

        detailed_response = json.loads(json_objects[0])
        summarised_response = json.loads(json_objects[1])

    except Exception as e:
        print(f"Error processing response: {e}")
        detailed_response = ""
        summarised_response = ""

    return detailed_response, summarised_response


def run(prompt):
    # Placeholder for OpenAI API call
    response = client.responses.create(model="o4-mini-2025-04-16", input=prompt)
    # print(response.output_text)
    return response.output_text
    # return response.choices[0].message.content
    # return "This is a placeholder response from the OpenAI API."


client = OpenAI()


if __name__ == "__main__":

    story_history = []
    turns = 10
    turn = 0
    story_over = False

    # agents = [villain, character1, character2]
    agents = ["villain", "wesley", "timothy", "zhuge"]
    agent_background = [villain_bg, wesley, timothy, zhuge]

    test_response = run(get_prompt(story_history, "villain", villain_bg))
    # print("test_response: ", test_response)

    # process the response
    detailed_response, summarised_response = process_response(test_response)
    # print("detailed_response: ", detailed_response)
    # print("summarised_response: ", summarised_response)

    # save summarised version to story history
    story_history.append(summarised_response)
    # print("story_history: ", story_history)

    # append the detailed response to file
    with open("test_response.txt", "a") as file:
        file.write(detailed_response["detailed"] + "\n")

    # append the summarised response to file
    with open("test_response_summarised.txt", "a") as file:
        file.write(summarised_response["summarised"] + "\n")

    # Process the response
    # detailed_response, summarised_response = process_response(test_response)
    # print("detailed_response: ", detailed_response)
    # print("summarised_response: ", summarised_response)

    if turn == turns:
        story_over = True
    else:
        story_over = False

    while not story_over:
        if (turn % 3) == 0 and turn != 0:
            # player turn
            action = input("What would you do: ")

            # save the action to story history
            story_history.append(action)

            print(action + "\n")
            print("\n")

            # save to detailed response to file
            with open("test_response.txt", "a") as file:
                file.write(action + "\n")

            # save to summarised response to file
            with open("test_response_summarised.txt", "a") as file:
                file.write(action + "\n")

        else:
            agent = agents[turn % len(agents)]
            agent_background = agent_background[turn % len(agent_background)]
            # context = get_context()

            response = run(get_prompt(story_history, agents, agent_background))

            # process the response
            detailed_response, summarised_response = process_response(response)

            print(detailed_response["detailed"])

            print("\n")

            # save summarised version to story history
            story_history.append(summarised_response)
            # print("story_history: ", story_history)
            # append the detailed response to file
            with open("test_response.txt", "a") as file:
                file.write(detailed_response["detailed"] + "\n")
            # append the summarised response to file
            with open("test_response_summarised.txt", "a") as file:
                file.write(summarised_response["summarised"] + "\n")

        turn += 1

        # print("Story history: ", story_history)
