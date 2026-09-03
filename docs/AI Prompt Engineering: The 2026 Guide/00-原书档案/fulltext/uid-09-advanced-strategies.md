---
uid: 09
level: 1
chapterNumber: 9
chapterKind: chapter
title: Chapter 9: Advanced Strategies
wordCount: 7135
parentPart: 03-进阶与商业应用
---

# Chapter 9: Advanced Strategies

“Now that you’ve mastered the basics, it’s time to unlock AI’s full potential. These advanced strategies will help you tackle complex tasks and build sophisticated AI workflows.”

## Chain-of-Thought Prompting

Chain-of-thought (CoT) prompting gives the model a scratchpad to reason through problems step by step.

### How It Works

Instead of asking for the final answer directly, guide the model through the reasoning.

Without CoT:

"Calculate the ROI for a $10,000 investment that generates
$2,500/month."

The model may guess or make an arithmetic mistake.

With CoT:

"Calculate the ROI for a $10,000 investment that generates
$2,500/month. Show your work step by step:
1) Annual returns.
2) Total return over \[timeframe\].
3) ROI percentage."

The model shows its work, making the answer easier to verify.

### Chain-of-Thought Templates

The Step-by-Step Solver.

"Break down \[problem\] into clear steps:
Step 1: \[first\].
Step 2: \[second\].
Step 3: \[third\].
Now solve each step."

The Reasoning Prompt.

"Explain your reasoning for \[problem\]:
1) Identify the key factors.
2) Analyze each factor.
3) Synthesize the answer."

The Self-Correction Prompt.

"Here's my attempt at \[problem\]: \[attempt\].
Identify any errors and provide the corrected solution
with explanation."

### When to Use Chain-of-Thought

| Scenario | Why CoT helps |
| Complex calculations | Prevents arithmetic errors |
| Multi-step problems | Ensures all steps are covered |
| Decision making | Shows the reasoning |
| Debugging code | Localizes the issue |

### Reasoning Models vs. CoT Prompting

In 2026, many providers offer reasoning models that run chain-of-thought internally. You don’t have to write “think step by step” — they do it automatically and hide most of the reasoning tokens. Use them when the task is hard, accuracy matters, and latency/cost are acceptable. For cheap everyday tasks, a fast model with a “think step by step” instruction is often enough.

## Self-Consistency Prompting

Self-consistency asks AI to generate multiple solutions, then pick the best one.

"Generate \[number\] different solutions for \[problem\].
For each:
- Describe it.
- List pros and cons.
- Rate 1–10.
Then select the best and explain why."

### Why It Works

- Reduces the impact of single-generation errors.
- Surfaces alternatives you hadn’t considered.
- Gives you explicit trade-offs to choose between.

## Prompt Chaining

Prompt chaining is an assembly line for AI — the output of one prompt becomes the input for the next.

\[Input\] → \[Prompt 1\] → \[Output 1\] → \[Prompt 2\] → \[Output 2\] → \[Final\]

### Common Chain Patterns

Analysis Pipeline.

Input: raw data
Prompt 1: summarize key points
Prompt 2: identify trends
Prompt 3: generate recommendations
Output: actionable insights

Content Pipeline.

Input: topic
Prompt 1: generate 10 article ideas
Prompt 2: expand the best into an outline
Prompt 3: draft the full article
Prompt 4: edit and tighten
Output: polished content

Code Refinement Pipeline.

Input: feature request
Prompt 1: generate initial code
Prompt 2: add error handling
Prompt 3: optimize performance
Prompt 4: add tests and docs
Output: production-ready code

### Building Your Own Chains

1. Define the goal — what’s the final artifact?
2. Break down the process — what intermediate steps?
3. Write each prompt — focused and single-purpose.
4. Test the chain — verify each step produces usable output.

### Automating Prompt Chains

- Plain API scripts — call the model N times in sequence.
- Zapier / Make / n8n — visual workflows with AI steps.
- LangChain / LlamaIndex — programmatic chains, RAG, tools.
- Claude Projects / Custom GPTs / Gems — persistent context + instructions.
- Agents (2026 standard) — the model decides when to call each tool instead of you hard-coding the chain.

## Role-Playing and Persona Prompting

Assigning specific roles dramatically improves output quality.

