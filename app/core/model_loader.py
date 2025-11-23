from transformers import AutoTokenizer, AutoModelForCausalLM, GenerationConfig, pipeline, TextStreamer
import torch
from fastapi import HTTPException
import boto3
import os


llama_tokenizer, llama_model = None, None

def download_from_s3():
    region_name = os.environ['AWS_REGION']
    s3 = boto3.client('s3', region_name=region_name)
    bucket_name = os.environ['S3_BUCKET_NAME']
    s3_prefix = os.environ['S3_PREFIX']

    # Example: Download a tokenizer file
    local_path = os.environ['MODEL_PATH']

    # List objects with the specified prefix
    paginator = s3.get_paginator('list_objects_v2')
    pages = paginator.paginate(Bucket=bucket_name, Prefix=s3_prefix)

    for page in pages:
        if 'Contents' in page:
            for obj in page['Contents']:
                s3_object_key = obj['Key']
                # Construct local file path, preserving directory structure
                relative_path = os.path.relpath(s3_object_key, s3_prefix)
                local_file_path = os.path.join(local_path, relative_path)

                # Create subdirectories if necessary
                os.makedirs(os.path.dirname(local_file_path), exist_ok=True)

                print(f"Downloading {s3_object_key} to {local_file_path}")
                s3.download_file(bucket_name, s3_object_key, local_file_path)
    
    print("Download from s3 complete.")



# --- 4. Model Loading and Generation (Simulated) ---

def load_ai_model(model_path):
    """
    Loads AI Model    
    """
    global llama_tokenizer, llama_model    

    # --- AI Model (for PLS Generation) ---
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
        print(f"FATAL: Could not load  tokenizer. Error: {e}")
        llama_tokenizer = None
        llama_model = None


def generate_pls_from_model(abstract: str, prompt_template: str) -> str:
    """
    Uses the loaded model to generate the PLS text.
    """
    pls_text = ""
    DEVICE = "cuda" if torch.cuda.is_available() else "cpu"

    if llama_model is None or llama_tokenizer is None:
        print("model or tokenizer not loaded.")
        raise HTTPException(status_code=500, detail="Model or tokenizer not loaded.")
   
    # 1. Create the Llama 3 Instruct chat message format
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
        min_new_tokens=500,    
        max_new_tokens=900,
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
    

