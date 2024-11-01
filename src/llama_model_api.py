from llama_cpp import Llama


class Llama_api():
    def __init__(
        self,
        model_path: str="models/qwen2.5-14b-instruct-q3_k_m-00001-of-00002.gguf",
        model_params: dict={
            "seed": 42,
            "n_ctx": 8000,
            "n_gpu_layers": 12,
            "verbose": False
        }
    ):    
        self.load_llm(model_path, model_params)


    def load_llm(
        self,
        model_path: str="models/qwen2.5-14b-instruct-q3_k_m-00001-of-00002.gguf",
        model_params: dict={
            "seed": 42,
            "n_ctx": 20000,
            "n_gpu_layers": 12,
            "verbose": False
        }
    ) -> None:
        self.llm = Llama(
            model_path,
            **model_params
        )        


    def llm_request(self, prompt: str) -> str:
        if not hasattr(self, 'llm'):
            self.load_llm()
        answer = self.llm.create_chat_completion(
            messages = [{
				"role": "assistant",
				"content": prompt
		    }]
	    )
        return answer['choices'][0]['message']['content']


    def get_model(self) -> Llama:
        """
        Геттер для загруженной модели
        """
        return self.llm