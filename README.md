# ai-tool-prompts

Claude Code plugin (and Claude.ai dashboard skill bundles) wrapping the system
prompts and tool schemas of 32 AI coding/assistant tools — Cursor, Windsurf,
Claude Code, v0, Devin, Lovable, Replit, Warp, and more. Sourced from
[`x1xhlol/system-prompts-and-models-of-ai-tools`](https://github.com/x1xhlol/system-prompts-and-models-of-ai-tools).

Each skill activates when you ask Claude to imitate, compare, or analyse a
specific tool's prompting style, then loads the canonical source files
bundled inside that skill's `sources/` directory.

## Install (Claude Code, all projects)

One-time, from any Claude Code session:

```text
/plugin marketplace add aupowell22-code/Claudecode-
/plugin install ai-tool-prompts@ai-tool-prompts-marketplace
```

After that, every project on that machine can trigger any of the 32 skills
listed below.

## Install (Claude.ai dashboard)

Each `dist/skills/<slug>.zip` is a standalone Claude skill bundle. Upload them
at <https://claude.ai/settings/skills> → Custom skills → **Upload skill**.
`dist/skills/all-skills.zip` aggregates the lot.

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

## Layout

```
.claude-plugin/
  plugin.json            Claude Code plugin manifest
  marketplace.json       Marketplace entry pointing at this repo
skills/
  <slug>/
    SKILL.md             Frontmatter + activation guidance
    sources/             Bundled prompt and tool files
dist/skills/
  <slug>.zip             Dashboard upload bundles
  all-skills.zip         All 32 zips, aggregated
<Tool folder>/           Upstream prompt mirror (unchanged from x1xhlol)
```

## License

Upstream prompt content remains under its original `LICENSE.md` (in this repo
root). Plugin scaffolding is MIT.
