import random

from config import MAX_OUTLINE_ITERATIONS, MAX_STORY_ITERATIONS
from classifier import classify_input, VALID_CATEGORIES
from storyteller import generate_outline, refine_outline, generate_story, refine_story
from judge import judge_outline, judge_story

# Numbered picks after genre; last option is always "surprise me"
STORY_IDEAS_BY_CATEGORY: dict[str, list[str]] = {
    "adventure": [
        "A child discovers a gentle riddle on a hiking trail and solves it with a new friend.",
        "Two siblings build a raft for a calm pond race and learn to cheer each other on.",
        "A shy camper finds courage when they help the group pack up before a summer storm.",
        "A backyard explorer maps a 'lost city' of flowers and shares the treasure map with friends.",
    ],
    "friendship": [
        "A new kid at school and a classmate bond over fixing a broken kite at recess.",
        "Two neighbors plan a surprise thank-you picnic for someone who helped their street.",
        "Friends disagree about a game rule, talk it out, and invent a fairer way to play.",
        "A child teaches a friend to ride a bike, patience and laughter along the way.",
    ],
    "bedtime": [
        "A little owl who is afraid of the dark learns that stars are friends watching overhead.",
        "A bunny cannot sleep until they remember three cozy things about their day.",
        "A teddy bear guards sweet dreams while a child drifts off in a soft rainstorm.",
        "A firefly leads a sleepy mouse home through a quiet, moonlit garden.",
    ],
    "fantasy": [
        "A child finds a tiny door in a tree and meets a polite gnome who needs one kind favor.",
        "A cloud painter accidentally makes rainbow puddles and tidies up with a dragon friend.",
        "A talking teacup grants one small wish: the hero chooses warmth for everyone at tea time.",
        "A gentle unicorn helps return lost laughter to a village festival.",
    ],
    "animal": [
        "A clever crow trades shiny pebbles to help friends build a safe winter nest.",
        "A puppy's first day at the park: mud, a ball, and learning to share with other pups.",
        "A shy turtle enters a slow-and-steady river race with encouragement from frogs.",
        "A farm cat organizes a barnyard talent show where every animal shines.",
    ],
}


def pick_category() -> str:
    print("\nChoose a genre:")
    for i, cat in enumerate(VALID_CATEGORIES, 1):
        print(f"  {i}. {cat}")
    while True:
        choice = input("Enter number: ").strip()
        if choice.isdigit() and 1 <= int(choice) <= len(VALID_CATEGORIES):
            return VALID_CATEGORIES[int(choice) - 1]
        print(f"  Please enter a number between 1 and {len(VALID_CATEGORIES)}.")


def pick_story_request(category: str) -> str:
    ideas = STORY_IDEAS_BY_CATEGORY.get(category) or STORY_IDEAS_BY_CATEGORY["bedtime"]
    surprise_index = len(ideas) + 1

    print(f"\nPick a story idea for '{category}':")
    for i, idea in enumerate(ideas, 1):
        print(f"  {i}. {idea}")
    print(f"  {surprise_index}. Surprise me - pick a random idea in this genre")

    while True:
        choice = input("Enter number: ").strip()
        if not choice.isdigit():
            print(f"  Please enter a number between 1 and {surprise_index}.")
            continue
        n = int(choice)
        if 1 <= n <= len(ideas):
            return ideas[n - 1]
        if n == surprise_index:
            return random.choice(ideas)
        print(f"  Please enter a number between 1 and {surprise_index}.")


def run_pipeline(user_input: str, category: str) -> str:
    """
    Full automated pipeline:
    1. Classify input
    2. Generate and judge outline (max 2 iterations)
    3. Generate and judge story (max 2 iterations)
    4. Return final story
    """

    # ── Step 1: Classify ──────────────────────────────────────────
    print("\n[1/4] Classifying your request...")
    classification = classify_input(user_input)
    age_group = classification["age_group"]
    print(f"      Age group : {age_group}")
    print(f"      Category  : {category}")


    # ── Step 2: Outline Generation + Judge Loop ───────────────────
    print("\n[2/4] Generating story outline...")
    outline = generate_outline(user_input, age_group, category)

    for iteration in range(MAX_OUTLINE_ITERATIONS):
        outline_result = judge_outline(outline, age_group, category)

        if outline_result.passed:
            print(f"      Outline approved (score: {outline_result.score}/10)")
            break

        print(f"      Outline score: {outline_result.score}/10 — refining... (attempt {iteration + 1}/{MAX_OUTLINE_ITERATIONS})")
        print(f"      Critique: {outline_result.critique}")

        outline = refine_outline(outline, outline_result.critique, age_group, category)

    else:
        # max iterations reached — judge final refined outline one last time
        outline_result = judge_outline(outline, age_group, category)
        if not outline_result.passed:
            print(f"      Outline did not reach threshold after {MAX_OUTLINE_ITERATIONS} attempts. Proceeding with best version.")


    # ── Step 3: Story Generation + Judge Loop ─────────────────────
    print("\n[3/4] Writing story...")
    story = generate_story(user_input, outline, age_group, category)

    for iteration in range(MAX_STORY_ITERATIONS):
        story_result = judge_story(story, age_group, category)

        if story_result.passed:
            print(f"      Story approved (score: {story_result.score}/10)")
            break

        print(f"      Story score: {story_result.score}/10 — refining... (attempt {iteration + 1}/{MAX_STORY_ITERATIONS})")
        print(f"      Critique: {story_result.critique}")

        story = refine_story(story, story_result.critique, age_group)

    else:
        # max iterations reached — judge final refined story one last time
        story_result = judge_story(story, age_group, category)
        if not story_result.passed:
            print(f"      Story did not reach threshold after {MAX_STORY_ITERATIONS} attempts. Proceeding with best version.")


    # ── Step 4: Output ────────────────────────────────────────────
    print("\n[4/4] Your story is ready!\n")
    print("=" * 60)
    return story


def main():
    print("=" * 60)
    print("   Welcome to the Bedtime Story Generator")
    print("=" * 60)

    category = pick_category()
    user_input = pick_story_request(category)

    story = run_pipeline(user_input, category)
    print(story)
    print("=" * 60)


if __name__ == "__main__":
    main()