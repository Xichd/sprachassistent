from ctransformers import AutoModelForCausalLM
import config

llama = AutoModelForCausalLM.from_pretrained(
    config.MODEL_PATH_LLAMA,
    model_file=config.MODEL_FILE_LLAMA,
    model_type="llama",
    gpu_layers=0  # wichtig für Raspberry Pi
)

def frage_llama(frage):
    print("💭 TinyLLaMA denkt nach...")
    prompt = f"User: {frage}\nAssistant:"
    antwort = llama(prompt, max_new_tokens=100)
    antwort = antwort.strip().split("User:")[0].strip()
    print("🦙 TinyLLaMA sagt:", antwort)
    return antwort

