import textstat
from bert_score import score as bert_score_calc
import numpy as np
from sentence_transformers import SentenceTransformer
import torch


# Initialize AlignScore model
# This will download the model weights the first time it's run
sbert_model = None
DEVICE = "cuda" if torch.cuda.is_available() else "cpu"
EMB_MODEL = "sentence-transformers/all-mpnet-base-v2"
EMB_BATCH = 256


def initialize_align_scorer():
    
    global sbert_model
    
    try:
                
        print(f"Loading SentenceTransformer model '{EMB_MODEL}' on {DEVICE}...")
        sbert_model = SentenceTransformer(EMB_MODEL, device=DEVICE)
        sbert_model.max_seq_length = 512
        print(f"SentenceTransformer model loaded successfully.")

    except Exception as e:
        print(f"FATAL: Could not load SentenceTransformer model. Error: {e}")
        sbert_model = None


# --- 5. Scoring Functions ---


def get_bertscore(candidate: str, reference: str) -> float:
    """
    Calculates BERTScore F1 for relevance.
    Compares the generated PLS (candidate) to the original abstract (reference).
    """
    try:
        # Note: Using 'gec' model type for better fluency/grammar check
        P, R, F1 = bert_score_calc(
            [candidate], [reference], lang="en", model_type="allenai/longformer-large-4096-finetuned-triviaqa"
        )
        return F1.mean().item()
    except Exception as e:
        print(f"Error calculating BERTScore: {e}")
        return 0.0


def _encode_texts(texts: list[str], batch_size: int) -> torch.Tensor:
    """Helper to encode texts in batches, using the global model."""
    if sbert_model is None:
        raise RuntimeError("SBERT model is not loaded.")
        
    all_embs = []
    # No tqdm in API
    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]
        b_emb = sbert_model.encode(
            batch, 
            convert_to_tensor=True, 
            show_progress_bar=False,
            device=DEVICE
        )
        b_emb = torch.nn.functional.normalize(b_emb, p=2, dim=1)
        all_embs.append(b_emb)
    
    if not all_embs:
        return torch.empty(0, sbert_model.get_sentence_embedding_dimension()).to(DEVICE)
        
    return torch.cat(all_embs, dim=0)

def compute_pairwise_align(ref_texts: list[str], gen_texts: list[str]) -> np.ndarray:
    """
    Calculates cosine similarity between paired lists of texts.
    Based on the function from the user's notebook.
    """
    if len(ref_texts) != len(gen_texts):
        raise ValueError("refs and gens must have the same length")
    
    refs_emb = _encode_texts(ref_texts, batch_size=EMB_BATCH)
    gens_emb = _encode_texts(gen_texts, batch_size=EMB_BATCH)

    with torch.no_grad():
        cosines = torch.sum(refs_emb * gens_emb, dim=1).clamp(-1.0, 1.0).cpu().numpy()
    return cosines

# --- MODIFIED: `get_alignscore` now uses `compute_pairwise_align` ---
def get_alignscore(pls: str, abstract: str) -> float:
    """
    Calculates "AlignScore" via SentenceTransformer cosine similarity
    based on the notebook's compute_pairwise_align function.
    """
    if sbert_model is None:
        print("Warning: SBERT model not loaded. AlignScore will be 0.")
        return 0.0
        
    try:
        # Based on the notebook's Cell 12:
        # ref_texts = df["reference"] (which was "pls")
        # gen_texts = df["generation"] (which was "non_pls")
        score_array = compute_pairwise_align(
            ref_texts=[pls],       # The PLS
            gen_texts=[abstract]   # The non-PLS/abstract
        )
        return float(score_array[0]) # Get the first (and only) score
    except Exception as e:
        print(f"Error calculating Cosine AlignScore: {e}")
        return 0.0

# --- Readability Functions ---

def get_cli(text: str) -> float:
    """Calculates Coleman-Liau Index."""
    try:
        return textstat.coleman_liau_index(text)
    except Exception as e:
        print(f"Error calculating CLI: {e}")
        return 0.0

def get_fre(text: str) -> float:
    """Calculates Flesch Reading Ease."""
    try:
        return textstat.flesch_reading_ease(text)
    except Exception as e:
        print(f"Error calculating FRE: {e}")
        return 0.0

def get_gfi(text: str) -> float:
    """Calculates Gunning Fog Index."""
    try:
        return textstat.gunning_fog(text)
    except Exception as e:
        print(f"Error calculating GFI: {e}")
        return 0.0

def get_smog(text: str) -> float:
    """Calculates SMOG Index."""
    try:
        # SMOG needs at least 30 sentences. textstat handles this.
        return textstat.smog_index(text)
    except Exception as e:
        print(f"Error calculating SMOG: {e}")
        return 0.0

def get_fkgl(text: str) -> float:
    """Calculates Flesch-Kincaid Grade Level."""
    try:
        return textstat.flesch_kincaid_grade(text)
    except Exception as e:
        print(f"Error calculating FKGL: {e}")
        return 0.0

def get_dcrs(text: str) -> float:
    """Calculates Dale-Chall Readability Score."""
    try:
        return textstat.dale_chall_readability_score(text)
    except Exception as e:
        print(f"Error calculating DCRS: {e}")
        return 0.0