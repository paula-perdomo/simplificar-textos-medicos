from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig, pipeline, TextStreamer
import torch
from fastapi import HTTPException

llama_tokenizer, llama_model = None, None

# --- 4. Model Loading and Generation (Simulated) ---

def load_ai_model(model_path: str = "./model"):
    """
    Loads Llama 3.2 3B Model    
    """
    global llama_tokenizer, llama_model    

    # --- Llama 3.2 3B Model (for PLS Generation) ---
    try:
       
        llama_model = AutoModelForCausalLM.from_pretrained(model_path, 
                                                           return_dict=True,
                                                           low_cpu_mem_usage=True,
                                                           dtype=torch.float16,
                                                           device_map="auto",
                                                           trust_remote_code=True)       
        
        llama_tokenizer = AutoTokenizer.from_pretrained(model_path)
        
        if llama_tokenizer.pad_token_id is None:
            llama_tokenizer.pad_token_id = llama_tokenizer.eos_token_id

        if llama_model.config.pad_token_id is None:
            llama_model.config.pad_token_id = llama_model.config.eos_token_id

        print(f"✅ Model loaded. Main device: {llama_model.device}")

    except Exception as e:
        print(f"FATAL: Could not load Llama 3 tokenizer. Error: {e}")
        llama_tokenizer = None
        llama_model = None

    return llama_tokenizer, llama_model


def generate_pls_from_model(abstract: str, prompt_template: str) -> str:
    """
    Uses the loaded Llama 3model to generate the PLS text.
    """
    pls_text = ""
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    if llama_model is None or llama_tokenizer is None:
        print("model or tokenizer not loaded.")
        raise HTTPException(status_code=500, detail="model or tokenizer not loaded.")
    """
    # 1. Format the full prompt
    full_prompt = prompt_template.format(text=abstract)

    # 3. Tokenize the input
    inputs = llama_tokenizer(full_prompt, return_tensors="pt", padding=True, truncation=True).to(llama_model.device)

    gen_config = GenerationConfig(
        max_new_tokens=1024,
        temperature=0.3,            # salida más determinista
        top_p=0.9,
        do_sample=False,            # greedy decoding (sin sampling)
        eos_token_id=llama_tokenizer.eos_token_id,
        pad_token_id=llama_tokenizer.pad_token_id,
        repetition_penalty=1.8,     # penaliza repeticiones
        no_repeat_ngram_size=4,     # evita repeticiones de frases
    )

    prompt_token_length = inputs["input_ids"].shape[1]

    llama_model.eval()

    with torch.no_grad():
        outputs = llama_model.generate(**inputs, generation_config=gen_config)
        print(outputs.shape)

    new_tokens = outputs[0, prompt_token_length:]
    print(len(new_tokens))

    # Decode the generated part
    generated_text = llama_tokenizer.decode(new_tokens, skip_special_tokens=True)
    """

    # 1. Create the Llama 3 chat message format
    # The prompt template is the "user" message.
    messages = [
        {"role": "system", "content": "You are an expert assistant specialized in creating Plain Language Summaries (PLS) from biomedical texts."},
        {"role": "user", "content": prompt_template.format(text=abstract)}
    ]

    # 2. Tokenize the input using the chat template
    # This is the critical change.
    inputs = llama_tokenizer.apply_chat_template(
        messages,
        add_generation_prompt=True,
        return_tensors="pt"
    ).to(llama_model.device)


    print(f"Data tensor is on: {inputs.device}") # This MUST match the model's device


    gen_config = GenerationConfig(        
        max_new_tokens=100,
        temperature=0.3,
        top_p=0.9,        
        do_sample=False,
        repetition_penalty=1.0,        
        no_repeat_ngram_size=0,

        eos_token_id=llama_tokenizer.eos_token_id,
        pad_token_id=llama_tokenizer.pad_token_id,
    )


    prompt_token_length = inputs.shape[1]
    print(f"Prompt token length: {prompt_token_length}")
    
    llama_model.eval()
    with torch.no_grad():
        # 4. Generate output
        # We pass input_ids and attention_mask from the tokenizer output
        outputs = llama_model.generate(
            input_ids=inputs,
            generation_config=gen_config
        )

    # 5. Decode only the *new* tokens
    new_tokens = outputs[0, prompt_token_length:]

    generated_text = llama_tokenizer.decode(new_tokens, skip_special_tokens=True)
    print(generated_text)

    return generated_text
    

