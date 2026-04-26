# AI Tool Prompt Skills

One skill per AI coding/assistant tool, generated from the system prompts and
tool schemas mirrored in this repo (sourced from
[`x1xhlol/system-prompts-and-models-of-ai-tools`](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools)).

Each `<slug>/SKILL.md` is a thin pointer: it carries trigger metadata in the
YAML frontmatter and lists the canonical source files (`*.txt`, `*.json`,
`*.yaml`, `*.md`) at the repo root that contain the actual prompt content.
Claude reads those source files on demand instead of duplicating their text
into the skill body.

## Skills

| Slug | Tool | Source folder |
| --- | --- | --- |
| `amp` | Amp | `Amp/` |
| `anthropic` | Anthropic (Claude.ai, Claude Code, Claude for Chrome) | `Anthropic/` |
| `augment-code` | Augment Code | `Augment Code/` |
| `cluely` | Cluely | `Cluely/` |
| `codebuddy` | CodeBuddy | `CodeBuddy Prompts/` |
| `comet-assistant` | Comet Assistant | `Comet Assistant/` |
| `cursor` | Cursor | `Cursor Prompts/` |
| `devin` | Devin AI | `Devin AI/` |
| `dia` | Dia | `dia/` |
| `emergent` | Emergent | `Emergent/` |
| `google-ai` | Google AI Studio + Antigravity | `Google/` |
| `junie` | Junie | `Junie/` |
| `kiro` | Kiro | `Kiro/` |
| `leap-new` | Leap.new | `Leap.new/` |
| `lovable` | Lovable | `Lovable/` |
| `manus` | Manus | `Manus Agent Tools & Prompt/` |
| `notion-ai` | Notion AI | `NotionAi/` |
| `orchids` | Orchids.app | `Orchids.app/` |
| `oss-agent-prompts` | Cline, Bolt, RooCode, Codex CLI, Gemini CLI, Lumo | `Open Source prompts/` |
| `perplexity` | Perplexity | `Perplexity/` |
| `poke` | Poke | `Poke/` |
| `qoder` | Qoder | `Qoder/` |
| `replit` | Replit | `Replit/` |
| `same-dev` | Same.dev | `Same.dev/` |
| `trae` | Trae | `Trae/` |
| `traycer` | Traycer AI | `Traycer AI/` |
| `v0` | v0 | `v0 Prompts and Tools/` |
| `vscode-agent` | VSCode / Copilot Chat agent | `VSCode Agent/` |
| `warp` | Warp.dev | `Warp.dev/` |
| `windsurf` | Windsurf | `Windsurf/` |
| `xcode` | Xcode AI | `Xcode/` |
| `zai-code` | Z.ai Code | `Z.ai Code/` |

## Adding a new tool

1. Drop the prompt and tool files into a new top-level folder (e.g. `NewTool/`).
2. Create `.claude/skills/<slug>/SKILL.md` with YAML frontmatter (`name`,
   `description`) and a list of the source files under a `## Source files`
   heading.
3. Append the row to the table above.
