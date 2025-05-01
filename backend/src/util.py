import re
import random
from openai import OpenAI
from dotenv import load_dotenv

from backend.src.prompt_template import INIT_STORY, CONTINUE_STORY

# load_dotenv()


def read_markdown_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content


def extract_beats(text: str):
    """
    Extracts all unique beats from a given text.
    Each beat is expected to start with 'Beat <number>:'.

    Args:
        text (str): The input text containing beats.

    Returns:
        list of dict: Each dict contains 'beat_number' and 'description'.
    """
    # Regex pattern to match 'Beat <number>:' and capture the number and description
    pattern = r"Beat (\d+):\s*(.*?)(?=\nBeat \d+:|\Z)"
    matches = re.findall(pattern, text, re.DOTALL)
    # print("matches: ", matches, "\n")

    beats = []
    for number, description in matches:
        # Clean up whitespace and newlines in the description
        clean_description = description.strip().replace("\n", " ")
        beats.append({"beat_number": int(number), "description": clean_description})
    return beats


class StoryGenerator:
    def __init__(self, client: OpenAI):
        self.client = client
        self.response = ""
        self.beats = []

    def init_storyline(self):

        # initialise the storyline

        # run the prompt
        response = self.client.responses.create(
            model="o4-mini-2025-04-16", input=INIT_STORY
        )
        # print(response.output_text)

        # get the output

        return response.output_text

    def reroll_storyline(self, beats: list, action):
        # add the action to the storyline

        # player_beat = {"beat_number": len(beats) + 1, "description": action}
        # beats.append(player_beat)

        response = self.client.responses.create(
            model="o4-mini-2025-04-16", input=CONTINUE_STORY(beats, action)
        )

        return response.output_text

    def run(self):
        # Load the initial storyline
        response = self.init_storyline()

        # log the response
        self.response += response + "\n"

        # Extract beats from the storyline
        beats = extract_beats(response)

        # get up to a certain beat
        n = random.randint(1, len(beats) - 1)

        # print the length of the beats
        print(f"Number of beats: {len(self.beats)}\n")
        # print rng
        print(f"Random number: {n}\n")

        # update beats
        self.beats = beats[:n]

        # write the story
        for i in self.beats:
            print(i["description"] + "\n")

        # update current beat
        current_beat = len(self.beats)
        print(f"Current beat: {current_beat}\n")

        # TODO: add cleanup to the action

        while True:
            action = input("What would you do: ")

            new_storyline = self.reroll_storyline(self.beats, action=action)
            beats = extract_beats(new_storyline)
            # print("beats", beats, "\n")

            n = random.randint(1, len(beats))
            print(f"Random number: {n}\n")
            print(f"Number of beats: {len(beats)}\n")
            print(f"Current beat: {current_beat}\n")

            # print the new beats
            if n > len(beats):
                self.beats + beats

                for i in self.beats[current_beat:]:
                    print(i["description"] + "\n")

                print("End of story")
                break

            else:
                print("Update ran")
                self.beats + beats[:n]
                for i in self.beats[current_beat:]:
                    print(i["description"] + "\n")
                current_beat += len(beats)


if __name__ == "__main__":
    load_dotenv()

    client = OpenAI()

    story_gen = StoryGenerator(client)

    story_gen.run()

    # choose a certain number of beats randomly to determine when the player can take action
