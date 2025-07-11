import os
from llama_cpp import Llama

BASE_DIR  = os.path.dirname(os.path.dirname(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "models","alpacacielo2-7b-8k.Q3_K_L.gguf")
LIB_PATH   = os.path.join(BASE_DIR, "llama.cpp", "build", "bin", "Release", "llama.dll") 


llm = Llama(model_path=MODEL_PATH, lib_path=LIB_PATH, n_ctx=2048, n_threads=8)


def ai_complete(prompt: str, max_tokens: int = 40, temperature: float = 0.2) -> str:
    out = llm(prompt, max_tokens=max_tokens, temperature=temperature)
    return out["choices"][0]["text"].strip()
