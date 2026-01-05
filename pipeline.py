# Day 139 – System decision layer

def clean_input(text):
    return text.lower().strip()

def route(text):
    if "refund" in text or "charged" in text:
        return "billing"
    if "error" in text or "crash" in text:
        return "technical"
    return "general"

def model_confidence(category):
    confidence_map = {
        "billing": 0.85,
        "technical": 0.78,
        "general": 0.50
    }
    return confidence_map.get(category, 0.40)

def system_decision(category, confidence):
    if confidence < 0.6:
        return {
            "status": "fallback",
            "message": "Please provide more details"
        }

    return {
        "status": "ok",
        "category": category,
        "confidence": confidence
    }

# ---- RUN PIPELINE ----
text = "I was charged twice this month"

cleaned = clean_input(text)
category = route(cleaned)
confidence = model_confidence(category)
result = system_decision(category, confidence)

print(result)
