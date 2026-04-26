---
name: vscode-agent
description: Reference system prompt and tool schemas for VSCode Agent. TRIGGER when: imitating, comparing, or analyzing VSCode Agent's prompting style; designing prompts inspired by VSCode Agent; answering questions about how VSCode Agent is prompted; or studying agent system-prompt patterns for AI tooling.
---

# VSCode Agent

GitHub Copilot Chat / VSCode Agent system prompts across multiple models (GPT-4o/4.1/5/5-mini, Claude Sonnet 4, Gemini 2.5 Pro).

When activated, read the source files below from this repository to ground
your response in the actual published prompt text. Do not paraphrase from
memory — the canonical content lives in these files.

## Source files

- `VSCode Agent/Prompt.txt`
- `VSCode Agent/chat-titles.txt`
- `VSCode Agent/claude-sonnet-4.txt`
- `VSCode Agent/gemini-2.5-pro.txt`
- `VSCode Agent/gpt-4.1.txt`
- `VSCode Agent/gpt-4o.txt`
- `VSCode Agent/gpt-5-mini.txt`
- `VSCode Agent/gpt-5.txt`
- `VSCode Agent/nes-tab-completion.txt`

## Usage

- Quote or summarise from the files above when answering "how does VSCode Agent prompt its agent?" style questions.
- When emulating VSCode Agent's style, mirror its structure (sections, tool-use rules, refusal patterns) rather than copying verbatim.
- These prompts were collected by the upstream `x1xhlol/system-prompts-and-models-of-ai-tools` repo and may drift from the live product over time.
