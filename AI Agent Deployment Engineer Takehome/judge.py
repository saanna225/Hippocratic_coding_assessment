from dataclasses import dataclass
from config import (
    TEMPERATURE_JUDGE,
    MAX_TOKENS_JUDGE,
    PASS_THRESHOLD
)
from prompts.judge_prompts import (
    OUTLINE_JUDGE_SYSTEM,
    OUTLINE_JUDGE_USER,
    STORY_JUDGE_SYSTEM,
    STORY_JUDGE_USER
)
from utils import call_model, parse_json_response


@dataclass
class JudgeResult:
    score: float
    passed: bool
    critique: str


# --- Fallbacks ---

OUTLINE_JUDGE_FALLBACK = {
    "reasoning": "Could not parse judgment.",
    "score": 0,
    "passed": False,
    "critique": "Could not evaluate outline. Please regenerate."
}

STORY_JUDGE_FALLBACK = {
    "reasoning": "Could not parse judgment.",
    "age_appropriateness_score": 0,
    "story_structure_score": 0,
    "engagement_score": 0,
    "overall_score": 0,
    "passed": False,
    "critique": "Could not evaluate story. Please regenerate."
}


# --- Private Parsers ---

def _parse_outline_judgment(raw: str) -> JudgeResult:
    """
    Parse raw outline judge response into JudgeResult.
    """
    result = parse_json_response(raw, OUTLINE_JUDGE_FALLBACK)

    score = result.get("score", 0)
    passed = score >= PASS_THRESHOLD
    critique = result.get("critique", "") if not passed else ""

    return JudgeResult(
        score=score,
        passed=passed,
        critique=critique
    )


def _parse_story_judgment(raw: str) -> JudgeResult:
    """
    Parse raw story judge response into JudgeResult.
    Recalculates overall score from three dimensions
    rather than trusting model arithmetic.
    """
    result = parse_json_response(raw, STORY_JUDGE_FALLBACK)

    age_score = result.get("age_appropriateness_score", 0)
    structure_score = result.get("story_structure_score", 0)
    engagement_score = result.get("engagement_score", 0)

    # recalculate ourselves — don't trust model math
    overall = round((age_score + structure_score + engagement_score) / 3, 1)
    passed = overall >= PASS_THRESHOLD
    critique = result.get("critique", "") if not passed else ""

    return JudgeResult(
        score=overall,
        passed=passed,
        critique=critique
    )


# --- Public Interface ---

def judge_outline(outline: dict, age_group: str, category: str) -> JudgeResult:
    """
    Judge the story outline.
    Returns JudgeResult with score, passed, critique.
    """
    system = OUTLINE_JUDGE_SYSTEM.format(age_group=age_group)
    user = OUTLINE_JUDGE_USER.format(
        age_group=age_group,
        category=category,
        act1=outline["act1"],
        act2=outline["act2"],
        act3=outline["act3"]
    )

    raw = call_model(
        system_prompt=system,
        user_prompt=user,
        temperature=TEMPERATURE_JUDGE,
        max_tokens=MAX_TOKENS_JUDGE
    )

    return _parse_outline_judgment(raw)


def judge_story(story: str, age_group: str, category: str) -> JudgeResult:
    """
    Judge the full story across three dimensions:
    - Age appropriateness
    - Story structure
    - Engagement
    Returns aggregated JudgeResult.
    """
    system = STORY_JUDGE_SYSTEM.format(age_group=age_group)
    user = STORY_JUDGE_USER.format(
        age_group=age_group,
        category=category,
        story=story
    )

    raw = call_model(
        system_prompt=system,
        user_prompt=user,
        temperature=TEMPERATURE_JUDGE,
        max_tokens=MAX_TOKENS_JUDGE
    )

    return _parse_story_judgment(raw)