"Act as a \[role\] with \[experience\] years of experience in \[field\].
Your task is to \[task\]."

### Effective Personas

Technical: senior architect, DevOps engineer, security specialist, data scientist, product manager.

Business: marketing director, consultant, financial analyst, HR manager, CEO.

Creative: copywriter, designer, UX researcher, content strategist, brand manager.

Academic: professor, researcher, editor, reviewer, tutor.

### Persona Templates

The Expert Consultant.

"Act as a \[expertise\] expert with 20 years of experience.
Advise me on \[problem\].
Include: root cause analysis, solutions, implementation steps."

The Skeptical Reviewer.

"Act as a skeptical expert reviewing \[work\].
Identify: weaknesses, potential failures, improvements needed."

The Optimistic Visionary.

"Act as a visionary expert in \[field\]. Imagine 5 years ahead.
What opportunities exist? What should I focus on?"

### The Dual-Persona Technique

For complex decisions, use two personas in sequence:

1) "Act as an optimistic founder. Argue why \[plan\] will succeed."
2) "Act as a skeptical investor. Identify what could go wrong."
3) "Synthesize both views into a balanced recommendation."

## Constraint-Driven Prompting

Constraints focus creativity and dramatically improve output quality.

### Effective Constraints

- Length: word count, character count, sentence count.
- Format: Markdown, HTML, JSON, CSV, specific structure.
- Style: tone, voice, reading level, jargon level.
- Technical: language version, framework, performance, security.

### Examples

Code:

"Write a Python function to \[purpose\] with these constraints:
- Standard library only (no external packages)
- Graceful error handling
- Include docstrings
- Max 30 lines of code
- O(n) time complexity"

Writing:

"Write a blog post about \[topic\] with these constraints:
- Exactly 500 words
- H2 headings for each section
- No jargon, 8th-grade reading level
- Include 3 examples"

Analysis:

"Analyze this data with these constraints:
- Exactly 5 key insights
- Each supported by evidence
- Prioritize actionable insights
- No more than 100 words per insight"

## Iterative Refinement

The key to great AI output is iteration — not getting it perfect on the first try.

Version 1: get the basics right
Version 2: refine the details
Version 3: polish and optimize

### Iteration Prompts

First draft.

"Create a first draft of \[output\] about \[topic\].
Focus on covering all key points; don't worry about perfection."

Refinement.

"Review this draft and improve it:
- Add specific examples
- Improve flow and transitions
- Strengthen arguments
- Make it more engaging"

Polish.

"Polish this to professional quality:
- Fix grammar and style
- Ensure consistency
- Add compelling hooks and conclusions
- Optimize for \[audience\]"

### The 3-Iteration Rule

Most high-quality outputs require three iterations: draft → refine → polish.

## Structured Output and JSON Mode

When you need machine-readable output, demand structure.

"Return your answer as JSON matching this schema:
{
   \"summary\": string,
   \"risks\": [{\"name\": string, \"severity\": \"low|med|high\"}],
   \"recommendation\": string
}
Return only the JSON. No prose."

Many APIs provide a JSON mode or structured outputs feature that enforces a schema. Use it whenever you’re wiring AI into code — it eliminates parsing bugs.

## Meta-Prompting

Use AI to improve your prompts. This is the single biggest leverage point in the whole book.

"Here's my current prompt: \[prompt\].
Here's the output I got: \[output\].
Here's what I actually wanted: \[desired\].
Rewrite the prompt to reliably produce the desired output.
Explain what you changed and why."

Or:

"I want to \[goal\]. Write me a prompt I can copy into a chatbot
that will reliably produce \[desired output\]. Then explain
the prompt's structure."

## Chapter Summary

Advanced strategies transform AI from a simple tool into a powerful collaborator:

1. Chain-of-thought — guide reasoning.
2. Self-consistency — generate multiple options, pick the best.
3. Prompt chaining — create AI assembly lines.
4. Role-playing — assign expert personas.
5. Constraints — focus creativity.
6. Iteration — refine through multiple passes.
7. Structured outputs — machine-readable results.
8. Meta-prompting — use AI to write your prompts.

For the deepest 2026 techniques (XML structuring, extended thinking, agentic workflows, tool use, prompt caching), see Appendix G: Expert Techniques for 2026.

Next: Chapter 10 — how to apply all of this to your business.
