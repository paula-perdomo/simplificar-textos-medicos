import torch
import json
import os
import torch.nn.functional as F
from transformers import DistilBertTokenizer, DistilBertForSequenceClassification

class PLSClassifier:
    def __init__(self, model_path):
        """
        Carga el modelo, el tokenizador y la configuracion desde la carpeta.
        """
        print(f"Cargando modelo desde {model_path}...")
        
        # 1. Cargar Tokenizer y Modelo
        self.tokenizer = DistilBertTokenizer.from_pretrained(model_path)
        self.model = DistilBertForSequenceClassification.from_pretrained(model_path)
        self.model.eval() # Modo evaluacion (desactiva dropout)
        
        # 2. Cargar Configuracion (Umbral)
        config_path = os.path.join(model_path, "inference_config.json")
        if os.path.exists(config_path):
            with open(config_path, "r") as f:
                config = json.load(f)
                self.threshold = config.get("threshold", 0.5)
                print(f"Configuracion cargada. Umbral de decision: {self.threshold}")
        else:
            self.threshold = 0.98 # Fallback seguro
            print("Advertencia: config no encontrada, usando umbral por defecto 0.98")

    def predict(self, text):
        """
        Recibe un texto y retorna un diccionario con la prediccion.
        """
        # Preprocesamiento
        inputs = self.tokenizer(
            text, 
            return_tensors="pt", 
            truncation=True, 
            padding=True, 
            max_length=256
        )
        
        # Inferencia (Sin gradientes para ahorrar memoria)
        with torch.no_grad():
            outputs = self.model(**inputs)
            # Obtener probabilidades reales
            probs = F.softmax(outputs.logits, dim=1)
            prob_pls = probs[0][1].item()
        
        # Decision basada en el umbral calibrado
        is_pls = prob_pls > self.threshold
        
        return {
            "label": "PLS" if is_pls else "Tecnico",
            "is_pls": bool(is_pls),
            "confidence": prob_pls if is_pls else (1 - prob_pls), # Confianza de la clase elegida
            "pls_probability": prob_pls
        }

# --- EJEMPLO DE USO ---
if __name__ == "__main__":
    # Asumiendo que descomprimiste el zip en esta carpeta
    classifier = PLSClassifier("clasificador_pls_distilbert")
    
    texto_prueba = "This systematic review shows that antibiotics help reduce symptoms."
    resultado = classifier.predict(texto_prueba)
    
    print("-" * 30)
    print(f"Texto: {texto_prueba}")
    print(f"Prediccion: {resultado['label']}")
    print(f"Probabilidad PLS: {resultado['pls_probability']:.4f}")