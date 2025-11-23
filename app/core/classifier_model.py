import torch
import json
import os
import torch.nn.functional as F
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification
from torch.optim import AdamW
from fastapi import HTTPException

claffier_tokenizer, classifier_model, optimizer = None, None, None

device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

def load_classifier_model():
    """
    Loads AI Classification Model    
    """

    global classifier_tokenizer, classifier_model, optimizer

    classifier_tokenizer = DistilBertTokenizer.from_pretrained('./model/pls_classifier')
    classifier_model = DistilBertForSequenceClassification.from_pretrained('./model/pls_classifier')
    classifier_model.to(device)
    classifier_model.eval()
    optimizer = AdamW(classifier_model.parameters(), lr=2e-5)
    print(f"✅ Classifier model loaded. Main device: {classifier_model.device}")


def classify_text(text: str):
    """
    Uses the loaded model to classify if text is PLS or not.
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    config_path = ("./model/pls_classifier/inference_config.json")
    custom_threshold = 0.5 # Default fallback

    if os.path.exists(config_path):
        with open(config_path, "r") as f:
            inference_config = json.load(f)
            custom_threshold = inference_config.get("threshold", 0.5)
            labels_map = inference_config.get("labels", {"0": "Technical", "1": "PLS"})
            print(f"[INFO] Loaded custom threshold: {custom_threshold}")
    else:
        labels_map = {"0": "Technical", "1": "PLS"}
        
    if classifier_model is None or classifier_tokenizer is None:
        print("model or tokenizer not loaded.")
        raise HTTPException(status_code=500, detail="Model or tokenizer not loaded.")

    
    inputs = classifier_tokenizer(
            text, 
            return_tensors="pt", 
            padding=True, 
            truncation=True, 
            max_length=256
        ).to(device)

    with torch.no_grad():
        outputs = classifier_model(**inputs)
        logits = outputs.logits
    
    # Convert logits to probabilities using Softmax
    probs = F.softmax(logits, dim=1)
    
    # Get probability of Class 1 (PLS)
    pls_probability = probs[0][1].item()
    
    # Apply the calibrated threshold
    if pls_probability > custom_threshold:
        predicted_label = labels_map["1"] # PLS
    else:
        predicted_label = labels_map["0"] # Technical / Non-PLS
        
    return predicted_label, pls_probability