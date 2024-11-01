print("Ждем загрузки всех модулей, никуда не расходимся!")

from src.llama_model_api import Llama_api
from src.vbd_api import Chromadb_api
from src.chain_of_thoughts import Chain_of_thoughts


db_api = Chromadb_api(
    bd_path="./chromadb/chromadb",
    collection_name="metalloprokat"
)
model_api = Llama_api(
    model_path="models/qwen2.5-14b-instruct-q3_k_m-00001-of-00002.gguf",
    model_params={
        "seed": 42,
        "n_ctx": 8000,
        "n_gpu_layers": 12,
        "verbose": False
    }
)
answer_generator = Chain_of_thoughts(
    query_to_db=db_api.query_to_db,
    llm_request=model_api.llm_request
)


query = ''

if __name__ == "__main__":
    while True:
        query = input("Напишите вопрос по ГОСТ 19281-2014 или ГОСТ 14637-89, либо exit для выхода: ")
        if (query == "exit"):
            break
        else:
            print(answer_generator.start(query))