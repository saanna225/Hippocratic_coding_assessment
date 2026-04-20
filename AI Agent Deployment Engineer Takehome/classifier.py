import json
#import openai
from config import (
    OPENAI_API_KEY,
    TEMPERATURE_CLASSIFIER,
    MAX_TOKENS_CLASSIFIER
)
from prompts.classifier_prompts import CLASSIFIER_SYSTEM, CLASSIFIER_USER
from utils import call_model, parse_json_response

#openai.api_key=OPENAI_API_KEY

CLASSIFIER_FALLBACK = {
    "age_group": "5-7",
    "category": "adventure"
}

VALID_AGE_GROUPS = ["5-7", "8-10"]
VALID_CATEGORIES = ["adventure", "friendship", "bedtime", "fantasy", "animal"]


def classify_input(user_input: str) -> dict:
    system = CLASSIFIER_SYSTEM
    user = CLASSIFIER_USER.format(user_input=user_input)

    raw = call_model(
        system_prompt=system,
        user_prompt=user,
        temperature=TEMPERATURE_CLASSIFIER,
        max_tokens=MAX_TOKENS_CLASSIFIER
    )

    result = parse_json_response(raw, CLASSIFIER_FALLBACK)

    # validate
    if (result.get("age_group") not in VALID_AGE_GROUPS or
            result.get("category") not in VALID_CATEGORIES):
        return CLASSIFIER_FALLBACK

    return result