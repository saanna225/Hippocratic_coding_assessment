# System Block Diagram

```mermaid
flowchart TD
    A([👤 User Input\nStory Request]) --> B

    subgraph CLASSIFIER["① CLASSIFIER"]
        B[Classify Input]
        B --> C[Age Group\n5-7 or 8-10]
        B --> D[Category\nadventure / friendship\nbedtime / fantasy / animal]
    end

    C & D --> E

    subgraph OUTLINE_LOOP["② OUTLINE GENERATION + JUDGE LOOP  (max 2 iterations)"]
        E[Outline Generator\n3-Act Structure] --> F
        F{Outline Judge\nScore out of 10}
        F -- "✅ score ≥ 8\nPASS" --> G([Approved Outline\nAct 1 · Act 2 · Act 3])
        F -- "❌ score < 8\nFAIL + critique" --> E
    end

    G --> H

    subgraph STORY_LOOP["③ STORY GENERATION + JUDGE LOOP  (max 2 iterations)"]
        H[Story Generator\nFull Story from Outline] --> I
        I{Story Judge Panel\nAge Appropriateness\nStory Structure\nEngagement}
        I -- "✅ avg score ≥ 8\nPASS" --> J([Approved Story])
        I -- "❌ avg score < 8\nFAIL + combined critique" --> H
    end

    J --> K([📖 Final Story Output\nPrinted to User])

    style CLASSIFIER fill:#f0f0f0,stroke:#999
    style OUTLINE_LOOP fill:#f0f0f0,stroke:#999
    style STORY_LOOP fill:#f0f0f0,stroke:#999
    style A fill:#fff,stroke:#333
    style K fill:#fff,stroke:#333
    style G fill:#fff,stroke:#333
    style J fill:#fff,stroke:#333
```

## Component Descriptions

| Component | Role |
|---|---|
| **User** | Provides a natural language story request |
| **Classifier** | Detects age group (5-7 or 8-10) and story category from input |
| **Outline Generator** | Produces a 3-act story structure (setup, struggle, resolution) |
| **Outline Judge** | Scores outline on structure and age-appropriateness. Feeds critique back if score < 8 |
| **Story Generator** | Writes full story strictly following the approved outline |
| **Story Judge Panel** | Evaluates story across 3 dimensions: age appropriateness, story structure, engagement |
| **Refinement Loop** | Rewrites story using combined critique from all 3 judges if score < 8 |

## Prompting Strategies

| Strategy | Where Used |
|---|---|
| Chain-of-Thought (CoT) | Outline Judge, Story Judge — reason before scoring |
| Structured JSON output | All LLM calls — reliable parsing, no free text |
| Critique-driven refinement | Outline + Story loops — targeted fixes, not full regeneration |
| Separated system/user prompts | All components — clear role separation |
| Temperature control | Low (0.1) for judges/classifier, High (0.7-0.8) for generation |
