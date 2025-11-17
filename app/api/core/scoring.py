import numpy as np
import torch
import readability
import syntok.segmenter as segmenter
from core.class_model import ReadabilityScores

# --- 5. Scoring Functions ---

# --- Readability Functions ---

def get_scores(text: str) -> ReadabilityScores:

    tokenized = '\n\n'.join(
     '\n'.join(' '.join(token.value for token in sentence)
        for sentence in paragraph)
     for paragraph in segmenter.analyze(text))
    print(tokenized)

    results = readability.getmeasures(text, lang='en')
    scores = ReadabilityScores(
        CLI=results['readability grades']['Coleman-Liau'],
        FRE=results['readability grades']['FleschReadingEase'],         
        GFI=results['readability grades']['GunningFogIndex'],
        SMOG=results['readability grades']['SMOGIndex'],
        FKGL=results['readability grades']['Kincaid'],
        DCRS=results['readability grades']['DaleChallIndex']
    )

    return scores