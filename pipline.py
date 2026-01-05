def clean_input(text):
    return text.lower().strip()

def route(text):
    if "refund" in text or "charged" in text:
        return "billing"
    return "general"

text = "I was charged twice"
cleaned = clean_input(text)
category = route(cleaned)

print(category)
