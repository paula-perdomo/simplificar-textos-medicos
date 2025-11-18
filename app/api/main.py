import uvicorn
import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from core.model_loader import load_ai_model, generate_pls_from_model
from core.class_model import GenerateRequest, GenerateResponse, ErrorResponse, ReadabilityScores, AllScores
from core.scoring import get_scores
from core.prompt_template import PROMPT_TEMPLATE

# Load model

try:
    
    model_name = os.environ['MODEL_NAME']
    model_path = os.environ['MODEL_PATH']
    
except:

    model_name = "Llama 3.2 3B Instruct"
    model_path = "meta-llama/Llama-3.2-3B-Instruct"

load_ai_model(model_path)

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

@app.get("/get_model_name",
         response_model=str, 
          responses={500: {"model": ErrorResponse}})
async def get_model_name():
    return model_name


@app.post("/generate_pls", 
          response_model=GenerateResponse, 
          responses={500: {"model": ErrorResponse}})
async def generate_pls(request: GenerateRequest):
    """
    Generates a Plain Language Summary (PLS) from an abstract and evaluates it.
    """
    try:
        print("Init Generating PLS...")
        
        # --- Step 2: Generate PLS (Simulated) ---
        abstract_text = request.text
        if not abstract_text.strip():
            raise HTTPException(status_code=400, detail="Input text cannot be empty.")
        
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
            detail={"status": "error", "message": f"An internal error occurred: {e}"}
        )


# --- 7. Run the Application ---

if __name__ == "__main__":
    """
    This allows you to run the app directly using `python main.py`
    """
    
    uvicorn.run(app, host="127.0.0.1", port=8000)