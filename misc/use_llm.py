#
from llama_cpp import Llama


#
MODEL_CONFIGS: dict[str, dict] = {

    #
    "phi3_mini_instruct": {
        "repo_id": "microsoft/Phi-3-mini-4k-instruct-gguf",
        "filename": "*q4.gguf", # Using q4_0 quantization as suggested by the ollama library page example
        "verbose": False,
        # "n_gpu_layers": -1, # Uncomment to use GPU acceleration
        # "seed": 1337, # Uncomment to set a specific seed
        "n_ctx": 4096, # Uncomment to increase the context window - keeping the original size as a default
    }

}


#
class LLMGenerate:

    #
    def __init__(self, model_type: str = "phi3_mini_instruct") -> None:

        #
        self.llm: Llama = Llama.from_pretrained(**MODEL_CONFIGS[model_type])

        #
        system_prompt: str = "You are a helpful assistant that provides meaningful analysis and useful comments on the given data."

    #
    def generate(self, user_prompt: str) -> str:

        #
        prompt: str = f"<|system|> {system_prompt}<|end|> <|user|> {user_prompt}<|end|> <|assistant|>"

        #
        """
        output: dict{
            "id": str
            "object": str
            "created": int
            "model": str
            "choices": list[dict]
                [0]: dict
                "text": str
                "index": int
                "logprobs": NoneType | dict  # (Likely NoneType in this case)
                "finish_reason": str
                [1]: dict # (If multiple choices were requested)
                ... (same structure as above)
            "usage": dict
                "prompt_tokens": int
                "completion_tokens": int
                "total_tokens": int
        }
        """
        output: dict = llm(
            prompt, # Prompt
            max_tokens=None, # Generate up to the end of the context window unless stop sequences are hit
            stop=["<|end|>", "<|user|>", "<|assistant|>"], # Stop generating based on phi3 defined stops
            echo=False # Set to False to not echo the prompt back in the output
        ) # Generate a completion, can also call create_completion

        #
        output_text: str = ""

        #
        for elt in output.get("choices", []):

            # The output directly contains the assistant's response after the prompt
            output_text += elt["text"]

        #
        return output_text
