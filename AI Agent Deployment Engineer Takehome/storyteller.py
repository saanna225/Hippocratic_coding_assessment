from config import (
    TEMPERATURE_OUTLINE,
    TEMPERATURE_STORY,
    MAX_TOKENS_OUTLINE,
    MAX_TOKENS_STORY,
    STORY_MIN_WORDS,
    STORY_MAX_WORDS,
    STORY_REFINEMENT_MAX_WORDS,
)
from prompts.storyteller_prompts import (
    OUTLINE_SYSTEM,
    OUTLINE_USER,
    STORY_SYSTEM,
    STORY_USER,
    REFINEMENT_SYSTEM,
    REFINEMENT_USER
)
from utils import call_model, parse_json_response

OUTLINE_FALLBACK = {
    "act1": "A young child discovers a problem in their world.",
    "act2": "They try to solve it but face challenges along the way.",
    "act3": "With courage and kindness, they solve the problem and learn a lesson."
}


def generate_outline(user_input: str, age_group: str, category: str) -> dict:
    """
    Generate a 3-act story outline.
    Returns dict with act1, act2, act3.
    """
    system = OUTLINE_SYSTEM.format(
        age_group=age_group,
        category=category
    )
    user = OUTLINE_USER.format(user_input=user_input)

    raw = call_model(
        system_prompt=system,
        user_prompt=user,
        temperature=TEMPERATURE_OUTLINE,
        max_tokens=MAX_TOKENS_OUTLINE
    )

    result = parse_json_response(raw, OUTLINE_FALLBACK)

    # validate all three acts exist and are non-empty
    if not all([
        result.get("act1"),
        result.get("act2"),
        result.get("act3")
    ]):
        return OUTLINE_FALLBACK

    return result


def refine_outline(outline: dict, critique: str, age_group: str, category: str) -> dict:
    """
    Refine outline based on judge critique.
    Returns improved outline dict.
    """
    system = OUTLINE_SYSTEM.format(
        age_group=age_group,
        category=category
    )
    user = f"""
The following outline was rejected. Rewrite it addressing this critique:

Critique: {critique}

Current outline:
Act 1: {outline['act1']}
Act 2: {outline['act2']}
Act 3: {outline['act3']}

Return the improved outline in the same JSON format.
"""

    raw = call_model(
        system_prompt=system,
        user_prompt=user,
        temperature=TEMPERATURE_OUTLINE,
        max_tokens=MAX_TOKENS_OUTLINE
    )

    result = parse_json_response(raw, outline)  # fallback to original if parse fails

    if not all([
        result.get("act1"),
        result.get("act2"),
        result.get("act3")
    ]):
        return outline  # return original rather than breaking pipeline

    return result


def generate_story(user_input: str, outline: dict, age_group: str, category: str) -> str:
    """
    Generate full story from approved outline.
    Returns story as plain string.
    """
    system = STORY_SYSTEM.format(
        age_group=age_group,
        act1=outline["act1"],
        act2=outline["act2"],
        act3=outline["act3"],
        story_min_words=STORY_MIN_WORDS,
        story_max_words=STORY_MAX_WORDS,
    )
    user = STORY_USER.format(
        user_input=user_input,
        category=category
    )

    return call_model(
        system_prompt=system,
        user_prompt=user,
        temperature=TEMPERATURE_STORY,
        max_tokens=MAX_TOKENS_STORY
    )


def refine_story(story: str, critique: str, age_group: str) -> str:
    """
    Refine story based on combined judge critique.
    Returns improved story as plain string.
    """
    system = REFINEMENT_SYSTEM.format(
        age_group=age_group,
        story=story,
        critique=critique,
        story_min_words=STORY_MIN_WORDS,
        story_refinement_max_words=STORY_REFINEMENT_MAX_WORDS,
    )
    user = REFINEMENT_USER

    return call_model(
        system_prompt=system,
        user_prompt=user,
        temperature=TEMPERATURE_STORY,
        max_tokens=MAX_TOKENS_STORY
    )