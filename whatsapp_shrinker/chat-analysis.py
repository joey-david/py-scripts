from llama_cpp import Llama

llm = Llama.from_pretrained(
	repo_id="leafspark/Llama-3-8B-Instruct-Gradient-4194k-GGUF",
	filename="Llama-3-8B-Instruct-Gradient-4194k.Q4_K_M.fixed.gguf",
)

