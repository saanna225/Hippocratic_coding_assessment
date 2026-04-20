# Bedtime Story Generator
A multi-agent LLM pipeline that generates age-appropriate stories for children aged 5–10.

## How It Works
1. **Classifier** - detects age group (5-7 or 8-10) and story genre from user input
2. **Outline Generator** - creates a 3 way story structure tailored to age and category
3. **Outline Judge** - scores the outline and refines it if below threshold (score < 8/10)
4. **Story Generator** - writes the full story from the approved outline
5. **Story Judge** - evaluates across 3 dimensions: age appropriateness, structure, engagement
6. **Refinement Loop** - rewrites the story with combined knowledge if below threshold

## Prompting Strategies Used
1.**Chain-of-Thought (CoT)** - judges reason step by step before scoring
2.**Structured output** - all LLM responses return JSON 
3.**Separation of concerns** - classifier, outline, story, and judge each have dedicated prompts
4.**Critique-driven refinement** - failed outputs are improved with specific actionable feedback, not regenerated again and again

