---
uid: 03
level: 1
chapterNumber: 3
chapterKind: chapter
title: Chapter 3: The 4 C’s Framework
wordCount: 6745
parentPart: 01-基础与导读
---

# Chapter 3: The 4 C’s Framework

“You wouldn’t order a complex dish at a restaurant by saying ‘Make me something good.’ You’d specify ingredients, cooking style, portion size, and dietary needs. Prompt engineering works the same way — the more specific you are, the better the result.”

## Why Structure Matters

Prompt engineering is not about memorizing magic phrases. It is about structured thinking.

A prompt is a recipe for the AI’s mind. A good cake recipe needs:

- Ingredients (the data)
- Quantities (the constraints)
- Instructions (the steps)
- Oven temperature (the parameters)

A good prompt needs:

- Clear intent
- Concise wording
- Contextual information
- Conversational tone

### The Cost of Unstructured Prompts

| Problem | Result | Fix |
| Vague request | Generic output | Add specifics |
| Missing context | Wrong assumptions | Provide background |
| Overly long | Buried key points | Be more concise |
| Robotic tone | Stilted output | Use natural language |

## 1. CLEAR — The “What” Principle

### The Problem with Vague Prompts

Bad: “Write about marketing.”

The model guesses at your intent. Output will be generic, likely bloated, and require revisions.

Better: “Write a 500-word blog post about AI marketing strategies for small businesses targeting entrepreneurs aged 25–40.”

Specific length, clear topic, defined audience. The model knows exactly what to build.

### How to Be Clear

1. Specify the task type.

Instead of: "Write about marketing"
Try: "Create a marketing strategy outline"
Try: "Write a marketing email"
Try: "Analyze marketing campaign performance"

2. Define the output format.

Instead of: "Write a blog post"
Try: "Write a 600-word blog post with H2 headings for:
      Introduction, Strategy, Implementation, Metrics"

3. Set constraints.

Instead of: "Write code"
Try: "Write a Python function using pandas that processes CSV
      data and handles missing values. Include type hints and
      a docstring."

4. Provide examples (few-shot learning).

"Here are examples of good marketing headlines:
- 'Boost Your Sales with AI: 5 Strategies That Work'
- 'The AI Marketing Tool That Saves 10 Hours/Week'

Create 3 more headlines in this style for a new
marketing automation platform."

### The Clear Prompt Template

\[Task Type\]: \[Specific task\]
\[Output Format\]: [Length / structure]
\[Audience\]: \[Who will use this\]
\[Constraints\]: \[Limitations\]
\[Example\]: [Optional — what good looks like]

## 2. CONCISE — The “How Long” Principle

Contrary to intuition, longer prompts are often less effective.

Why concise works better:

- Key information stays salient.
- Filler adds noise the model has to filter out.
- Fewer tokens = lower cost and latency.

### The Concise Prompt Formula

\[Action\] + \[Subject\] + \[Constraints\] + \[Format\]

Example breakdown:

- Action: “Write”
- Subject: “3 LinkedIn posts about AI marketing”
- Constraints: “150 words each, professional tone, include 1 question”
- Format: “Use bullet points for key takeaways”

### How to Tighten a Prompt

1. Remove filler.

Before: "I was wondering if you could maybe help me write
         something about AI marketing?"
After:  "Write about AI marketing strategies."

2. Combine related clauses.

Before: "I need a blog post. It should be about marketing.
         The audience is small businesses."
After:  "Write a marketing blog post for small businesses."

3. Use direct commands, not polite scaffolding.

Instead of: "Could you please generate a code snippet that..."
Use:        "Write a Python function that..."

### Verbose vs. Concise

Verbose (44 words): “Hello, I’m trying to figure out how to do some marketing content for my business, and I was wondering if you could possibly help me write something about AI marketing strategies that would be good for small business owners?”

Concise (12 words): “Write a marketing blog post about AI strategies for small business owners.”

Same meaning, fraction of the tokens, clearer intent.

