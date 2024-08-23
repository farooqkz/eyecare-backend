import random

IrisFeatures = list[float]

def detect_diabetes(feats: IrisFeatures) -> bool:
    return random.choice((True, False))
