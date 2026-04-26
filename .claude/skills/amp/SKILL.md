---
name: amp
description: Reference system prompt and tool schemas for Amp. TRIGGER when: imitating, comparing, or analyzing Amp's prompting style; designing prompts inspired by Amp; answering questions about how Amp is prompted; or studying agent system-prompt patterns for AI tooling.
---

# Amp

Sourcegraph Amp coding agent.

When activated, read the source files below from this repository to ground
your response in the actual published prompt text. Do not paraphrase from
memory — the canonical content lives in these files.

## Source files

- `Amp/README.md`
- `Amp/claude-4-sonnet.yaml`
- `Amp/gpt-5.yaml`

## Usage

- Quote or summarise from the files above when answering "how does Amp prompt its agent?" style questions.
- When emulating Amp's style, mirror its structure (sections, tool-use rules, refusal patterns) rather than copying verbatim.
- These prompts were collected by the upstream `x1xhlol/system-prompts-and-models-of-ai-tools` repo and may drift from the live product over time.
