# Dingo Marketing

An OpenClaw skill for generating release announcement posts for open-source projects across multiple platforms.

## What it does

Given a project's release notes (changelog, GitHub Release URL, etc.), this skill generates platform-adapted announcement posts for:

- **Reddit** — technical community posts for r/MachineLearning, r/LocalLLaMA, etc.
- **Twitter/X** — thread format + single tweet (English and Chinese)
- **Xiaohongshu (小红书)** — Chinese-language posts in 3 versions (technical, scenario, short)
- **Hacker News** — Show HN posts with engineering-focused tone

## Project Structure

```
SKILL.md              # OpenClaw skill definition
projects/
  dingo.yaml          # Dingo project config (first use case)
  _template.yaml      # Template for adding new projects
templates/
  reddit.md           # Reddit post style rules and structure
  twitter.md          # Twitter/X style rules and structure
  xiaohongshu.md      # Xiaohongshu style rules and structure
  hacker_news.md      # Hacker News style rules and structure
```

## Usage

### With OpenClaw

Install this skill in your OpenClaw instance, then use natural language:

```
> Generate release posts for Dingo v2.1.0 based on:
> https://github.com/MigoXLab/dingo/releases/tag/v2.1.0

[Agent reads projects/dingo.yaml + release notes + templates, generates 4 posts]

> Make the Reddit title focus on the SaaS launch

[Agent revises the Reddit post]
```

### Without OpenClaw

The `SKILL.md`, project configs, and templates can also be used as a prompt kit with any LLM:

1. Copy the contents of `SKILL.md` as the system prompt
2. Attach the relevant `projects/<name>.yaml` and `templates/*.md` files
3. Provide the release notes as the user message

## Adding a New Project

1. Copy `projects/_template.yaml` to `projects/<your-project>.yaml`
2. Fill in your project's details (repo URL, install command, highlights, etc.)
3. That's it. The skill and templates are generic — no other changes needed.

## Future Extensions

- GitHub Action for automated generation on new releases
- API publishing scripts (Reddit via praw, Twitter via tweepy)
- Browser automation for platforms without APIs (Xiaohongshu, Hacker News)
