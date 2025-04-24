from smolagents import Tool
from langchain_community.retrievers import BM25Retriever

# from tools.retrieve_markdown_processor import UnstructuredMarkdownProcessor
from retrieve_markdown_processor import UnstructuredMarkdownProcessor


class RetrieverTool(Tool):
    name = "retriever"
    description = "Uses semantic search to retrieve the most relevant markdown file content and title for the query."
    inputs = {
        "query": {
            "type": "string",
            "description": "The query to perform. This should be semantically close to your target documents. Use the affirmative form rather than a question.",
        }
    }
    output_type = "string"

    def __init__(self, docs, **kwargs):
        super().__init__(**kwargs)
        self.retriever = BM25Retriever.from_documents(docs, k=10)

    def forward(self, query: str) -> str:
        assert isinstance(query, str), "Your search query must be a string"

        docs = self.retriever.invoke(
            query,
        )

        with open(docs[0].metadata["source"], "r") as file:
            retrieved_info = {
                "title": docs[0].metadata["source"],
                "content": file.read(),
            }

            print(retrieved_info)
            return retrieved_info

    def forward_docs(self, query: str) -> str:
        assert isinstance(query, str), "Your search query must be a string"

        docs = self.retriever.invoke(
            query,
        )

        # return docs as a list of dictionaries
        print(docs)
        return docs


if __name__ == "__main__":
    processor = UnstructuredMarkdownProcessor(input_path="knowledge_base")
    documents = processor.process_documents(
        split_docs=True, chunk_size=1000, chunk_overlap=200
    )

    retriever_tool = RetrieverTool(docs=documents)
    query = """Blindman's Bluff: Page From a dispersed
Bhagavata Purana
Time Period: c. 1715--20
Medium: Watercolour and gold on paper
Place of Origin: Mewar, India
Dimensions: 24 x 27.6 cm"""
    result = retriever_tool.forward_docs(query)
