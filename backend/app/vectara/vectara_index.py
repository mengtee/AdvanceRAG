from llama_index.core.readers import SimpleDirectoryReader
from llama_index.indices.managed.vectara import VectaraIndex  
import os

file_path_global = None

def index_file(file_path):
    global file_path_global
    try:
        file_path_global = file_path
        print(f"The global file path: {file_path_global}")
        print(f"Successfully run the index_file function {file_path}")
        return file_path  # Assuming the result is a dictionary with a success key
    except Exception as e:
        print(f"Error indexing file: {e}")
        return False

def create_vectara_response(input: str):
    global file_path_global

    print(file_path_global)
    documents = SimpleDirectoryReader(input_files=[file_path_global]).load_data()
    index = VectaraIndex.from_documents(documents)

    response = index.as_query_engine().query(input)
    print(response)

    return response
    # try:
    #     if file_path_global is None or not os.path.isfile(file_path_global):
    #         raise ValueError("File does not exist")

    #     print(f"calling file path from create_vectara_response: {file_path_global}")
    #     documents = SimpleDirectoryReader(input_files=[file_path_global]).load_data()
    #     index = VectaraIndex.from_documents(documents)

    #     response = index.as_query_engine().query(input_str)
    #     print(response)
    #     return response

    # except Exception as e:
    #     print(f"Error in create_vectara_response: {e}")
    #     return False
