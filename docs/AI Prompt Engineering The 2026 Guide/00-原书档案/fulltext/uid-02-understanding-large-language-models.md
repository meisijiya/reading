---
uid: 02
level: 1
chapterNumber: 2
chapterKind: chapter
title: Chapter 2: Understanding Large Language Models
wordCount: 7722
parentPart: 01-基础与导读
---

# Chapter 2: Understanding Large Language Models

“Before you can master prompt engineering, you need to understand the mind you’re working with. It’s like collaborating with a genius who speaks a different language — you need to learn how they think before you can get the best results.”

## What Exactly Is an LLM?

LLM stands for Large Language Model — an AI system trained on massive volumes of text (and in 2026, often images, audio, and video) to understand and generate human-like language.

### The Three Key Components

1. Neural Networks Think of an LLM as a vast network of digital neurons connected in layers. When you provide a prompt, the signal travels through these layers, each processing different aspects of the information.

Prompt → Input Layer → Transformer Layers → Output Layer → Response

2. Training on Massive Data LLMs learn from trillions of text (and multimodal) examples drawn from:

- Books, articles, and academic papers
- Websites, blogs, and forums
- Code repositories
- Transcripts, captions, and image-text pairs
- Curated, high-quality expert datasets

3. Predictive Processing An LLM does not “know” things the way a human expert does. It predicts the most likely next token given the prompt and its training. When you ask “What is AI?”, the model predicts which tokens most plausibly complete a helpful response — conditioned on the rest of your conversation.

## The Major LLMs in 2026

The landscape moves fast. Specific model names and pricing change often — always check each provider’s current page. What follows is the lay of the land as of this writing.

### Anthropic’s Claude

Claude’s defining traits in 2026 are long context, careful reasoning, and strong coding and writing.

- Claude Opus — the flagship. Best for the hardest reasoning, research, and agentic work.
- Claude Sonnet — the workhorse. Excellent quality at lower cost and faster latency.
- Claude Haiku — fast, cheap, ideal for high-volume tasks.

Strengths: Nuanced instruction-following, honest about uncertainty, excellent for long-form analysis, code review, and structured outputs using XML tags.

Best for: Long-context work (books, codebases, legal docs), careful analysis, sustained conversations, agentic workflows.

### OpenAI’s ChatGPT / GPT Models

- Flagship GPT models — strong general-purpose performance, excellent tool use, wide ecosystem.
- Reasoning models (o-series) — spend extra compute “thinking” before answering, great for math, logic, and coding.
- Efficient models — fast and cheap for high-volume tasks.

Strengths: Huge ecosystem of custom GPTs and plugins, strong multimodal, integrated image generation, “Projects” for persistent context.

Best for: Broad general use, creative writing, quick prototypes, building custom GPTs for your team.

### Google’s Gemini

- Gemini Pro / Ultra — multimodal flagship with massive context windows (1M+ tokens are routine).
- Gemini Flash — faster, cheaper variant for everyday tasks.

Strengths: Deep Google ecosystem integration (Docs, Sheets, Gmail), massive context, strong multimodal understanding (video + audio).

Best for: Research, long-document analysis, multimodal reasoning, Workspace automation.

### Meta’s Llama

- Open-weight models you can run yourself or via many providers.
- Multiple sizes, from edge-deployable to frontier-competitive.

Strengths: Open weights, data sovereignty, cheaper at scale, fine-tunable.

Best for: Enterprise deployments with privacy requirements, specialized fine-tunes, on-prem use cases.

### xAI’s Grok

Strong real-time web access, conversational style. Best for current-event queries and X integration.

### Mistral

European alternative with open-weight and API offerings. Best for privacy-sensitive workloads and European compliance needs.

## Context Windows Explained

The context window is how much text the model can “see” at once — your prompt, any documents you paste, and the ongoing conversation.

| Context Size | What It Roughly Means | Good For |
| 8K tokens | A short chapter | Simple Q&A, short conversations |
| 32K–128K | A novella | Documents, sustained chats |
| 200K | A full novel | Entire books, long codebases |
| 1M+ | A small library | Whole repos, multi-hour transcripts, video |

### Working Within Context Limits

Even giant context windows have practical limits — latency, cost, and “lost in the middle” attention effects. Use these patterns:

1. Chunking. Split long documents into labeled sections, then process each in turn.

2. Summarize first, analyze second.

