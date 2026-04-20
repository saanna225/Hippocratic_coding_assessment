import os
from dotenv import load_dotenv

load_dotenv()

# Model - do not change as per assignment rules
MODEL = "gpt-3.5-turbo"

# API Key
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Judge threshold
PASS_THRESHOLD = 8

# Max refinement iterations (cost control)
MAX_OUTLINE_ITERATIONS = 2
MAX_STORY_ITERATIONS = 2

# Story length guidance (used in prompts)
STORY_MIN_WORDS = 550
STORY_MAX_WORDS = 750
# Refinement may run slightly longer while fixing critique
STORY_REFINEMENT_MAX_WORDS = 950

# Temperature per use case
TEMPERATURE_CLASSIFIER = 0.1
TEMPERATURE_OUTLINE = 0.7
TEMPERATURE_STORY = 0.8
TEMPERATURE_JUDGE = 0.1

# Token limits
MAX_TOKENS_CLASSIFIER = 100
MAX_TOKENS_OUTLINE = 500
MAX_TOKENS_STORY = 2000
MAX_TOKENS_JUDGE = 800