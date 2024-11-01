print("Ждем загрузки всех модулей, никуда не расходимся!")

from src.llama_model_api import Llama_api
from src.vbd_api import Chromadb_api
from src.docx_parse import GOST_parser


db_api = Chromadb_api(
    bd_path="./chromadb/chromadb",
    collection_name="12345"
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


query = ''

if __name__ == "__main__":
    while True:
        query = input("Укажите имя документа для парсина или напишие exit для выхода: ")
        if (query == "exit"):
            break
        else:
            GOST_parser(
                query,
                db_adder=db_api.add_doc,
                llm_request=model_api.llm_request
            )