from dotenv import load_dotenv
import os
from smolagents import HfApiModel, CodeAgent, ToolCallingAgent
import markdown

# from tools.markdown_editor import MarkdownTool
# from retriever import RetrieverTool

# from tools.retrieve_markdown_processor import UnstructuredMarkdownProcessor

load_dotenv()

# knowledge_base = datasets.load_dataset("m-ric/huggingface_doc", split="train")
# knowledge_base = knowledge_base.filter(
#     lambda row: row["source"].startswith("huggingface/transformers")
# )


# source_docs = [
#     Document(page_content=doc["text"], metadata={"source": doc["source"].split("/")[1]})
#     for doc in knowledge_base
# ]

# text_splitter = RecursiveCharacterTextSplitter(
#     chunk_size=500,
#     chunk_overlap=50,
#     add_start_index=True,
#     strip_whitespace=True,
#     separators=["\n\n", "\n", ".", " ", ""],
# )
# docs_processed = text_splitter.split_documents(source_docs)

# markdown_tool = MarkdownTool(knowledge_base="knowledge_base")

# processor = UnstructuredMarkdownProcessor(input_path="knowledge_base")
# documents = processor.process_documents(
#     split_docs=True, chunk_size=1000, chunk_overlap=200
# )
# retriever_tool = RetrieverTool(docs=documents)


# model_id = "mistralai/Mistral-7B-Instruct-v0.2"

# Shared story memory (could be a list, database, or vector store)

# read markdown file


def read_markdown_file(file_path):
    with open(file_path, "r") as file:
        content = file.read()
    return content


villain_bg = read_markdown_file("stories/fake/villain.md")
character0_bg = read_markdown_file("stories/fake/kera.md")
character1_bg = read_markdown_file("stories/fake/amon.md")

# Function to summarize or retrieve context
# def get_context():
#     # Summarize or select last N turns
#     return summarize(story_history[-10:])


model_id = "Qwen/Qwen2.5-Coder-32B-Instruct"

# markdown_agent = CodeAgent(
#     name="markdown_agent",
#     description="Incorporate existing content markdown content (if any) to the new content and write to the correct markdown file or create a new file",
#     tools=[markdown_tool],
#     model=HfApiModel(
#         model_id=model_id,
#         token=os.getenv("HF_TOKEN"),
#         timeout=300,
#         temperature=0.5,
#     ),
#     max_steps=4,
#     verbosity_level=2,
# )

character1 = CodeAgent(
    name="kera",
    description="Incorporate existing content markdown content (if any) to the new content and write to the correct markdown file or create a new file",
    tools=[],
    model=HfApiModel(
        model_id=model_id,
        token=os.getenv("HF_TOKEN"),
        timeout=300,
        temperature=0.5,
    ),
    max_steps=4,
    verbosity_level=2,
)

character2 = CodeAgent(
    name="amon",
    description="Incorporate existing content markdown content (if any) to the new content and write to the correct markdown file or create a new file",
    tools=[],
    model=HfApiModel(
        model_id=model_id,
        token=os.getenv("HF_TOKEN"),
        timeout=300,
        temperature=0.5,
    ),
    max_steps=4,
    verbosity_level=2,
)

villain = CodeAgent(
    name="villain_agent",
    description="Incorporate existing content markdown content (if any) to the new content and write to the correct markdown file or create a new file",
    tools=[],
    model=HfApiModel(
        model_id=model_id,
        token=os.getenv("HF_TOKEN"),
        timeout=300,
        temperature=0.5,
    ),
    max_steps=4,
    verbosity_level=2,
)

# message = "Polar bear have black skin that absorbs UV light to keep them warm"
# update_message = "Polar bear has white fur reflects light, making them blend in with their surroundings"


def get_prompt(story_history, agent_name, agent_background):

    prompt = f"""Write an action or dialogue for the character that is consistent with the existing story and background
        
        Story:
        {story_history}
        Character:
        {agent_name}
        Background:
        {agent_background}
        
        """

    return prompt


def openai(model, prompt):
    # Placeholder for OpenAI API call
    # response = openai.ChatCompletion.create(
    #     model=model,
    #     messages=[{"role": "user", "content": prompt}],
    # )
    # return response.choices[0].message.content
    return "This is a placeholder response from the OpenAI API."


if __name__ == "__main__":

    story_history = []

    turns = 10
    turn = 0

    story_over = False

    agents = [villain, character1, character2]
    agent_background = [villain_bg, character0_bg, character1_bg]

    print("background: ", agent_background)

    if turn == turns:
        story_over = True
    else:
        story_over = False

    while not story_over:
        if (turn % 4) == 0 and turn != 0:
            # player turn
            action = input("Your turn: ")
            story_history.append(action)
        else:
            agent = agents[turn % len(agents)]
            agent_background = agent_background[turn % len(agent_background)]
            # context = get_context()
            action = agent.run(
                get_prompt(story_history, agent.agent_name, agent_background)
            )
            story_history.append(action)

        turn += 1

        print("Story history: ", story_history)
