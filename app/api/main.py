import uvicorn
from fastapi import FastAPI, HTTPException
from core.model_loader import load_ai_model, generate_pls_from_model
from core.class_model import GenerateRequest, GenerateResponse, ErrorResponse, ReadabilityScores, AllScores
from core.scoring import get_bertscore, get_alignscore, get_cli, get_fre, get_gfi, get_smog, get_fkgl, get_dcrs, initialize_align_scorer
from core.prompt_template import PROMPT_TEMPLATE



# Load model

#model_path = "./model/llama_3_2_3b"
load_ai_model("meta-llama/Llama-3.2-3B-Instruct")

# --- 1. Initialize App and Models ---

app = FastAPI(
    title="BioMedical Text simplification",
    description="An API to generate and evaluate Plain Language Summaries (PLS) from biomedical abstracts.",
)

# Initialize AlignScore model
initialize_align_scorer()
    


# --- 6. API Endpoint ---

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
        
        # Relevance
        bert_f1 = get_bertscore(generated_pls, abstract_text)
        
        # Factuality
        align_score = get_alignscore(generated_pls, abstract_text)
        
        # Readability
        readability_scores = ReadabilityScores(
            CLI=get_cli(generated_pls),
            FRE=get_fre(generated_pls),
            GFI=get_gfi(generated_pls),
            SMOG=get_smog(generated_pls),
            FKGL=get_fkgl(generated_pls),
            DCRS=get_dcrs(generated_pls)
        )
        
        # --- Step 4: Bundle Scores ---
        all_scores = AllScores(
            relevance_bertscore_f1=bert_f1,
            factuality_alignscore=align_score,
            readability=readability_scores
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
    
    uvicorn.run(app, host="127.0.0.1", port=8000, log_level="debug")