Step 1: "Summarize this 200-page report in 1,500 words."
Step 2: "Based on that summary, identify the top 3 risks."

3. Retrieval-Augmented Generation (RAG). Store documents in a vector database. Retrieve only the relevant passages for each query. This is how most production AI applications handle knowledge that won’t fit in context.

## Free vs. Paid Models

### Free Tiers — Great for Learning

Most major providers offer a free tier that’s more than enough to learn on. Free tiers typically include a smaller or older model, lower daily limits, and reduced context. That’s fine for learning.

### Paid Tiers — For Power Users

Consumer subscriptions (typically around $20/month per provider in 2026) unlock flagship models, longer context, image generation, file uploads, and higher limits. For most knowledge workers, one paid subscription pays for itself within a week.

### API Access — For Developers

Pay per token. Typical patterns:

- Input tokens are cheaper than output tokens.
- Prompt caching can cut input costs dramatically for repeated prefixes.
- Batch APIs offer a discount (often ~50%) for non-urgent workloads.
- Reasoning models charge extra for “thinking” tokens.

See Appendix B for a 2026 model comparison chart.

## How LLMs Actually “Think”

### Tokenization

When you type a prompt, the model doesn’t see words. It sees tokens — sub-word units.

- cat → 1 token
- unbelievable → usually 2–3 tokens
- An emoji → 1 or more tokens
- A line of code may tokenize completely differently than you’d guess.

Why tokens matter: you’re billed per token, context limits are in tokens, and shorter prompts are often more efficient.

### The Generation Process

1. Your prompt → tokenization
2. Embedding (each token → a vector)
3. Transformer layers process attention + context
4. Output layer produces a probability distribution over next tokens
5. Sampling picks the next token
6. Repeat until stop condition

### Temperature and Sampling

Temperature controls how deterministic the output is.

| Temperature | Behavior | Best For |
| 0.0 | Deterministic, focused | Code, factual answers, tests |
| 0.3–0.5 | Balanced | Most analysis and writing |
| 0.7–0.9 | Creative, varied | Brainstorming, creative writing |
| 1.0+ | Highly random | Experimental only |

Top-P (nucleus sampling) narrows or widens which tokens are eligible at each step. Lower Top-P is more focused; higher is more creative.

In most chat apps you don’t touch these directly — but on API access and in playgrounds you can, and it’s a superpower.

### Reasoning Models and Extended Thinking

A major shift in 2025–2026: models that deliberately spend extra compute “thinking” before answering. They produce internal reasoning tokens before the final response, improving math, logic, and multi-step problems.

When you have a tricky problem, use a reasoning model or ask a regular model to “think step by step before answering.” We cover this in depth in Chapter 9.

## Limitations and Pitfalls

### Hallucinations

What it is: The model confidently states false information.

Why it happens: The model predicts plausible-sounding tokens. If it has no real knowledge, it guesses and sounds certain.

How to reduce hallucinations:

- Give explicit permission to say “I don’t know.”
- Ask for sources and verify them.
- Use RAG or tool use so the model cites real documents.
- Cross-check important facts.
- Use reasoning models for high-stakes outputs.

### Bias

LLMs reflect biases in their training data. Mitigate by:

- Explicitly requesting diverse perspectives.
- Using inclusive language in your prompt.
- Reviewing outputs for one-sided framings.
- Asking the model to critique its own output.

### Knowledge Cutoffs

Every model has a training cutoff. After that date, it doesn’t know what happened. To get current information:

- Use a model with live web access, or
- Paste in the current context yourself, or
- Use a RAG system over current sources.

### Cost Awareness

- Longer prompts cost more.
- Reasoning tokens cost more.
- Repeated prefixes are a perfect use case for prompt caching.
- Use cheaper models for simple tasks; reserve the flagship for the hard ones.

## Chapter Summary

LLMs are powerful, but they work differently from traditional software. To prompt them effectively, know their:

- Architecture — neural networks and predictive token generation.
- Major models — Claude, GPT, Gemini, Llama, Grok, Mistral.
- Context windows — how much the model can see at once.
- Free vs. paid — what’s worth upgrading.
- Sampling — temperature, Top-P, reasoning mode.
- Limitations — hallucinations, bias, cutoffs, cost.

Next chapter: the 4 C’s framework — the four principles you’ll use in every prompt for the rest of your life.
