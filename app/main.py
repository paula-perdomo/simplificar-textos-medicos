import uvicorn
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.model_loader import load_ai_model, generate_pls_from_model, download_from_s3
from core.class_model import GenerateRequest, GenerateResponse, AllScores
from core.scoring import get_scores
from core.classifier_model import classify_text, load_classifier_model
from core.prompt_template import PROMPT_TEMPLATE
from core.secret_manager import get_secret
from core.text_cleaning import clean_text
from huggingface_hub import login

# Load model and secrets
model_name = "Llama-3.2-3B-Instruct"
model_path = "meta-llama/Llama-3.2-3B-Instruct"
model_source = os.environ.get('MODEL_SOURCE')

if model_source == 's3':
    print("Downloading model from S3...")
    download_from_s3()
elif model_source == 'huggingface':
    print("Logging in to HuggingFace...")
    hf_token_source = os.environ.get('HF_TOKEN_SOURCE')
    if hf_token_source == 'aws':        
        hf_token =  get_secret('huggingface_token')
        login(token=hf_token)
    elif hf_token_source == 'local':
        login()
    else:
        raise HTTPException(status_code=511, detail="HF_TOKEN source not provided")

if os.environ.get('MODEL_PATH'):
    model_name = os.environ.get('MODEL_NAME')
    model_path = os.environ.get('MODEL_PATH')


load_ai_model(model_path)
load_classifier_model()

# --- 1. Initialize App and Models ---

app = FastAPI(
    title="BioMedical Text simplification",
    description="An API to generate and evaluate Plain Language Summaries (PLS) from biomedical abstracts.",
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],     # Allow requests from any origin
    allow_methods=["*"],     # Allow all HTTP methods (GET, POST, PUT, DELETE, etc.)
    allow_headers=["*"],     # Allow all headers in the request
)

# --- 6. API Endpoint ---

@app.get("/health")
async def health_check():
    return {"status": "ok"}

@app.get("/get_model_name",
         response_model=str)
async def get_model_name():
    return model_name


@app.post("/generate_pls", 
          response_model=GenerateResponse)
async def generate_pls(request: GenerateRequest):
    """
    Generates a Plain Language Summary (PLS) from an abstract and evaluates it.
    """
    try:
        print("Init Generating PLS...")
        abstract_text = request.text
        if not abstract_text.strip():
            raise HTTPException(status_code=400, detail="Input text cannot be empty.")
        
        # --- Step 0: Clean text ---
        abstract_text = clean_text(abstract_text)
        
        # --- Step 1: Classify Text ---
        pred, prob = classify_text(abstract_text)
        print("Text classification: ", pred, " Probability of class 1 (PLS): ", prob)
        if pred == 'PLS':
            raise HTTPException(status_code=422, detail="Input text is PLS already.")

        
        # --- Step 2: Generate PLS (Simulated) ---
        
        
        # Generate PLS
        print("Generating PLS with real Llama 3.2 3B model...")
        generated_pls = generate_pls_from_model(abstract_text, PROMPT_TEMPLATE)
        print("PLS generated successfully.")
        print(f"PLS: {generated_pls}")

        # --- Step 3: Calculate Scores ---
                
        # Readability
        original_scores = get_scores(abstract_text)
        generated_scores = get_scores(generated_pls)
        
        
        # --- Step 4: Bundle Scores ---
        all_scores = AllScores(
            original=original_scores,
            generated=generated_scores
        )

        # --- Step 5: Return Success Response ---
        return GenerateResponse(
            status="ok",
            pls=generated_pls,
            scores=all_scores
        )

    except HTTPException as http_e:
        # Re-raise HTTP exceptions (like 400 bad request)
        raise http_e
    except Exception as e:
        # Catch any other server-side errors
        print(f"An internal server error occurred: {e}")
        # Return a structured error response
        raise HTTPException(
            status_code=500, 
            detail=f"An internal error occurred: {e}"
        )


# --- 7. Run the Application ---

if __name__ == "__main__":
    """
    This allows you to run the app directly using `python main.py`
    """
    
    uvicorn.run(app, host="127.0.0.1", port=8000)