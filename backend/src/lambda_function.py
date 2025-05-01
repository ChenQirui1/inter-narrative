import logging
import json

from openai import OpenAI
from dotenv import load_dotenv

from prompt_template import INIT_STORY, CONTINUE_STORY
from util import extract_beats

logger = logging.getLogger()
logger.setLevel(logging.INFO)


def lambda_handler(event, context):
    load_dotenv()
    client = OpenAI()

    # Get the length and width parameters from the event object. The
    # runtime converts the event object to a Python dictionary
    story = event["story"]
    action = event["action"]

    if story != "":
        # If the story is not empty, continue the story
        prompt = CONTINUE_STORY(story=story, action=action)
    else:
        # If the story is empty, initialize the story
        prompt = INIT_STORY

    # Run the prompt
    response = client.responses.create(model="o4-mini-2025-04-16", input=prompt)

    # process the response into beats
    beats = extract_beats(response.output_text)

    data = {"response": response.output_text, "beats": beats}

    return json.dumps(data)