Note: Concise is not the same as terse. If context is genuinely needed, include it — see the next section.

## 3. CONTEXTUAL — The “Background” Principle

An LLM without context is like a doctor without a diagnosis. The model needs background to give you useful output.

### The Context Triangle

┌──────────────────────────────────────────────────────────────┐
│                     CONTEXTUAL PROMPTING                     │
├──────────────────────────────────────────────────────────────┤
│  ROLE         │     SITUATION         │     GOAL             │
│  "Who are     │  "What's              │  "What do            │
│   you?"       │   happening?"         │   you want?"         │
└──────────────────────────────────────────────────────────────┘

### Providing Context

1. Define the role.

"Act as a senior marketing director with 20 years of experience..."
"You are an expert Python developer reviewing a junior's code..."
"Think of yourself as a business coach for technical founders..."

2. Explain the situation.

"...working with a SaaS company that has 50 employees..."
"...facing a 15% monthly churn problem..."
"...launching a new product next month..."

3. State the goal.

"...my goal is to create a marketing strategy that
increases qualified leads by 30% in 90 days..."

### The Contextual Template

Role: \[Who the AI should be\]
Situation: \[The current context\]
Goal: \[What you want to achieve\]
Constraints: \[Any limitations\]
Output: \[Format you want\]

Full example:

Role: Marketing director with 15 years of experience
Situation: Tech startup, 10 employees, launching a new
           collaboration tool
Goal: Create a 30-day marketing plan to reach 1,000 signups
Constraints: $500 budget, no paid ads
Output: Week-by-week action plan with owners and metrics

## 4. CONVERSATIONAL — The “Tone” Principle

LLMs are trained on human conversation. They respond better to natural language than to robotic instructions.

### The Power of “You” and “I”

Robotic: “The user requests marketing content.” Conversational: “I need help creating marketing content.”

### Conversational Techniques

1. Use natural language.

Instead of: "Create a list of marketing strategies"
Try:        "What are some effective marketing strategies for..."

2. Ask questions.

Instead of: "Write a blog post introduction"
Try:        "How would you start a blog post about..."

3. Build on previous responses.

You: "What are 3 marketing strategies for a B2B SaaS?"
AI:  \[lists three\]
You: "Go deeper on #2 — what would the first 30 days look like?"
AI:  \[detailed plan for strategy 2\]

### The Empathy Test

Before sending a prompt, ask:

- Would I talk to a colleague this way?
- Does this sound like a natural conversation?
- Am I specific without being robotic?

## Putting It All Together

### The Complete Prompt Formula

\[Role\] + \[Situation\] + \[Task\] + \[Constraints\] + \[Format\] + \[Tone\]

Full example:

Role: Senior marketing director with 15 years of experience
Situation: Launching a new SaaS product with a $500 budget
Task: Create a 30-day marketing plan
Constraints: No paid ads, focus on organic growth
Format: Week-by-week action plan with specific tasks
Tone: Practical and actionable — this should read like a
      peer handing me a playbook, not a textbook

### Common Prompt Structures

The Problem-Solver. “I’m facing \[problem\]. Here’s what I’ve tried: \[list\]. What would you do differently?”

The Creator. “Create \[output\] about \[topic\]. Style: \[style\]. Audience: \[audience\].”

The Analyzer. “I have [data / context]. What insights can you draw? What should I do next?”

The Improver. “Here’s what I have: \[content\]. Make it \[specific improvement\].”

### The Iterative Approach

One prompt rarely nails it. Use conversation to refine:

1. First prompt: Get the bones right.
2. Second prompt: Refine the details.
3. Third prompt: Polish and optimize.

## Chapter Summary

The 4 C’s Framework gives you a repeatable system:

1. CLEAR — specific, constrained, example-driven.
2. CONCISE — short, direct, no filler.
3. CONTEXTUAL — role, situation, goal.
4. CONVERSATIONAL — natural, collaborative.

Master these four principles and you’ll consistently get better output from any AI tool.

Next chapter: 50 battle-tested prompts for chat and conversation.
