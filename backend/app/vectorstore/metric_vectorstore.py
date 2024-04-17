from llama_index.core.schema import TextNode
from llama_index.core import VectorStoreIndex
from llama_index.core import Settings
from llama_index.embeddings.huggingface import HuggingFaceEmbedding

def retrive_vectara_input(input: str):
    embed_model = HuggingFaceEmbedding(
        model_name="sentence-transformers/all-mpnet-base-v2", max_length=512
    )

    Settings.embed_model = embed_model

    # set text and metrics 
    node1 = TextNode(text="Valuation of a Company", id_="1", metadata={"metric":"What are the Cash, Cash Equivalents and Short Term Investments and Current Debt Long-Term Debt, and Net Income Available to Common Stockholder in TTM?"})
    node2 = TextNode(text="Profit of a Company", id_="2", metadata={"metric":"revenue, spendings, earnings"})
    nodes = [node1, node2]
    index = VectorStoreIndex(nodes)
    retriever = index.as_retriever()

    # retrieve matched nodes
    nodes = retriever.retrieve(input)
    print(nodes)
    return nodes[0].metadata["metric"]