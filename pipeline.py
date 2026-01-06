import os
import json
import logging
import uuid
from datetime import datetime



threshold = float(os.getenv("CONFIDENCE_THRESHOLD", 0.5))
# -----------------------
# LOGGING SETUP
# -----------------------
LOG_FILE = "pipeline.log"

logger = logging.getLogger("pipeline")
logger.setLevel(logging.INFO)

# Avoid duplicate handlers if you run the file multiple times in same session
if not logger.handlers:
    file_handler = logging.FileHandler(LOG_FILE)
    file_handler.setLevel(logging.INFO)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S"
    )
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

# -----------------------
# PIPELINE FUNCTIONS
# -----------------------
def clean_input(text: str) -> str:
    return text.lower().strip()

def route_task(text: str) -> str:
    if "charged" in text or "refund" in text or "invoice" in text:
        return "billing"
    if "error" in text or "crash" in text or "bug" in text:
        return "technical"
    return "unknown"

def model_confidence(task: str) -> float:
    confidence_map = {
        "billing": 0.85,
        "technical": 0.78,
        "unknown": 0.45
    }
    return confidence_map.get(task, 0.40)

def system_check(task: str, confidence: float) -> dict:
    # System safety/decision layer
    if confidence < threshold:
        return {
            "status": "fallback",
            "message": "Need more information to help safely.",
            "category": task,
            "confidence": confidence
        }

    return {
        "status": "ok",
        "category": task,
        "confidence": confidence
    }

# -----------------------
# ONE REQUEST RUN
# -----------------------
def handle_request(user_text: str) -> dict:
    request_id = str(uuid.uuid4())[:8]  # short id for readability

    logger.info(f"[{request_id}] START request")
    logger.info(f"[{request_id}] raw_input={user_text!r}")

    cleaned = clean_input(user_text)
    logger.info(f"[{request_id}] cleaned_input={cleaned!r}")

    task = route_task(cleaned)
    logger.info(f"[{request_id}] routed_task={task}")

    conf = model_confidence(task)
    logger.info(f"[{request_id}] model_confidence={conf}")

    result = system_check(task, conf)
    logger.info(f"[{request_id}] system_result={result}")

    logger.info(f"[{request_id}] END request")
    return result

# -----------------------
# MAIN (RUN)
# -----------------------
if __name__ == "__main__":
    user_text = input("Type a message (example: 'I was charged twice'):\n> ")
    result = handle_request(user_text)

    # Final output to user (clean JSON)
    print(json.dumps(result, indent=2))
    print(f"\n(Log saved to {LOG_FILE})")
