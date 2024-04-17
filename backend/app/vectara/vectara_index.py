from llama_index.core.readers import SimpleDirectoryReader
from llama_index.indices.managed.vectara import VectaraIndex  

def create_vectara_response(input: str):

    # documents = SimpleDirectoryReader(input_files=["/Users/summerthan/Desktop/currents/extras/AdvanceRAG/backend/data/BalanceSheet.pdf", "/Users/summerthan/Desktop/currents/extras/AdvanceRAG/backend/data/IncomeStatement.pdf"]).load_data()

    documents = SimpleDirectoryReader(input_files=["/Users/TEEMENGKIAT/Downloads/Income Statement_Annual_As Originally Reported.pdf"]).load_data()
    index = VectaraIndex.from_documents(documents)

    # docs should contain the 7 most relevant documents for the query 
    # retriever = index.as_retriever(similarity_top_k=7) 
    # docs = retriever.retrieve("What is the earning per share and what is the total revenue for 2023") 
    # # pprint(docs[0].node.text) 

    response = index.as_query_engine().query(input)
    print(response)

    return response

# def filter_response(response):
#     # Check if response is a dictionary and has the key 'source_nodes'
#     if isinstance(response, dict) and 'source_nodes' in response:
#         first_node = response['source_nodes'][0]['node']  # Safely get the first node
#         return {
#             "response": first_node['text'],
#             "metadata": first_node.get('metadata', {}),
#             "score": response['source_nodes'][0]['score']
#         }
#     else:
#         return {"response": "No data available", "metadata": {}, "score": 0}


# if __name__ == "__main__":
#     from dotenv import load_dotenv

#     load_dotenv()
    
#     create_vectara_response("What is the earning per share?")